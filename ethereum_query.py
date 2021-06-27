from web3 import Web3
from hexbytes import HexBytes

IP_ADDR='18.188.235.196'
PORT='8545'

w3 = Web3(Web3.HTTPProvider('http://' + IP_ADDR + ':' + PORT))

# if w3.isConnected():
# #     This line will mess with our autograders, but might be useful when debugging
#     print( "Connected to Ethereum node" )
# else:
#     print( "Failed to connect to Ethereum node!" )

def get_transaction(tx):
    tx = w3.eth.get_transaction(tx)   #YOUR CODE HERE
    return tx

# Return the gas price used by a particular transaction,
#   tx is the transaction
def get_gas_price(tx):
    tx = get_transaction(tx)
    gas_price =  tx.gasPrice #YOUR CODE HERE
    return gas_price

def get_gas(tx): 
    gas = w3.eth.get_transaction_receipt(tx) #YOUR CODE HERE
    return gas

def get_transaction_cost(tx):
    gas = get_gas(tx)
    tx_cost = get_gas_price(tx) * gas.gasUsed #YOUR CODE HERE
    return tx_cost

def get_block_cost(block_num):
    block_count = w3.eth.getBlockTransactionCount(block_num)
    block_cost = 0
    for i in range(block_count):
        block_cost += w3.eth.get_transaction_by_block(block_num, i).value  #YOUR CODE HERE
    return block_cost

# Return the hash of the most expensive transaction
def get_most_expensive_transaction(block_num):
    block_count = w3.eth.getBlockTransactionCount(block_num)
    max_tx = HexBytes('0xf7f4905225c0fde293e2fd3476e97a9c878649dd96eb02c86b86be5b92d826b6')  #YOUR CODE HERE
    max_cost = 0
    for i in range(block_count): 
        tx = w3.eth.get_transaction_by_block(block_num, i)
        tx_cost = tx.value
        if tx_cost > max_cost: 
            max_cost = tx_cost
            max_tx = tx.hash
    return max_tx