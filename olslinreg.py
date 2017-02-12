import math, os
import numpy as np
from numpy.linalg import pinv, norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

r1train_unix = 'datasets/regression/reg-1d-train.csv'
r1test_unix = 'datasets/regression/reg-1d-test.csv'
r2train_unix = 'datasets/regression/reg-2d-train.csv'
r2test_unix = 'datasets/regression/reg-2d-test.csv'

r1train_w = 'datasets\regression\reg-1d-train.csv'
r1test_w = 'datasets\regression\reg-1d-test.csv'
r2train_w = 'datasets\regression\reg-2d-train.csv'
r2test_w = 'datasets\regression\reg-2d-test.csv'

c1train_unix = 'datasets\classification\cl-train-1.csv'
c1test_unix = 'datasets\classification\cl-test-1.csv'
c2train_unix = 'datasets\classification\cl-train-2.csv'
c2test_unix = 'datasets\classification\cl-test-2.csv'

c1train_w = 'cl-train-1.csv'
c1test_w = 'cl-test-1.csv'
c2train_w = 'cl-train-2.csv'
c2test_w = 'cl-test-2.csv'

def get_dataset(filename):
    """Collects input and output vectors from csv file.
    """
    with open(filename, 'r') as f:
        dataset = [line.rstrip('\n') for line in f]
    X = [[float(num) for num in line.split(',')] for line in dataset]
    y = []
    for vector in X:
        vector.insert(0, 1.0)
        y.append(vector.pop())
    return np.array(X), np.array(y)

def ols(X, y):
    return pinv(X.T @ X) @ X.T @ y

def sigmoid(z):
    return (1.0/(1.0+math.exp(-z)))

def logistic_gd(X, y, Xtest, ytest):
    eta = 0.1
    w = np.zeros(3)
    errs = []
    terrs = []
    for _ in range(1000):
        w = w - eta*dE_ce(X, y, w)
        errs.append(E_ce(X, y, w))
        terrs.append(E_ce(Xtest, ytest, w))
    plot_error(errs, terrs)
    return w

def E_mse(X, y, w):
    return (1/len(y))*norm(X @ w - y)**2

def E_ce(X, y, w):
    e = 0
    for xi, yi in zip(X, y):
        z = h(xi, w)
        e += yi*math.log(sigmoid(z)) + (1 - yi)*math.log(1 - sigmoid(z))
    e *= -(1/len(y))
    return e

def dE_ce(X, y, w):
    dE = np.zeros(3)
    for xi, yi in zip(X, y):
        dE += (sigmoid(h(xi, w)) - yi) * xi
    return dE

def h(x, w):
    return w.T @ x

def classify_z(z):
    return 1 if z > 0 else 0

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def c2p_a(A):
    new = []
    for ai in A:
        r, p = cart2pol(ai[1]-0.5, ai[2]-0.5)
        new.append([1, r, p])
    return np.array(new)

def plot_error(errs, terrs):
    fig, ax = plt.subplots()
    ax.plot([i for i in range(len(errs))], errs, label='Training Data Error')
    ax.plot([i for i in range(len(terrs))], terrs, label='Test Data Error')
    ax.legend(shadow=True)
    plt.savefig("gd_error.png")
    plt.show()

def plot1D(inS0, outS0, inS1, outS1, inP, outP):
    fig, ax = plt.subplots()
    ax.scatter(inS0, outS0, marker='x', label='Training Data')
    ax.scatter(inS1, outS1, marker='x', label='Test Data')
    ax.plot(inP, outP, c='r', label='Hypothesis')
    ax.legend(loc='upper center', shadow=True)
    plt.savefig("1d-linreg.png")
    plt.show()

def d_line(x, w):
    return -(w[0]+w[1]*x)/w[2]

def split(X, y):
    x0 = []
    y0 = []
    x1 = []
    y1 = []
    for xi, yi in zip(X, y):
        if yi == 0:
            x0.append(xi[1])
            y0.append(xi[2])
        else:
            x1.append(xi[1])
            y1.append(xi[2])
    return x0, y0, x1, y1

def plot_class(X, y, Xtest, ytest, w):
    x0, y0, x1, y1 = split(X, y)
    x0t, y0t, x1t, y1t = split(Xtest, ytest)
    d_line_x = [0, 1]
    d_line_y = [d_line(x, w) for x in d_line_x]
    fig, ax = plt.subplots()
    ax.set_ylim([-3.5,3.5])
    ax.scatter(x1, y1, marker='o', c='g', label='Class 1 Train')
    ax.scatter(x0, y0, marker='o', c='r', label='Class 0 Train')
    ax.scatter(x1t, y1t, marker='o', c='#005000', label='Class 1 Test')
    ax.scatter(x0t, y0t, marker='o', c='#500000', label='Class 0 Test')
    ax.plot(d_line_x, d_line_y, 'b--')
    ax.legend(loc='upper center', shadow=True)
    plt.show()


def regression2D():
    X, y = get_dataset('datasets/regression/reg-2d-train.csv')
    Xtest, ytest = get_dataset('datasets/regression/reg-2d-test.csv')
    w = ols(X, y)
    print(w)
    print(E_mse(X, y, w))
    print(E_mse(Xtest, ytest, w))

def regression1D():
    X, y = get_dataset('datasets/regression/reg-1d-train.csv')
    Xtest, ytest = get_dataset('datasets/regression/reg-1d-test.csv')
    w = ols(X, y)
    print(E_mse(X, y, w))
    print(E_mse(Xtest, ytest, w))
    inS = [x[1] for x in X]
    inP = np.array(sorted(inS))
    inS1 = [x[1] for x in Xtest]
    outP = [h(np.array([1, x]), w) for x in inP]
    plot1D(inS, y, inS1, ytest, inP, outP)

def classification1():
    X, y = get_dataset(c1train_w)
    Xtest, ytest = get_dataset(c1test_w)
    w = logistic_gd(X, y, Xtest, ytest)
    plot_class(X, y, Xtest, ytest, w)

def classification2():
    X, y = get_dataset(c2train_w)
    Xtest, ytest = get_dataset(c2test_w)
    X = c2p_a(X)
    Xtest = c2p_a(Xtest)
    w = logistic_gd(X, y, Xtest, ytest)
    plot_class(X, y, Xtest, ytest, w)

def main():
    #regression2D()
    #regression1D()
    classification2()

if __name__ == '__main__':
    main()
