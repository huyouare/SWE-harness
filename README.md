# SWE-harness

## Setup

We are using Python 3.10

Install poetry and then run:

```bash
poetry install
poetry shell
```

## Running

```bash
# Deploy the script to Modal and run the remote job
modal deploy main.py && modal run main.py::run_and_save
```

## Build and Push Images

```bash
python prepare_images.py \
    --push_to_registry True \
    --only_x86_64 True \
    --use_buildx True \
    --dockerhub_username huyouare \
    --dockerhub_repo swebench-lite
```

## Notes

- You cannot build x86 from arm (e.g. M-series Macbooks) out of the box.
- This requires docker buildx, which is not set up by default.

If running on arm:

```bash
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```
