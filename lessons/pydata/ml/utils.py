from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from numpy.linalg import pinv
import numpy as np


class PolynomialRegression:
    def __init__(self, degree):
        self.model = make_pipeline(
            PolynomialFeatures(degree), LinearRegression())

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)


class SimpleSolver():
    def __init__(self):
        self.w = None

    def fit(self, X, y):
        pinvx = pinv(X)
        self.w = np.dot(pinvx, y)
        return self

    def predict(self, X):
        return np.dot(X, self.w)


class SimpleRegressor:
    def __init__(self, C=0, beta=2.0):
        # self.model = make_pipeline(PolynomialFeatures(degree), SimpleSolver())
        self.C = C
        self.beta = beta
        self.w = None
        self.centroids = None

    def comp_h(self, X):
        C = np.expand_dims(self.centroids, -1)
        # print(C.shape)
        # print(X.shape)
        H = np.transpose(C - np.transpose(X))  # kazdej s kazdym
        H = np.exp(- self.beta * (H**2).sum(axis=1))
        return H

    def fit(self, X, y):
        self.centroids = np.array(X)  # prijede dataframe
        H = self.comp_h(np.array(X))
        H[np.diag_indices_from(H)] += self.C
        self.w = np.dot(pinv(H), y)
        print(self.w)
        return self

    def predict(self, X):
        H = self.comp_h(np.array(X))
        return np.dot(H, self.w)
