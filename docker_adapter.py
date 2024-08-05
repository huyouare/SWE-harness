from modal import App, Image

docker_app = App("docker-commands")


@docker_app.function(image=Image.debian_slim().pip_install("docker"))
def docker_command(cmd: str, *args, **kwargs):
    # This function will simulate Docker operations
    if cmd == "images.list":
        return [{"RepoTags": ["mock_image:latest"]}]
    elif cmd == "containers.run":
        return {"Id": "mock_container_id"}
    # Add more mock operations as needed
    return f"Mock Docker operation: {cmd}"


class DockerAdapter:
    def __init__(self):
        self.images = ImageAdapter()
        self.containers = ContainerAdapter()


class ImageAdapter:
    def list(self, *args, **kwargs):
        return docker_command.remote("images.list", *args, **kwargs)


class ContainerAdapter:
    def run(self, *args, **kwargs):
        return docker_command.remote("containers.run", *args, **kwargs)


def get_docker_client():
    return DockerAdapter()
