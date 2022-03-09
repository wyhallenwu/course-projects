import numpy as np
import argparse
import random


# generate a random polynomial
def genPolynomial(k):
    power = k - 1
    coefficient = []
    for i in range(power):
        coefficient.append(random.randint(1, 10))
    return coefficient


# generate a share pair
def genShare(x, coefficient, s):
    share = 0
    for i in range(len(coefficient)):
        share += coefficient[i] * int(np.power(x, i + 1))
    return (x, share + s)


# generate N share pair for N people
def genNshare(n, coefficient, s):
    shareList = []
    genToken = random.sample(range(n), n)
    for i in range(n):
        shareList.append(genShare(genToken[i], coefficient, s))
    return shareList


# reconstruct the f(0) which is the secret
def reconstruct(Kshare):
    secret = 0
    for i in range(len(Kshare)):
        mul, coe = lagrangeInterpolation(i, Kshare)
        secret += mul * Kshare[i][1] / coe
    return int(secret)


# lagrange Interpolation to compute the part of the intercept
def lagrangeInterpolation(index, Kshare):
    x_j = Kshare[index][0]
    coe = 1
    mul = 1
    for i in range(len(Kshare)):
        if i != index:
            coe *= (Kshare[i][0] - x_j)
            mul *= Kshare[i][0]
    return mul, coe


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k',
                        type=int,
                        help='at least k to unlock the secret',
                        action='store')
    parser.add_argument('-n',
                        type=int,
                        help='how many people share the secret',
                        action='store')
    parser.add_argument('-s', type=int, help='secret key', action='store')
    args = parser.parse_args()
    k = args.k
    n = args.n
    s = args.s
    # get the polynomial coefficient
    coefficient = genPolynomial(k)
    print("coefficient is: ", coefficient)
    shareList = genNshare(n, coefficient, s)
    print("N share pair: ", shareList)
    unlockList = random.sample(shareList, k)
    print("chose " + str(k) + " pairs randomly to unlock: ", unlockList)
    secret = reconstruct(unlockList)
    print("secret key is: ", secret)
