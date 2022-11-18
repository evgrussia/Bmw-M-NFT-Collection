#!/usr/bin/python3
from brownie import BmwMCollection, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_model, OPENSEA_FORMAT


bmw_metadata_dic = {
    "IX": "https://gateway.pinata.cloud/ipfs/QmVL4eJNh7gajfznwYKENtBFRrgeQjE42j3wzqZHdjyev8",
    "I4": "https://gateway.pinata.cloud/ipfs/",
    "Z4": "https://gateway.pinata.cloud/ipfs/",
    "XM": "https://gateway.pinata.cloud/ipfs/",
    "X7M": "https://gateway.pinata.cloud/ipfs/",
    "X6M": "https://gateway.pinata.cloud/ipfs/",
    "X5M": "https://gateway.pinata.cloud/ipfs/",
    "M850": "https://gateway.pinata.cloud/ipfs/QmbANpxqQMLABpErZvyWDtCQYTWtVZteJVehY2LMnd1E52",
    "M760": "https://gateway.pinata.cloud/ipfs/",
    "M235": "https://gateway.pinata.cloud/ipfs/",
    "M8_COUPE": "https://gateway.pinata.cloud/ipfs/",
    "M8_CABRIO": "https://gateway.pinata.cloud/ipfs/",
    "M5": "https://gateway.pinata.cloud/ipfs/",
    "M4_CSL": "https://gateway.pinata.cloud/ipfs/",
    "M4_CABRIO": "https://gateway.pinata.cloud/ipfs/",
    "M3": "https://gateway.pinata.cloud/ipfs/",
    "M2": "https://gateway.pinata.cloud/ipfs/",

}

def main():
    print("Working on " + network.show_active())
    bmw_m_collection = BmwMCollection[len(BmwMCollection) - 1]
    number_of_advanced_collectibles = bmw_m_collection.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        model = get_model(bmw_m_collection.tokenIdToModel(token_id))
        if not bmw_m_collection.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, bmw_m_collection,
                         bmw_metadata_dic[model])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
