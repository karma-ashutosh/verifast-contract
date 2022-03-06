import json

from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible
from brownie import accounts, network, config, Contract
from brownie.convert.datatypes import Wei

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"



def deploy_and_create():

    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button. ")
    return simple_collectible

def get_nft_count(username, password):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    return contract.balanceOf(account.address)

def get_all_nfts(username, password):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    count = contract.balanceOf(account.address)
    result = []
    for index in range(count):
        token = contract.tokenOfOwnerByIndex(account.addres, i)
        result.append(token)
    return result

def transfer_nft(username, password, nft_id, to_address):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    contract.approve(to_address, {'from': account.address})
    return "done"

def claim_approved(username, password, nft_id, approver):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    contract.transferFrom(approver, account.address, nft_id, {'from': account.address})
    return "done"


def create_nft(username, password):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    tx = contract.createCollectible(sample_token_uri, {"from": account.address})
    tx.wait(1)
    return tx.events['Transfer']

def transfer_fund(username, password, to, amount, path):
    account = accounts.load(username, password=password)
    tr = account.transfer(to=to, amount='{} ether'.format(amount))
    tr.wait(1)
    result = {
        'from': tr.sender.address,
        'to': tr.receiver,
        'amount': tr.value,
        'txId': tr.txid
    }
    print("Writing result to path {} {}".format(path, result))
    __write_to_path(result, path)
    return "done"


def account_details(username, password, path):
    account = accounts.load(username, password=password)
    result = {
        'address': account.address,
    }
    __write_to_path(result, path)
    return result

def __get_deployed(contract_address=None):
    address = config['live_contract']['address'] if not contract_address else contract_address 
    c = Contract.from_abi("SimpleCollectible", address, SimpleCollectible.abi)
    return c


def __write_to_path(result, path):
    if path:
        f = open(path, 'w')
        f.write(json.dumps(result))
        f.close()

def main():
    deploy_and_create()
