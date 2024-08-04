from main import run_swebench, create_shards, combine_results
import json
import os
import jsonlines

def main():
    predictions_path = os.path.expanduser("~/Downloads/20240623_moatless_claude-3.5-sonnet_all_preds.jsonl")
    run_id = "take_5_moatless"
    num_shards = 10
    workers_per_shard = 4

    # Create shards
    shards = create_shards(predictions_path, num_shards)

    # Process each shard
    results = []
    for shard in shards:
        print(f"Processing shard {shard['shard_id']}")
        print(f"Predictions path: {predictions_path}")
        print(f"Run ID: {run_id}")
        print(f"Workers per shard: {workers_per_shard}")
        print(f"Shard: {shard}")
        result = run_swebench(predictions_path, run_id, workers_per_shard, shard)
        results.append(result)

    # Combine results
    combined_results = combine_results(results)

    print("Combined Results:", json.dumps(combined_results, indent=2))

    # Optionally, save the results to a file
    output_file = f"{run_id}_local_combined_results.json"
    with open(output_file, "w") as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"Combined results written to {output_file}")

if __name__ == "__main__":
    main()