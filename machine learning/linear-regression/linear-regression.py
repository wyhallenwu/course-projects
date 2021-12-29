import numpy as np
import matplotlib.pyplot as plt
import time

# dataloader: extract data from dataset
def loadData(filename):
    data = np.genfromtxt(filename)
    print(data.shape)
    x = data[:, 1]
    y = data[:, 2]
    return x, y

# depict the data
def dataPlot(filename):
    x, y = loadData(filename)    
    p = plt.figure()
    plt.scatter(x, y, c='g', alpha=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("dataset")
    plt.show()

# gradient descent iteration
def gradient_descent_iter(x, y):
    # define hyperparameter
    learning_rate = 0.001
    iter_num = 10000
    m = 0
    b = 0
    num = len(x)
    # iteration 
    for i in range(iter_num):
        totalError = compute_total_error(x, y, m, b)
        # uptate parameters m, b
        m, b = step_gradient_descent(m, b, learning_rate, x, y)
    return m, b

# compute the error using MSE, return float
def compute_total_error(x, y, current_m, current_b):
    totalError = 0
    for i in range(len(x)):
        totalError += (y[i] - (current_m * x[i] + current_b)) ** 2
    return totalError / float(len(x))

# single step of gradient descent, return steped_m and steped_b
def step_gradient_descent(current_m, current_b, learning_rate, x, y):
    m_gradient = 0
    b_gradient = 0
    N = float(len(x))
    for i in range(len(x)):
        b_gradient += -(2 / N) * (y[i] - (current_m * x[i] + current_b))
        m_gradient += -(2 / N) * x[i] * (y[i] - ((current_m * x[i]) + current_b))
    step_m = current_m - (learning_rate * m_gradient)
    step_b = current_b - (learning_rate * b_gradient)
    return step_m, step_b

# a decorator to count time
def get_exec_time(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()
        print("consuming time: {}s".format(end - start))
        # return fn(*args, **kwargs)  if add this, it will execute two times
    return wrapper


# the training pipeline of linear regression
@get_exec_time
def gradient_run(filename):
    print("running...")
    x, y = loadData(filename)
    m, b = gradient_descent_iter(x, y)
    print("the coefficient is: {:.2f} \nthe bias is: {:.2f}".format(m, b))
    xd = np.arange(0, 1, 0.005)
    yd = m * xd + b
    plt.scatter(x, y, c='g', alpha=0.5)
    plt.plot(xd, yd, c='r')
    plt.show()


if __name__ == '__main__':
    # dataPlot('linear-regression/dataset.txt')
    gradient_run('linear-regression/dataset.txt')
     