from .RSA import RSA

class Server:

    def __init__(self):
        self.rsa = RSA()
        self.rsa.generate_key()
        self.last_log = b""
    
    def get_public_key(self):
        return self.rsa.public_key
    
    def encrypt(self, message):
        return self.rsa.encrypt(message)
    
    def decrypt(self, message):
        return self.rsa.decrypt(message)

    def change_key(self, reason: str):
        self.rsa = RSA()
        self.last_log = reason.encode()
        self.rsa.generate_key()
    
    def get_log(self):
        return self.last_log
