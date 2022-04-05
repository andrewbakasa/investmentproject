# imports
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def get_vla(x, y):
    # generate random data-set
    # np.random.seed(0)
    # x = [] #parameter var #np.random.rand(100, 1)
    # y = [] # npvc #2 + 3 * x + np.random.rand(100, 1)

    # model initialization
    regression_model = LinearRegression()
    # fit the data(train the model)
    regression_model.fit(x, y)
    
    # predict
    y_predicted = regression_model.predict(x)

    # model evaluation
    rmse = mean_squared_error(y, y_predicted)
    r2 = r2_score(y, y_predicted)

    # printing values
    print('The coefficient is {}'.format(regression_model.coef_))
    print('The intercept is {}'.format(regression_model.intercept_))
    print('Root mean squared error of the model is {}.'.format(rmse))
    print('R-squared score is {}.'.format(r2))
    return regression_model.coef_, regression_model.intercept_


class PerformanceMetrics:
    """Defines methods to evaluate the model
    Parameters
    ----------
    y_actual : array-like, shape = [n_samples]
            Observed values from the training samples
    y_predicted : array-like, shape = [n_samples]
            Predicted values from the model
    """

    def __init__(self, y_actual, y_predicted):
        self.y_actual = y_actual
        self.y_predicted = y_predicted

    def compute_rmse(self):
        """Compute the root mean squared error
        Returns
        ------
        rmse : root mean squared error
        """
        return np.sqrt(self.sum_of_square_of_residuals())

    def compute_r2_score(self):
        """Compute the r-squared score
            Returns
            ------
            r2_score : r-squared score
            """
        # sum of square of residuals
        ssr = self.sum_of_square_of_residuals()

        # total sum of errors
        sst = np.sum((self.y_actual - np.mean(self.y_actual)) ** 2)

        return 1 - (ssr / sst)

    def sum_of_square_of_residuals(self):
        return np.sum((self.y_actual - self.y_predicted) ** 2)


class LinearRegressionUsingGD:
    """Linear Regression Using Gradient Descent.
    Parameters
    ----------
    eta : float
        Learning rate
    n_iterations : int
        No of passes over the training set
    Attributes
    ----------
    w_ : weights/ after fitting the model
    cost_ : total error of the model after each iteration
    """

    def __init__(self, eta=0.05, n_iterations=1000):
        self.eta = eta
        self.n_iterations = n_iterations

    def fit(self, x, y):
        """Fit the training data
        Parameters
        ----------
        x : array-like, shape = [n_samples, n_features]
            Training samples
        y : array-like, shape = [n_samples, n_target_values]
            Target values
        Returns
        -------
        self : object
        """

        self.cost_ = []
        self.w_ = np.zeros((x.shape[1], 1))
        m = x.shape[0]

        for _ in range(self.n_iterations):
            y_pred = np.dot(x, self.w_)
            residuals = y_pred - y
            gradient_vector = np.dot(x.T, residuals)
            self.w_ -= (self.eta / m) * gradient_vector
            cost = np.sum((residuals ** 2)) / (2 * m)
            self.cost_.append(cost)
        return self

    def predict(self, x):
        """ Predicts the value after the model has been trained.
        Parameters
        ----------
        x : array-like, shape = [n_samples, n_features]
            Test samples
        Returns
        -------
        Predicted value
        """
        return np.dot(x, self.w_)

import numpy as np
#from numpy import *
#import numpy.linalg as linalg
#import scipy.optimize as optimize
def loss(x, w, t):
    N, D = np.shape(x)
    y = np.matmul(x,w)
    loss = (y - t)
    return loss

def cost(x,w, t):
    '''
    Evaluate the cost function in a vectorized manner for 
    inputs `x` and targets `t`, at weights `w1`, `w2` and `b`.
    '''
    N, D = np.shape(x)
    return (loss(x, w,t) **2).sum() / (2.0 * 5)
def getGradient(x, w, t):
    N, D = np.shape(x)
    gradient = (2) * np.matmul(x.T, loss(x,w,t))
    return gradient

def getGradient(x, w, t):
    N, D = np.shape(x)
    gradient = (1.0/ float(N)) * np.matmul(np.transpose(x), loss(x,w,t))
    return gradient


def gradientDescentMethod(x, t, alpha=0.1, tolerance=1e-2):
    N, D = np.shape(x)
    #w = np.random.randn(D)
    w = np.zeros([D])
    # Perform Gradient Descent
    iterations = 1
    w_cost = [(w, cost(x,w, t))]
    while True:
        dw = getGradient(x, w, t)
        w_k = w - alpha * dw
        w_cost.append((w, cost(x, w, t)))
        # Stopping Condition
        if np.sum(abs(w_k - w)) < tolerance:
            print ("Converged.")
            break
        if iterations % 100 == 0:
            print ("Iteration: %d - cost: %.4f" %(iterations, cost(x, w, t)))
        iterations += 1
        w = w_k
    return  w, w_cost
x = np.array([[1,1,1,1,1],[1,2,4,8,16],[1,3,9,27,81],[1,4,16,64,256],[1,5,25,125,625]])
t = np.array([[5],[31],[121],[341],[781]])
print(gradientDescentMethod(x,t))