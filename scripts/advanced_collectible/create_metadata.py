#!/usr/bin/python3
import os
import requests
import json
from brownie import BmwMCollection, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_model
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

model_to_image_uri = {
    "I4": "https://gateway.pinata.cloud/ipfs/QmfZeJkzHaMZmdqC4TKpqxhNoAURsbcZ1YNnMCpquWA3Ce",
    "Z4": "https://gateway.pinata.cloud/ipfs/QmZKv61hFCafiaGA867JR8oA8MTYjcp7c32bXqWU29WMwe",
    "XM": "https://gateway.pinata.cloud/ipfs/QmQoV6YwiF7BDJpZXiyJCgXU2pYLtAvLjFbAu8vErvuBV2",
    "X7M": "https://gateway.pinata.cloud/ipfs/QmRANJuFwGchbNibHV8fcb5bZL9HytvDXcj3eGKxGoQ2Je",
    "X6M": "https://gateway.pinata.cloud/ipfs/QmWGVrBnE4PaKsLf2yNnsRF8YDNk65E1Y88g8J5gCTiTVX",
    "X5M": "https://gateway.pinata.cloud/ipfs/QmeXqHS9LVMNax6UKybDXgtD7pPJYMwgBnuSp2439zpB6o",
    "M850": "https://gateway.pinata.cloud/ipfs/Qmc5EgW9peeckKZxRjxRDHAPBKPbAZFC8tQ5nZA3QK5dEq",
    "M760": "https://gateway.pinata.cloud/ipfs/QmTCM843jg9mzWvccu3PYRJdQPRaUUgP4JASjztC6ooK4W",
    "M235": "https://gateway.pinata.cloud/ipfs/Qmek3mmHyNud4QMmdjYcSj7ByKgvRyg6WVvUjNwVjXbA6P",
    "M8_COUPE": "https://gateway.pinata.cloud/ipfs/QmSPnmHvxA2sxEb7VhbRrA5PbYLVYbyELipDTwryY79pEh",
    "M8_CABRIO": "https://gateway.pinata.cloud/ipfs/QmaxFjdJQRpPAQ8MysKq1Sf3Dq4sAydmVMyLpbACwUk8Cr",
    "M5": "https://gateway.pinata.cloud/ipfs/QmUh293tLaXz9uhJm4oEAQDpgWdEVzCFqfSyrBK7P4RH6V",
    "M4_CSL": "https://gateway.pinata.cloud/ipfs/QmXVcQ64q4UMGKLcvYS7b3FmNNMQbBp2NYTc2eWRSP9Tme",
    "M4_CABRIO": "https://gateway.pinata.cloud/ipfs/QmXWyrC9ypCMEf1rgCNn5v9wbt6DVLS6Qp9rATPUWSD5Pk",
    "M3": "https://gateway.pinata.cloud/ipfs/Qmf7Dc5nJMe9BCh2RCXKDyzFtGwu6Esooo3ZjFSidKPw2c",
    "M2": "https://gateway.pinata.cloud/ipfs/QmYEWFBqGxd71LoV1ckpvVqQqeNHGPM9Drtg2dj7yd8mYh",
    "IX": "https://gateway.pinata.cloud/ipfs/QmaWqXCocnFkicjDrM5YkLb29eAMMEarwYvZ3sDtAvT9zw",
}


def main():
    print("Working on " + network.show_active())
    bmw_m_collection = BmwMCollection[-1]
    number_of_advanced_collectibles = bmw_m_collection.tokenCounter()
    print("The number of tokens you've deployed is: " + str(number_of_advanced_collectibles))
    write_metadata(number_of_advanced_collectibles, bmw_m_collection)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        model = get_model(nft_contract.tokenIdToModel(token_id))
        metadata_file_name = (f"./metadata/{network.show_active()}/" + str(token_id) + "-" + model + ".json")
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already found, delete it to overwrite!")
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_model(nft_contract.tokenIdToModel(token_id))
            collectible_metadata["description"] = f"This is BMW {collectible_metadata['name']} NFT collection car!"
            image_to_upload = None
            #if os.getenv("UPLOAD_IPFS") == "true":
            #    image_path = f"./img/{model.lower().replace('_', '-')}.png"
            #    image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (model_to_image_uri[model] if not image_to_upload else image_to_upload)
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            #if os.getenv("UPLOAD_IPFS") == "true":
            #    upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "ipfs://{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri
