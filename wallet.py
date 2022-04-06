class wallet():

    def __init__(self):
        self.wallets = []
        self.createWallet()

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
    #creat a list of transactions
    #print all
    print("\n")
    print("Wallet Created:")
    print("Private Key:     ", wallet['private_key'])
    print("Public Key:      ", wallet['public_key'])
    print("Public Address:  ", wallet['public_address'])

    self.wallets.append(wallet)
    return wallet
    
    def generatePrivateKey(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    def generatePublicKey(self, private_key):
        return hashlib.sha256(str(private_key).encode('utf-8')).hexdigest()
    def generatePublicAdress(self, public_key):
        return hashlib.sha256(str(public_key).encode('utf-8')).hexdigest()
    
    #function transaction
    def transaction(self, transaction):
        if not self.verifyTransaction(transaction):
            return False
        sender_wallet = transaction['sender_wallet']
        sender_wallet['balance'] -= transaction['amount']
        self.data.append(transaction)
        return True
