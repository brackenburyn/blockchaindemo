# Noah Brackenbury, December 2018
# This program is a demo for how blockchain technology can be used to keep 
# a secure list of valid currency transactions.  
# getLatestBlock takes a starting balance, a list of transactions, and 
# a number of transactions per block

import hashlib

def getLatestBlock(startBalances, pendingTransactions, blockSize):
  # initialize variables
  pendingTs = pendingTransactions # list of transactions. Each take the form of:
  # [giver id, reciever id, amount]
  bal = startBalances # this is an array with each person's balance at their id's index
  prevBlockHash = "0000000000000000000000000000000000000000"
  blockString = ""
  # continuously mine blocks while there are still transactions left to be logged
  while pendingTs:
    # mine a block, adjust variables if successful
    results = mineBlock(bal, pendingTs, prevBlockHash, blockSize)
    if results:
      blockString = results[0]
      prevBlockHash = blockString[0:40]
      bal = results[1]
      pendingTs = results[2]
  # when all valid transactions are logged, return the final block
  return blockString
    
# Helper function to mine one block
def mineBlock(balances, pendingTransactions, prevBlockHash, blockSize):
  # compile a <=blockSize list of valid transactions
  transactions = []
  while (len(transactions) < blockSize) and pendingTransactions:
    current_transaction = pendingTransactions.pop(0)
    if balances[current_transaction[0]] >= current_transaction[2]:
      balances[current_transaction[0]] -= current_transaction[2]
      balances[current_transaction[1]] += current_transaction[2]
      transactions.append(stringifyList(current_transaction))
  # if there are no valid transactions, don't mine the block
  if not transactions:
    return False
  
  # mine the block- find the smallest valid int nonce so that the hash begins with "0000"
  nonce = 0
  while (sha1(str(prevBlockHash) + ", " + str(nonce) + ", " + stringifyList(transactions))[0:4] != "0000"):
    nonce += 1
  blockHash = sha1(str(prevBlockHash) + ", " + str(nonce) + ", " + stringifyList(transactions))
  
  # stringify the block and return it
  blockString = blockHash + ", " + str(prevBlockHash) + ", " + str(nonce) + ", " + stringifyList(transactions)
  return (blockString, balances, pendingTransactions)
  
# helper function to hash our stringified representations of blocks
def sha1(text):
  s = hashlib.sha1()
  s.update(text.encode('utf-8'))
  return s.hexdigest()

# helper function to stingify lists more easily
def stringifyList(array):
  return "[" + ', '.join(str(x) for x in array) + "]"