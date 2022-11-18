import pytest
from brownie import network, BmwMCollection
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    listen_for_event,
)
import time


def test_can_create_advanced_collectible_integration(
    get_keyhash,
    chainlink_fee,
):
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    bmw_m_collection = BmwMCollection.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_keyhash,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        bmw_m_collection.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    bmw_m_collection.createCollectible("None", {"from": get_account()})
    # time.sleep(75)
    listen_for_event(
        bmw_m_collection, "ReturnedCollectible", timeout=200, poll_interval=10
    )
    # Assert
    assert bmw_m_collection.tokenCounter() > 0
