from classes.blockchain import BlockChain
from classes.transaction import Transaction

if __name__ == "__main__":
    blockchain = BlockChain()
    blockchain.returnHashAndIndex()
    
    blockchain.createWallet()
    blockchain.createWallet()
        
    transaction = Transaction(
        blockchain.wallets[0]['public_key'],
        blockchain.wallets[1]['public_key'],
        10,
        blockchain.wallets[0]['private_key']
    )
    blockchain.addBlock([transaction])
    
    print("\nBalance first Wallet", blockchain.getBalance(blockchain.wallets[0]['public_key']))
    print("\nBalance second Wallet", blockchain.getBalance(blockchain.wallets[1]['public_key']))
    blockchain.returnHashAndIndex()