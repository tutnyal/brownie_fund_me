# export PATH=~/.npm-global/bin:$PATH
from scripts.helpful_scripts import get_accounts, deploy_Mock, LOCAL_BLOCKCHAIN_NETWORKS
from brownie import FundMeContrc, config, network, MockV3Aggregator


def deploy_fund_me():
    account = get_accounts()
    print(f"using account {account}")
    print("...")

    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        print("the network is NOT dev or local...")
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_Mock()
        price_feed_address = MockV3Aggregator[-1].address

    Fund_me = FundMeContrc.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"FundMe contrc deployed to ...{Fund_me.address}")
    return Fund_me


def main():
    deploy_fund_me()
