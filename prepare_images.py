import docker
import resource

from argparse import ArgumentParser

from swebench.harness.constants import KEY_INSTANCE_ID
from docker_build import build_instance_images  # Local import
from swebench.harness.docker_utils import list_images
from swebench.harness.test_spec import make_test_spec
from swebench.harness.utils import load_swebench_dataset, str2bool

# This is only imported so we can monkey patch platform.machine().
import platform


def filter_dataset_to_build(
    dataset: list, instance_ids: list, client: docker.DockerClient, force_rebuild: bool
):
    """
    Filter the dataset to only include instances that need to be built.

    Args:
        dataset (list): List of instances (usually all of SWE-bench dev/test split)
        instance_ids (list): List of instance IDs to build.
        client (docker.DockerClient): Docker client.
        force_rebuild (bool): Whether to force rebuild all images.
    """
    # Get existing images
    existing_images = list_images(client)
    data_to_build = []

    # Check if all instance IDs are in the dataset
    not_in_dataset = set(instance_ids).difference(
        set([instance[KEY_INSTANCE_ID] for instance in dataset])
    )
    if not_in_dataset:
        raise ValueError(f"Instance IDs not found in dataset: {not_in_dataset}")

    for instance in dataset:
        if instance[KEY_INSTANCE_ID] not in instance_ids:
            # Skip instances not in the list
            continue

        # Check if the instance needs to be built (based on force_rebuild flag and existing images)
        spec = make_test_spec(instance)
        if force_rebuild:
            data_to_build.append(instance)
        elif spec.instance_image_key not in existing_images:
            data_to_build.append(instance)

    return data_to_build


def main(
    dataset_name,
    split,
    instance_ids,
    max_workers,
    force_rebuild,
    open_file_limit,
    only_x86_64,
    use_buildx,
    push_to_registry,
    dockerhub_username,
    dockerhub_repo,
):
    """
    Build Docker images for the specified instances.

    Args:
        instance_ids (list): List of instance IDs to build.
        max_workers (int): Number of workers for parallel processing.
        force_rebuild (bool): Whether to force rebuild all images.
        open_file_limit (int): Open file limit.
        only_x86_64 (bool): Whether to only build x86_64 images.
        use_buildx (bool): Whether to use buildx to build multi-architecture images.
        push_to_registry (bool): Whether to push images to DockerHub registry.
        dockerhub_username (str): DockerHub username.
        dockerhub_repo (str): DockerHub repository name.
    """
    if only_x86_64:
        # TODO: Do something better here.
        # Monkey patch platform.machine() so that we always build x86_64 images.
        platform.machine = lambda: "x86_64"

    # Set open file limit
    resource.setrlimit(resource.RLIMIT_NOFILE, (open_file_limit, open_file_limit))
    client = docker.from_env()

    # Filter out instances that were not specified
    dataset = load_swebench_dataset(dataset_name, split)
    if instance_ids:
        dataset = filter_dataset_to_build(dataset, instance_ids, client, force_rebuild)

    # Construct DockerHub prefix
    dockerhub_prefix = (
        f"{dockerhub_username}/{dockerhub_repo}"
        if dockerhub_username and dockerhub_repo
        else ""
    )

    # Build images for remaining instances
    successful, failed = build_instance_images(
        client=client,
        dataset=dataset,
        force_rebuild=force_rebuild,
        max_workers=max_workers,
        use_buildx=use_buildx,
        push_to_registry=push_to_registry,
        dockerhub_prefix=dockerhub_prefix,
    )
    print(f"Successfully built {len(successful)} images")
    print(f"Failed to build {len(failed)} images")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--dataset_name",
        type=str,
        default="princeton-nlp/SWE-bench_Lite",
        help="Name of the dataset to use",
    )
    parser.add_argument("--split", type=str, default="test", help="Split to use")
    parser.add_argument(
        "--instance_ids",
        nargs="+",
        type=str,
        help="Instance IDs to run (space separated)",
    )
    parser.add_argument(
        "--max_workers", type=int, default=4, help="Max workers for parallel processing"
    )
    parser.add_argument(
        "--force_rebuild", type=str2bool, default=False, help="Force rebuild images"
    )
    parser.add_argument(
        "--open_file_limit", type=int, default=8192, help="Open file limit"
    )
    parser.add_argument(
        "--only_x86_64", type=str2bool, default=True, help="Only build x86_64 images"
    )
    parser.add_argument(
        "--use_buildx",
        type=str2bool,
        default=True,
        help="Use buildx to build multi-architecture images (building x86_64 images from arm64)",
    )
    parser.add_argument(
        "--push_to_registry",
        type=str2bool,
        default=True,
        help="Push images to DockerHub registry",
    )
    parser.add_argument(
        "--dockerhub_username",
        type=str,
        default="",
        help="DockerHub username",
    )
    parser.add_argument(
        "--dockerhub_repo",
        type=str,
        default="",
        help="DockerHub repository name",
    )
    args = parser.parse_args()
    main(**vars(args))
