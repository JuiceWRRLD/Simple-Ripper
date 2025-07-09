# utils/pixeldrain.py
import requests

def upload(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://pixeldrain.com/api/file",
            files={"file": f}
        )
    if response.status_code == 200:
        data = response.json()
        return f"https://pixeldrain.com/u/{data['id']}"
    else:
        raise Exception(f"Pixeldrain error: {response.status_code} {response.text}")
