from __future__ import annotations

import modal
from pathlib import Path
import subprocess
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
