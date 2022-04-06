import hashlib
import json
import random
import string
import time
from msilib.schema import SelfReg
from re import T

from flask import Flask, jsonify, request

from block import Block
from wallet import classWallet

app = Flask(__name__)

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.data = []
        self.wallets = []
        self.current_transactions = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.data = "This is the Genesis Block Data"
        genesisblock = Block(self.data,"0" * 64 ,0, time.time())
        self.chain.append(genesisblock)

    def addBlock(self, data):
        time.sleep(0.1)
        block = Block(data, self.chain[-1].hash, len(self.chain), time.time())
        self.chain.append(block)

    
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

    #function transaction
    def transaction(self, transaction):
        if not self.verifyTransaction(transaction):
            return False
        sender_wallet = transaction['sender_wallet']
        sender_wallet['balance'] -= transaction['amount']
        self.data.append(transaction)
        return True

    #verify transaction
    def verifyTransaction(self, transaction):
        #public_key = self.wallets[transaction['sender_wallet']]['public_key']
        public_key = self.wallets[0]['public_key']
        signature = transaction['signature']
        string_transaction = "{}{}{}".format(transaction['recipient_address'], transaction['amount'], transaction['timestamp'])
        return self.verifySignature(public_key, signature, string_transaction)

    #function with wallet to create transaction
    def createTransacdtion(self, sender_wallet, recipient_address, amount):
        transaction = {
            'sender_wallet': sender_wallet,
            'recipient_address': recipient_address,
            'amount': amount,
            'timestamp': time.time()
        }
        return transaction
    
    #function to sign transaction
    def signTransaction(self, transaction, sender_private_key):
        transaction['signature'] = self.generateSignature(transaction, sender_private_key)
        return transaction

    #function to generate signature
    def generateSignature(self, transaction, sender_private_key):
        string_transaction = "{}{}{}".format(transaction['recipient_address'], transaction['amount'], transaction['timestamp'])
        return hashlib.sha256(str(string_transaction).encode('utf-8')).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.chain[-1].index + 1
    @property
    def last_block(self):
        return self.chain[-1]
    




blockchain = BlockChain()
blockchain.addBlock("Person 1 20CHF-> Person 2")
blockchain.addBlock("Person 2 20CHF-> Person 3")
blockchain.addBlock("Person 3 20CHF-> Person 4")
blockchain.addBlock("Person 4 20CHF-> Person 5")

wallet1 = classWallet()
wallet2 = classWallet()
blockchain.wallets = [wallet1, wallet2]

for block in blockchain.chain:
    print(block)

for wallet in blockchain.wallets:
    print(wallet)



blockchain.validateBlockChain()
from uuid import uuid4

node_identifier = str(uuid4()).replace('-', '')

@app.route('/mine', methods=['GET'])
def mine():

    # first we have to run the proof of work algorithm to calculate the new proof..


    # we must receive reward for finding the proof
    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )

    response = {
        'message': "Forged new block.",
        'index': block['index'],
        'transactions': block['transaction'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
#https://github.com/janfilips/blockchain/tree/eb79d45c292f2abf950822afcc4153f8c6440c4c
@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to the Block {index}.'}

    return jsonify(response, 200)

@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)




