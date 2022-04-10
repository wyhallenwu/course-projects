from crypt import crypt
from re import A
from Crypto.Cipher import AES
import binascii


def unpadding(ciphertext):
    iv = ciphertext[:32]
    padding_message = ciphertext[32:]
    return iv, padding_message


def xor(iv, block):
    result = ""
    for i in range(16):
        result += hex(iv[i] ^ block[i]).replace("0x", "")
    return binascii.a2b_hex(result)


def AES_ECB(key, iv, block):
    aes = AES.new(key, AES.MODE_ECB)
    decrypt_result = aes.decrypt(block)
    result = xor(decrypt_result, iv)
    # print(binascii.b2a_hex(result))
    return result.decode('utf8', 'ignore')


def decrypt(ciphertext, key):
    key = binascii.a2b_hex(key)
    iv, ciphertext = unpadding(ciphertext)
    # print(ciphertext)
    length = len(ciphertext)
    # print(length)
    decryptor_num = int(length / 32)
    # print(decryptor_num)
    ciphertext = binascii.a2b_hex(ciphertext)
    # print(ciphertext)
    iv = binascii.a2b_hex(iv)
    message = ""
    for i in range(decryptor_num):
        if i == 0:
            message += AES_ECB(key, iv, ciphertext[i * 16:i * 16 + 16])
        else:
            message += AES_ECB(key, ciphertext[(i - 1) * 16:(i - 1) * 16 + 16],
                               ciphertext[i * 16:i * 16 + 16])

    return message


if __name__ == '__main__':

    cipher1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    key1 = "140b41b22a29beb4061bda66b6747e14"
    cipher2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
    m = decrypt(cipher1, key1)
    print(m)
    m = decrypt(cipher2, key1)
    print(m)