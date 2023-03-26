from brownie import FundMe, MockV3Aggregator, accounts, config, network
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
from scripts.utilities import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
gas_price(gas_strategy)


def deploy_fund_me():
    account = get_account()
    # pass price feed address to our fundme contract

    # If working in dev or prd chain use sepolia for eth else deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[
            -1
        ].address  # address of latest MockV3Aggregator deployed
        print(f"Mocks Deployed...")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account, "gas_price": gas_strategy},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # .get() is better
    )

    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
