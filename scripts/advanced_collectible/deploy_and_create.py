from scripts.helpful_scripts import (
    get_account,
    get_contract,
    config,
    network,
    OPENSEA_URL,
    fund_with_link,
)
from brownie import AdvancedCollectible


sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():

    account = get_account()
    if len(AdvancedCollectible) <= 0:
        AdvancedCollectible.deploy(
            get_contract("vrf_coordinator").address,
            get_contract("link_token").address,
            config["networks"][network.show_active()]["keyhash"],
            config["networks"][network.show_active()]["fee"],
            {"from": account},
        )
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
