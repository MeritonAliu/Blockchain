import hashlib
import time
import ecdsa
from classes.block import Block
from classes.transaction import Transaction

class BlockChain(object):
    MINING_REWARD = 0.5 # The reward amount for adding a block
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.wallets = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        genesis_transactions = []
        genesisblock = Block(
            genesis_transactions,
            "0" * 64,
            0, 
            time.time()
        )
        self.chain.append(genesisblock)

    def verifyTransaction(self, transaction):
        return Transaction.verifyTransaction(transaction)
    
    def getBalance(self, public_address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.pubAddrSender == public_address:
                    balance -= transaction.amount
                if transaction.pubAddrReceiver == public_address:
                    balance += transaction.amount
        return balance
    
    def isTransactionValid(self, transaction):
        sender_balance = self.getBalance(transaction.pubAddrSender)
        return sender_balance >= transaction.amount and self.verifyTransaction(transaction)

    def createRewardTransaction(self, miner_address):
        reward_transaction = Transaction(
                    pubAddrSender="0" * 64,  # A special sender address for rewards
                    pubAddrReceiver=miner_address,
                    amount=self.MINING_REWARD,
                    signature="Reward"  # Optionally, use a special signature
                )
        return reward_transaction

    def addBlock(self, transactions, miner_address):
        if all(self.isTransactionValid(transaction) for transaction in transactions):
            reward_transaction = self.createRewardTransaction(miner_address)
            transactions_with_reward = transactions + [reward_transaction]

            time.sleep(0.1)
            previous_hash = self.chain[-1].hash if self.chain else '0' * 64
            block = Block(transactions_with_reward, previous_hash, len(self.chain), time.time())
            self.chain.append(block)
            print("\nBlock successfully mined and added to the blockchain.")
        else:
            print("\nOne or more transactions are invalid due to insufficient balance or verification failure.")

    def returnHashAndIndex(self):
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
    
    def get_total_coin_supply(self):
        initial_supply = 0  # Adjust this value based on your actual genesis block configuration
        reward_per_block = self.MINING_REWARD
        total_mined_blocks = len(self.chain)
        total_coin_supply = initial_supply + (reward_per_block * total_mined_blocks)
        return total_coin_supply
    