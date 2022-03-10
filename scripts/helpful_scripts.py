from brownie import accounts, network, config, Contract
from brownie import SimpleCollectible

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]

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


contract_to_contract_type = {"simple_collectible": SimpleCollectible}


def get_contract(contract_name):
    """
    This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
    """
    contract_type = contract_to_contract_type[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


# add contracts as they are needed.
def deploy_mocks():
    account = get_account()
    print("Mocks Deployed!")
