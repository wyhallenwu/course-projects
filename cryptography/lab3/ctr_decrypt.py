from Crypto.Cipher import AES
import binascii
import math


def xor(x, y):
    result = ""
    length = 0
    if len(x) < len(y):
        length = len(x)
    else:
        length = len(y)
    for i in range(length):
        result += hex(x[i] ^ y[i]).replace("0x", "")
    return binascii.a2b_hex(result).decode('utf8', 'ignore')


def unpadding(ciphertext):
    iv = ciphertext[:32]
    padding_message = ciphertext[32:]
    return iv, padding_message


# use AES to encrypt counter
def encrypt_counter(key, counter):
    aes = AES.new(key, AES.MODE_ECB)
    c = aes.encrypt(counter)
    return c


# counter plus 1 after each block
def counter_plus(counter):
    counter = int(counter, 16) + 1
    counter = hex(counter).replace("0x", "")
    counter = binascii.a2b_hex(counter)
    return counter


def decrypt(key, ciphertext):
    # counter is at the front of the cipher content
    counter, ciphertext = unpadding(ciphertext)
    # how many blocks
    counter_num = math.ceil(len(ciphertext) / 32)
    # convert to bytes
    ciphertext = binascii.a2b_hex(ciphertext)
    # plaintext
    message = ""
    # decrypt each block
    for i in range(counter_num):
        if i == 0:
            c = encrypt_counter(binascii.a2b_hex(key),
                                binascii.a2b_hex(counter))
            message += xor(c, ciphertext[i * 16:i * 16 + 16])
        elif i == counter_num - 1:
            c = encrypt_counter(binascii.a2b_hex(key), counter_plus(counter))
            message += xor(c, ciphertext[i * 16:])
        else:
            c = encrypt_counter(binascii.a2b_hex(key), counter_plus(counter))
            message += xor(c, ciphertext[i * 16:i * 16 + 16])
    print(message)


if __name__ == '__main__':
    cipher1 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
    key1 = "36f18357be4dbd77f050515c73fcf9f2"
    cipher2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

    decrypt(key1, cipher1)
    # CTR mode lets you build a streamn8ƫq+!<@d
    decrypt(key1, cipher2)
    # Always avoid the two time pad!