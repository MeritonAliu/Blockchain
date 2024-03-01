from classes.blockchain import BlockChain
from classes.transaction import Transaction

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