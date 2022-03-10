from scripts.helpful_scripts import get_account, get_contract, OPENSEA_URL
from scripts.create_metadata import create_metadata


def create_sample_collectible(metadata_uri=None):
    account = get_account()
    simple_collectible = get_contract("simple_collectible")

    if not metadata_uri:
        filepath = "./img/pug.png"
        filename = filepath.split("/")[-1:][0]
        metadata_uri = create_metadata(
            0, "pugsandpugs", "pug", "a cute pug!!", filepath, filename
        )
        print(metadata_uri)

    # https://testnets.opensea.io/assets/0x41f70a6b5FA43a31116C19eb4EaFF09d1B3fa983/0
    tx = simple_collectible.createCollectible(metadata_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button. ")
    return simple_collectible


def main():
    create_sample_collectible(
        metadata_uri="https://ipfs.io/ipfs/QmVubQBogxySuuCXkJc5Y1zigrdgkdiT7W69wgGQEx3snr?filename=0-pugsandpugs.json"
    )
