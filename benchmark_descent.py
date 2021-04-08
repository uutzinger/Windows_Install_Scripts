#
# https://www.renatocandido.org/2019/05/pure-python-vs-numpy-vs-tensorflow-performance-comparison/
#
# Model y = w_0 + w_1 * x with random data
#
# https://www.guru99.com/linear-regression-tensorflow.html
#

import itertools as it
import time
import timeit

# Linear fit using python
def py_descent(x, d, mu, N_epochs):
    N = len(x)
    f = 2 / N    
    # "Empty" predictions, errors, weights, gradients.
    y = [0] * N
    w = [0, 0]
    grad = [0, 0]
    
    for _ in it.repeat(None, N_epochs):
        # Can't use a generator because we need to
        # access its elements twice.
        err = tuple(i - j for i, j in zip(d, y))
        grad[0] = f * sum(err)
        grad[1] = f * sum(i * j for i, j in zip(err, x))
        w = [i + mu * j for i, j in zip(w, grad)]
        y = (w[0] + w[1] * i for i in x)

    return w

# Linear fit using numpy
def np_descent(x, d, mu, N_epochs):
    d = d.squeeze()
    N = len(x)
    f = 2 / N
 
    y = np.zeros(N)
    err = np.zeros(N)
    w = np.zeros(2)
    grad = np.empty(2)
    
    for _ in it.repeat(None, N_epochs):
        np.subtract(d, y, out=err)                        #
        grad[:] = f * np.sum(err), f * (err @ x)          # @ is dot product or matrix/vectors
        w = w + mu * grad                                 # w[0] is offset, w[1] is slope
        y = w[0] + w[1] * x                               #

    return w

# Linear fit using tensorflow

def tf_descent(X_tf, d_tf, mu, N_epochs):
    N = X_tf.get_shape().as_list()[0]
    f = 2 / N

    w = tf.Variable(tf.zeros((2, 1)), name="w_tf")        # initialize weight
    y = tf.matmul(X_tf, w, name="y_tf")                   # y = w * X matrix multiplication
    e = y - d_tf                                          # error 
    grad = f * tf.matmul(tf.transpose(X_tf), e)           # gradient calculation grad = X * e

    # initialize variables and graph and execute code
    training_op = tf.compat.v1.assign(w, w - mu * grad)   # update appoximation w = w - mu * grad
    init_op = tf.compat.v1.global_variables_initializer() #

    with tf.compat.v1.Session() as sess:
        sess.run(init_op)
        for epoch in range(N_epochs):
            sess.run(training_op)
        opt = w.eval()

    return opt

# Generate Test Data
##########################################################
np.random.seed(444)

N = 10000
sigma = 0.1
noise = sigma * np.random.randn(N)
# `mu` is a step size, or scaling factor.
mu = 0.001
N_epochs = 10000

x = np.linspace(0, 2, N) # x is between 0 and 2 linearly distributed
d = 3 + 2 * x + noise    # desired output with noise

import numpy as np
# We need to prepend a column vector of 1s to `x`.
X = np.column_stack((np.ones(N, dtype=x.dtype), x))

#  Solution to linear fit is:
########################################################### 
Xplus = np.linalg.pinv(X)
w_opt = Xplus @ d
print(w_opt)

# Pure Python Fit
########################################################### 
x_list = x.tolist()
d_list = d.squeeze().tolist()  # Need 1d lists
  
t0 = time.time()
py_w = py_descent(x_list, d_list, mu, N_epochs)
t1 = time.time()
 
print(py_w) 
print('Solve time: {:.2f} seconds'.format(round(t1 - t0, 2)))

# Numpy Fit
########################################################### 
np_w = np_descent(x, d, mu, N_epochs)
print(np_w)

setup = ("from __main__ import x, d, mu, N_epochs, np_descent;"
         ";import numpy as np")
repeat = 5
number = 5  # Number of loops within each repeat
 
np_times = timeit.repeat('np_descent(x, d, mu, N_epochs)', setup=setup,
                         repeat=repeat, number=number)

print(min(np_times) / number)

# Tensorflow Fit
########################################################### 
import tensorflow as tf

# Tensorflow variables
X_tf = tf.constant(X, dtype=tf.float32, name="X_tf")
d_tf = tf.constant(d, dtype=tf.float32, name="d_tf")

tf_w = tf_descent(X_tf, d_tf, mu, N_epochs)
print(tf_w)

setup = ("from __main__ import X_tf, d_tf, mu, N_epochs, tf_descent;"
         "import tensorflow as tf")
 
tf_times = timeit.repeat("tf_descent(X_tf, d_tf, mu, N_epochs)", setup=setup,
                         repeat=repeat, number=number)
 
print(min(tf_times) / number)
