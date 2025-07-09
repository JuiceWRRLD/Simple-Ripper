import httpx
from httpx import BasicAuth

API_KEY = "600de034-beea-4ae0-8986-aaab371b8bc7"

def upload(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/octet-stream")}
            auth = BasicAuth("", API_KEY)
            response = httpx.post(
                "https://pixeldrain.com/api/file",
                files=files,
                auth=auth,
                timeout=60.0
            )

        if response.status_code == 200:
            data = response.json()
            return f"https://pixeldrain.com/u/{data['id']}"
        else:
            raise Exception(f"Pixeldrain error: {response.status_code} {response.text}")

    except Exception as e:
        raise Exception(f"Pixeldrain Exception: {e}")
