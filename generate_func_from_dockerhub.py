import json
import requests


def _extract_instance_ids_from_dockerhub():
    repository = "huyouare/swebench-lite"
    url = f"https://hub.docker.com/v2/repositories/{repository}/tags"
    instance_ids = []

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching tags: {response.status_code}")
            break

        data = response.json()
        for tag in data["results"]:
            if tag["name"].startswith("sweb.eval.x86_64."):
                instance_id = tag["name"].split("sweb.eval.x86_64.")[1]
                instance_ids.append(instance_id)

        url = data.get("next")

    return sorted(instance_ids)


def _generate_functions(instance_ids, output_file_path):
    with open(output_file_path, "w") as output_file:
        for instance_id in instance_ids:
            # Create a valid Python function name
            function_name = (
                f"run_instance_modal_{instance_id.replace('-', '_').replace('__', '_')}"
            )

            output_file.write(
                f'@app.function(image=create_modal_image("{instance_id}"), cpu=1, memory=2048, timeout=60 * 10)\n'
            )
            output_file.write(
                f"def {function_name}(patch_content: str, eval_script: str):\n"
            )
            output_file.write(
                "    return run_instance_modal_inner(patch_content, eval_script)\n"
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
    output_file_path = "generated_functions.py"

    # Extract instance_ids from Docker Hub
    instance_ids = _extract_instance_ids_from_dockerhub()

    # Print the extracted instance_ids
    print("Extracted instance_ids:")
    for instance_id in instance_ids:
        print(instance_id)

    print(f"\nTotal instance_ids found: {len(instance_ids)}")

    # Generate functions
    _generate_functions(instance_ids, output_file_path)
