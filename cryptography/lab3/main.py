from Crypto.Cipher import AES
import base64
import os
import binascii


class AES_CBC(object):

    def __init__(self, message):
        self.iv = os.urandom(16)
        self.mode = AES.MODE_CBC
        self.message = message
        self.block_size = 16

    def padding(self):
        padding_message = self.message + (
            self.block_size - (len(self.message) % self.block_size)
        ) * chr(self.block_size - (len(self.message) % self.block_size))
        return padding_message

    def unpadding(self, ciphertext):
        iv = ciphertext[:32]
        padding_message = ciphertext[32:]
        return iv, padding_message

    def encrypt(self, key):
        aes = AES.new(key, self.mode, self.iv)
        # padding message using pkcs5
        message_pad = self.padding()
        # check padding
        print("*" * 20)
        print(message_pad.encode())
        print(self.message.encode())
        print("*" * 20)
        # encrypt and get a binary ciphertext
        ciphertext = aes.encrypt(message_pad)
        # convert to byte hex str
        ciphertext = binascii.b2a_hex(ciphertext)
        iv = binascii.b2a_hex(self.iv)
        ciphertext = iv + ciphertext
        return ciphertext.decode()

    def decrypt(self, key, ciphertext):
        iv, padding_message = self.unpadding(ciphertext)
        aes = AES.new(key, self.mode, binascii.a2b_hex(iv))
        message = aes.decrypt(binascii.a2b_hex(padding_message))
        print(message.decode())


if __name__ == '__main__':
    text = "asdfhiasfjoavnorihbbhhtru"
    cipher1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    key1 = "140b41b22a29beb4061bda66b6747e14"
    cipher2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    key = os.urandom(16)
    a = AES_CBC(text)
    ciphertext = a.encrypt(key)
    a.decrypt(key, ciphertext)
    a.decrypt(binascii.a2b_hex(key1), cipher1)
    a.decrypt(binascii.a2b_hex(key1), cipher2)
