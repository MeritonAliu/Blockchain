import hashlib
import random
import string
import time
import ecdsa
import binascii

class Block():
    def __init__(self, data, previous_hash, index, timestamp=None):
        self.nonce = -1
        self.previous_hash = previous_hash
        self.index = index
        self.data = data
        difficulty = 2
        self.timestamp = timestamp or time.time()
        self.hash = self.mine(difficulty)

    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.nonce, self.index,self.previous_hash, self.data, self.timestamp)
        return hashlib.sha256(str(string_block).encode('utf-8')).hexdigest()
    
    def mine(self, difficulty):
        found = False
        while not found:
            #print(str(self.nonce) + "  "+ str(self.hash))
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

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.data = []
        self.wallets = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.data = "This is the Genesis Block Data"
        genesisblock = Block(self.data,0000000000000000000000000000000000000000000000000000000000000000,0, time.time())
        self.chain.append(genesisblock)

    def addBlock(self, data):
        time.sleep(0.1)
        block = Block(data, self.chain[-1].hash, len(self.chain), time.time())
        self.chain.append(block)

    def returnHashAndIndex(self):
        #funtion to print details of the block
        for i in range(len(self.chain)):
            print("Previous Hash:       ", self.chain[i].previous_hash)
            print("Block Hash:          ", self.chain[i].hash)
            print("Block Index:         ", self.chain[i].index)
            print("Block Proof Number:  ", self.chain[i].nonce)
            print("Block Timestamp:     ", self.chain[i].timestamp)
            print("\n")
        
    def validateBlockChain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].index != i:
                print("Manipulation of index in Block {} ".format(i))
                return False
            if self.chain[i-1].hash != self.chain[i].previous_hash:
                print("Manipulation of hash in Block {} ".format(i))
                return False
            if self.chain[i].timestamp <= self.chain[i-1].timestamp:
                print("Manipulation of timestamp in Block {} ".format(i))
                return False
        print("Blockchain is valid")
        return True

    def createWallet(self):
        #create a wallet
        wallet = {}
        #create a private key
        wallet['private_key'] = self.generatePrivateKey()
        #create a public key
        wallet['public_key'] = self.generatePublicKey(wallet['private_key'])
        #create a public address
        wallet['public_address'] = self.generatePublicAdress(wallet['public_key'])
        #create a balance
        wallet['balance'] = 0
        #print a list of transactions
        print("\n")
        print("Wallet Created:")
        print("Private Key:     ", wallet['private_key'])
        print("Public Key:      ", wallet['public_key'])
        print("Public Address:  ", wallet['public_address'])
        self.wallets.append(wallet)
        return wallet
    
    def generatePrivateKey(self):
        # Generate a new ECDSA private key
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # Convert the private key to its hexadecimal string representation for storage
        private_key_hex = private_key.to_string().hex()
        return private_key_hex
    
    def generatePublicKey(self, private_key_hex):
        # Convert the hex private key back to a bytes object
        private_key_bytes = bytes.fromhex(private_key_hex)
        # Create a SigningKey object from the bytes
        private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        # Derive the public key
        public_key = private_key.get_verifying_key()
        # Convert the public key to hex format for easy storage and use
        public_key_hex = public_key.to_string().hex()
        return public_key_hex
    
    def generatePublicAdress(self, public_key):
        return hashlib.sha256(public_key.encode('utf-8')).hexdigest()

class Transaction:
    def __init__(self, pubAddrSender, pubAddrReceiver, amount, privAddrSender):
        self.pubAddrSender = pubAddrSender
        self.pubAddrReceiver = pubAddrReceiver
        self.privAddrSender = privAddrSender
        self.amount = amount
        self.timestamp = time.time()
        self.signature = self.signTransaction()
        self.printAll()

    def printAll(self): # only for debugging
        print("\nTransaction created: ")
        print("Sender:    ", self.pubAddrSender)
        print("Receiver:  ", self.pubAddrReceiver)
        print("Amount:    ", self.amount)
        print("Timestamp: ", self.timestamp)
        print("Signature: ", self.signature)
    
    def signTransaction(self):
        private_key_bytes = bytes.fromhex(self.privAddrSender)
        private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        message = f"{self.pubAddrSender}{self.pubAddrReceiver}{self.amount}{self.timestamp}".encode()
        signature = private_key.sign(message)
        return signature.hex()

    @staticmethod
    def verifyTransaction(transaction):
        message = f"{transaction.pubAddrSender}{transaction.pubAddrReceiver}{transaction.amount}{transaction.timestamp}".encode()
        public_key_bytes = bytes.fromhex(transaction.pubAddrSender)
        public_key = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)
        signature = bytes.fromhex(transaction.signature)
        try:
            print("\n transcation verify")
            return public_key.verify(signature, message)
        except ecdsa.BadSignatureError:
            print("\n transcation could not verify")
            return False

## main code
if __name__ == "__main__":
    blockchain = BlockChain()
    blockchain.addBlock("Hello this is my first block in the blockchain")
    blockchain.addBlock("And this the second")
    blockchain.returnHashAndIndex()
    blockchain.createWallet()
    blockchain.createWallet()
    print(blockchain.wallets[1]['public_key'])
    transaction = Transaction(
        blockchain.wallets[0]['public_key'],
        blockchain.wallets[1]['public_key'],
        10,
        blockchain.wallets[0]['private_key']
    )
    Transaction.verifyTransaction(transaction)
    print(blockchain.wallets[1]['balance'])