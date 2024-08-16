import json
import subprocess
import time
import traceback
from pathlib import Path

import modal

from swebench.harness.constants import (
    APPLY_PATCH_FAIL,
    APPLY_PATCH_PASS,
)
from swebench.harness.docker_build import (
    close_logger,
    setup_logger,
)
from swebench.harness.grading import get_eval_report
from swebench.harness.test_spec import TestSpec


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


app = modal.App("run-instance")


@app.function(
    cpu=1,
    memory=2048,
    timeout=60 * 10,
)
def run_instance_modal(
    test_spec: TestSpec,
    pred: dict,
    run_id: str,
    timeout: int | None = None,
):
    start_time = time.time()
    instance_id = test_spec.instance_id

    try:
        # Set up logging directory
        model_name_or_path = pred.get("model_name_or_path", "None").replace("/", "__")
        log_dir = Path(f"/tmp/{run_id}/{model_name_or_path}/{instance_id}")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "run_instance.log"

        # Set up report file + logger
        report_path = log_dir / "report.json"
        if report_path.exists():
            return instance_id, json.loads(report_path.read_text())
        logger = setup_logger(instance_id, log_file)

        print(f"Running instance {instance_id}...")

        # Copy model prediction as patch file
        patch_file = log_dir / "patch.diff"
        patch_file.write_text(pred["model_patch"] or "")
        logger.info(f"Intermediate patch for {instance_id} written to {patch_file}")

        print(f"Applying patch...")
        # Attempt to apply patch
        result = subprocess.run(
            ["git", "apply", "--allow-empty", "-v", str(patch_file)],
            cwd="/testbed",
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.info("Failed to apply patch, trying again...")
            result = subprocess.run(
                ["patch", "--batch", "--fuzz=5", "-p1", "-i", str(patch_file)],
                cwd="/testbed",
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logger.info(f"{APPLY_PATCH_FAIL}:\n{result.stderr}")
                raise EvaluationError(
                    instance_id,
                    f"{APPLY_PATCH_FAIL}:\n{result.stderr}",
                    logger,
                )
            else:
                logger.info(f"{APPLY_PATCH_PASS}:\n{result.stdout}")
        else:
            logger.info(f"{APPLY_PATCH_PASS}:\n{result.stdout}")

        # Get git diff before running eval script
        git_diff_before = subprocess.run(
            ["git", "diff"], cwd="/testbed", capture_output=True, text=True
        ).stdout.strip()
        logger.info(f"Git diff before:\n{git_diff_before}")

        eval_file = log_dir / "eval.sh"
        eval_file.write_text(test_spec.eval_script)
        logger.info(f"Eval script for {instance_id} written to {eval_file}")

        print(f"Running eval script...")
        # Run eval script, write output to logs
        try:
            result = subprocess.run(
                ["/bin/bash", str(eval_file)],
                timeout=timeout,
                capture_output=True,
                text=True,
            )
            test_output = result.stdout + result.stderr
            timed_out = False
        except subprocess.TimeoutExpired as e:
            test_output = (
                e.stdout + e.stderr
                if e.stdout and e.stderr
                else "Timeout occurred, no output captured."
            )
            timed_out = True

        total_runtime = time.time() - start_time
        test_output_path = log_dir / "test_output.txt"
        logger.info(f"Test runtime: {total_runtime:_.2f} seconds")
        with open(test_output_path, "w") as f:
            f.write(test_output)
            logger.info(f"Test output for {instance_id} written to {test_output_path}")
            if timed_out:
                f.write(f"\n\nTimeout error: {timeout} seconds exceeded.")
                raise EvaluationError(
                    instance_id,
                    f"Test timed out after {timeout} seconds.",
                    logger,
                )

        # Get git diff after running eval script
        git_diff_after = subprocess.run(
            ["git", "diff"], cwd="/testbed", capture_output=True, text=True
        ).stdout.strip()

        # Check if git diff changed after running eval script
        logger.info(f"Git diff after:\n{git_diff_after}")
        if git_diff_after != git_diff_before:
            logger.info(f"Git diff changed after running eval script")

        print(f"Grading answer for {instance_id}...")
        # Get report from test output
        logger.info(f"Grading answer for {instance_id}...")
        report = get_eval_report(
            test_spec=test_spec,
            prediction=pred,
            log_path=test_output_path,
            include_tests_status=True,
        )
        logger.info(
            f"report: {report}\n"
            f"Result for {instance_id}: resolved: {report[instance_id]['resolved']}"
        )

        # Write report to report.json
        with open(report_path, "w") as f:
            f.write(json.dumps(report, indent=4))
        return instance_id, report
    except EvaluationError as e:
        error_msg = traceback.format_exc()
        logger.info(error_msg)
        print(e)
    except Exception as e:
        error_msg = (
            f"Error in evaluating model for {instance_id}: {e}\n"
            f"{traceback.format_exc()}\n"
            f"Check ({logger.log_file}) for more information."
        )
        logger.error(error_msg)
    finally:
        print(f"Instance {instance_id} ran in {time.time() - start_time:.2f} seconds")
    return
