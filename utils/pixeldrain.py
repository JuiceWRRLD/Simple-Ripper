import httpx

def upload(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {'file': (file_path, f, 'application/octet-stream')}
            response = httpx.post("https://pixeldrain.com/api/file", files=files, timeout=60.0)

        if response.status_code == 200:
            data = response.json()
            return f"https://pixeldrain.com/u/{data['id']}"
        else:
            raise Exception(f"Pixeldrain error: {response.status_code} {response.text}")

    except Exception as e:
        raise Exception(f"Pixeldrain Exception: {e}")
