import hashlib
import time

class Block():
    def __init__(self, transactions, previous_hash, index, timestamp=None, coinbase_transaction=None):
        self.nonce = -1
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        difficulty = 2
        self.timestamp = timestamp or time.time()
        self.hash = self.mine(difficulty)
        self.coinbase_transaction = coinbase_transaction

    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.nonce, self.index,self.previous_hash, self.transactions, self.timestamp)
        return hashlib.sha256(str(string_block).encode('utf-8')).hexdigest()
    
    def mine(self, difficulty):
        found = False
        while not found:
            print(str(self.nonce) + "  "+ str(self.compute_hash))
            self.nonce += 1
            self.hash = self.compute_hash()
            if self.hash[0:difficulty] == "0" * difficulty:
                found = True
                print("Block mined: {}".format(self.hash))
                return self.hash
    
    #validate block
    def validateBlock(self, previous_hash):
        if self.previous_hash != previous_hash:
            return False
        if self.hash != self.compute_hash():
            return False
        return True