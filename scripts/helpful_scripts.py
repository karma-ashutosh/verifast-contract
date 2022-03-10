from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])
