import logging
import re
import traceback
import docker
from tqdm import tqdm
from pathlib import Path
import subprocess
import time
from datetime import timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed

from swebench.harness.constants import (
    BASE_IMAGE_BUILD_DIR,
    ENV_IMAGE_BUILD_DIR,
    INSTANCE_IMAGE_BUILD_DIR,
    MAP_REPO_VERSION_TO_SPECS,
)
from swebench.harness.test_spec import (
    get_test_specs_from_dataset,
    make_test_spec,
    TestSpec,
)
from swebench.harness.docker_utils import (
    cleanup_container,
    remove_image,
    find_dependent_images,
)

ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


class BuildImageError(Exception):
    def __init__(self, image_name, message, logger):
        super().__init__(message)
        self.super_str = super().__str__()
        self.image_name = image_name
        self.log_path = logger.log_file
        self.logger = logger

    def __str__(self):
        return (
            f"Error building image {self.image_name}: {self.super_str}\n"
            f"Check ({self.log_path}) for more information."
        )


def setup_logger(instance_id: str, log_file: Path, mode="w"):
    """
    This logger is used for logging the build process of images and containers.
    It writes logs to the log file.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"{instance_id}.{log_file.name}")
    handler = logging.FileHandler(log_file, mode=mode)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    setattr(logger, "log_file", log_file)
    return logger


def close_logger(logger):
    # To avoid too many open files
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)


def build_image(
    image_name: str,
    setup_scripts: dict,
    dockerfile: str,
    platform: str,
    build_dir: Path,
    nocache: bool = False,
    use_buildx: bool = False,
):
    """
    Builds a docker image with the given name, setup scripts, dockerfile, and platform.

    Args:
        image_name (str): Name of the image to build
        setup_scripts (dict): Dictionary of setup script names to setup script contents
        dockerfile (str): Contents of the Dockerfile
        platform (str): Platform to build the image for
        client (docker.DockerClient): Docker client to use for building the image
        build_dir (Path): Directory for the build context (will also contain logs, scripts, and artifacts)
        nocache (bool): Whether to use the cache when building
        use_buildx (bool): Whether to use buildx for cross-platform builds
    """
    start_time = time.time()

    client = docker.from_env()
    # Create a logger for the build process
    logger = setup_logger(image_name, build_dir / "build_image.log")
    logger.info(
        f"Building image {image_name}\n"
        f"Using dockerfile:\n{dockerfile}\n"
        f"Adding ({len(setup_scripts)}) setup scripts to image build repo"
    )

    for setup_script_name, setup_script in setup_scripts.items():
        logger.info(f"[SETUP SCRIPT] {setup_script_name}:\n{setup_script}")
    try:
        # Write the setup scripts to the build directory
        for setup_script_name, setup_script in setup_scripts.items():
            setup_script_path = build_dir / setup_script_name
            with open(setup_script_path, "w") as f:
                f.write(setup_script)
            if setup_script_name not in dockerfile:
                logger.warning(
                    f"Setup script {setup_script_name} may not be used in Dockerfile"
                )

        # Write the dockerfile to the build directory
        dockerfile_path = build_dir / "Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile)

        # Build the image
        print(
            f"Building docker image {image_name} in {build_dir} with platform {platform}"
        )
        print(
            f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
        )
        logger.info(
            f"Building docker image {image_name} in {build_dir} with platform {platform}"
        )

        if use_buildx:
            # Use buildx for cross-platform builds.
            # `docker build` calls `docker buildx build` under the hood.
            cmd = [
                "docker",
                "build",
                "--platform",
                platform,
                "-t",
                image_name,
                "--load",
                str(build_dir),
            ]
            print(f"Using buildx to build image {image_name} on platform {platform}")
            print(f"Command: `{' '.join(cmd)}`")
            if nocache:
                cmd.append("--no-cache")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            try:
                stdout, stderr = process.communicate(timeout=3600)  # 60 minutes timeout
                buildlog = stdout + stderr
                for line in buildlog.splitlines():
                    logger.info(line.strip())
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                print(f"Build process timed out after 60 minutes")
                logger.error("Build process timed out after 60 minutes")
                raise BuildImageError(image_name, "Build timed out", logger)

            if process.returncode != 0:
                print(f"Build failed with exit code {process.returncode}")
                logger.error(
                    f"Build failed with exit code {process.returncode}\nError: {stderr}"
                )
                raise BuildImageError(
                    image_name,
                    f"Build failed with exit code {process.returncode}\nError: {stderr}",
                    logger,
                )

        else:
            # Use Docker Python SDK for regular builds
            response = client.api.build(
                path=str(build_dir),
                tag=image_name,
                rm=True,
                forcerm=True,
                decode=True,
                platform=platform,
                nocache=nocache,
            )

            buildlog = ""
            for chunk in response:
                if "stream" in chunk:
                    chunk_stream = ansi_escape.sub("", chunk["stream"])
                    logger.info(chunk_stream.strip())
                    buildlog += chunk_stream
                elif "errorDetail" in chunk:
                    logger.error(
                        f"Error: {ansi_escape.sub('', chunk['errorDetail']['message'])}"
                    )
                    raise docker.errors.BuildError(
                        chunk["errorDetail"]["message"], buildlog
                    )

        logger.info("Image built successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error during {image_name} build: {e}")
        raise BuildImageError(image_name, str(e), logger) from e
    except docker.errors.BuildError as e:
        logger.error(f"docker.errors.BuildError during {image_name}: {e}")
        raise BuildImageError(image_name, str(e), logger) from e
    except Exception as e:
        logger.error(f"Error building image {image_name}: {e}")
        raise BuildImageError(image_name, str(e), logger) from e
    finally:
        end_time = time.time()
        build_time = end_time - start_time
        print(f"Build time for {image_name}: {timedelta(seconds=build_time)}")
        logger.info(f"Build time for {image_name}: {timedelta(seconds=build_time)}")
        close_logger(logger)


def build_base_images(
    client: docker.DockerClient,
    dataset: list,
    force_rebuild: bool = False,
    use_buildx: bool = False,
):
    """
    Builds the base images required for the dataset if they do not already exist.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
        force_rebuild (bool): Whether to force rebuild the images even if they already exist
    """
    # Get the base images to build from the dataset
    test_specs = get_test_specs_from_dataset(dataset)
    base_images = {
        x.base_image_key: (x.base_dockerfile, x.platform) for x in test_specs
    }
    if force_rebuild:
        for key in base_images:
            remove_image(client, key, "quiet")

    # Build the base images
    for image_name, (dockerfile, platform) in base_images.items():
        try:
            # Check if the base image already exists
            client.images.get(image_name)
            if force_rebuild:
                # Remove the base image if it exists and force rebuild is enabled
                remove_image(client, image_name, "quiet")
            else:
                print(f"Base image {image_name} already exists, skipping build.")
                continue
        except docker.errors.ImageNotFound:
            pass
        # Build the base image (if it does not exist or force rebuild is enabled)
        print(f"Building base image ({image_name})")
        build_image(
            image_name=image_name,
            setup_scripts={},
            dockerfile=dockerfile,
            platform=platform,
            build_dir=BASE_IMAGE_BUILD_DIR / image_name.replace(":", "__"),
            use_buildx=use_buildx,
        )
    print("Base images built successfully.")


def get_env_configs_to_build(
    client: docker.DockerClient,
    dataset: list,
):
    """
    Returns a dictionary of image names to build scripts and dockerfiles for environment images.
    Returns only the environment images that need to be built.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
    """
    image_scripts = dict()
    base_images = dict()
    test_specs = get_test_specs_from_dataset(dataset)

    for test_spec in test_specs:
        # Check if the base image exists
        try:
            if test_spec.base_image_key not in base_images:
                base_images[test_spec.base_image_key] = client.images.get(
                    test_spec.base_image_key
                )
            base_image = base_images[test_spec.base_image_key]
        except docker.errors.ImageNotFound:
            raise Exception(
                f"Base image {test_spec.base_image_key} not found for {test_spec.env_image_key}\n."
                "Please build the base images first."
            )

        # Check if the environment image exists
        image_exists = False
        try:
            env_image = client.images.get(test_spec.env_image_key)
            image_exists = True

            if env_image.attrs["Created"] < base_image.attrs["Created"]:
                # Remove the environment image if it was built after the base_image
                for dep in find_dependent_images(client, test_spec.env_image_key):
                    # Remove instance images that depend on this environment image
                    remove_image(client, dep.image_id, "quiet")
                remove_image(client, test_spec.env_image_key, "quiet")
                image_exists = False
        except docker.errors.ImageNotFound:
            pass
        if not image_exists:
            # Add the environment image to the list of images to build
            image_scripts[test_spec.env_image_key] = {
                "setup_script": test_spec.setup_env_script,
                "dockerfile": test_spec.env_dockerfile,
                "platform": test_spec.platform,
            }
    return image_scripts


def build_env_images(
    client: docker.DockerClient,
    dataset: list,
    force_rebuild: bool = False,
    max_workers: int = 4,
    use_buildx: bool = False,
):
    """
    Builds the environment images required for the dataset if they do not already exist.

    Args:
        client (docker.DockerClient): Docker client to use for building the images
        dataset (list): List of test specs or dataset to build images for
        force_rebuild (bool): Whether to force rebuild the images even if they already exist
        max_workers (int): Maximum number of workers to use for building images
    """
    # Get the environment images to build from the dataset
    if force_rebuild:
        env_image_keys = {x.env_image_key for x in get_test_specs_from_dataset(dataset)}
        for key in env_image_keys:
            remove_image(client, key, "quiet")
    build_base_images(client, dataset, force_rebuild, use_buildx)
    configs_to_build = get_env_configs_to_build(client, dataset)
    if len(configs_to_build) == 0:
        print("No environment images need to be built.")
        return [], []
    print(f"Total environment images to build: {len(configs_to_build)}")

    # Build the environment images
    successful, failed = list(), list()
    build_times = {}
    total_start_time = time.time()

    with tqdm(
        total=len(configs_to_build), smoothing=0, desc="Building environment images"
    ) as pbar:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Create a future for each image to build
            futures = {
                executor.submit(
                    build_image,
                    image_name,
                    {"setup_env.sh": config["setup_script"]},
                    config["dockerfile"],
                    config["platform"],
                    ENV_IMAGE_BUILD_DIR / image_name.replace(":", "__"),
                    use_buildx=use_buildx,
                ): image_name
                for image_name, config in configs_to_build.items()
            }

            # Wait for each future to complete
            for future in as_completed(futures):
                pbar.update(1)
                try:
                    # Update progress bar, check if image built successfully
                    future.result()
                    successful.append(futures[future])
                except BuildImageError as e:
                    print(f"BuildImageError {e.image_name}")
                    traceback.print_exc()
                    failed.append(futures[future])
                    continue
                except Exception as e:
                    print(f"Error building image")
                    traceback.print_exc()
                    failed.append(futures[future])
                    continue

    total_end_time = time.time()
    total_build_time = total_end_time - total_start_time
    print(f"Total build time for all images: {timedelta(seconds=total_build_time)}")
    print(
        f"Average build time per image: {timedelta(seconds=total_build_time / len(configs_to_build))}"
    )

    if build_times:
        longest_build = max(build_times, key=build_times.get)
        shortest_build = min(build_times, key=build_times.get)
        print(
            f"Longest build: {longest_build} ({timedelta(seconds=build_times[longest_build])})"
        )
        print(
            f"Shortest build: {shortest_build} ({timedelta(seconds=build_times[shortest_build])})"
        )

    # Show how many images failed to build
    if len(failed) == 0:
        print("All environment images built successfully.")
    else:
        print(f"{len(failed)} environment images failed to build.")

    # Return the list of (un)successfuly built images
    return successful, failed


def build_instance_images(
    client: docker.DockerClient,
    dataset: list,
    force_rebuild: bool = False,
    max_workers: int = 4,
    use_buildx: bool = False,
    dockerhub_prefix: str = "",
    push_to_registry: bool = False,
):
    """
    Builds the instance images required for the dataset if they do not already exist.

    Args:
        dataset (list): List of test specs or dataset to build images for
        client (docker.DockerClient): Docker client to use for building the images
        force_rebuild (bool): Whether to force rebuild the images even if they already exist
        max_workers (int): Maximum number of workers to use for building images
        use_buildx (bool): Whether to use buildx for cross-platform builds
        dockerhub_prefix (str): Prefix for DockerHub image names
        push_to_registry (bool): Whether to push images to DockerHub registry
    """
    # Build environment images (and base images as needed) first
    test_specs = list(map(make_test_spec, dataset))
    if force_rebuild:
        for spec in test_specs:
            remove_image(client, spec.instance_image_key, "quiet")
    _, env_failed = build_env_images(
        client, test_specs, force_rebuild, max_workers, use_buildx
    )

    if len(env_failed) > 0:
        # Don't build images for instances that depend on failed-to-build env images
        dont_run_specs = [
            spec for spec in test_specs if spec.env_image_key in env_failed
        ]
        test_specs = [
            spec for spec in test_specs if spec.env_image_key not in env_failed
        ]
        print(
            f"Skipping {len(dont_run_specs)} instances - due to failed env image builds"
        )
    print(f"Building instance images for {len(test_specs)} instances")
    successful, failed = list(), list()

    # Build the instance images
    with tqdm(
        total=len(test_specs), smoothing=0, desc="Building instance images"
    ) as pbar:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Create a future for each image to build
            futures = {
                executor.submit(
                    build_and_push,
                    test_spec,
                    client,
                    force_rebuild,
                    dockerhub_prefix,
                    push_to_registry,
                ): test_spec
                for test_spec in test_specs
            }

            # Wait for each future to complete
            for future in as_completed(futures):
                pbar.update(1)
                try:
                    # Update progress bar, check if image built successfully
                    result = future.result()
                    if result:
                        successful.append(futures[future])
                except BuildImageError as e:
                    print(f"BuildImageError {e.image_name}")
                    traceback.print_exc()
                    failed.append(futures[future])
                    continue
                except Exception as e:
                    print(f"Error building image")
                    traceback.print_exc()
                    failed.append(futures[future])
                    continue

    # Show how many images failed to build
    if len(failed) == 0:
        print("All instance images built successfully.")
    else:
        print(f"{len(failed)} instance images failed to build.")

    # Return the list of (un)successfuly built images
    return successful, failed


def build_and_push(
    test_spec: TestSpec,
    client: docker.DockerClient,
    nocache: bool,
    dockerhub_prefix: str,
    push_to_registry: bool,
):
    try:
        full_image_name = (
            f"{dockerhub_prefix}/{test_spec.instance_image_key}"
            if dockerhub_prefix
            else test_spec.instance_image_key
        )

        build_instance_image(
            test_spec=test_spec,
            client=client,
            nocache=nocache,
            full_image_name=full_image_name,
        )

        if push_to_registry:
            push_to_dockerhub(client, full_image_name)
            # Delete the local image after successful push
            remove_image(client, full_image_name, None)

        return full_image_name
    except Exception as e:
        print(f"Error building/pushing image for {test_spec.instance_id}: {e}")
        return None


def push_to_dockerhub(client, full_image_name):
    try:
        print(f"Pushing {full_image_name} to DockerHub...")
        for line in client.images.push(full_image_name, stream=True, decode=True):
            if "status" in line:
                print(f"Push status: {line['status']}")
        print(f"Successfully pushed {full_image_name} to DockerHub")
    except Exception as e:
        print(f"Error pushing {full_image_name} to DockerHub: {e}")


def build_instance_image(
    test_spec: TestSpec,
    client: docker.DockerClient,
    logger: logging.Logger,
    nocache: bool,
    full_image_name: str,
):
    """
    Builds the instance image for the given test spec if it does not already exist.

    Args:
        test_spec (TestSpec): Test spec to build the instance image for
        client (docker.DockerClient): Docker client to use for building the image
        logger (logging.Logger): Logger to use for logging the build process
        nocache (bool): Whether to use the cache when building
        full_image_name (str): Full name of the image (including DockerHub prefix)
    """
    # Set up logging for the build process
    build_dir = INSTANCE_IMAGE_BUILD_DIR / test_spec.instance_image_key.replace(
        ":", "__"
    )
    new_logger = False
    if logger is None:
        new_logger = True
        logger = setup_logger(test_spec.instance_id, build_dir / "prepare_image.log")

    # Get the image names and dockerfile for the instance image
    env_image_name = test_spec.env_image_key
    dockerfile = test_spec.instance_dockerfile

    # Check that the env. image the instance image is based on exists
    try:
        env_image = client.images.get(env_image_name)
    except docker.errors.ImageNotFound as e:
        raise BuildImageError(
            test_spec.instance_id,
            f"Environment image {env_image_name} not found for {test_spec.instance_id}",
            logger,
        ) from e
    logger.info(
        f"Environment image {env_image_name} found for {test_spec.instance_id}\n"
        f"Building instance image {full_image_name} for {test_spec.instance_id}"
    )

    # Check if the instance image already exists
    image_exists = False
    try:
        instance_image = client.images.get(full_image_name)
        if instance_image.attrs["Created"] < env_image.attrs["Created"]:
            # the environment image is newer than the instance image, meaning the instance image may be outdated
            remove_image(client, full_image_name, "quiet")
            image_exists = False
        else:
            image_exists = True
    except docker.errors.ImageNotFound:
        pass

    # Build the instance image
    if not image_exists:
        build_image(
            image_name=full_image_name,
            setup_scripts={
                "setup_repo.sh": test_spec.install_repo_script,
            },
            dockerfile=dockerfile,
            platform=test_spec.platform,
            build_dir=build_dir,
            nocache=nocache,
        )
        logger.info(f"Image {full_image_name} built successfully.")
    else:
        logger.info(f"Image {full_image_name} already exists, skipping build.")

    if new_logger:
        close_logger(logger)
