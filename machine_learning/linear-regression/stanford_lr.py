import numpy as np
import matplotlib.pyplot as plt

def loadData(filename):
    data = np.genfromtxt(filename)
    x = data[:, 1]
    y = data[:, 2]
    return x, y

def sgd(x, y, theta, bias, learning_rate, iter_num):
    # iteration
    for count in range(iter_num):
        # single step (stochastic gradient descent)
        for i in range(len(x)):
            theta = theta + learning_rate * (y[i] - theta * x[i] - bias) * x[i]
            bias = bias + learning_rate * (y[i] - theta * x[i] - bias)
        print('theta: {}; bias: {}'.format(theta, bias))
    print('theta: {}; bias: {}'.format(theta, bias))
    return theta, bias

def batch_gd(x, y, theta, bias, learning_rate, iter_num):
    # iteration
    for count in range(iter_num):
        th = 0
        bi = 0
        # single step
        for i in range(len(x)):
            th += (y[i] - theta * x[i] - bias) * x[i]
            bi += (y[i] - theta * x[i] - bias)
        theta = theta + learning_rate * th
        bias = bias + learning_rate * bi
        print('theta: {}; bias: {}'.format(theta, bias))
    return theta, bias

def plotshow(x, y, theta, bias, method):
    xd = np.arange(0, 1, 0.005)
    yd = theta * xd + bias
    plt.scatter(x, y, c='g', alpha=0.5)
    plt.plot(xd, yd, c='r')
    plt.title(method)
    plt.show()
    

def pipeline():
    x, y = loadData('./dataset.txt')
    # y = theta * x + bias

    # initialize parameters
    theta = 0
    bias = 0
    learning_rate = 0.0001
    iter_num = 2000

    method = input('please input method: ')
    if method == 'sgd':
        theta, bias = sgd(x, y, theta, bias, learning_rate, iter_num)
    elif method == 'bgd':
        theta, bias = batch_gd(x, y, theta, bias, learning_rate, iter_num)

    plotshow(x, y, theta, bias, method)
    
if __name__ == '__main__':
    pipeline()