#!/usr/bin/python3
from brownie import BmwMCollection
from scripts.helpful_scripts import fund_with_link


def main():
    bmw_m_collection = BmwMCollection[len(BmwMCollection) - 1]
    fund_with_link(bmw_m_collection.address)
