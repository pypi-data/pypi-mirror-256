import numpy as np
from Crypto.Util import number
import hashlib
import os

class RSA:
    def __init__(self):
        self.private_key = np.empty([2], dtype='|S256')
        self.public_key = np.empty([2], dtype='|S256')
    
    def generate_key(self):
        while True:
            p = number.getPrime(1024)
            q = number.getPrime(1024)
            if p != q:
                break

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537

        if number.GCD(e, phi) != 1:
            raise ValueError("e is not coprime to phi(n)")

        d = number.inverse(e, phi)
        self.private_key[0] = n.to_bytes(256, "big")
        self.private_key[1] = d.to_bytes(256, "big")
        self.public_key[0] = n.to_bytes(256, "big")
        self.public_key[1] = e.to_bytes(256, "big")

    def encrypt(self, message):
        padded_message = self._oaep_pad(message.encode('utf-8'), hash_algo='sha256')
        return pow(int.from_bytes(padded_message, byteorder='big'), int.from_bytes(self.public_key[1], 'big'), int.from_bytes(self.public_key[0], 'big'))
    
    def decrypt(self, ciphertext):
        decrypted = pow(ciphertext, int.from_bytes(self.private_key[1], 'big'), int.from_bytes(self.private_key[0], 'big'))
        unpadded_message = self._oaep_unpad(decrypted.to_bytes(256, byteorder='big'), hash_algo='sha256')
        return unpadded_message.decode('utf-8')

    def _oaep_pad(self, message, hash_algo):
        hash_len = hashlib.new(hash_algo).digest_size
        k = 256
        if len(message) > k - 2 * hash_len - 2:
            raise ValueError("Message too long")

        l_hash = hashlib.new(hash_algo, b'').digest()
        ps = b'\x00' * (k - len(message) - 2 * hash_len - 2)
        db = l_hash + ps + b'\x01' + message
        seed = os.urandom(hash_len)
        db_mask = self._mgf1(seed, k - hash_len - 1, hash_algo)
        masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
        seed_mask = self._mgf1(masked_db, hash_len, hash_algo)
        masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
        return b'\x00' + masked_seed + masked_db

    def _oaep_unpad(self, ciphertext, hash_algo):
        hash_len = hashlib.new(hash_algo).digest_size
        k = 256
        if len(ciphertext) != k or k < 2 * hash_len + 2:
            raise ValueError("Decryption error")

        _, masked_seed, masked_db = ciphertext[:1], ciphertext[1:hash_len+1], ciphertext[hash_len+1:]
        seed_mask = self._mgf1(masked_db, hash_len, hash_algo)
        seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
        db_mask = self._mgf1(seed, k - hash_len - 1, hash_algo)
        db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
        l_hash = db[:hash_len]
        l_hash_expected = hashlib.new(hash_algo, b'').digest()
        if l_hash != l_hash_expected:
            raise ValueError("Decryption error")
        
        i = hash_len
        while i < len(db):
            if db[i] == 1:
                break
            if db[i] != 0:
                raise ValueError("Decryption error")
            i += 1
        else:
            raise ValueError("Decryption error")

        return db[i+1:]

    def _mgf1(self, seed, mask_len, hash_algo):
        counter = 0
        output = b''
        while len(output) < mask_len:
            c = counter.to_bytes(4, byteorder='big')
            output += hashlib.new(hash_algo, seed + c).digest()
            counter += 1
        return output[:mask_len]


if __name__ == "__main__":
    # Example usage
    rsa = RSA()
    rsa.generate_key()

    message = "Hello, RSA!"
    encrypted = rsa.encrypt(message)
    print("Encrypted:", encrypted)

    decrypted = rsa.decrypt(encrypted)
    print("Decrypted:", decrypted)
