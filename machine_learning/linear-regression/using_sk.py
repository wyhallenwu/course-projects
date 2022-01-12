import matplotlib.pyplot as plt
from numpy import *
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


def loadDataSet(filename):      
    data = np.genfromtxt(filename)
    x = data[:, 0:2]
    y = data[:, 2]
    return x, y

if __name__ =='__main__':
    dataX, dataY =loadDataSet('./dataset.txt')
    matX=mat(dataX);matY=mat(dataY).T #将数据保存到矩阵中
    regr = linear_model.LinearRegression()  #生成线性回归模型
    regr.fit(dataX, dataY)
    #填充训练数据 matX(n_samples,n_features);matY(n_samples,n_targets)

    xCopy = matX.copy()
    xCopy.sort(0)
    predictY = regr.predict(xCopy) #得到模型预测值

    plt.scatter(matX[:,1].flatten().A[0],matY[:,0].flatten().A[0],s=20,color='green',alpha=.5) #绘制散点图
    plt.plot(xCopy[:,1],predictY,color='red',linewidth=1) #绘制最佳拟合直线
 
    plt.xticks(())
    plt.yticks(())

    plt.show()
