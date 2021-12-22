import numpy as np
import matplotlib.pyplot as plt
""" 
this version only uses numpy and matplotlib
there will be a verison use sklearn
 """

# dataloader
def loadData(filename):
    data = np.genfromtxt(filename)
    print(data.shape)
    x = data[:, :2]
    y = data[:, 2]
    return x, y

def dataPlot(filename):
    x, y = loadData(filename)    
    p = plt.figure()
    plt.scatter(x[:, 1], y, c='g', alpha=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def linear_regression(x, y):
    # use generator
    x_data = (x_i for x_i in x)
    y_data = (y_i for y_i in y)
    
    pass



if __name__ == '__main__':
    dataPlot('linear-regression/dataset.txt')
            