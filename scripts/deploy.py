from brownie import accounts, MerkleTree, FlightAuth, config, network

def deploy_merkletree():
    account = get_account() #accounts[0]
    tree = MerkleTree.deploy({"from": account, "gasPrice": 100000000000000000}, publish_source=True)
    print(tree)

def deploy_flight_auth():
    account = get_account()#accounts[0]
    flight_auth = FlightAuth.deploy({"from": account, "gasPrice": 100000000000000000}, publish_source=True)
    print(flight_auth)

def get_account():
    if (network.show_active()) == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_flight_auth()
    deploy_merkletree()
