import numpy as np
import argparse


def initialize():
    # create a cipherbook
    alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    # index = [i for i in range(len(alphabet))]
    # cipherbook = dict(zip(alphabet, index))

    # set arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--step',
                        '-s',
                        type=int,
                        action='store',
                        help='please input steps')

    parser.add_argument('--plaintext',
                        '-p',
                        action='store',
                        help='please input plaintext')

    args = parser.parse_args()
    step = args.step
    plaintext = args.plaintext
    return plaintext.lower(), step, alphabet


# encrypt
def encrypt(plaintext, step, cipherbook):
    encryptText = ""
    for c in plaintext:
        if c in cipherbook:
            index = cipherbook.index(c)
            newIndex = (index + step) % len(cipherbook)
            encryptText += cipherbook[newIndex]
    return encryptText


def decrypt(encryptText, step, cipherbook):
    plaintext = ""
    for c in encryptText:
        if c in cipherbook:
            index = cipherbook.index(c)
            originIndex = ((index - step) + len(cipherbook)) % len(cipherbook)
            plaintext += cipherbook[originIndex]
    return plaintext


if __name__ == '__main__':
    plaintext, step, cipherbook = initialize()
    encryptText = encrypt(plaintext, step, cipherbook)
    print("encrypt text: ", encryptText)
    decryptText = decrypt(encryptText, step, cipherbook)
    print("decrypt text: ", decryptText)