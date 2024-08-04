import modal
from modal import Image, Mount
import json
import random

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
    results = mock_swebench_main(predictions_path, run_id, workers, shard)
    return results

@app.function(image=custom_image, mounts=[mount])
def main(predictions_path: str, run_id: str, num_shards: int = 10, workers_per_shard: int = 4):
    shards = create_shards(predictions_path, num_shards)
    
    results = list(run_shard.map(shards, [predictions_path]*num_shards, [run_id]*num_shards, [workers_per_shard]*num_shards))
    
    combined_results = combine_results(results)
    
    print(f"Processing completed for run_id: {run_id}")
    return combined_results

def mock_swebench_main(predictions_path, run_id, workers, shard):
    print(f"Processing shard {shard['shard_id']} with {workers} workers")
    return {
        "shard_id": shard["shard_id"],
        "processed_data": [x * 2 for x in shard["data"]],
        "metadata": {
            "predictions_path": predictions_path,
            "run_id": run_id,
            "workers": workers
        }
    }

def create_shards(predictions_path, num_shards):
    print(f"Creating {num_shards} shards from {predictions_path}")
    shards = []
    for i in range(num_shards):
        shard = {
            "shard_id": i,
            "data": [random.randint(1, 100) for _ in range(10)]  # 10 random numbers per shard
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
    predictions_path = "~/Downloads/all_preds.jsonl"
    run_id = "test_run"
    num_shards = 10
    workers_per_shard = 4
    
    results = main.remote(predictions_path, run_id, num_shards, workers_per_shard)
    
    output_file = f"{run_id}_combined_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Combined results written to {output_file}")

if __name__ == "__main__":
    modal.runner.deploy_app(app)