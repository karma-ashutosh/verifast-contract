import json

from brownie.network.account import LocalAccount

from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible
from brownie import accounts, config, Contract
from brownie.network.transaction import TransactionReceipt

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


def account_details(username, password, path):
    account = accounts.load(username, password=password)
    result = {
        'address': account.address,
    }
    __write_to_path(result, path)
    return result


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


def create_nft(username, password, path):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    tx = contract.createCollectible(sample_token_uri, {"from": account.address})
    tx.wait(1)
    transfer_details = tx.events['Transfer']
    result = {
        'from': transfer_details['from'],
        'to': transfer_details['to'],
        'tokenId': transfer_details['tokenId']
    }
    __write_to_path(result, path)
    return result


def transfer_nft(username, password, nft_id, to_address, path):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    tr = contract.approve(to_address, nft_id, {'from': account.address})
    tr.wait(1)
    result = {
        'from': account.address,
        'to': to_address,
        'nft_id': nft_id,
        'action': 'approved'
    }
    __write_to_path(result, path)
    return result


def claim_approved(username, password, nft_id, approver, path):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    tr: TransactionReceipt = contract.transferFrom(approver, account.address, nft_id, {'from': account.address})
    tr.wait(1)
    result = {
        'from': approver,
        'to': account.address,
        'nft_id': nft_id,
        'action': 'claimed'
    }
    __write_to_path(result, path)
    return result


def get_nft_count(username, password, path):
    contract = __get_deployed()
    account: LocalAccount = accounts.load(username, password=password)
    result = {
        'count': contract.balanceOf(account.address)
    }
    __write_to_path(result, path)
    return result


def get_all_nfts(username, password, path):
    contract = __get_deployed()
    account = accounts.load(username, password=password)
    count = contract.balanceOf(account.address)
    result = []
    for index in range(count):
        token = contract.tokenOfOwnerByIndex(account.addres, index)
        result.append(__get_token_info(contract, token))
    result = {
        'username': username,
        'all_nfts': result
    }
    __write_to_path(result, path)
    return result


def get_nft(nft_id, path):
    contract = __get_deployed()
    result = __get_token_info(contract, nft_id)
    __write_to_path(result, path)
    return result

def __get_token_info(contract: Contract, token_index):
    uri = contract.tokenURI(token_index)
    return {
        'tokenId': token_index,
        'uri': uri
    }


def __get_deployed(contract_address=None) -> Contract:
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
