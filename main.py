import modal
from modal import Image, Mount
import json
import random

app = modal.App("distributed-swebench")

# Create a custom image with swebench and other dependencies
custom_image = (
    Image.debian_slim(python_version="3.10")
        .poetry_install_from_file(
            poetry_pyproject_toml="pyproject.toml",
            poetry_lockfile="poetry.lock",
        )
)

# Mount the current directory
mount = Mount.from_local_dir(".", remote_path="/root/app")

def mock_swebench_main(predictions_path, run_id, workers, shard):
    # Mock implementation of swebench_main
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

@app.function(image=custom_image, mounts=[mount], cpu=2, memory=4096)
def run_shard(shard, predictions_path, run_id, workers=4):
    results = mock_swebench_main(predictions_path, run_id, workers, shard)
    return results


@app.function(image=custom_image, mounts=[mount])
def main(predictions_path: str, run_id: str, num_shards: int = 10, workers_per_shard: int = 4):
    shards = create_shards(predictions_path, num_shards)
    
    # Use Function.map() for parallel execution
    results = list(run_shard.map(shards, [predictions_path]*num_shards, [run_id]*num_shards, [workers_per_shard]*num_shards))
    
    combined_results = combine_results(results)
    
    with open(f"{run_id}_combined_results.json", "w") as f:
        json.dump(combined_results, f)

def create_shards(predictions_path, num_shards):
    print(f"Creating {num_shards} shards from {predictions_path}")
    # Dummy implementation: create random data for each shard
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
    # Dummy implementation: merge all results into a single dictionary
    combined = {}
    for i, result in enumerate(results):
        combined[f"shard_{i}"] = result
    return combined

if __name__ == "__main__":
    modal.runner.deploy_app(app)