import os
from pathlib import Path
import requests

IPFS_LOCAL_URL = "http://127.0.0.1:5001"
endpoint = "/api/v0/add"

# curl -X POST -F file=@img/pug.png http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath, filename):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            IPFS_LOCAL_URL + endpoint, files={"file": image_binary}
        )
        ipfs_hash = response.json()["Hash"]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


# def main():
#     # Change this filepath
#     filepath = "./img/pug.png"
#     filename = filepath.split("/")[-1:][0]

#     upload_to_ipfs(filepath, filename)
