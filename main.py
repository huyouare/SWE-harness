import modal
from modal import Image, Mount
import json
import random
from swebench.harness.run_evaluation import main as swebench_main
import os
import sys
import argparse
import inspect
import jsonlines

app = modal.App("distributed-swebench")

custom_image = (
    Image.debian_slim(python_version="3.10")
        .poetry_install_from_file(
            poetry_pyproject_toml="pyproject.toml",
            poetry_lockfile="poetry.lock",
        )
)

mount = Mount.from_local_dir(".", remote_path="/root/app")

@app.function(image=custom_image, mounts=[mount], cpu=2, memory=4096)
def run_shard(shard, predictions_path, run_id, workers=4):
    results = run_swebench(predictions_path, run_id, workers, shard)
    return results

@app.function(image=custom_image, mounts=[mount])
def main(predictions_path: str, run_id: str, num_shards: int = 10, workers_per_shard: int = 4):
    shards = create_shards(predictions_path, num_shards)
    
    results = list(run_shard.map(shards, [predictions_path]*num_shards, [run_id]*num_shards, [workers_per_shard]*num_shards))
    
    combined_results = combine_results(results)
    
    print(f"Processing completed for run_id: {run_id}")
    return combined_results

def run_swebench(predictions_path, run_id, workers, shard):
    print(f"Processing shard {shard['shard_id']} with {workers} workers")

    shard_predictions_path = f"/tmp/shard_{shard['shard_id']}.jsonl"
    
    os.makedirs(os.path.dirname(shard_predictions_path), exist_ok=True)
    with jsonlines.open(shard_predictions_path, mode='w') as writer:
        writer.write_all(shard['data'])
    
    try:
        swebench_results = swebench_main(
            dataset_name="princeton-nlp/SWE-bench_Lite",
            split="test",
            instance_ids=None,
            predictions_path=shard_predictions_path,
            max_workers=workers,
            open_file_limit=4096,
            timeout=1800,
            force_rebuild=False,
            cache_level="env",
            clean=False,
            run_id=f"{run_id}_shard_{shard['shard_id']}"
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        swebench_results = None
    
    return {
        "shard_id": shard["shard_id"],
        "swebench_results": swebench_results,
        "metadata": {
            "predictions_path": predictions_path,
            "run_id": run_id,
            "workers": workers
        }
    }

def create_shards(predictions_path, num_shards):
    print(f"Creating {num_shards} shards from {predictions_path}")
    with jsonlines.open(predictions_path) as reader:
        data = list(reader)

    print(f"Data length: {len(data)}")
    print("data:")
    print(data)
    
    shard_size = len(data) // num_shards
    shards = []
    for i in range(num_shards):
        start = i * shard_size
        end = start + shard_size if i < num_shards - 1 else len(data)
        shard = {
            "shard_id": i,
            "data": data[start:end]
        }
        shards.append(shard)
    return shards

def combine_results(results):
    print(f"Combining {len(results)} results")
    combined = {}
    for i, result in enumerate(results):
        combined[f"shard_{i}"] = result
    return combined

@app.local_entrypoint()
def run_and_save():
    predictions_path = "/root/app/20240623_moatless_claude-3.5-sonnet_all_preds.jsonl"
    run_id = "test_run"
    num_shards = 10
    workers_per_shard = 4
    
    results = main.remote(predictions_path, run_id, num_shards, workers_per_shard)
    
    output_file = f"{run_id}_combined_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Combined results written to {output_file}")

if __name__ == "__main__":
    # This block will only run when the script is executed directly (not imported)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "local_debug":
        from debug_local import main as debug_main
        debug_main()
    else:
        modal.runner.deploy_app(app)