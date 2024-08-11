# SWE-harness

## Setup

We are using Python 3.10

### Installation on EC2 (Ubuntu)

Use instance `t3a.2xlarge`. Make sure it's x86 and not arm/amd.

Install Docker:

```bash
sudo apt install docker.io
```

Install pyenv and Python 3.10: https://ericsysmin.com/2024/01/11/how-to-install-pyenv-on-ubuntu-22-04/

Then install and run Poetry:

```bash
sudo apt install python3-poetry
poetry install --no-root
poetry shell
```

### Installation on personal machine (Mac)

Install poetry and then run:

```bash
poetry install --no-root
poetry shell
```

## Running (outdated)

```bash
# Deploy the script to Modal and run the remote job
modal deploy main.py && modal run main.py::run_and_save
```

## Build and Push Images

### For EC2 (Ubuntu)

```bash
python prepare_images.py \
    --push_to_registry True \
    --only_x86_64 True \
    --use_buildx False \
    --dockerhub_username huyouare \
    --dockerhub_repo swebench-lite \
    --max_workers 8
```

### For Mac

```bash
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```

```bash
python prepare_images.py \
    --push_to_registry True \
    --only_x86_64 True \
    --use_buildx True \
    --dockerhub_username huyouare \
    --dockerhub_repo swebench-lite \
    --max_workers 4
```

## Notes

- You cannot build x86 from arm (e.g. M-series Macbooks) out of the box.
- This requires docker buildx, which is not set up by default.

If running on arm:

```bash
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```
