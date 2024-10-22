from __future__ import annotations

import modal
import json
import time
from pathlib import Path
from argparse import ArgumentParser
from typing import Optional, TypedDict, List, Optional
from tqdm import tqdm
from pydantic import BaseModel
import os

from modal_functions.swebench_verified import app as helper_app, dispatcher

image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install("git")
    .pip_install("tqdm")
    .pip_install("modal")
    .pip_install("jsonlines")
    .pip_install("redis")
    .pip_install("python-ulid")
    .run_commands("pip install git+https://github.com/princeton-nlp/SWE-bench.git")
)

app = modal.App("swebench-evaluation-verified", image=image)
app.include(helper_app)


class SWEbenchInstance(TypedDict):
    repo: str
    instance_id: str
    base_commit: str
    patch: str
    test_patch: str
    problem_statement: str
    hints_text: str
    created_at: str
    version: str
    FAIL_TO_PASS: str
    PASS_TO_PASS: str
    environment_setup_commit: str


class TestResult(TypedDict):
    test_name: str
    passed: bool
    output: str


class ModelPrediction(TypedDict):
    model_name_or_path: str
    model_patch: str


class InstanceRecord(TypedDict):
    test_input_instance: SWEbenchInstance  # Original SWEbenchInstance fields
    model_prediction: ModelPrediction
    report: Optional[dict]


async def process_instance(instance: SWEbenchInstance, predictions: dict, run_id: str):
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

    # Decode the output if it's in bytes
    output_str = (
        result["output"].decode("utf-8")
        if isinstance(result["output"], bytes)
        else result["output"]
    )

    with open(log_dir / "test_output.txt", "w") as f:
        f.write(output_str)

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


def create_redis_client():
    from redis import Redis

    return Redis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"],
        password=os.environ["REDIS_PASSWORD"],
        ssl=True,
    )


async def run_instances(predictions, instances, run_id, job_id):
    import asyncio
    from swebench.harness.utils import load_swebench_dataset

    start_time = time.time()
    tasks = [process_instance(instance, predictions, run_id) for instance in instances]
    results = []
    instance_records = []
    redis = create_redis_client()
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        try:
            result = await task
            print(f"Result: {result}")
            if result:
                instance_id, report = result
                results.append(result)
                instance_record = {
                    "instance_id": instance_id,
                    "test_input_instance": next(
                        i for i in instances if i["instance_id"] == instance_id
                    ),
                    "model_prediction": predictions[instance_id],
                    "report": report,
                }
                instance_records.append(instance_record)

                # Store individual instance record in Redis
                redis.set(
                    f"job:{job_id}:instance:{instance_id}", json.dumps(instance_record)
                )

                # Update job progress
                full_dataset = load_swebench_dataset(
                    "princeton-nlp/SWE-bench_Verified", "test"
                )
                full_report = make_run_report(
                    predictions, full_dataset, results, run_id
                )
                progress = len(results) / len(tasks) * 100
                elapsed_time = time.time() - start_time
                redis.set(
                    f"job:{job_id}",
                    json.dumps(
                        {
                            "status": "in_progress",
                            "progress": progress,
                            "start_time": start_time,
                            "elapsed_time": elapsed_time,
                            "report": full_report,
                        }
                    ),
                )

        except asyncio.CancelledError:
            print("Task was cancelled")
        except Exception as e:
            print(f"An error occurred during task execution: {str(e)}")
            import traceback

            print(traceback.format_exc())

    # Store the list of instance IDs
    redis.set(
        f"job:{job_id}:instance_ids",
        json.dumps([r["instance_id"] for r in instance_records]),
    )

    return results


def get_dataset_from_preds(
    dataset_name: str,
    split: str,
    instance_ids: list,
    predictions: dict,
    run_id: str,
    exclude_completed: bool = False,
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
    return report


@app.local_entrypoint()
def main(
    dataset_name: str = "princeton-nlp/SWE-bench_Verified",
    split: str = "test",
    instance_ids: Optional[str] = None,
    predictions_path: str = None,
    run_id: str = None,
    job_id: str = None,
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

    start_time = time.time()

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
        results = asyncio.run(run_instances(predictions, dataset, run_id, job_id))

    print("Running final report...")

    report = make_run_report(predictions, full_dataset, results, run_id)
    # Write report to Redis
    redis = create_redis_client()
    elapsed_time = time.time() - start_time
    redis.set(
        f"job:{job_id}",
        json.dumps(
            {
                "status": "completed",
                "report": report,
                "progress": 100,
                "start_time": start_time,
                "elapsed_time": elapsed_time,
            }
        ),
    )

    return report


class Prediction(BaseModel):
    model_name_or_path: str
    instance_id: str
    model_patch: str


class EvaluationRequest(BaseModel):
    predictions: list[Prediction]
    run_id: str


@app.function(secrets=[modal.Secret.from_name("upstash")], timeout=10 * 60)
def run_evaluation(job_id: str, request: EvaluationRequest):
    # Write preds to file
    timestamp = int(time.time())
    with open(f"preds_{request.run_id}_{timestamp}.json", "w") as f:
        # Convert Prediction objects to dictionaries
        predictions_dict = [pred.dict() for pred in request.predictions]
        json.dump(predictions_dict, f)

    return main(
        dataset_name="princeton-nlp/SWE-bench_Verified",
        split="test",
        instance_ids=None,
        predictions_path=f"preds_{request.run_id}_{timestamp}.json",
        run_id=request.run_id,
        job_id=job_id,
    )


@app.function(secrets=[modal.Secret.from_name("upstash")])
@modal.web_endpoint(method="POST")
def start_evaluation(request: EvaluationRequest):
    from ulid import ULID

    job_id = str(ULID())

    redis = create_redis_client()
    # Store initial job status
    redis.set(
        f"job:{job_id}",
        json.dumps(
            {
                "status": "queued",
                "progress": 0,
                "start_time": time.time(),
                "elapsed_time": 0,
                "report": {},
            }
        ),
    )

    # Start the evaluation process asynchronously
    run_evaluation.spawn(job_id, request)

    return {"job_id": job_id}


@app.function(secrets=[modal.Secret.from_name("upstash")])
@modal.web_endpoint(method="GET", docs=True)
def get_job_status(job_id: str, instance_id: Optional[str] = None):
    redis = create_redis_client()
    status_json = redis.get(f"job:{job_id}")
    if status_json is None:
        return {"error": "Job not found"}

    status = json.loads(status_json)

    if instance_id:
        # Fetch specific instance record
        instance_record = redis.get(f"job:{job_id}:instance:{instance_id}")
        if instance_record:
            instance_data = json.loads(instance_record)
        else:
            instance_data = None
    else:
        instance_data = None

    # Get the list of all instance IDs for this job
    all_instance_ids = json.loads(redis.get(f"job:{job_id}:instance_ids") or "[]")

    return {
        "status": status["status"],
        "progress": status["progress"],
        "start_time": status["start_time"],
        "elapsed_time": status["elapsed_time"],
        "report": status["report"],
        "all_instance_ids": all_instance_ids,
        "instance_record": instance_data,
    }


async def execute_instance(instance: SWEbenchInstance, predictions: dict, run_id: str):
    from swebench.harness.grading import get_eval_report
    from swebench.harness.test_spec import make_test_spec
    from swebench.harness.constants import (
        RUN_EVALUATION_LOG_DIR,
        MAP_REPO_VERSION_TO_SPECS,
    )

    def make_exec_script_list(instance, specs, env_name, repo_directory, base_commit):
        """
        Applies the test patch and runs the tests.
        """
        import re
        from swebench.harness.test_spec import (
            DIFF_MODIFIED_FILE_REGEX,
            MAP_REPO_VERSION_TO_SPECS,
            get_test_directives,
        )

        HEREDOC_DELIMITER = "EOF_114329324912"
        # test_files = re.findall(DIFF_MODIFIED_FILE_REGEX, test_patch)
        # Reset test files to the state they should be in before the patch.
        # reset_tests_command = f"git checkout {base_commit} {' '.join(test_files)}"
        reset_tests_command = f"git checkout {base_commit}"
        # apply_test_patch_command = (
        #     f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{test_patch}\n{HEREDOC_DELIMITER}"
        # )
        test_command = " ".join(
            [
                MAP_REPO_VERSION_TO_SPECS[instance["repo"]][instance["version"]][
                    "test_cmd"
                ],
                # *get_test_directives(instance),
            ]
        )
        eval_commands = [
            f"source /opt/miniconda3/bin/activate",
            f"conda activate {env_name}",
            f"cd {repo_directory}",
        ]
        if "eval_commands" in specs:
            eval_commands += specs["eval_commands"]
        eval_commands += [
            f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
            f"cd {repo_directory}",
            # This is just informational, so we have a record
            f"git status",
            f"git show",
            f"git diff {base_commit}",
            "source /opt/miniconda3/bin/activate",
            f"conda activate {env_name}",
        ]
        if "install" in specs:
            eval_commands.append(specs["install"])
        eval_commands += [
            reset_tests_command,
            test_command,
            reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
        ]
        return eval_commands

    test_spec = make_test_spec(instance)
    instance_id = test_spec.instance_id
    pred = predictions[instance_id]

    instance_function = dispatcher(instance_id)
    if instance_function is None:
        print(f"No function found for instance ID: {instance_id}")
        return None

    exec_script = make_exec_script_list(
        instance,
        MAP_REPO_VERSION_TO_SPECS[instance["repo"]][instance["version"]],
        "testbed",
        "/testbed",
        instance["base_commit"],
    )

    def eval_script(exec_script):
        return "\n".join(["#!/bin/bash", "set -uxo pipefail"] + exec_script) + "\n"

    result = await instance_function.remote.aio(
        pred["model_patch"], eval_script(exec_script)
    )
    print(f"Result for {instance_id}: {result}")

    # Process the result
    model_name_or_path = pred.get("model_name_or_path", "None").replace("/", "__")
    log_dir = Path(
        f"{RUN_EVALUATION_LOG_DIR}/{run_id}/{model_name_or_path}/{instance_id}"
    )
    log_dir.mkdir(parents=True, exist_ok=True)

    # Decode the output if it's in bytes
    output_str = (
        result["output"].decode("utf-8")
        if isinstance(result["output"], bytes)
        else result["output"]
    )

    with open(log_dir / "test_output.txt", "w") as f:
        f.write(output_str)

    return result


class ExecuteSingleInstanceRequest(BaseModel):
    model_name_or_path: str
    instance_id: str
    model_patch: str


@app.function(timeout=10 * 60)
@modal.web_endpoint(method="POST")
async def execute_single_instance(request: ExecuteSingleInstanceRequest):
    """
    Endpoint to process an instance.
    """
    prediction = {
        request.instance_id: {
            "model_name_or_path": request.model_name_or_path,
            "model_patch": request.model_patch,
            "instance_id": request.instance_id,
        }
    }

    instance = get_dataset_from_preds(
        "princeton-nlp/SWE-bench_Verified",
        "test",
        [request.instance_id],
        prediction,
        f"execute_single_{request.instance_id}",
        exclude_completed=False,
    )[0]
    return await execute_instance(
        instance, prediction, f"execute_single_{request.instance_id}"
    )


if __name__ == "__main__":
    from swebench.harness.utils import str2bool

    parser = ArgumentParser()
    parser.add_argument(
        "--dataset_name",
        default="princeton-nlp/SWE-bench_Verified",
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
        "--timeout",
        type=int,
        default=1_800,
        help="Timeout (in seconds) for running tests for each instance",
    )
    parser.add_argument(
        "--run_id", type=str, required=True, help="Run ID - identifies the run"
    )
    args = parser.parse_args()

    app.run()
