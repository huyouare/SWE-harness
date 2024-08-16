from __future__ import annotations

import modal
import json
from pathlib import Path
import subprocess
from argparse import ArgumentParser
from typing import Optional
from tqdm import tqdm


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


def run_instance_wrapper(image, patch_content: str, eval_script: str, timeout: int):
    @app.function(
        image=image,
        cpu=1,
        memory=2048,
        timeout=60 * 10,
        serialized=True,
    )
    def run_instance_modal(patch_content: str, eval_script: str, timeout: int):
        print(f"Running instance with patch: {patch_content}")
        # Set up working directory
        work_dir = Path("/tmp/workdir")
        work_dir.mkdir(exist_ok=True)

        # Write patch file
        patch_file = work_dir / "patch.diff"
        patch_file.write_text(patch_content)

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
        try:
            result = subprocess.run(
                ["/bin/bash", str(eval_file)],
                timeout=timeout,
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
        git_diff = subprocess.run(
            ["git", "diff"], cwd="/testbed", capture_output=True, text=True
        ).stdout.strip()

        return {"status": status, "output": output, "git_diff": git_diff}

    return run_instance_modal.remote(patch_content, eval_script, timeout)


def run_instances(
    predictions: dict,
    instances: list,
    run_id: str,
    timeout: int,
):

    from swebench.harness.grading import get_eval_report
    from swebench.harness.test_spec import make_test_spec
    from swebench.harness.constants import (
        RUN_EVALUATION_LOG_DIR,
    )

    results = []
    for instance in tqdm(instances):
        test_spec = make_test_spec(instance)
        instance_id = test_spec.instance_id
        pred = predictions[instance_id]

        # Create a new image for each instance
        instance_image = create_modal_image(instance_id)

        result = run_instance_wrapper(
            instance_image, pred["model_patch"], test_spec.eval_script, timeout
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
            results.append((instance_id, report))
        else:
            print(f"Error for {instance_id}: {result['status']}")

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
        results = run_instances(
            predictions,
            dataset,
            run_id,
            timeout,
        )

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
