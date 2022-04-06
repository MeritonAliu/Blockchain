import hashlib
import string
import time
from msilib.schema import SelfReg

#from sys import last_traceback


class Block():
    def __init__(self, data, previous_hash, index, proof_number, timestamp=None):
        self.hash = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        self.previous_hash = previous_hash
        self.proof_number = proof_number
        self.index = index
        self.data = data
        self.timestamp = timestamp or time.time()
    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.index, self.proof_number, self.previous_hash, self.data, self.timestamp)
        return hashlib.sha256(str(self.data).encode('utf-8')).hexdigest()
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.data = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.data = "This is the Genesis Block Data"
        genesisblock = Block(self.data,0000000000000000000000000000000000000000000000000000000000000000,0, 0, time.time())
        self.chain.append(genesisblock)
        print(genesisblock.timestamp)

    def addBlock(self, data):
        time.sleep(0.1)
        block = Block(data, self.chain[-1].hash, len(self.chain), time.time())
        self.chain.append(block)

    def returnHashAndIndex(self):
        #funtion to print details of the block
        for i in range(len(self.chain)):
            print("Block Hash: ", self.chain[i].hash)
            print("Block Index: ", self.chain[i].index)
            print("Block Proof Number: ", self.chain[i].proof_number)
            print("Block Timestamp: ", self.chain[i].timestamp)
            print("\n")
        
    #function to validate the block
    def validateBlockWithPrevious(self, block):
        previous_block = self.chain[block.index - 1]
        if previous_block.index + 1 != block.index:
            print("Block index not valid i")
            return False
        elif block.timestamp <= previous_block.timestamp:
            print("Block index not valid t")
            return False
        else:
            print("Block index valid")
            return True


blockchain = BlockChain()
blockchain.addBlock("Person 1 20CHF-> Person 2")
blockchain.addBlock("Person 2 20CHF-> Person 3")
blockchain.addBlock("Person 3 20CHF-> Person 4")
blockchain.addBlock("Person 4 20CHF-> Person 5")
#print validate block

blockchain.returnHashAndIndex()
blockchain.validateBlockWithPrevious(blockchain.chain[4])

