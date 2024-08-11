import requests
import json

url = "https://papaya-ai--swebench-modal-app-endpoint.modal.run"


headers = {
    "Content-Type": "application/json"
}

data = {
    "patch": "My patch"
}

response = requests.post(url, json=data, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
print(f"Response Content: {response.text}")

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print("Error:", response.status_code)
    print(response.text)