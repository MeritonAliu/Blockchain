import hashlib
import time


class Block():
    def __init__(self, data, previous_hash, index, timestamp=None):
        self.nonce = -1
        self.previous_hash = previous_hash
        self.index = index
        self.data = data
        difficulty = 2
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()
        self.hash = self.mine(difficulty)

    def __str__(self) -> str:
        return "\nIndex:       {}\nTimestamp:   {}\nData:        {}\nHash:        {}\n".format(self.index, self.timestamp, self.data, self.hash)

    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.nonce, self.index,self.previous_hash, self.data, self.timestamp)
        return hashlib.sha256(str(string_block).encode('utf-8')).hexdigest()
    
    def mine(self, difficulty):
        found = False
        while not found:
            self.nonce += 1
            self.hash = self.compute_hash()
            if self.hash[0:difficulty] == "0" * difficulty:
                found = True
                print("Block mined: {}".format(self.hash))
                return self.hash
    
    def validateBlock(self, previous_hash):
        if self.previous_hash != previous_hash:
            return False
        if self.hash != self.compute_hash():
            return False
        return True
    


