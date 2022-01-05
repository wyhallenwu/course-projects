import numpy as np
import matplotlib.pyplot as plt


def loadDataSet(fileName):
    f = open('machine learning/linear-regression/dataset.txt')
    numFeatures = len(f.readline().split('\t')) - 1         # 除去y那一列，即是特征的数量
    xArr = []
    yArr = []
    fr = open('machine learning/linear-regression/dataset.txt')
    for line in fr.readlines():
        xLine = []  # 由于x有多个特征{x0,x1}，读取每一行后都先初始化并重新保存当前样本行的
        curline = line.strip().split('\t')  # 当前读取的行，根据空格分割.strip()可以移除首尾的'\t' '\n'
        for i in range(numFeatures):
            xLine.append(float(curline[i]))    # 保存当前样本行的x0 x1;注意需要将string格式转化为float形
        xArr.append(xLine)
        yArr.append(float(curline[-1]))    # y的值是每行最后一个；需要将string格式转化为float形
    f.close()
    fr.close()
    return xArr,yArr


def lwlr(xTest,xArr,yArr,k = 0.1):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).T
    n = np.shape(xArr)[0]      # number of data pairs
    yPredict = np.zeros(n)
    # compute w and theta for each point
    for point in range(n):

        w = np.mat(np.eye((n)))           # weight matrix

        # 计算该点的权重矩阵
        for i in range(n):
            difMat = xTest[point,:] - xMat[i,:]
            w[i,i] = np.exp(difMat * difMat.T / (-2 * k * k))

        # 计算最优的参数theta
        xTwx = xMat.T * (w * xMat)
        if np.linalg.det(xTwx) == 0:
            print('sigular matrix cant get inverse')
            return
        theta = xTwx.I * (xMat.T * (w * yMat))
        yPredict[point] = xTest[point,:] * theta        # predictions

    return yPredict


def plotLWLR(xArr,yArr,xTest,yPredict1,yPredict2,yPredict3):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr)
    srtIdx = xTest[:, 1].argsort(0)
    xSort = xTest[srtIdx][:,0,:]

    fig, axs = plt.subplots(nrows=3, ncols=1, sharex=False, sharey=False, figsize=(10, 8))
    axs[0].plot(xSort[:, 1], yPredict1[srtIdx], c='red')  
    axs[1].plot(xSort[:, 1], yPredict2[srtIdx], c='red')  
    axs[2].plot(xSort[:, 1], yPredict3[srtIdx], c='red')
    axs[0].scatter(xMat[:, 1].flatten().A[0], yMat.flatten().A[0], s=20, c='g', alpha=.5) 
    axs[1].scatter(xMat[:, 1].flatten().A[0], yMat.flatten().A[0], s=20, c='g', alpha=.5)  
    axs[2].scatter(xMat[:, 1].flatten().A[0], yMat.flatten().A[0], s=20, c='g', alpha=.5)  
    axs0_title_text = axs[0].set_title(u'LWLR,k=1.0')
    axs1_title_text = axs[1].set_title(u'LWLR,k=0.01')
    axs2_title_text = axs[2].set_title(u'LWLR,k=0.003')
    plt.setp(axs0_title_text, size=8, weight='bold', color='red')
    plt.setp(axs1_title_text, size=8, weight='bold', color='red')
    plt.setp(axs2_title_text, size=8, weight='bold', color='red')
    plt.xlabel('X')
    plt.show()

def pipeline(filename):
    xArr ,yArr = loadDataSet(filename)
    xMat = np.mat(xArr)
    yP1 = lwlr(xMat,xArr,yArr,k=1)
    yP2 = lwlr(xMat,xArr,yArr,k=0.01)
    yP3 = lwlr(xMat,xArr,yArr,k=0.003)
    plotLWLR(xArr,yArr,xMat,yP1,yP2,yP3)

if __name__ == '__main__':
    pipeline('machine learning/linear-regression/dataset.txt')