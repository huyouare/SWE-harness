import docker
import requests

def push_to_dockerhub(client, image, prefix="exploiter007/"):
    # grab the latest tag and append prefix
    if prefix:
        new_tag = f"{prefix}{image.tags[0]}"
        image.tag(new_tag)
    else:
        new_tag = image.tags[0]
    
    
    # Push the image to Docker Hub
    print(f"Pushing image to Docker Hub: {new_tag}")
    for line in client.api.push(new_tag, stream=True, decode=True):
        print(line)


def check_image_exists(image_name):
    # Split the image name into repository and tag
    repo, tag = image_name.split(':')
    print(repo, tag)
    # Construct the DockerHub API URL
    # url = f"https://hub.docker.com/v2/repositories/{repo}/tags/{tag}"
    url = "https://hub.docker.com/r/bansaltushar92/genime"
    
    # Send a GET request to the DockerHub API
    response = requests.get(url)
    
    # Return True if the status code is 200 (OK), False otherwise
    return response.status_code == 200

if __name__ == "__main__":
    client = docker.from_env()
    local_image_name = "sweb.eval.x86_64.astropy__astropy-12907:latest"
    repository = "exploiter007/swebench:sweb.eval.x86_64.astropy__astropy-12907"
    client.images.get(local_image_name).tag(repository)

    # Push the image to the repository
    response = client.images.push(repository, stream=True, decode=True)

    # Print the push progress
    for line in response:
        if 'status' in line:
            print(line['status'])

    # images = client.images.list()
    # push_img_list = ["sweb.eval.arm64.astropy__astropy-14182:latest"]
    # for image in images:
    #     if any(tag in push_img_list for tag in image.tags):
    #         push_to_dockerhub(client, image)
    # print(check_image_exists("ishan/sweb.eval.arm64.astropy__astropy-14182:latest"))