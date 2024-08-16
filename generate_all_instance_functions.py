import json


def _extract_instance_ids(jsonl_file):
    instance_ids = []
    with open(jsonl_file, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                instance_id = data.get("instance_id")
                if instance_id:
                    instance_ids.append(instance_id)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse line: {line}")
    return sorted(instance_ids)


def _generate_functions(instance_ids, output_file_path):
    with open(output_file_path, "w") as output_file:
        for instance_id in instance_ids:
            # Create a valid Python function name
            function_name = (
                f"run_instance_modal_{instance_id.replace('-', '_').replace('__', '_')}"
            )

            output_file.write(
                f'@app.function(image=create_modal_image("{instance_id}"), cpu=1, memory=2048, timeout=60 * 10, serialized=True)\n'
            )
            output_file.write(
                f"def {function_name}(patch_content: str, eval_script: str, timeout: int):\n"
            )
            output_file.write(
                "    return run_instance_modal_inner(patch_content, eval_script, timeout)\n"
            )
            output_file.write("\n")

        # Generate dispatcher function
        output_file.write(
            "def dispatcher(instance_id: str) -> Callable[[str, str, int], str]:\n"
        )
        output_file.write("    function_map = {\n")
        for instance_id in sorted(instance_ids):
            function_name = (
                f"run_instance_modal_{instance_id.replace('-', '_').replace('__', '_')}"
            )
            output_file.write(f'        "{instance_id}": {function_name},\n')
        output_file.write("    }\n")
        output_file.write("    return function_map.get(instance_id)\n")

    print(f"Functions have been written to {output_file_path}")


# Main execution
if __name__ == "__main__":
    jsonl_file_path = "20240623_moatless_claude-3.5-sonnet_all_preds.jsonl"
    output_file_path = "generated_functions.py"

    # Extract instance_ids
    instance_ids = _extract_instance_ids(jsonl_file_path)

    # Print the extracted instance_ids
    print("Extracted instance_ids:")
    for instance_id in instance_ids:
        print(instance_id)

    print(f"\nTotal instance_ids found: {len(instance_ids)}")

    # Generate functions
    _generate_functions(instance_ids, output_file_path)
