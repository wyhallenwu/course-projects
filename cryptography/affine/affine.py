import argparse


def initialize():
    # cipherbook
    alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    # parse input plaintext
    parser = argparse.ArgumentParser()
    parser.add_argument('--plaintext',
                        '-p',
                        help='please input plaintext',
                        action='store')

    parser.add_argument('--slope',
                        '-s',
                        help='please input slope',
                        type=int,
                        action='store')

    parser.add_argument('--offset',
                        '-o',
                        help='please input offset',
                        type=int,
                        action='store')

    args = parser.parse_args()
    plainText = args.plaintext
    slope = args.slope
    offset = args.offset
    # basic condition: slope and length of alphabet are coprime
    if gcd(slope, len(alphabet)) != 1:
        print("slope and length of alphabet are not coprime. Please try again")
        exit(0)
    return plainText.lower(), alphabet, slope, offset, gcd(
        slope, len(alphabet))


# affine
def affine(index, slope, offset, length):
    return (index * slope + offset) % length


# encrypt
def encrypt(plainText, alphabet, slope, offset):
    encryptText = ""
    cipherbookLength = len(alphabet)
    for c in plainText:
        if c in alphabet:
            index = alphabet.index(c)
            newIndex = affine(index, slope, offset, cipherbookLength)
            encryptText += alphabet[newIndex]
        else:
            encryptText += c
    return encryptText


# Euclidean Algorithm
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


# get a reverse
def reverse(a, m):
    if m == 0:
        return 1, 0
    else:
        x, y = reverse(m, a % m)
        x, y = y, (x - (a // m) * y)
        return x, y


# decrypt
def decrypt(encryptText, alphabet, slope, offset, gcdNum):
    plainText = ""
    cipherbookLength = len(alphabet)
    aReverse, _ = reverse(slope, cipherbookLength)
    for c in encryptText:
        if c in alphabet:
            index = alphabet.index(c)
            formerIndex = aReverse * (index - offset) % cipherbookLength
            plainText += alphabet[formerIndex]
        else:
            plainText += c

    return plainText


if __name__ == '__main__':
    plainText, alphabet, slope, offset, gcdNum = initialize()
    encryptText = encrypt(plainText, alphabet, slope, offset)
    print("encrypt text: ", encryptText)
    decryptText = decrypt(encryptText, alphabet, slope, offset, gcdNum)
    print("decrypt text: ", decryptText)
