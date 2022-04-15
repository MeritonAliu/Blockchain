import hashlib
import random
import string
from platform import win32_edition
#test

class classWallet():
    def __init__(self, ):
        wallet = {}
        wallet['private_key'] = self.generatePrivateKey()
        wallet['public_key'] = self.generatePublicKey(wallet['private_key'])
        wallet['address'] = self.generatePublicAdress(wallet['public_key'])
        wallet['balance'] = 0
        self.private_key = wallet['private_key']
        self.public_key = wallet['public_key']
        self.address = wallet['address']
        self.balance = wallet['balance']
        self.wallet = wallet

        #self.wallets = [wallet]
        #for wallet in self.wallets:
            #print(wallet)
        
    def __str__(self) -> str:
        return "\nPrivate key: {}\nPublic key:  {}\nAddress:     {}\nBalance:     {}\n".format(self.private_key, self.public_key, self.address, self.balance)
       
    def generatePrivateKey(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    def generatePublicKey(self, private_key):
        return hashlib.sha256(str(private_key).encode('utf-8')).hexdigest()
    def generatePublicAdress(self, public_key):
        return hashlib.sha256(str(public_key).encode('utf-8')).hexdigest()

    

    

        
