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
    return f"huyouare/swebench-verified:sweb.eval.x86_64.{instance_id}"


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


@app.function(image=create_modal_image("astropy__astropy-12907"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_12907(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13033"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13033(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13236"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13236(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13398"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13398(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13453"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13453(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13579"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13579(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-13977"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_13977(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14096"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14096(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14182"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14182(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14309"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14309(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14365"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14365(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14369"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14369(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14508"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14508(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14539"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14539(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14598"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14598(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-14995"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_14995(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-7166"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_7166(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-7336"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_7336(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-7606"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_7606(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-7671"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_7671(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-8707"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_8707(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("astropy__astropy-8872"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_astropy_astropy_8872(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-10554"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_10554(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-10880"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_10880(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-10914"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_10914(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-10973"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_10973(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-10999"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_10999(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11066"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11066(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11087"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11087(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11095"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11095(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11099"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11099(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11119"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11119(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11133"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11133(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11138"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11138(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11141"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11141(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11149"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11149(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11163"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11163(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11179"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11179(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11206"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11206(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11211"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11211(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11239"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11239(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11265"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11265(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11276"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11276(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11292"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11292(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11299"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11299(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11333"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11333(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11400"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11400(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11433"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11433(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11451"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11451(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11477"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11477(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11490"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11490(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11532"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11532(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11551"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11551(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11555"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11555(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11603"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11603(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11728"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11728(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11734"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11734(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11740"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11740(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11749"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11749(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11790"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11790(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11815"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11815(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11820"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11820(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11848"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11848(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11880"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11880(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11885"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11885(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11951"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11951(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11964"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11964(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-11999"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_11999(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12039"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12039(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12050"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12050(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12125"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12125(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12143"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12143(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12155"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12155(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12193"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12193(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12262"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12262(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12273"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12273(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12276"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12276(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12304"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12304(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12308"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12308(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12325"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12325(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12406"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12406(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12419"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12419(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12663"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12663(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12708"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12708(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12713"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12713(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12741"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12741(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12754"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12754(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12774"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12774(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12858"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12858(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-12965"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_12965(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13012"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13012(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13023"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13023(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13028"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13028(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13033"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13033(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13089"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13089(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13109"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13109(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13112"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13112(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13121"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13121(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13128"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13128(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13158"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13158(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13195"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13195(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13212"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13212(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13279"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13279(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13297"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13297(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13315"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13315(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13343"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13343(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13344"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13344(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13346"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13346(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13363"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13363(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13401"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13401(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13406"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13406(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13410"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13410(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13417"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13417(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13449"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13449(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13512"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13512(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13513"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13513(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13516"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13516(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13551"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13551(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13568"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13568(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13569"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13569(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13590"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13590(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13658"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13658(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13670"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13670(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13741"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13741(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13786"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13786(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13794"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13794(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13807"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13807(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13809"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13809(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13810"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13810(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13820"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13820(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13821"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13821(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13837"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13837(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13925"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13925(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13933"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13933(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-13964"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_13964(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14007"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14007(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14011"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14011(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14017"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14017(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14034"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14034(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14053"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14053(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14089"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14089(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14122"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14122(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14140"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14140(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14155"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14155(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14170"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14170(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14238"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14238(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14311"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14311(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14315"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14315(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14349"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14349(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14351"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14351(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14373"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14373(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14376"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14376(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14404"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14404(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14493"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14493(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14500"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14500(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14534"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14534(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14539"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14539(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14559"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14559(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14580"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14580(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14608"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14608(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14631"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14631(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14672"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14672(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14725"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14725(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14752"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14752(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14765"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14765(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14771"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14771(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14787"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14787(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14792"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14792(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14855"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14855(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14915"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14915(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-14999"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_14999(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15022"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15022(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15037"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15037(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15098"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15098(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15103"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15103(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15104"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15104(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15127"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15127(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15128"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15128(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15161"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15161(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15252"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15252(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15268"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15268(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15277"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15277(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15278"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15278(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15280"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15280(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15315"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15315(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15368"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15368(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15375"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15375(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15380"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15380(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15382"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15382(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15467"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15467(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15499"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15499(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15503"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15503(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15525"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15525(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15554"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15554(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15561"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15561(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15563"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15563(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15569"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15569(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15572"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15572(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15629"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15629(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15695"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15695(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15731"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15731(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15732"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15732(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15741"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15741(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15814"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15814(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15851"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15851(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15863"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15863(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15916"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15916(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15930"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15930(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15957"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15957(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15973"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15973(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-15987"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_15987(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16032"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16032(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16082"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16082(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16100"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16100(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16116"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16116(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16139"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16139(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16145"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16145(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16255"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16255(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16256"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16256(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16263"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16263(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16315"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16315(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16333"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16333(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16429"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16429(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16454"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16454(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16485"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16485(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16493"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16493(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16502"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16502(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16527"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16527(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16560"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16560(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16569"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16569(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16595"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16595(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16612"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16612(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16631"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16631(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16642"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16642(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16661"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16661(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16662"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16662(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16667"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16667(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16801"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16801(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16819"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16819(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16899"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16899(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16901"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16901(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-16938"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_16938(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-17029"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_17029(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-17084"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_17084(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-17087"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_17087(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("django__django-9296"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_django_django_9296(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-22719"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_22719(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-22865"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_22865(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-22871"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_22871(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-23299"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_23299(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-23412"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_23412(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25287"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25287(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25311"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25311(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25332"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25332(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25479"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25479(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25775"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25775(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-25960"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_25960(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-26113"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_26113(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-26208"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_26208(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-26291"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_26291(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-26342"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_26342(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("matplotlib__matplotlib-26466"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_matplotlib_matplotlib_26466(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("mwaskom__seaborn-3069"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_mwaskom_seaborn_3069(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("mwaskom__seaborn-3187"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_mwaskom_seaborn_3187(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pallets__flask-5014"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pallets_flask_5014(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-1142"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_1142(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-1724"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_1724(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-1766"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_1766(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-1921"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_1921(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-2317"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_2317(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-2931"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_2931(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-5414"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_5414(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("psf__requests-6028"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_psf_requests_6028(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-2905"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_2905(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-3095"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_3095(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-3151"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_3151(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-3305"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_3305(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-3677"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_3677(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-3993"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_3993(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4075"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4075(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4094"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4094(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4356"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4356(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4629"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4629(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4687"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4687(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4695"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4695(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pydata__xarray-4966"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pydata_xarray_4966(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pylint-dev__pylint-6386"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pylint_dev_pylint_6386(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pylint-dev__pylint-6528"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pylint_dev_pylint_6528(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pylint-dev__pylint-6903"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pylint_dev_pylint_6903(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pylint-dev__pylint-7080"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pylint_dev_pylint_7080(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pylint-dev__pylint-7277"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pylint_dev_pylint_7277(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-5262"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_5262(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-5631"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_5631(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-5787"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_5787(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-5809"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_5809(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-5840"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_5840(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-6197"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_6197(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-6202"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_6202(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7205"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7205(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7236"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7236(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7324"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7324(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7432"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7432(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7490"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7490(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7521"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7521(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7571"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7571(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-7982"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_7982(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("pytest-dev__pytest-8399"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_pytest_dev_pytest_8399(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-10297"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_10297(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-10844"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_10844(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-10908"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_10908(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-11310"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_11310(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-11578"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_11578(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-12585"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_12585(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-12682"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_12682(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-12973"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_12973(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13124"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13124(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13135"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13135(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13142"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13142(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13439"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13439(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13496"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13496(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-13779"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_13779(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14053"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14053(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14087"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14087(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14141"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14141(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14496"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14496(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14629"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14629(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14710"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14710(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14894"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14894(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-14983"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_14983(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-15100"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_15100(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-25102"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_25102(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-25232"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_25232(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-25747"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_25747(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-25931"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_25931(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-25973"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_25973(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-26194"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_26194(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-26323"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_26323(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("scikit-learn__scikit-learn-9288"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_scikit_learn_scikit_learn_9288(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10323"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10323(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10435"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10435(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10449"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10449(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10466"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10466(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10614"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10614(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-10673"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_10673(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-11445"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_11445(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-11510"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_11510(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7440"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7440(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7454"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7454(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7462"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7462(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7590"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7590(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7748"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7748(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7757"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7757(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7889"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7889(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7910"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7910(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-7985"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_7985(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8035"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8035(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8056"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8056(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8120"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8120(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8265"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8265(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8269"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8269(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8459"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8459(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8475"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8475(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8548"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8548(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8551"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8551(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8593"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8593(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8595"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8595(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8621"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8621(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8638"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8638(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-8721"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_8721(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9229"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9229(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9230"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9230(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9281"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9281(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9320"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9320(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9367"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9367(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9461"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9461(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9591"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9591(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9602"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9602(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9658"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9658(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9673"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9673(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9698"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9698(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sphinx-doc__sphinx-9711"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sphinx_doc_sphinx_9711(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-11618"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_11618(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-12096"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_12096(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-12419"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_12419(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-12481"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_12481(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-12489"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_12489(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13031"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13031(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13091"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13091(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13372"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13372(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13480"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13480(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13551"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13551(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13615"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13615(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13647"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13647(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13757"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13757(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13798"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13798(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13852"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13852(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13877"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13877(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13878"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13878(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-13974"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_13974(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-14248"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_14248(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-14531"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_14531(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-14711"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_14711(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-14976"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_14976(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15017"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15017(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15345"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15345(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15349"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15349(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15599"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15599(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15809"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15809(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15875"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15875(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-15976"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_15976(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-16450"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_16450(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-16597"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_16597(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-16766"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_16766(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-16792"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_16792(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-16886"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_16886(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-17139"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_17139(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-17318"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_17318(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-17630"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_17630(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-17655"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_17655(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-18189"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_18189(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-18199"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_18199(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-18211"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_18211(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-18698"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_18698(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-18763"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_18763(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19040"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19040(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19346"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19346(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19495"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19495(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19637"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19637(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19783"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19783(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-19954"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_19954(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20154"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20154(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20428"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20428(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20438"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20438(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20590"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20590(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20801"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20801(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-20916"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_20916(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-21379"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_21379(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-21596"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_21596(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-21612"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_21612(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-21847"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_21847(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-21930"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_21930(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-22080"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_22080(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-22456"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_22456(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-22714"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_22714(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-22914"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_22914(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-23262"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_23262(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-23413"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_23413(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-23534"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_23534(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-23824"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_23824(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-23950"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_23950(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24066"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24066(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24213"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24213(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24443"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24443(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24539"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24539(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24562"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24562(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

@app.function(image=create_modal_image("sympy__sympy-24661"), cpu=1, memory=2048, timeout=60 * 10)
def run_instance_modal_sympy_sympy_24661(patch_content: str, eval_script: str):
    return run_instance_modal_inner(patch_content, eval_script)

def dispatcher(instance_id: str):
    function_map = {
        "astropy__astropy-12907": run_instance_modal_astropy_astropy_12907,
        "astropy__astropy-13033": run_instance_modal_astropy_astropy_13033,
        "astropy__astropy-13236": run_instance_modal_astropy_astropy_13236,
        "astropy__astropy-13398": run_instance_modal_astropy_astropy_13398,
        "astropy__astropy-13453": run_instance_modal_astropy_astropy_13453,
        "astropy__astropy-13579": run_instance_modal_astropy_astropy_13579,
        "astropy__astropy-13977": run_instance_modal_astropy_astropy_13977,
        "astropy__astropy-14096": run_instance_modal_astropy_astropy_14096,
        "astropy__astropy-14182": run_instance_modal_astropy_astropy_14182,
        "astropy__astropy-14309": run_instance_modal_astropy_astropy_14309,
        "astropy__astropy-14365": run_instance_modal_astropy_astropy_14365,
        "astropy__astropy-14369": run_instance_modal_astropy_astropy_14369,
        "astropy__astropy-14508": run_instance_modal_astropy_astropy_14508,
        "astropy__astropy-14539": run_instance_modal_astropy_astropy_14539,
        "astropy__astropy-14598": run_instance_modal_astropy_astropy_14598,
        "astropy__astropy-14995": run_instance_modal_astropy_astropy_14995,
        "astropy__astropy-7166": run_instance_modal_astropy_astropy_7166,
        "astropy__astropy-7336": run_instance_modal_astropy_astropy_7336,
        "astropy__astropy-7606": run_instance_modal_astropy_astropy_7606,
        "astropy__astropy-7671": run_instance_modal_astropy_astropy_7671,
        "astropy__astropy-8707": run_instance_modal_astropy_astropy_8707,
        "astropy__astropy-8872": run_instance_modal_astropy_astropy_8872,
        "django__django-10554": run_instance_modal_django_django_10554,
        "django__django-10880": run_instance_modal_django_django_10880,
        "django__django-10914": run_instance_modal_django_django_10914,
        "django__django-10973": run_instance_modal_django_django_10973,
        "django__django-10999": run_instance_modal_django_django_10999,
        "django__django-11066": run_instance_modal_django_django_11066,
        "django__django-11087": run_instance_modal_django_django_11087,
        "django__django-11095": run_instance_modal_django_django_11095,
        "django__django-11099": run_instance_modal_django_django_11099,
        "django__django-11119": run_instance_modal_django_django_11119,
        "django__django-11133": run_instance_modal_django_django_11133,
        "django__django-11138": run_instance_modal_django_django_11138,
        "django__django-11141": run_instance_modal_django_django_11141,
        "django__django-11149": run_instance_modal_django_django_11149,
        "django__django-11163": run_instance_modal_django_django_11163,
        "django__django-11179": run_instance_modal_django_django_11179,
        "django__django-11206": run_instance_modal_django_django_11206,
        "django__django-11211": run_instance_modal_django_django_11211,
        "django__django-11239": run_instance_modal_django_django_11239,
        "django__django-11265": run_instance_modal_django_django_11265,
        "django__django-11276": run_instance_modal_django_django_11276,
        "django__django-11292": run_instance_modal_django_django_11292,
        "django__django-11299": run_instance_modal_django_django_11299,
        "django__django-11333": run_instance_modal_django_django_11333,
        "django__django-11400": run_instance_modal_django_django_11400,
        "django__django-11433": run_instance_modal_django_django_11433,
        "django__django-11451": run_instance_modal_django_django_11451,
        "django__django-11477": run_instance_modal_django_django_11477,
        "django__django-11490": run_instance_modal_django_django_11490,
        "django__django-11532": run_instance_modal_django_django_11532,
        "django__django-11551": run_instance_modal_django_django_11551,
        "django__django-11555": run_instance_modal_django_django_11555,
        "django__django-11603": run_instance_modal_django_django_11603,
        "django__django-11728": run_instance_modal_django_django_11728,
        "django__django-11734": run_instance_modal_django_django_11734,
        "django__django-11740": run_instance_modal_django_django_11740,
        "django__django-11749": run_instance_modal_django_django_11749,
        "django__django-11790": run_instance_modal_django_django_11790,
        "django__django-11815": run_instance_modal_django_django_11815,
        "django__django-11820": run_instance_modal_django_django_11820,
        "django__django-11848": run_instance_modal_django_django_11848,
        "django__django-11880": run_instance_modal_django_django_11880,
        "django__django-11885": run_instance_modal_django_django_11885,
        "django__django-11951": run_instance_modal_django_django_11951,
        "django__django-11964": run_instance_modal_django_django_11964,
        "django__django-11999": run_instance_modal_django_django_11999,
        "django__django-12039": run_instance_modal_django_django_12039,
        "django__django-12050": run_instance_modal_django_django_12050,
        "django__django-12125": run_instance_modal_django_django_12125,
        "django__django-12143": run_instance_modal_django_django_12143,
        "django__django-12155": run_instance_modal_django_django_12155,
        "django__django-12193": run_instance_modal_django_django_12193,
        "django__django-12262": run_instance_modal_django_django_12262,
        "django__django-12273": run_instance_modal_django_django_12273,
        "django__django-12276": run_instance_modal_django_django_12276,
        "django__django-12304": run_instance_modal_django_django_12304,
        "django__django-12308": run_instance_modal_django_django_12308,
        "django__django-12325": run_instance_modal_django_django_12325,
        "django__django-12406": run_instance_modal_django_django_12406,
        "django__django-12419": run_instance_modal_django_django_12419,
        "django__django-12663": run_instance_modal_django_django_12663,
        "django__django-12708": run_instance_modal_django_django_12708,
        "django__django-12713": run_instance_modal_django_django_12713,
        "django__django-12741": run_instance_modal_django_django_12741,
        "django__django-12754": run_instance_modal_django_django_12754,
        "django__django-12774": run_instance_modal_django_django_12774,
        "django__django-12858": run_instance_modal_django_django_12858,
        "django__django-12965": run_instance_modal_django_django_12965,
        "django__django-13012": run_instance_modal_django_django_13012,
        "django__django-13023": run_instance_modal_django_django_13023,
        "django__django-13028": run_instance_modal_django_django_13028,
        "django__django-13033": run_instance_modal_django_django_13033,
        "django__django-13089": run_instance_modal_django_django_13089,
        "django__django-13109": run_instance_modal_django_django_13109,
        "django__django-13112": run_instance_modal_django_django_13112,
        "django__django-13121": run_instance_modal_django_django_13121,
        "django__django-13128": run_instance_modal_django_django_13128,
        "django__django-13158": run_instance_modal_django_django_13158,
        "django__django-13195": run_instance_modal_django_django_13195,
        "django__django-13212": run_instance_modal_django_django_13212,
        "django__django-13279": run_instance_modal_django_django_13279,
        "django__django-13297": run_instance_modal_django_django_13297,
        "django__django-13315": run_instance_modal_django_django_13315,
        "django__django-13343": run_instance_modal_django_django_13343,
        "django__django-13344": run_instance_modal_django_django_13344,
        "django__django-13346": run_instance_modal_django_django_13346,
        "django__django-13363": run_instance_modal_django_django_13363,
        "django__django-13401": run_instance_modal_django_django_13401,
        "django__django-13406": run_instance_modal_django_django_13406,
        "django__django-13410": run_instance_modal_django_django_13410,
        "django__django-13417": run_instance_modal_django_django_13417,
        "django__django-13449": run_instance_modal_django_django_13449,
        "django__django-13512": run_instance_modal_django_django_13512,
        "django__django-13513": run_instance_modal_django_django_13513,
        "django__django-13516": run_instance_modal_django_django_13516,
        "django__django-13551": run_instance_modal_django_django_13551,
        "django__django-13568": run_instance_modal_django_django_13568,
        "django__django-13569": run_instance_modal_django_django_13569,
        "django__django-13590": run_instance_modal_django_django_13590,
        "django__django-13658": run_instance_modal_django_django_13658,
        "django__django-13670": run_instance_modal_django_django_13670,
        "django__django-13741": run_instance_modal_django_django_13741,
        "django__django-13786": run_instance_modal_django_django_13786,
        "django__django-13794": run_instance_modal_django_django_13794,
        "django__django-13807": run_instance_modal_django_django_13807,
        "django__django-13809": run_instance_modal_django_django_13809,
        "django__django-13810": run_instance_modal_django_django_13810,
        "django__django-13820": run_instance_modal_django_django_13820,
        "django__django-13821": run_instance_modal_django_django_13821,
        "django__django-13837": run_instance_modal_django_django_13837,
        "django__django-13925": run_instance_modal_django_django_13925,
        "django__django-13933": run_instance_modal_django_django_13933,
        "django__django-13964": run_instance_modal_django_django_13964,
        "django__django-14007": run_instance_modal_django_django_14007,
        "django__django-14011": run_instance_modal_django_django_14011,
        "django__django-14017": run_instance_modal_django_django_14017,
        "django__django-14034": run_instance_modal_django_django_14034,
        "django__django-14053": run_instance_modal_django_django_14053,
        "django__django-14089": run_instance_modal_django_django_14089,
        "django__django-14122": run_instance_modal_django_django_14122,
        "django__django-14140": run_instance_modal_django_django_14140,
        "django__django-14155": run_instance_modal_django_django_14155,
        "django__django-14170": run_instance_modal_django_django_14170,
        "django__django-14238": run_instance_modal_django_django_14238,
        "django__django-14311": run_instance_modal_django_django_14311,
        "django__django-14315": run_instance_modal_django_django_14315,
        "django__django-14349": run_instance_modal_django_django_14349,
        "django__django-14351": run_instance_modal_django_django_14351,
        "django__django-14373": run_instance_modal_django_django_14373,
        "django__django-14376": run_instance_modal_django_django_14376,
        "django__django-14404": run_instance_modal_django_django_14404,
        "django__django-14493": run_instance_modal_django_django_14493,
        "django__django-14500": run_instance_modal_django_django_14500,
        "django__django-14534": run_instance_modal_django_django_14534,
        "django__django-14539": run_instance_modal_django_django_14539,
        "django__django-14559": run_instance_modal_django_django_14559,
        "django__django-14580": run_instance_modal_django_django_14580,
        "django__django-14608": run_instance_modal_django_django_14608,
        "django__django-14631": run_instance_modal_django_django_14631,
        "django__django-14672": run_instance_modal_django_django_14672,
        "django__django-14725": run_instance_modal_django_django_14725,
        "django__django-14752": run_instance_modal_django_django_14752,
        "django__django-14765": run_instance_modal_django_django_14765,
        "django__django-14771": run_instance_modal_django_django_14771,
        "django__django-14787": run_instance_modal_django_django_14787,
        "django__django-14792": run_instance_modal_django_django_14792,
        "django__django-14855": run_instance_modal_django_django_14855,
        "django__django-14915": run_instance_modal_django_django_14915,
        "django__django-14999": run_instance_modal_django_django_14999,
        "django__django-15022": run_instance_modal_django_django_15022,
        "django__django-15037": run_instance_modal_django_django_15037,
        "django__django-15098": run_instance_modal_django_django_15098,
        "django__django-15103": run_instance_modal_django_django_15103,
        "django__django-15104": run_instance_modal_django_django_15104,
        "django__django-15127": run_instance_modal_django_django_15127,
        "django__django-15128": run_instance_modal_django_django_15128,
        "django__django-15161": run_instance_modal_django_django_15161,
        "django__django-15252": run_instance_modal_django_django_15252,
        "django__django-15268": run_instance_modal_django_django_15268,
        "django__django-15277": run_instance_modal_django_django_15277,
        "django__django-15278": run_instance_modal_django_django_15278,
        "django__django-15280": run_instance_modal_django_django_15280,
        "django__django-15315": run_instance_modal_django_django_15315,
        "django__django-15368": run_instance_modal_django_django_15368,
        "django__django-15375": run_instance_modal_django_django_15375,
        "django__django-15380": run_instance_modal_django_django_15380,
        "django__django-15382": run_instance_modal_django_django_15382,
        "django__django-15467": run_instance_modal_django_django_15467,
        "django__django-15499": run_instance_modal_django_django_15499,
        "django__django-15503": run_instance_modal_django_django_15503,
        "django__django-15525": run_instance_modal_django_django_15525,
        "django__django-15554": run_instance_modal_django_django_15554,
        "django__django-15561": run_instance_modal_django_django_15561,
        "django__django-15563": run_instance_modal_django_django_15563,
        "django__django-15569": run_instance_modal_django_django_15569,
        "django__django-15572": run_instance_modal_django_django_15572,
        "django__django-15629": run_instance_modal_django_django_15629,
        "django__django-15695": run_instance_modal_django_django_15695,
        "django__django-15731": run_instance_modal_django_django_15731,
        "django__django-15732": run_instance_modal_django_django_15732,
        "django__django-15741": run_instance_modal_django_django_15741,
        "django__django-15814": run_instance_modal_django_django_15814,
        "django__django-15851": run_instance_modal_django_django_15851,
        "django__django-15863": run_instance_modal_django_django_15863,
        "django__django-15916": run_instance_modal_django_django_15916,
        "django__django-15930": run_instance_modal_django_django_15930,
        "django__django-15957": run_instance_modal_django_django_15957,
        "django__django-15973": run_instance_modal_django_django_15973,
        "django__django-15987": run_instance_modal_django_django_15987,
        "django__django-16032": run_instance_modal_django_django_16032,
        "django__django-16082": run_instance_modal_django_django_16082,
        "django__django-16100": run_instance_modal_django_django_16100,
        "django__django-16116": run_instance_modal_django_django_16116,
        "django__django-16139": run_instance_modal_django_django_16139,
        "django__django-16145": run_instance_modal_django_django_16145,
        "django__django-16255": run_instance_modal_django_django_16255,
        "django__django-16256": run_instance_modal_django_django_16256,
        "django__django-16263": run_instance_modal_django_django_16263,
        "django__django-16315": run_instance_modal_django_django_16315,
        "django__django-16333": run_instance_modal_django_django_16333,
        "django__django-16429": run_instance_modal_django_django_16429,
        "django__django-16454": run_instance_modal_django_django_16454,
        "django__django-16485": run_instance_modal_django_django_16485,
        "django__django-16493": run_instance_modal_django_django_16493,
        "django__django-16502": run_instance_modal_django_django_16502,
        "django__django-16527": run_instance_modal_django_django_16527,
        "django__django-16560": run_instance_modal_django_django_16560,
        "django__django-16569": run_instance_modal_django_django_16569,
        "django__django-16595": run_instance_modal_django_django_16595,
        "django__django-16612": run_instance_modal_django_django_16612,
        "django__django-16631": run_instance_modal_django_django_16631,
        "django__django-16642": run_instance_modal_django_django_16642,
        "django__django-16661": run_instance_modal_django_django_16661,
        "django__django-16662": run_instance_modal_django_django_16662,
        "django__django-16667": run_instance_modal_django_django_16667,
        "django__django-16801": run_instance_modal_django_django_16801,
        "django__django-16819": run_instance_modal_django_django_16819,
        "django__django-16899": run_instance_modal_django_django_16899,
        "django__django-16901": run_instance_modal_django_django_16901,
        "django__django-16938": run_instance_modal_django_django_16938,
        "django__django-17029": run_instance_modal_django_django_17029,
        "django__django-17084": run_instance_modal_django_django_17084,
        "django__django-17087": run_instance_modal_django_django_17087,
        "django__django-9296": run_instance_modal_django_django_9296,
        # "matplotlib__matplotlib-22719": run_instance_modal_matplotlib_matplotlib_22719,
        # "matplotlib__matplotlib-22865": run_instance_modal_matplotlib_matplotlib_22865,
        # "matplotlib__matplotlib-22871": run_instance_modal_matplotlib_matplotlib_22871,
        # "matplotlib__matplotlib-23299": run_instance_modal_matplotlib_matplotlib_23299,
        # "matplotlib__matplotlib-23412": run_instance_modal_matplotlib_matplotlib_23412,
        # "matplotlib__matplotlib-25287": run_instance_modal_matplotlib_matplotlib_25287,
        # "matplotlib__matplotlib-25311": run_instance_modal_matplotlib_matplotlib_25311,
        # "matplotlib__matplotlib-25332": run_instance_modal_matplotlib_matplotlib_25332,
        # "matplotlib__matplotlib-25479": run_instance_modal_matplotlib_matplotlib_25479,
        # "matplotlib__matplotlib-25775": run_instance_modal_matplotlib_matplotlib_25775,
        # "matplotlib__matplotlib-25960": run_instance_modal_matplotlib_matplotlib_25960,
        # "matplotlib__matplotlib-26113": run_instance_modal_matplotlib_matplotlib_26113,
        # "matplotlib__matplotlib-26208": run_instance_modal_matplotlib_matplotlib_26208,
        # "matplotlib__matplotlib-26291": run_instance_modal_matplotlib_matplotlib_26291,
        # "matplotlib__matplotlib-26342": run_instance_modal_matplotlib_matplotlib_26342,
        # "matplotlib__matplotlib-26466": run_instance_modal_matplotlib_matplotlib_26466,
        # "mwaskom__seaborn-3069": run_instance_modal_mwaskom_seaborn_3069,
        # "mwaskom__seaborn-3187": run_instance_modal_mwaskom_seaborn_3187,
        # "pallets__flask-5014": run_instance_modal_pallets_flask_5014,
        # "psf__requests-1142": run_instance_modal_psf_requests_1142,
        # "psf__requests-1724": run_instance_modal_psf_requests_1724,
        # "psf__requests-1766": run_instance_modal_psf_requests_1766,
        # "psf__requests-1921": run_instance_modal_psf_requests_1921,
        # "psf__requests-2317": run_instance_modal_psf_requests_2317,
        # "psf__requests-2931": run_instance_modal_psf_requests_2931,
        # "psf__requests-5414": run_instance_modal_psf_requests_5414,
        # "psf__requests-6028": run_instance_modal_psf_requests_6028,
        # "pydata__xarray-2905": run_instance_modal_pydata_xarray_2905,
        # "pydata__xarray-3095": run_instance_modal_pydata_xarray_3095,
        # "pydata__xarray-3151": run_instance_modal_pydata_xarray_3151,
        # "pydata__xarray-3305": run_instance_modal_pydata_xarray_3305,
        # "pydata__xarray-3677": run_instance_modal_pydata_xarray_3677,
        # "pydata__xarray-3993": run_instance_modal_pydata_xarray_3993,
        # "pydata__xarray-4075": run_instance_modal_pydata_xarray_4075,
        # "pydata__xarray-4094": run_instance_modal_pydata_xarray_4094,
        # "pydata__xarray-4356": run_instance_modal_pydata_xarray_4356,
        # "pydata__xarray-4629": run_instance_modal_pydata_xarray_4629,
        # "pydata__xarray-4687": run_instance_modal_pydata_xarray_4687,
        # "pydata__xarray-4695": run_instance_modal_pydata_xarray_4695,
        # "pydata__xarray-4966": run_instance_modal_pydata_xarray_4966,
        # "pylint-dev__pylint-6386": run_instance_modal_pylint_dev_pylint_6386,
        # "pylint-dev__pylint-6528": run_instance_modal_pylint_dev_pylint_6528,
        # "pylint-dev__pylint-6903": run_instance_modal_pylint_dev_pylint_6903,
        # "pylint-dev__pylint-7080": run_instance_modal_pylint_dev_pylint_7080,
        # "pylint-dev__pylint-7277": run_instance_modal_pylint_dev_pylint_7277,
        # "pytest-dev__pytest-5262": run_instance_modal_pytest_dev_pytest_5262,
        # "pytest-dev__pytest-5631": run_instance_modal_pytest_dev_pytest_5631,
        # "pytest-dev__pytest-5787": run_instance_modal_pytest_dev_pytest_5787,
        # "pytest-dev__pytest-5809": run_instance_modal_pytest_dev_pytest_5809,
        # "pytest-dev__pytest-5840": run_instance_modal_pytest_dev_pytest_5840,
        # "pytest-dev__pytest-6197": run_instance_modal_pytest_dev_pytest_6197,
        # "pytest-dev__pytest-6202": run_instance_modal_pytest_dev_pytest_6202,
        # "pytest-dev__pytest-7205": run_instance_modal_pytest_dev_pytest_7205,
        # "pytest-dev__pytest-7236": run_instance_modal_pytest_dev_pytest_7236,
        # "pytest-dev__pytest-7324": run_instance_modal_pytest_dev_pytest_7324,
        # "pytest-dev__pytest-7432": run_instance_modal_pytest_dev_pytest_7432,
        # "pytest-dev__pytest-7490": run_instance_modal_pytest_dev_pytest_7490,
        # "pytest-dev__pytest-7521": run_instance_modal_pytest_dev_pytest_7521,
        # "pytest-dev__pytest-7571": run_instance_modal_pytest_dev_pytest_7571,
        # "pytest-dev__pytest-7982": run_instance_modal_pytest_dev_pytest_7982,
        # "pytest-dev__pytest-8399": run_instance_modal_pytest_dev_pytest_8399,
        # "scikit-learn__scikit-learn-10297": run_instance_modal_scikit_learn_scikit_learn_10297,
        # "scikit-learn__scikit-learn-10844": run_instance_modal_scikit_learn_scikit_learn_10844,
        # "scikit-learn__scikit-learn-10908": run_instance_modal_scikit_learn_scikit_learn_10908,
        # "scikit-learn__scikit-learn-11310": run_instance_modal_scikit_learn_scikit_learn_11310,
        # "scikit-learn__scikit-learn-11578": run_instance_modal_scikit_learn_scikit_learn_11578,
        # "scikit-learn__scikit-learn-12585": run_instance_modal_scikit_learn_scikit_learn_12585,
        # "scikit-learn__scikit-learn-12682": run_instance_modal_scikit_learn_scikit_learn_12682,
        # "scikit-learn__scikit-learn-12973": run_instance_modal_scikit_learn_scikit_learn_12973,
        # "scikit-learn__scikit-learn-13124": run_instance_modal_scikit_learn_scikit_learn_13124,
        # "scikit-learn__scikit-learn-13135": run_instance_modal_scikit_learn_scikit_learn_13135,
        # "scikit-learn__scikit-learn-13142": run_instance_modal_scikit_learn_scikit_learn_13142,
        # "scikit-learn__scikit-learn-13439": run_instance_modal_scikit_learn_scikit_learn_13439,
        # "scikit-learn__scikit-learn-13496": run_instance_modal_scikit_learn_scikit_learn_13496,
        # "scikit-learn__scikit-learn-13779": run_instance_modal_scikit_learn_scikit_learn_13779,
        # "scikit-learn__scikit-learn-14053": run_instance_modal_scikit_learn_scikit_learn_14053,
        # "scikit-learn__scikit-learn-14087": run_instance_modal_scikit_learn_scikit_learn_14087,
        # "scikit-learn__scikit-learn-14141": run_instance_modal_scikit_learn_scikit_learn_14141,
        # "scikit-learn__scikit-learn-14496": run_instance_modal_scikit_learn_scikit_learn_14496,
        # "scikit-learn__scikit-learn-14629": run_instance_modal_scikit_learn_scikit_learn_14629,
        # "scikit-learn__scikit-learn-14710": run_instance_modal_scikit_learn_scikit_learn_14710,
        # "scikit-learn__scikit-learn-14894": run_instance_modal_scikit_learn_scikit_learn_14894,
        # "scikit-learn__scikit-learn-14983": run_instance_modal_scikit_learn_scikit_learn_14983,
        # "scikit-learn__scikit-learn-15100": run_instance_modal_scikit_learn_scikit_learn_15100,
        # "scikit-learn__scikit-learn-25102": run_instance_modal_scikit_learn_scikit_learn_25102,
        # "scikit-learn__scikit-learn-25232": run_instance_modal_scikit_learn_scikit_learn_25232,
        # "scikit-learn__scikit-learn-25747": run_instance_modal_scikit_learn_scikit_learn_25747,
        # "scikit-learn__scikit-learn-25931": run_instance_modal_scikit_learn_scikit_learn_25931,
        # "scikit-learn__scikit-learn-25973": run_instance_modal_scikit_learn_scikit_learn_25973,
        # "scikit-learn__scikit-learn-26194": run_instance_modal_scikit_learn_scikit_learn_26194,
        # "scikit-learn__scikit-learn-26323": run_instance_modal_scikit_learn_scikit_learn_26323,
        # "scikit-learn__scikit-learn-9288": run_instance_modal_scikit_learn_scikit_learn_9288,
        # "sphinx-doc__sphinx-10323": run_instance_modal_sphinx_doc_sphinx_10323,
        # "sphinx-doc__sphinx-10435": run_instance_modal_sphinx_doc_sphinx_10435,
        # "sphinx-doc__sphinx-10449": run_instance_modal_sphinx_doc_sphinx_10449,
        # "sphinx-doc__sphinx-10466": run_instance_modal_sphinx_doc_sphinx_10466,
        # "sphinx-doc__sphinx-10614": run_instance_modal_sphinx_doc_sphinx_10614,
        # "sphinx-doc__sphinx-10673": run_instance_modal_sphinx_doc_sphinx_10673,
        # "sphinx-doc__sphinx-11445": run_instance_modal_sphinx_doc_sphinx_11445,
        # "sphinx-doc__sphinx-11510": run_instance_modal_sphinx_doc_sphinx_11510,
        # "sphinx-doc__sphinx-7440": run_instance_modal_sphinx_doc_sphinx_7440,
        # "sphinx-doc__sphinx-7454": run_instance_modal_sphinx_doc_sphinx_7454,
        # "sphinx-doc__sphinx-7462": run_instance_modal_sphinx_doc_sphinx_7462,
        # "sphinx-doc__sphinx-7590": run_instance_modal_sphinx_doc_sphinx_7590,
        # "sphinx-doc__sphinx-7748": run_instance_modal_sphinx_doc_sphinx_7748,
        # "sphinx-doc__sphinx-7757": run_instance_modal_sphinx_doc_sphinx_7757,
        # "sphinx-doc__sphinx-7889": run_instance_modal_sphinx_doc_sphinx_7889,
        # "sphinx-doc__sphinx-7910": run_instance_modal_sphinx_doc_sphinx_7910,
        # "sphinx-doc__sphinx-7985": run_instance_modal_sphinx_doc_sphinx_7985,
        # "sphinx-doc__sphinx-8035": run_instance_modal_sphinx_doc_sphinx_8035,
        # "sphinx-doc__sphinx-8056": run_instance_modal_sphinx_doc_sphinx_8056,
        # "sphinx-doc__sphinx-8120": run_instance_modal_sphinx_doc_sphinx_8120,
        # "sphinx-doc__sphinx-8265": run_instance_modal_sphinx_doc_sphinx_8265,
        # "sphinx-doc__sphinx-8269": run_instance_modal_sphinx_doc_sphinx_8269,
        # "sphinx-doc__sphinx-8459": run_instance_modal_sphinx_doc_sphinx_8459,
        # "sphinx-doc__sphinx-8475": run_instance_modal_sphinx_doc_sphinx_8475,
        # "sphinx-doc__sphinx-8548": run_instance_modal_sphinx_doc_sphinx_8548,
        # "sphinx-doc__sphinx-8551": run_instance_modal_sphinx_doc_sphinx_8551,
        # "sphinx-doc__sphinx-8593": run_instance_modal_sphinx_doc_sphinx_8593,
        # "sphinx-doc__sphinx-8595": run_instance_modal_sphinx_doc_sphinx_8595,
        # "sphinx-doc__sphinx-8621": run_instance_modal_sphinx_doc_sphinx_8621,
        # "sphinx-doc__sphinx-8638": run_instance_modal_sphinx_doc_sphinx_8638,
        # "sphinx-doc__sphinx-8721": run_instance_modal_sphinx_doc_sphinx_8721,
        # "sphinx-doc__sphinx-9229": run_instance_modal_sphinx_doc_sphinx_9229,
        # "sphinx-doc__sphinx-9230": run_instance_modal_sphinx_doc_sphinx_9230,
        # "sphinx-doc__sphinx-9281": run_instance_modal_sphinx_doc_sphinx_9281,
        # "sphinx-doc__sphinx-9320": run_instance_modal_sphinx_doc_sphinx_9320,
        # "sphinx-doc__sphinx-9367": run_instance_modal_sphinx_doc_sphinx_9367,
        # "sphinx-doc__sphinx-9461": run_instance_modal_sphinx_doc_sphinx_9461,
        # "sphinx-doc__sphinx-9591": run_instance_modal_sphinx_doc_sphinx_9591,
        # "sphinx-doc__sphinx-9602": run_instance_modal_sphinx_doc_sphinx_9602,
        # "sphinx-doc__sphinx-9658": run_instance_modal_sphinx_doc_sphinx_9658,
        # "sphinx-doc__sphinx-9673": run_instance_modal_sphinx_doc_sphinx_9673,
        # "sphinx-doc__sphinx-9698": run_instance_modal_sphinx_doc_sphinx_9698,
        # "sphinx-doc__sphinx-9711": run_instance_modal_sphinx_doc_sphinx_9711,
        # "sympy__sympy-11618": run_instance_modal_sympy_sympy_11618,
        # "sympy__sympy-12096": run_instance_modal_sympy_sympy_12096,
        # "sympy__sympy-12419": run_instance_modal_sympy_sympy_12419,
        # "sympy__sympy-12481": run_instance_modal_sympy_sympy_12481,
        # "sympy__sympy-12489": run_instance_modal_sympy_sympy_12489,
        # "sympy__sympy-13031": run_instance_modal_sympy_sympy_13031,
        # "sympy__sympy-13091": run_instance_modal_sympy_sympy_13091,
        # "sympy__sympy-13372": run_instance_modal_sympy_sympy_13372,
        # "sympy__sympy-13480": run_instance_modal_sympy_sympy_13480,
        # "sympy__sympy-13551": run_instance_modal_sympy_sympy_13551,
        # "sympy__sympy-13615": run_instance_modal_sympy_sympy_13615,
        # "sympy__sympy-13647": run_instance_modal_sympy_sympy_13647,
        # "sympy__sympy-13757": run_instance_modal_sympy_sympy_13757,
        # "sympy__sympy-13798": run_instance_modal_sympy_sympy_13798,
        # "sympy__sympy-13852": run_instance_modal_sympy_sympy_13852,
        # "sympy__sympy-13877": run_instance_modal_sympy_sympy_13877,
        # "sympy__sympy-13878": run_instance_modal_sympy_sympy_13878,
        # "sympy__sympy-13974": run_instance_modal_sympy_sympy_13974,
        # "sympy__sympy-14248": run_instance_modal_sympy_sympy_14248,
        # "sympy__sympy-14531": run_instance_modal_sympy_sympy_14531,
        # "sympy__sympy-14711": run_instance_modal_sympy_sympy_14711,
        # "sympy__sympy-14976": run_instance_modal_sympy_sympy_14976,
        # "sympy__sympy-15017": run_instance_modal_sympy_sympy_15017,
        # "sympy__sympy-15345": run_instance_modal_sympy_sympy_15345,
        # "sympy__sympy-15349": run_instance_modal_sympy_sympy_15349,
        # "sympy__sympy-15599": run_instance_modal_sympy_sympy_15599,
        # "sympy__sympy-15809": run_instance_modal_sympy_sympy_15809,
        # "sympy__sympy-15875": run_instance_modal_sympy_sympy_15875,
        # "sympy__sympy-15976": run_instance_modal_sympy_sympy_15976,
        # "sympy__sympy-16450": run_instance_modal_sympy_sympy_16450,
        # "sympy__sympy-16597": run_instance_modal_sympy_sympy_16597,
        # "sympy__sympy-16766": run_instance_modal_sympy_sympy_16766,
        # "sympy__sympy-16792": run_instance_modal_sympy_sympy_16792,
        # "sympy__sympy-16886": run_instance_modal_sympy_sympy_16886,
        # "sympy__sympy-17139": run_instance_modal_sympy_sympy_17139,
        # "sympy__sympy-17318": run_instance_modal_sympy_sympy_17318,
        # "sympy__sympy-17630": run_instance_modal_sympy_sympy_17630,
        # "sympy__sympy-17655": run_instance_modal_sympy_sympy_17655,
        # "sympy__sympy-18189": run_instance_modal_sympy_sympy_18189,
        # "sympy__sympy-18199": run_instance_modal_sympy_sympy_18199,
        # "sympy__sympy-18211": run_instance_modal_sympy_sympy_18211,
        # "sympy__sympy-18698": run_instance_modal_sympy_sympy_18698,
        # "sympy__sympy-18763": run_instance_modal_sympy_sympy_18763,
        # "sympy__sympy-19040": run_instance_modal_sympy_sympy_19040,
        # "sympy__sympy-19346": run_instance_modal_sympy_sympy_19346,
        # "sympy__sympy-19495": run_instance_modal_sympy_sympy_19495,
        # "sympy__sympy-19637": run_instance_modal_sympy_sympy_19637,
        # "sympy__sympy-19783": run_instance_modal_sympy_sympy_19783,
        # "sympy__sympy-19954": run_instance_modal_sympy_sympy_19954,
        # "sympy__sympy-20154": run_instance_modal_sympy_sympy_20154,
        # "sympy__sympy-20428": run_instance_modal_sympy_sympy_20428,
        # "sympy__sympy-20438": run_instance_modal_sympy_sympy_20438,
        # "sympy__sympy-20590": run_instance_modal_sympy_sympy_20590,
        # "sympy__sympy-20801": run_instance_modal_sympy_sympy_20801,
        # "sympy__sympy-20916": run_instance_modal_sympy_sympy_20916,
        # "sympy__sympy-21379": run_instance_modal_sympy_sympy_21379,
        # "sympy__sympy-21596": run_instance_modal_sympy_sympy_21596,
        # "sympy__sympy-21612": run_instance_modal_sympy_sympy_21612,
        # "sympy__sympy-21847": run_instance_modal_sympy_sympy_21847,
        # "sympy__sympy-21930": run_instance_modal_sympy_sympy_21930,
        # "sympy__sympy-22080": run_instance_modal_sympy_sympy_22080,
        # "sympy__sympy-22456": run_instance_modal_sympy_sympy_22456,
        # "sympy__sympy-22714": run_instance_modal_sympy_sympy_22714,
        # "sympy__sympy-22914": run_instance_modal_sympy_sympy_22914,
        # "sympy__sympy-23262": run_instance_modal_sympy_sympy_23262,
        # "sympy__sympy-23413": run_instance_modal_sympy_sympy_23413,
        # "sympy__sympy-23534": run_instance_modal_sympy_sympy_23534,
        # "sympy__sympy-23824": run_instance_modal_sympy_sympy_23824,
        # "sympy__sympy-23950": run_instance_modal_sympy_sympy_23950,
        # "sympy__sympy-24066": run_instance_modal_sympy_sympy_24066,
        # "sympy__sympy-24213": run_instance_modal_sympy_sympy_24213,
        # "sympy__sympy-24443": run_instance_modal_sympy_sympy_24443,
        # "sympy__sympy-24539": run_instance_modal_sympy_sympy_24539,
        # "sympy__sympy-24562": run_instance_modal_sympy_sympy_24562,
        # "sympy__sympy-24661": run_instance_modal_sympy_sympy_24661,
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
