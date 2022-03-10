from scripts.helpful_scripts import get_account

from brownie import SimpleCollectible


def deploy():
    print(
        "Are u sure, you want to deploy a new contract, if yes then uncomment next lines of code."
    )
    # account = get_account()
    # simple_collectible = SimpleCollectible.deploy({"from": account})
    # print("Deployed SimpleCollectible!")
    # return simple_collectible


def main():
    deploy()
