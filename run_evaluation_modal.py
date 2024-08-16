from __future__ import annotations

import modal
import json
from pathlib import Path
import subprocess
from argparse import ArgumentParser
from typing import Optional
from tqdm import tqdm
import time


class EvaluationError(Exception):
    def __init__(self, instance_id, message, logger):
        super().__init__(message)
        self.super_str = super().__str__()
        self.instance_id = instance_id
        self.log_file = logger.log_file
        self.logger = logger

    def __str__(self):
        return (
            f"Evaluation error for {self.instance_id}: {self.super_str}\n"
            f"Check ({self.log_file}) for more information."
        )


app = modal.App("swebench-evaluation")


def docker_image(instance_id):
    return f"huyouare/swebench-lite:sweb.eval.x86_64.{instance_id}"


def create_modal_image(instance_id):
    print(f"Creating modal image for {instance_id}")
    base_image = modal.Image.from_registry(
        docker_image(instance_id),
    )

    return base_image


def run_instance_modal_inner(patch_content: str, eval_script: str):
    print(f"Called run_instance_modal_inner...")
    start_time = time.time()
    # Set up working directory
    work_dir = Path("/tmp/workdir")
    work_dir.mkdir(exist_ok=True)

    # Write patch file
    patch_file = work_dir / "patch.diff"
    patch_file.write_text(patch_content)

    print(f"Applying patch file: {patch_file}")
    # Apply patch
    result = subprocess.run(
        ["git", "apply", "--allow-empty", "-v", str(patch_file)],
        cwd="/testbed",
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        result = subprocess.run(
            ["patch", "--batch", "--fuzz=5", "-p1", "-i", str(patch_file)],
            cwd="/testbed",
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"Failed to apply patch: {result.stderr}",
            }

    # Write eval script
    eval_file = work_dir / "eval.sh"
    eval_file.write_text(eval_script)

    # Run eval script
    print(f"Running eval script: {eval_file}")
    try:
        result = subprocess.run(
            ["/bin/bash", str(eval_file)],
            timeout=60 * 5,
            capture_output=True,
            text=True,
            cwd="/testbed",
        )
        output = result.stdout + result.stderr
        status = "success"
    except subprocess.TimeoutExpired as e:
        output = (
            e.stdout + e.stderr
            if e.stdout and e.stderr
            else "Timeout occurred, no output captured."
        )
        status = "timeout"

    # Get git diff
    print(f"Getting git diff")
    git_diff = subprocess.run(
        ["git", "diff"], cwd="/testbed", capture_output=True, text=True
    ).stdout.strip()

    print(f"Finished running eval script.")
    print(f"Result: {status}")
    print(f"Output: {output}")
    print(f"Git diff: {git_diff}")
    print(f"Time taken: {time.time() - start_time} seconds")
    return {"status": status, "output": output, "git_diff": git_diff}


@app.function(
    image=create_modal_image("astropy__astropy-12907"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_12907(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("astropy__astropy-14182"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_14182(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("astropy__astropy-14365"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_14365(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("astropy__astropy-14995"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_14995(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("astropy__astropy-6938"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_6938(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("astropy__astropy-7746"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_astropy_astropy_7746(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-10914"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_10914(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-10924"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_10924(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11001"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11001(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11019"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11019(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11039"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11039(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11049"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11049(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11099"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11099(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11133"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11133(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11179"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11179(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11283"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11283(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11422"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11422(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11564"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11564(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11583"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11583(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11620"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11620(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11630"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11630(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11742"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11742(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11797"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11797(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11815"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11815(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11848"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11848(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11905"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11905(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11910"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11910(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11964"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11964(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-11999"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_11999(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12113"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12113(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12125"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12125(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12184"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12184(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12284"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12284(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12286"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12286(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12308"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12308(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12453"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12453(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12470"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12470(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12497"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12497(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12589"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12589(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12700"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12700(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12708"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12708(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12747"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12747(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12856"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12856(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12908"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12908(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12915"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12915(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-12983"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_12983(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13028"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13028(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13033"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13033(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13158"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13158(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13220"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13220(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13230"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13230(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13265"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13265(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13315"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13315(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13321"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13321(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13401"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13401(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13447"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13447(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13448"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13448(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13551"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13551(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13590"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13590(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13658"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13658(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13660"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13660(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13710"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13710(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13757"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13757(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13768"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13768(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13925"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13925(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13933"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13933(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-13964"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_13964(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14016"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14016(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14017"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14017(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14155"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14155(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14238"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14238(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14382"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14382(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14411"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14411(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14534"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14534(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14580"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14580(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14608"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14608(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14667"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14667(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14672"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14672(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14730"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14730(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14752"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14752(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14787"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14787(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14855"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14855(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14915"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14915(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14997"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14997(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-14999"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_14999(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15061"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15061(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15202"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15202(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15213"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15213(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15252"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15252(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15320"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15320(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15347"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15347(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15388"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15388(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15400"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15400(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15498"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15498(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15695"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15695(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15738"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15738(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15781"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15781(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15789"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15789(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15790"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15790(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15814"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15814(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15819"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15819(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15851"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15851(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15902"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15902(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-15996"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_15996(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16041"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16041(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16046"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16046(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16139"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16139(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16229"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16229(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16255"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16255(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16379"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16379(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16400"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16400(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16408"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16408(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16527"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16527(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16595"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16595(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16816"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16816(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16820"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16820(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16873"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16873(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-16910"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_16910(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-17051"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_17051(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("django__django-17087"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_django_django_17087(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-18869"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_18869(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-22711"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_22711(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-22835"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_22835(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-23299"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_23299(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-23314"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_23314(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-23476"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_23476(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-23562"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_23562(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-23563"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_23563(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-25311"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_25311(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-25332"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_25332(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-25433"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_25433(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-25442"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_25442(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-25498"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_25498(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-26011"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_26011(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("matplotlib__matplotlib-26020"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_matplotlib_matplotlib_26020(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("mwaskom__seaborn-2848"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_mwaskom_seaborn_2848(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("mwaskom__seaborn-3010"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_mwaskom_seaborn_3010(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("mwaskom__seaborn-3190"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_mwaskom_seaborn_3190(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("mwaskom__seaborn-3407"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_mwaskom_seaborn_3407(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pallets__flask-4992"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pallets_flask_4992(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pallets__flask-5063"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pallets_flask_5063(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-1963"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_1963(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-2148"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_2148(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-2317"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_2317(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-2674"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_2674(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-3362"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_3362(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("psf__requests-863"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_psf_requests_863(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pydata__xarray-3364"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pydata_xarray_3364(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pydata__xarray-4094"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pydata_xarray_4094(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pydata__xarray-4248"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pydata_xarray_4248(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pydata__xarray-4493"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pydata_xarray_4493(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pydata__xarray-5131"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_pydata_xarray_5131(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-5859"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_5859(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-6506"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_6506(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-7080"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_7080(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-7114"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_7114(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-7228"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_7228(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pylint-dev__pylint-7993"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pylint_dev_pylint_7993(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-11143"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_11143(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-11148"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_11148(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5103"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5103(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5221"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5221(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5227"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5227(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5413"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5413(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5495"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5495(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-5692"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_5692(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-6116"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_6116(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-7168"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_7168(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-7220"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_7220(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-7373"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_7373(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-7432"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_7432(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-7490"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_7490(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-8365"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_8365(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-8906"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_8906(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("pytest-dev__pytest-9359"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_pytest_dev_pytest_9359(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-10297"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_10297(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-10508"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_10508(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-10949"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_10949(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-11040"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_11040(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-11281"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_11281(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-12471"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_12471(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13142"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13142(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13241"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13241(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13439"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13439(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13496"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13496(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13497"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13497(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13584"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13584(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-13779"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_13779(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-14087"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_14087(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-14092"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_14092(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-14894"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_14894(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-14983"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_14983(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-15512"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_15512(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-15535"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_15535(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-25500"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_25500(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-25570"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_25570(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-25638"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_25638(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("scikit-learn__scikit-learn-25747"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_scikit_learn_scikit_learn_25747(
    patch_content: str, eval_script: str
):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-10325"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_10325(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-10451"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_10451(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-11445"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_11445(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-7686"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_7686(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-7738"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_7738(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-7975"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_7975(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8273"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8273(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8282"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8282(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8435"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8435(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8474"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8474(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8506"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8506(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8595"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8595(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8627"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8627(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8713"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8713(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8721"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8721(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sphinx-doc__sphinx-8801"),
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal_sphinx_doc_sphinx_8801(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-11400"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_11400(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-11870"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_11870(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-11897"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_11897(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-12171"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_12171(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-12236"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_12236(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-12419"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_12419(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-12454"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_12454(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-12481"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_12481(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13031"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13031(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13043"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13043(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13146"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13146(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13177"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13177(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13437"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13437(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13471"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13471(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13480"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13480(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13647"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13647(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13773"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13773(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13895"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13895(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13915"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13915(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-13971"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_13971(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14024"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14024(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14308"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14308(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14317"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14317(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14396"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14396(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14774"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14774(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-14817"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_14817(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15011"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15011(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15308"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15308(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15345"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15345(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15346"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15346(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15609"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15609(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-15678"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_15678(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-16106"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_16106(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-16281"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_16281(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-16503"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_16503(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-16792"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_16792(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-16988"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_16988(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-17022"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_17022(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-17139"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_17139(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-17630"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_17630(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-17655"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_17655(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18057"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18057(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18087"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18087(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18189"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18189(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18199"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18199(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18532"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18532(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18621"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18621(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18698"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18698(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-18835"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_18835(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-19007"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_19007(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-19254"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_19254(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-19487"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_19487(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20049"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20049(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20154"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20154(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20212"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20212(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20322"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20322(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20442"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20442(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20590"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20590(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-20639"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_20639(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21055"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21055(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21171"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21171(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21379"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21379(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21612"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21612(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21614"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21614(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21627"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21627(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-21847"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_21847(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-22005"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_22005(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-22714"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_22714(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-22840"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_22840(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-23117"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_23117(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-23191"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_23191(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-23262"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_23262(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-24066"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_24066(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-24102"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_24102(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-24152"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_24152(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-24213"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_24213(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


@app.function(
    image=create_modal_image("sympy__sympy-24909"), cpu=1, memory=2048, timeout=60 * 10
)
def run_instance_modal_sympy_sympy_24909(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)


def dispatcher(instance_id: str):
    function_map = {
        "astropy__astropy-12907": run_instance_modal_astropy_astropy_12907,
        "astropy__astropy-14182": run_instance_modal_astropy_astropy_14182,
        "astropy__astropy-14365": run_instance_modal_astropy_astropy_14365,
        "astropy__astropy-14995": run_instance_modal_astropy_astropy_14995,
        "astropy__astropy-6938": run_instance_modal_astropy_astropy_6938,
        "astropy__astropy-7746": run_instance_modal_astropy_astropy_7746,
        "django__django-10914": run_instance_modal_django_django_10914,
        "django__django-10924": run_instance_modal_django_django_10924,
        "django__django-11001": run_instance_modal_django_django_11001,
        "django__django-11019": run_instance_modal_django_django_11019,
        "django__django-11039": run_instance_modal_django_django_11039,
        "django__django-11049": run_instance_modal_django_django_11049,
        "django__django-11099": run_instance_modal_django_django_11099,
        "django__django-11133": run_instance_modal_django_django_11133,
        "django__django-11179": run_instance_modal_django_django_11179,
        "django__django-11283": run_instance_modal_django_django_11283,
        "django__django-11422": run_instance_modal_django_django_11422,
        "django__django-11564": run_instance_modal_django_django_11564,
        "django__django-11583": run_instance_modal_django_django_11583,
        "django__django-11620": run_instance_modal_django_django_11620,
        "django__django-11630": run_instance_modal_django_django_11630,
        "django__django-11742": run_instance_modal_django_django_11742,
        "django__django-11797": run_instance_modal_django_django_11797,
        "django__django-11815": run_instance_modal_django_django_11815,
        "django__django-11848": run_instance_modal_django_django_11848,
        "django__django-11905": run_instance_modal_django_django_11905,
        "django__django-11910": run_instance_modal_django_django_11910,
        "django__django-11964": run_instance_modal_django_django_11964,
        "django__django-11999": run_instance_modal_django_django_11999,
        "django__django-12113": run_instance_modal_django_django_12113,
        "django__django-12125": run_instance_modal_django_django_12125,
        "django__django-12184": run_instance_modal_django_django_12184,
        "django__django-12284": run_instance_modal_django_django_12284,
        "django__django-12286": run_instance_modal_django_django_12286,
        "django__django-12308": run_instance_modal_django_django_12308,
        "django__django-12453": run_instance_modal_django_django_12453,
        "django__django-12470": run_instance_modal_django_django_12470,
        "django__django-12497": run_instance_modal_django_django_12497,
        "django__django-12589": run_instance_modal_django_django_12589,
        "django__django-12700": run_instance_modal_django_django_12700,
        "django__django-12708": run_instance_modal_django_django_12708,
        "django__django-12747": run_instance_modal_django_django_12747,
        "django__django-12856": run_instance_modal_django_django_12856,
        "django__django-12908": run_instance_modal_django_django_12908,
        "django__django-12915": run_instance_modal_django_django_12915,
        "django__django-12983": run_instance_modal_django_django_12983,
        "django__django-13028": run_instance_modal_django_django_13028,
        "django__django-13033": run_instance_modal_django_django_13033,
        "django__django-13158": run_instance_modal_django_django_13158,
        "django__django-13220": run_instance_modal_django_django_13220,
        "django__django-13230": run_instance_modal_django_django_13230,
        "django__django-13265": run_instance_modal_django_django_13265,
        "django__django-13315": run_instance_modal_django_django_13315,
        "django__django-13321": run_instance_modal_django_django_13321,
        "django__django-13401": run_instance_modal_django_django_13401,
        "django__django-13447": run_instance_modal_django_django_13447,
        "django__django-13448": run_instance_modal_django_django_13448,
        "django__django-13551": run_instance_modal_django_django_13551,
        "django__django-13590": run_instance_modal_django_django_13590,
        "django__django-13658": run_instance_modal_django_django_13658,
        "django__django-13660": run_instance_modal_django_django_13660,
        "django__django-13710": run_instance_modal_django_django_13710,
        "django__django-13757": run_instance_modal_django_django_13757,
        "django__django-13768": run_instance_modal_django_django_13768,
        "django__django-13925": run_instance_modal_django_django_13925,
        "django__django-13933": run_instance_modal_django_django_13933,
        "django__django-13964": run_instance_modal_django_django_13964,
        "django__django-14016": run_instance_modal_django_django_14016,
        "django__django-14017": run_instance_modal_django_django_14017,
        "django__django-14155": run_instance_modal_django_django_14155,
        "django__django-14238": run_instance_modal_django_django_14238,
        "django__django-14382": run_instance_modal_django_django_14382,
        "django__django-14411": run_instance_modal_django_django_14411,
        "django__django-14534": run_instance_modal_django_django_14534,
        "django__django-14580": run_instance_modal_django_django_14580,
        "django__django-14608": run_instance_modal_django_django_14608,
        "django__django-14667": run_instance_modal_django_django_14667,
        "django__django-14672": run_instance_modal_django_django_14672,
        "django__django-14730": run_instance_modal_django_django_14730,
        "django__django-14752": run_instance_modal_django_django_14752,
        "django__django-14787": run_instance_modal_django_django_14787,
        "django__django-14855": run_instance_modal_django_django_14855,
        "django__django-14915": run_instance_modal_django_django_14915,
        "django__django-14997": run_instance_modal_django_django_14997,
        "django__django-14999": run_instance_modal_django_django_14999,
        "django__django-15061": run_instance_modal_django_django_15061,
        "django__django-15202": run_instance_modal_django_django_15202,
        "django__django-15213": run_instance_modal_django_django_15213,
        "django__django-15252": run_instance_modal_django_django_15252,
        "django__django-15320": run_instance_modal_django_django_15320,
        "django__django-15347": run_instance_modal_django_django_15347,
        "django__django-15388": run_instance_modal_django_django_15388,
        "django__django-15400": run_instance_modal_django_django_15400,
        "django__django-15498": run_instance_modal_django_django_15498,
        "django__django-15695": run_instance_modal_django_django_15695,
        "django__django-15738": run_instance_modal_django_django_15738,
        "django__django-15781": run_instance_modal_django_django_15781,
        "django__django-15789": run_instance_modal_django_django_15789,
        "django__django-15790": run_instance_modal_django_django_15790,
        "django__django-15814": run_instance_modal_django_django_15814,
        "django__django-15819": run_instance_modal_django_django_15819,
        "django__django-15851": run_instance_modal_django_django_15851,
        "django__django-15902": run_instance_modal_django_django_15902,
        "django__django-15996": run_instance_modal_django_django_15996,
        "django__django-16041": run_instance_modal_django_django_16041,
        "django__django-16046": run_instance_modal_django_django_16046,
        "django__django-16139": run_instance_modal_django_django_16139,
        "django__django-16229": run_instance_modal_django_django_16229,
        "django__django-16255": run_instance_modal_django_django_16255,
        "django__django-16379": run_instance_modal_django_django_16379,
        "django__django-16400": run_instance_modal_django_django_16400,
        "django__django-16408": run_instance_modal_django_django_16408,
        "django__django-16527": run_instance_modal_django_django_16527,
        "django__django-16595": run_instance_modal_django_django_16595,
        "django__django-16816": run_instance_modal_django_django_16816,
        "django__django-16820": run_instance_modal_django_django_16820,
        "django__django-16873": run_instance_modal_django_django_16873,
        "django__django-16910": run_instance_modal_django_django_16910,
        "django__django-17051": run_instance_modal_django_django_17051,
        "django__django-17087": run_instance_modal_django_django_17087,
        "matplotlib__matplotlib-18869": run_instance_modal_matplotlib_matplotlib_18869,
        "matplotlib__matplotlib-22711": run_instance_modal_matplotlib_matplotlib_22711,
        "matplotlib__matplotlib-22835": run_instance_modal_matplotlib_matplotlib_22835,
        "matplotlib__matplotlib-23299": run_instance_modal_matplotlib_matplotlib_23299,
        "matplotlib__matplotlib-23314": run_instance_modal_matplotlib_matplotlib_23314,
        "matplotlib__matplotlib-23476": run_instance_modal_matplotlib_matplotlib_23476,
        "matplotlib__matplotlib-23562": run_instance_modal_matplotlib_matplotlib_23562,
        "matplotlib__matplotlib-23563": run_instance_modal_matplotlib_matplotlib_23563,
        "matplotlib__matplotlib-25311": run_instance_modal_matplotlib_matplotlib_25311,
        "matplotlib__matplotlib-25332": run_instance_modal_matplotlib_matplotlib_25332,
        "matplotlib__matplotlib-25433": run_instance_modal_matplotlib_matplotlib_25433,
        "matplotlib__matplotlib-25442": run_instance_modal_matplotlib_matplotlib_25442,
        "matplotlib__matplotlib-25498": run_instance_modal_matplotlib_matplotlib_25498,
        "matplotlib__matplotlib-26011": run_instance_modal_matplotlib_matplotlib_26011,
        "matplotlib__matplotlib-26020": run_instance_modal_matplotlib_matplotlib_26020,
        "mwaskom__seaborn-2848": run_instance_modal_mwaskom_seaborn_2848,
        "mwaskom__seaborn-3010": run_instance_modal_mwaskom_seaborn_3010,
        "mwaskom__seaborn-3190": run_instance_modal_mwaskom_seaborn_3190,
        "mwaskom__seaborn-3407": run_instance_modal_mwaskom_seaborn_3407,
        "pallets__flask-4992": run_instance_modal_pallets_flask_4992,
        "pallets__flask-5063": run_instance_modal_pallets_flask_5063,
        "psf__requests-1963": run_instance_modal_psf_requests_1963,
        "psf__requests-2148": run_instance_modal_psf_requests_2148,
        "psf__requests-2317": run_instance_modal_psf_requests_2317,
        "psf__requests-2674": run_instance_modal_psf_requests_2674,
        "psf__requests-3362": run_instance_modal_psf_requests_3362,
        "psf__requests-863": run_instance_modal_psf_requests_863,
        "pydata__xarray-3364": run_instance_modal_pydata_xarray_3364,
        "pydata__xarray-4094": run_instance_modal_pydata_xarray_4094,
        "pydata__xarray-4248": run_instance_modal_pydata_xarray_4248,
        "pydata__xarray-4493": run_instance_modal_pydata_xarray_4493,
        "pydata__xarray-5131": run_instance_modal_pydata_xarray_5131,
        "pylint-dev__pylint-5859": run_instance_modal_pylint_dev_pylint_5859,
        "pylint-dev__pylint-6506": run_instance_modal_pylint_dev_pylint_6506,
        "pylint-dev__pylint-7080": run_instance_modal_pylint_dev_pylint_7080,
        "pylint-dev__pylint-7114": run_instance_modal_pylint_dev_pylint_7114,
        "pylint-dev__pylint-7228": run_instance_modal_pylint_dev_pylint_7228,
        "pylint-dev__pylint-7993": run_instance_modal_pylint_dev_pylint_7993,
        "pytest-dev__pytest-11143": run_instance_modal_pytest_dev_pytest_11143,
        "pytest-dev__pytest-11148": run_instance_modal_pytest_dev_pytest_11148,
        "pytest-dev__pytest-5103": run_instance_modal_pytest_dev_pytest_5103,
        "pytest-dev__pytest-5221": run_instance_modal_pytest_dev_pytest_5221,
        "pytest-dev__pytest-5227": run_instance_modal_pytest_dev_pytest_5227,
        "pytest-dev__pytest-5413": run_instance_modal_pytest_dev_pytest_5413,
        "pytest-dev__pytest-5495": run_instance_modal_pytest_dev_pytest_5495,
        "pytest-dev__pytest-5692": run_instance_modal_pytest_dev_pytest_5692,
        "pytest-dev__pytest-6116": run_instance_modal_pytest_dev_pytest_6116,
        "pytest-dev__pytest-7168": run_instance_modal_pytest_dev_pytest_7168,
        "pytest-dev__pytest-7220": run_instance_modal_pytest_dev_pytest_7220,
        "pytest-dev__pytest-7373": run_instance_modal_pytest_dev_pytest_7373,
        "pytest-dev__pytest-7432": run_instance_modal_pytest_dev_pytest_7432,
        "pytest-dev__pytest-7490": run_instance_modal_pytest_dev_pytest_7490,
        "pytest-dev__pytest-8365": run_instance_modal_pytest_dev_pytest_8365,
        "pytest-dev__pytest-8906": run_instance_modal_pytest_dev_pytest_8906,
        "pytest-dev__pytest-9359": run_instance_modal_pytest_dev_pytest_9359,
        "scikit-learn__scikit-learn-10297": run_instance_modal_scikit_learn_scikit_learn_10297,
        "scikit-learn__scikit-learn-10508": run_instance_modal_scikit_learn_scikit_learn_10508,
        "scikit-learn__scikit-learn-10949": run_instance_modal_scikit_learn_scikit_learn_10949,
        "scikit-learn__scikit-learn-11040": run_instance_modal_scikit_learn_scikit_learn_11040,
        "scikit-learn__scikit-learn-11281": run_instance_modal_scikit_learn_scikit_learn_11281,
        "scikit-learn__scikit-learn-12471": run_instance_modal_scikit_learn_scikit_learn_12471,
        "scikit-learn__scikit-learn-13142": run_instance_modal_scikit_learn_scikit_learn_13142,
        "scikit-learn__scikit-learn-13241": run_instance_modal_scikit_learn_scikit_learn_13241,
        "scikit-learn__scikit-learn-13439": run_instance_modal_scikit_learn_scikit_learn_13439,
        "scikit-learn__scikit-learn-13496": run_instance_modal_scikit_learn_scikit_learn_13496,
        "scikit-learn__scikit-learn-13497": run_instance_modal_scikit_learn_scikit_learn_13497,
        "scikit-learn__scikit-learn-13584": run_instance_modal_scikit_learn_scikit_learn_13584,
        "scikit-learn__scikit-learn-13779": run_instance_modal_scikit_learn_scikit_learn_13779,
        "scikit-learn__scikit-learn-14087": run_instance_modal_scikit_learn_scikit_learn_14087,
        "scikit-learn__scikit-learn-14092": run_instance_modal_scikit_learn_scikit_learn_14092,
        "scikit-learn__scikit-learn-14894": run_instance_modal_scikit_learn_scikit_learn_14894,
        "scikit-learn__scikit-learn-14983": run_instance_modal_scikit_learn_scikit_learn_14983,
        "scikit-learn__scikit-learn-15512": run_instance_modal_scikit_learn_scikit_learn_15512,
        "scikit-learn__scikit-learn-15535": run_instance_modal_scikit_learn_scikit_learn_15535,
        "scikit-learn__scikit-learn-25500": run_instance_modal_scikit_learn_scikit_learn_25500,
        "scikit-learn__scikit-learn-25570": run_instance_modal_scikit_learn_scikit_learn_25570,
        "scikit-learn__scikit-learn-25638": run_instance_modal_scikit_learn_scikit_learn_25638,
        "scikit-learn__scikit-learn-25747": run_instance_modal_scikit_learn_scikit_learn_25747,
        "sphinx-doc__sphinx-10325": run_instance_modal_sphinx_doc_sphinx_10325,
        "sphinx-doc__sphinx-10451": run_instance_modal_sphinx_doc_sphinx_10451,
        "sphinx-doc__sphinx-11445": run_instance_modal_sphinx_doc_sphinx_11445,
        "sphinx-doc__sphinx-7686": run_instance_modal_sphinx_doc_sphinx_7686,
        "sphinx-doc__sphinx-7738": run_instance_modal_sphinx_doc_sphinx_7738,
        "sphinx-doc__sphinx-7975": run_instance_modal_sphinx_doc_sphinx_7975,
        "sphinx-doc__sphinx-8273": run_instance_modal_sphinx_doc_sphinx_8273,
        "sphinx-doc__sphinx-8282": run_instance_modal_sphinx_doc_sphinx_8282,
        "sphinx-doc__sphinx-8435": run_instance_modal_sphinx_doc_sphinx_8435,
        "sphinx-doc__sphinx-8474": run_instance_modal_sphinx_doc_sphinx_8474,
        "sphinx-doc__sphinx-8506": run_instance_modal_sphinx_doc_sphinx_8506,
        "sphinx-doc__sphinx-8595": run_instance_modal_sphinx_doc_sphinx_8595,
        "sphinx-doc__sphinx-8627": run_instance_modal_sphinx_doc_sphinx_8627,
        "sphinx-doc__sphinx-8713": run_instance_modal_sphinx_doc_sphinx_8713,
        "sphinx-doc__sphinx-8721": run_instance_modal_sphinx_doc_sphinx_8721,
        "sphinx-doc__sphinx-8801": run_instance_modal_sphinx_doc_sphinx_8801,
        "sympy__sympy-11400": run_instance_modal_sympy_sympy_11400,
        "sympy__sympy-11870": run_instance_modal_sympy_sympy_11870,
        "sympy__sympy-11897": run_instance_modal_sympy_sympy_11897,
        "sympy__sympy-12171": run_instance_modal_sympy_sympy_12171,
        "sympy__sympy-12236": run_instance_modal_sympy_sympy_12236,
        "sympy__sympy-12419": run_instance_modal_sympy_sympy_12419,
        "sympy__sympy-12454": run_instance_modal_sympy_sympy_12454,
        "sympy__sympy-12481": run_instance_modal_sympy_sympy_12481,
        "sympy__sympy-13031": run_instance_modal_sympy_sympy_13031,
        "sympy__sympy-13043": run_instance_modal_sympy_sympy_13043,
        "sympy__sympy-13146": run_instance_modal_sympy_sympy_13146,
        "sympy__sympy-13177": run_instance_modal_sympy_sympy_13177,
        "sympy__sympy-13437": run_instance_modal_sympy_sympy_13437,
        "sympy__sympy-13471": run_instance_modal_sympy_sympy_13471,
        "sympy__sympy-13480": run_instance_modal_sympy_sympy_13480,
        "sympy__sympy-13647": run_instance_modal_sympy_sympy_13647,
        "sympy__sympy-13773": run_instance_modal_sympy_sympy_13773,
        "sympy__sympy-13895": run_instance_modal_sympy_sympy_13895,
        "sympy__sympy-13915": run_instance_modal_sympy_sympy_13915,
        "sympy__sympy-13971": run_instance_modal_sympy_sympy_13971,
        "sympy__sympy-14024": run_instance_modal_sympy_sympy_14024,
        "sympy__sympy-14308": run_instance_modal_sympy_sympy_14308,
        "sympy__sympy-14317": run_instance_modal_sympy_sympy_14317,
        "sympy__sympy-14396": run_instance_modal_sympy_sympy_14396,
        "sympy__sympy-14774": run_instance_modal_sympy_sympy_14774,
        "sympy__sympy-14817": run_instance_modal_sympy_sympy_14817,
        "sympy__sympy-15011": run_instance_modal_sympy_sympy_15011,
        "sympy__sympy-15308": run_instance_modal_sympy_sympy_15308,
        "sympy__sympy-15345": run_instance_modal_sympy_sympy_15345,
        "sympy__sympy-15346": run_instance_modal_sympy_sympy_15346,
        "sympy__sympy-15609": run_instance_modal_sympy_sympy_15609,
        "sympy__sympy-15678": run_instance_modal_sympy_sympy_15678,
        "sympy__sympy-16106": run_instance_modal_sympy_sympy_16106,
        "sympy__sympy-16281": run_instance_modal_sympy_sympy_16281,
        "sympy__sympy-16503": run_instance_modal_sympy_sympy_16503,
        "sympy__sympy-16792": run_instance_modal_sympy_sympy_16792,
        "sympy__sympy-16988": run_instance_modal_sympy_sympy_16988,
        "sympy__sympy-17022": run_instance_modal_sympy_sympy_17022,
        "sympy__sympy-17139": run_instance_modal_sympy_sympy_17139,
        "sympy__sympy-17630": run_instance_modal_sympy_sympy_17630,
        "sympy__sympy-17655": run_instance_modal_sympy_sympy_17655,
        "sympy__sympy-18057": run_instance_modal_sympy_sympy_18057,
        "sympy__sympy-18087": run_instance_modal_sympy_sympy_18087,
        "sympy__sympy-18189": run_instance_modal_sympy_sympy_18189,
        "sympy__sympy-18199": run_instance_modal_sympy_sympy_18199,
        "sympy__sympy-18532": run_instance_modal_sympy_sympy_18532,
        "sympy__sympy-18621": run_instance_modal_sympy_sympy_18621,
        "sympy__sympy-18698": run_instance_modal_sympy_sympy_18698,
        "sympy__sympy-18835": run_instance_modal_sympy_sympy_18835,
        "sympy__sympy-19007": run_instance_modal_sympy_sympy_19007,
        "sympy__sympy-19254": run_instance_modal_sympy_sympy_19254,
        "sympy__sympy-19487": run_instance_modal_sympy_sympy_19487,
        "sympy__sympy-20049": run_instance_modal_sympy_sympy_20049,
        "sympy__sympy-20154": run_instance_modal_sympy_sympy_20154,
        "sympy__sympy-20212": run_instance_modal_sympy_sympy_20212,
        "sympy__sympy-20322": run_instance_modal_sympy_sympy_20322,
        "sympy__sympy-20442": run_instance_modal_sympy_sympy_20442,
        "sympy__sympy-20590": run_instance_modal_sympy_sympy_20590,
        "sympy__sympy-20639": run_instance_modal_sympy_sympy_20639,
        "sympy__sympy-21055": run_instance_modal_sympy_sympy_21055,
        "sympy__sympy-21171": run_instance_modal_sympy_sympy_21171,
        "sympy__sympy-21379": run_instance_modal_sympy_sympy_21379,
        "sympy__sympy-21612": run_instance_modal_sympy_sympy_21612,
        "sympy__sympy-21614": run_instance_modal_sympy_sympy_21614,
        "sympy__sympy-21627": run_instance_modal_sympy_sympy_21627,
        "sympy__sympy-21847": run_instance_modal_sympy_sympy_21847,
        "sympy__sympy-22005": run_instance_modal_sympy_sympy_22005,
        "sympy__sympy-22714": run_instance_modal_sympy_sympy_22714,
        "sympy__sympy-22840": run_instance_modal_sympy_sympy_22840,
        "sympy__sympy-23117": run_instance_modal_sympy_sympy_23117,
        "sympy__sympy-23191": run_instance_modal_sympy_sympy_23191,
        "sympy__sympy-23262": run_instance_modal_sympy_sympy_23262,
        "sympy__sympy-24066": run_instance_modal_sympy_sympy_24066,
        "sympy__sympy-24102": run_instance_modal_sympy_sympy_24102,
        "sympy__sympy-24152": run_instance_modal_sympy_sympy_24152,
        "sympy__sympy-24213": run_instance_modal_sympy_sympy_24213,
        "sympy__sympy-24909": run_instance_modal_sympy_sympy_24909,
    }
    return function_map.get(instance_id)


async def process_instance(instance, predictions, run_id):
    from swebench.harness.grading import get_eval_report
    from swebench.harness.test_spec import make_test_spec
    from swebench.harness.constants import (
        RUN_EVALUATION_LOG_DIR,
    )

    test_spec = make_test_spec(instance)
    instance_id = test_spec.instance_id
    pred = predictions[instance_id]

    instance_function = dispatcher(instance_id)
    if instance_function is None:
        print(f"No function found for instance ID: {instance_id}")
        return None

    result = await instance_function.remote.aio(
        pred["model_patch"], test_spec.eval_script
    )
    print(f"Result for {instance_id}: {result}")

    # Process the result
    model_name_or_path = pred.get("model_name_or_path", "None").replace("/", "__")
    log_dir = Path(
        f"{RUN_EVALUATION_LOG_DIR}/{run_id}/{model_name_or_path}/{instance_id}"
    )
    log_dir.mkdir(parents=True, exist_ok=True)

    with open(log_dir / "test_output.txt", "w") as f:
        f.write(result["output"])

    if result["status"] == "success":
        report = get_eval_report(
            test_spec=test_spec,
            prediction=pred,
            log_path=log_dir / "test_output.txt",
            include_tests_status=True,
        )
        with open(log_dir / "report.json", "w") as f:
            json.dump(report, f, indent=4)
        return (instance_id, report)
    else:
        print(f"Error for {instance_id}: {result['status']}")
        return None


async def run_instances(predictions, instances, run_id):
    import asyncio

    tasks = [process_instance(instance, predictions, run_id) for instance in instances]
    results = []
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        try:
            result = await task
            print(f"Result: {result}")
            if result:
                results.append(result)
        except asyncio.CancelledError:
            print("Task was cancelled")
        except Exception as e:
            print(f"An error occurred during task execution: {str(e)}")
            # Optionally, you can log the full traceback
            import traceback
            print(traceback.format_exc())
    return results


def get_dataset_from_preds(
    dataset_name: str,
    split: str,
    instance_ids: list,
    predictions: dict,
    run_id: str,
    exclude_completed: bool = True,
):
    """
    Return only instances that have predictions and are in the dataset.
    If instance_ids is provided, only return instances with those IDs.
    If exclude_completed is True, only return instances that have not been run yet.
    """
    from swebench.harness.constants import (
        KEY_INSTANCE_ID,
        RUN_EVALUATION_LOG_DIR,
    )
    from swebench.harness.utils import load_swebench_dataset

    # load dataset
    dataset = load_swebench_dataset(dataset_name, split)
    dataset_ids = {i[KEY_INSTANCE_ID] for i in dataset}

    if instance_ids:
        # check that all instance IDs are in the dataset
        instance_ids = set(instance_ids)
        if instance_ids - dataset_ids:
            raise ValueError(
                (
                    "Some instance IDs not found in dataset!"
                    f"\nMissing IDs:\n{' '.join(instance_ids - dataset_ids)}"
                )
            )
        # check that all instance IDs have predictions
        missing_preds = instance_ids - set(predictions.keys())
        if missing_preds:
            print(
                f"Warning: Missing predictions for {len(missing_preds)} instance IDs."
            )

    # check that all prediction IDs are in the dataset
    prediction_ids = set(predictions.keys())
    if prediction_ids - dataset_ids:
        raise ValueError(
            (
                "Some prediction IDs not found in dataset!"
                f"\nMissing IDs:\n{' '.join(prediction_ids - dataset_ids)}"
            )
        )

    if instance_ids:
        # filter dataset to just the instance IDs
        dataset = [i for i in dataset if i[KEY_INSTANCE_ID] in instance_ids]

    # check which instance IDs have already been run
    completed_ids = set()
    for instance in dataset:
        if instance[KEY_INSTANCE_ID] not in prediction_ids:
            # skip instances without predictions
            continue
        prediction = predictions[instance[KEY_INSTANCE_ID]]
        report_file = (
            RUN_EVALUATION_LOG_DIR
            / run_id
            / prediction["model_name_or_path"].replace("/", "__")
            / prediction[KEY_INSTANCE_ID]
            / "report.json"
        )
        if report_file.exists():
            completed_ids.add(instance[KEY_INSTANCE_ID])

    if completed_ids and exclude_completed:
        # filter dataset to only instances that have not been run
        print(f"{len(completed_ids)} instances already run, skipping...")
        dataset = [i for i in dataset if i[KEY_INSTANCE_ID] not in completed_ids]

    empty_patch_ids = {
        k
        for k, v in predictions.items()
        if v["model_patch"] == "" or v["model_patch"] is None
    }

    # filter dataset to only instances with predictions
    dataset = [
        i
        for i in dataset
        if i[KEY_INSTANCE_ID] in prediction_ids
        and i[KEY_INSTANCE_ID] not in empty_patch_ids
    ]
    return dataset


def make_run_report(
    predictions: dict, full_dataset: list, results: list, run_id: str
) -> Path:
    """
    Make a final evaluation and run report of the instances that have been run.
    Also reports on images and containers that may still running!

    Args:
        predictions (dict): Predictions dict generated by the model
        full_dataset (list): List of all instances
        results (list): List of results from run_instances
        run_id (str): Run ID

    Returns:
        Path to report file
    """
    from swebench.harness.constants import (
        KEY_INSTANCE_ID,
        RUN_EVALUATION_LOG_DIR,
    )

    # instantiate sets to store IDs of different outcomes
    completed_ids = set()
    resolved_ids = set()
    error_ids = set()
    unresolved_ids = set()
    incomplete_ids = set()
    # get instances with empty patches
    empty_patch_ids = set()

    # iterate through dataset and check if the instance has been run
    for instance in full_dataset:
        instance_id = instance[KEY_INSTANCE_ID]
        if instance_id not in predictions:
            # skip instances without
            incomplete_ids.add(instance_id)
            continue
        prediction = predictions[instance_id]
        if prediction.get("model_patch", None) in ["", None]:
            empty_patch_ids.add(instance_id)
            continue
        report_file = (
            RUN_EVALUATION_LOG_DIR
            / run_id
            / prediction["model_name_or_path"].replace("/", "__")
            / prediction[KEY_INSTANCE_ID]
            / "report.json"
        )
        if report_file.exists():
            # If report file exists, then the instance has been run
            completed_ids.add(instance_id)
            report = json.loads(report_file.read_text())
            if report[instance_id]["resolved"]:
                # Record if the instance was resolved
                resolved_ids.add(instance_id)
            else:
                unresolved_ids.add(instance_id)
        else:
            # Otherwise, the instance was not run successfully
            error_ids.add(instance_id)

    # print final report
    print(f"Total instances: {len(full_dataset)}")
    print(f"Instances submitted: {len(predictions)}")
    print(f"Instances completed: {len(completed_ids)}")
    print(f"Instances incomplete: {len(incomplete_ids)}")
    print(f"Instances resolved: {len(resolved_ids)}")
    print(f"Instances unresolved: {len(unresolved_ids)}")
    print(f"Instances with empty patches: {len(empty_patch_ids)}")
    print(f"Instances with errors: {len(error_ids)}")

    # write report to file
    report = {
        "total_instances": len(full_dataset),
        "submitted_instances": len(predictions),
        "completed_instances": len(completed_ids),
        "resolved_instances": len(resolved_ids),
        "unresolved_instances": len(unresolved_ids),
        "empty_patch_instances": len(empty_patch_ids),
        "error_instances": len(error_ids),
        "completed_ids": list(sorted(completed_ids)),
        "incomplete_ids": list(sorted(incomplete_ids)),
        "empty_patch_ids": list(sorted(empty_patch_ids)),
        "submitted_ids": list(sorted(predictions.keys())),
        "resolved_ids": list(sorted(resolved_ids)),
        "unresolved_ids": list(sorted(unresolved_ids)),
        "error_ids": list(sorted(error_ids)),
        "schema_version": 2,
    }
    report_file = Path(
        list(predictions.values())[0]["model_name_or_path"].replace("/", "__")
        + f".{run_id}"
        + ".json"
    )
    with open(report_file, "w") as f:
        print(json.dumps(report, indent=4), file=f)
    print(f"Report written to {report_file}")
    return report_file


@app.local_entrypoint()
def main(
    dataset_name: str = "princeton-nlp/SWE-bench_Lite",
    split: str = "test",
    instance_ids: Optional[str] = None,
    predictions_path: str = None,
    max_workers: int = 4,
    force_rebuild: bool = False,
    cache_level: str = "env",
    clean: bool = False,
    run_id: str = None,
    timeout: int = 1800,
):
    """
    Run evaluation harness for the given dataset and predictions.
    """
    import asyncio
    from swebench.harness.constants import (
        KEY_INSTANCE_ID,
    )
    from swebench.harness.utils import load_swebench_dataset

    print(f"Running SWEBench on dataset {dataset_name} with split {split}")
    assert len(run_id) > 0, "Run ID must be provided"

    def get_gold_predictions(dataset_name: str, split: str):
        """
        Get gold predictions for the given dataset and split.
        """
        dataset = load_swebench_dataset(dataset_name, split)
        return [
            {
                KEY_INSTANCE_ID: datum[KEY_INSTANCE_ID],
                "model_patch": datum["patch"],
                "model_name_or_path": "gold",
            }
            for datum in dataset
        ]

    # load predictions as map of instance_id to prediction
    if predictions_path == "gold":
        print("Using gold predictions - ignoring predictions_path")
        predictions = get_gold_predictions(dataset_name, split)
    else:
        if predictions_path.endswith(".json"):
            with open(predictions_path, "r") as f:
                predictions = json.load(f)
        elif predictions_path.endswith(".jsonl"):
            with open(predictions_path, "r") as f:
                predictions = [json.loads(line) for line in f]
        else:
            raise ValueError('Predictions path must be "gold", .json, or .jsonl')
    predictions = {pred[KEY_INSTANCE_ID]: pred for pred in predictions}

    print(f"Predictions loaded: {len(predictions)}")
    # get dataset from predictions
    dataset = get_dataset_from_preds(
        dataset_name, split, instance_ids, predictions, run_id
    )
    print(f"Dataset loaded: {len(dataset)}")
    full_dataset = load_swebench_dataset(dataset_name, split)
    print(f"Full dataset loaded: {len(full_dataset)}")

    if not dataset:
        print("No instances to run.")
    else:
        results = asyncio.run(run_instances(predictions, dataset, run_id))

    print("Running final report...")
    make_run_report(predictions, full_dataset, results, run_id)


if __name__ == "__main__":
    from swebench.harness.utils import str2bool

    parser = ArgumentParser()
    parser.add_argument(
        "--dataset_name",
        default="princeton-nlp/SWE-bench_Lite",
        type=str,
        help="Name of dataset or path to JSON file.",
    )
    parser.add_argument(
        "--split", type=str, default="test", help="Split of the dataset"
    )
    parser.add_argument(
        "--instance_ids",
        nargs="+",
        type=str,
        help="Instance IDs to run (space separated)",
    )
    parser.add_argument(
        "--predictions_path",
        type=str,
        help="Path to predictions file - if 'gold', uses gold predictions",
        required=True,
    )
    parser.add_argument(
        "--max_workers",
        type=int,
        default=4,
        help="Maximum number of workers (should be <= 75%% of CPU cores)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1_800,
        help="Timeout (in seconds) for running tests for each instance",
    )
    parser.add_argument(
        "--force_rebuild",
        type=str2bool,
        default=False,
        help="Force rebuild of all images",
    )
    parser.add_argument(
        "--cache_level",
        type=str,
        choices=["none", "base", "env", "instance"],
        help="Cache level - remove images above this level",
        default="env",
    )
    # if clean is true then we remove all images that are above the cache level
    # if clean is false, we only remove images above the cache level if they don't already exist
    parser.add_argument(
        "--clean", type=str2bool, default=False, help="Clean images above cache level"
    )
    parser.add_argument(
        "--run_id", type=str, required=True, help="Run ID - identifies the run"
    )
    args = parser.parse_args()

    app.run()
