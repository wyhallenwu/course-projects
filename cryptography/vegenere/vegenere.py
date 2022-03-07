import argparse


# initialize arguments
def initialize():
    alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                        '-f',
                        action='store',
                        help='please input file path')

    parser.add_argument('--crypto',
                        '-c',
                        action='store',
                        help='please input crypto')

    args = parser.parse_args()
    filePath = args.file
    crypto = args.crypto
    return filePath, crypto, alphabet, alphabet


# get plainText from file
def plainTextFromFile(filePath):
    with open(filePath, 'r') as f:
        plainText = f.read()
        return plainText.lower()


# encrypt
def encrypt(filePath, crypto, alphabet):
    plainText = plainTextFromFile(filePath)

    encryptText = ""
    cryptoLength = len(crypto)
    alphabetLengh = len(alphabet)
    for i in range(len(plainText)):
        yIndex = alphabet.index(crypto[i % cryptoLength])
        xIndex = alphabet.index(plainText[i])
        encryptText += alphabet[(xIndex + yIndex) % alphabetLengh]
    return encryptText


# decrypt
def decrypt(encryptText, alphabet, crypto):
    plainText = ""
    cryptoLength = len(crypto)
    alphabetLengh = len(alphabet)
    for i in range(len(encryptText)):
        Index = alphabet.index(encryptText[i])
        yIndex = alphabet.index(crypto[i % cryptoLength])
        xIndex = (Index - yIndex + alphabetLengh) % alphabetLengh
        plainText += alphabet[xIndex]
    return plainText


# test
if __name__ == '__main__':
    filePath, crypto, alphabet, alphabet = initialize()
    plainText = plainTextFromFile(filePath)
    print("plain text: ", plainText)
    encryptText = encrypt(filePath, crypto, alphabet)
    print("encrypt text: ", encryptText)
    decryptText = decrypt(encryptText, alphabet, crypto)
    print("decrypt text: ", decryptText)
