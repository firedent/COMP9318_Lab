# https://blog.csdn.net/XiaoXIANGZI222/article/details/55097570
import pandas as pd
import numpy as np


def logistic_regression(data, labels, weights, num_epochs, learning_rate):
    data = np.insert(data, 0, np.ones(data.shape[0]), axis=-1)
    labels = labels.reshape((1, labels.shape[0])).T
    weights = weights.reshape((1, weights.shape[0])).T
    for _ in range(num_epochs):
        dot = np.matmul(data, weights)
        h = 1 / (1 + np.exp(-1 * dot))
        E = h - labels
        weights = weights - learning_rate*np.matmul(data.T, E)
    return weights.reshape((weights.shape[0],))


raw_data = pd.read_csv('./asset/a', sep=',')
labels=raw_data['Label'].values
data=np.stack((raw_data['Col1'].values,raw_data['Col2'].values), axis=-1)
weights = np.zeros(3) # We compute the weight for the intercept as well...
num_epochs = 50000
learning_rate = 50e-5

print(logistic_regression(data, labels, weights, num_epochs, learning_rate))
