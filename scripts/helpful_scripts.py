from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
MAINNET_NETWORK = ["mainnet-fork-dev", "mainnet-fork"]
LOCAL_BLOCKCHAIN_NETWORKS = ["development", "local-network"]


def get_accounts():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS
        or network.show_active() in MAINNET_NETWORK
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_Mock():
    print("the network is development, deploying MockV3...")
    if len(MockV3Aggregator) <= 0:
        print("MockV3Aggregator was NOT deployed, so DEPLOYING...")
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_accounts()}
        )
        # print(f"MockV3 deployed to this address...{aggregator.address}")
        print("MockV3 deployed")
