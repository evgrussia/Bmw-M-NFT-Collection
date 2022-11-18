#!/usr/bin/python3
from brownie import BmwMCollection, accounts, network, config, interface
import json


def main():
    flatten()


def flatten():
    file = open("./BmwMCollection_flattened.json", "w")
    json.dump(BmwMCollection.get_verification_info(), file)
    file.close()
