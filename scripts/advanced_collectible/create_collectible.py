#!/usr/bin/python3
from brownie import BmwMCollection, accounts, config
from scripts.helpful_scripts import get_model, fund_with_link, listen_for_event
import time


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    bmw_m_collection = BmwMCollection[len(BmwMCollection) - 1]
    fund_with_link(bmw_m_collection.address)
    transaction = bmw_m_collection.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    # time.sleep(35)
    listen_for_event(bmw_m_collection, "ReturnedCollectible", timeout=200, poll_interval=10)
    requestId = transaction.events["RequestedCollectible"]["requestId"]
    token_id = bmw_m_collection.requestIdToTokenId(requestId)
    model = get_model(bmw_m_collection.tokenIdToModel(token_id))
    print("BMW M Model of tokenId {} is {}".format(token_id, model))
