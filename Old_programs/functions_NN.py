import random
import numpy as np

def create_t_and_t(num, stock_array, spy_array):
    '''Creates the input for a NN x_,y_traing and x_,y_test. right now randomly selects from 80% sampling instead of a single run through all -- could change'''
    x_train = np.zeros((num, 14))
    y_train = np.zeros(num)
    x_test = np.zeros((len(stock_array) - int(len(stock_array)*.8), 14))
    y_test = np.zeros(len(stock_array) - int(len(stock_array)*.8))



    for i in range(num):
        random_num = random.randint(0, int(len(stock_array)*.8) - 8)
        x_train[i, :7] = spy_array[random_num:random_num + 7]
        x_train[i, 7:14] = stock_array[random_num:random_num + 7]
        if (stock_array[random_num+8] > 0.0): 
            y_train[i] = 1
        else:
            y_train[i] = 0
    for i in range(int(len(stock_array) *.8), len(stock_array)):
        k = i - int(len(stock_array) *.8)
        x_test[k, :7] = spy_array[k:k + 7]
        x_test[k, 7:14] = stock_array[k:k + 7]
        if (stock_array[k+8] > 0.0): 
            y_test[k] = 1
        else:
            y_test[k] = 0
    return x_train, y_train, x_test, y_test

