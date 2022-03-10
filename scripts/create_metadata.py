from brownie import SimpleCollectible, network
from metadata.sample_metadata import metadata_template
from scripts.upload_to_ipfs import upload_to_ipfs
from pathlib import Path
import requests, json, os


def create_metadata(
    token_id, brand_identifier, name, description, image_path, image_filename
):
    metadata_filepath = (
        f"./metadata/{network.show_active()}/{token_id}-{brand_identifier}.json"
    )
    metadata_filename = metadata_filepath.split("/")[-1:][0]

    collectible_metadata = metadata_template
    if Path(metadata_filepath).exists():
        print(f"{metadata_filepath} already exists! Delete it to overwrite")
    else:
        print(f"Creating Metadata file: {metadata_filepath}")
        collectible_metadata["name"] = name
        collectible_metadata["description"] = description
        image_uri = upload_to_ipfs(image_path, image_filename)
        collectible_metadata["image"] = image_uri
        with open(metadata_filepath, "w") as file:
            json.dump(collectible_metadata, file)
        upload_to_ipfs(metadata_filepath, metadata_filename)


# def main():
#     # Change this filepath
#     filepath = "./img/pug.png"
#     filename = filepath.split("/")[-1:][0]

#     create_metadata(0, "puma", "superfast", "superfast shoes", filepath, filename)
