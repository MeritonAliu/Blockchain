import hashlib
import time
import ecdsa
from classes.block import Block

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
        wallet = {}
        wallet['private_key'] = self.generatePrivateKey()
        wallet['public_key'] = self.generatePublicKey(wallet['private_key'])
        wallet['public_address'] = self.generatePublicAdress(wallet['public_key'])
        wallet['balance'] = 0
        print("\n")
        print("Wallet Created:")
        print("Private Key:     ", wallet['private_key'])
        print("Public Key:      ", wallet['public_key'])
        print("Public Address:  ", wallet['public_address'])
        self.wallets.append(wallet)
        return wallet
    
    def generatePrivateKey(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        private_key_hex = private_key.to_string().hex()
        return private_key_hex
    
    def generatePublicKey(self, private_key_hex):
        private_key_bytes = bytes.fromhex(private_key_hex)
        private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        public_key_hex = public_key.to_string().hex()
        return public_key_hex
    
    def generatePublicAdress(self, public_key):
        return hashlib.sha256(public_key.encode('utf-8')).hexdigest()
    