import json
from web3 import Web3
import random


#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x654De8A96B58FCe358196c391523284ba66E4456'
deployed_contract_address = Web3.to_checksum_address(deployed_contract_address)

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)


#Calling a contract function createAcc(uint,uint,uint)
# txn_receipt = contract.functions.createAcc(1, 2, 5).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
# txn_receipt_json = json.loads(w3.to_json(txn_receipt))
# print(txn_receipt_json) # print transaction hash

# print block info that has the transaction
# print(w3.eth.get_transaction(txn_receipt_json)) 

#Call a read only contract function by replacing transact() with call()

# User registration
def registerUser(id, name):
    """
    Register a user with id and name
    """
    txn_receipt =  contract.functions.registerUser(id,name).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600})
    w3.eth.wait_for_transaction_receipt(txn_receipt)
    txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    print(contract.functions.registerUser1().call({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600}))
 
    return w3.eth.get_transaction(txn_receipt_json)

# Account creation
def createAcc(id1, id2, balance):
    """
    Create an account with id1 and id2
    """
    txn_receipt = contract.functions.createAcc(id1, id2, balance).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600})
    w3.eth.wait_for_transaction_receipt(txn_receipt)
    txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    return w3.eth.get_transaction(txn_receipt_json)

# Closing account
def closeAcc(id1, id2):
    """
    Close an account with id1 and id2
    """
    txn_receipt = contract.functions.closeAccount(id1, id2).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600})
    w3.eth.wait_for_transaction_receipt(txn_receipt)
    txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    # print(contract.functions.closeAccount1(id1,id2).call())
    return w3.eth.get_transaction(txn_receipt_json)

# Send Amount
def sendAmount(fromId, toId):
    """
    Send amount from fromId to toId
    """
    # Check the status of functions.sendAmount
    # If true then return 1 else 0
    txn_receipt = contract.functions.sendAmount(fromId, toId).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600})
    w3.eth.wait_for_transaction_receipt(txn_receipt)
    # txn_receipt_json = json.loads(w3.to_json(txn_receipt))

    return contract.functions.sendAmount1().call({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409600})
    # return w3.eth.get_transaction(txn_receipt_json)


# Generate graph
def generateGraph(num):
    """
    Creates a connected graph with num nodes and 1 connected component
    """
    
    def barabasi(n, m):
        """
        Generates a graph with power-law degree distribution

        """

        def random_subset_with_weights(weights, m):
            """
            Returns a random subset of m elements from the given list of weights
            """
            mapped_weights = [
                (random.expovariate(w), i)
                for i, w in enumerate(weights)
            ]
            return { i for _, i in sorted(mapped_weights)[:m] }

        # initialise with a complete graph on m vertices
        neighbours = [set(range(m)) - {i} for i in range(m)]
        degrees = [m-1 for i in range(m) ]

        for i in range(m, n):
            n_neighbours = random_subset_with_weights(degrees, m)

            # add node with back-edges
            neighbours.append(n_neighbours)
            degrees.append(m)

            # add forward-edges
            for j in n_neighbours:
                neighbours[j].add(i)
                degrees[j] += 1

        return neighbours

    def generate_random_graph(num=num):
        """Generates a random graph."""
        return dict(enumerate(barabasi(num, 2)))

    return generate_random_graph(num)

# Testing
num = 100
num_trx = 1000
num_successful = 0

for i in range(num):
    """
    Register users
    """
    print()
    print("##########", i, "##########")
    registerUser(i, "User" + str(i))
    print("##########", i, "##########")
    print()

# Dictionary of users
graph = generateGraph(num)

for i, neighbors in graph.items():
    for j in neighbors:
        """
        Create accounts
        """
        init_bal = int(random.expovariate(1/10))
        createAcc(i, j, init_bal//2)

# Send money
while num_trx > 0:
    """
    Send money
    """
    fromId = random.randint(0, num-1)
    toId = random.randint(0, num-1)
    if(fromId == toId):
        continue
    num_successful += 1 if sendAmount(fromId, toId) else 0
    if(num_trx % 100 == 1):
        print("Successful transactions:", num_successful)
        num_successful = 0
    num_trx -= 1

# Close accounts
for i, neighbors in graph.items():
    for j in neighbors:
        closeAcc(i, j)

    