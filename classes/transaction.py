import time
import ecdsa

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
            print("\nTranscation verify")
            return public_key.verify(signature, message)
        except ecdsa.BadSignatureError:
            print("\nTranscation could not verify")
            return False