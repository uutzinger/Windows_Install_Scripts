import numpy as np
from time import time

print('----------------------------------------------------------')
print('This was obtained using the following Numpy configuration:')
np.__config__.show()
print('----------------------------------------------------------')


# Let's take the randomness out of random numbers (for reproducibility)
np.random.seed(0)

size = 4096
A, B = np.random.random((size, size)), np.random.random((size, size))
C, D = np.random.random((size * 128,)), np.random.random((size * 128,))
E = np.random.random((int(size / 2), int(size / 4)))
F = np.random.random((int(size / 2), int(size / 2)))
F = np.dot(F, F.T)
G = np.random.random((int(size / 2), int(size / 2)))

# Matrix multiplication
N = 10
t = time()
for i in range(N):
    np.dot(A, B)

delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (size, size, delta / N))
print('----------------------------------------------------------')
del A, B

# Vector multiplication
N = 5000
t = time()
for i in range(N):
    np.dot(C, D)
delta = time() - t
print('Dotted two vectors of length %d in %0.2f ms.' % (size * 128, 1e3 * delta / N))
print('----------------------------------------------------------')
del C, D

# Singular Value Decomposition (SVD)
N = 20
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print("SVD of a %dx%d matrix in %0.2f s." % (size / 2, size / 4, delta / N))
print('----------------------------------------------------------')
del E

# Cholesky Decomposition
N = 50
t = time()
for i in range(N):
    np.linalg.cholesky(F)
delta = time() - t
print("Cholesky decomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))
print('----------------------------------------------------------')

# Eigendecomposition
N = 3
t = time()
for i in range(N):
    np.linalg.eig(G)
delta = time() - t
print("Eigendecomposition of a %dx%d matrix in %0.2f s." % (size / 2, size / 2, delta / N))
print('----------------------------------------------------------')
print('----------------------------------------------------------')
