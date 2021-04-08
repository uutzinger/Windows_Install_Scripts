#
# Expand this with tensorflow matrix multiplication
#
import numpy as np
import cv2 as cv
import time

npTmp = np.random.random((1024, 1024)).astype(np.float32)
npMat1 = np.stack([npTmp,npTmp],axis=2)
npMat2 = npMat1
npMat3 = npTmp + npTmp*1j
npMat4 = npMat3
cuMat1 = cv2.cuda_GpuMat()
cuMat2 = cv2.cuda_GpuMat()
cuMat1.upload(npMat1)
cuMat2.upload(npMat2)

jit_time = time.time()
_ = cv2.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)
current_time = time.time()

for i in range(100):
   _ = cv2.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)

cuda_time = time.time()

for i in range(100):
   _ = cv2.gemm(npMat1,npMat2,1,None,0,None,1)

cpu_time = time.time()

for i in range(100):
   _ = npMat3 @ npMat4

np_time = time.time()

# CUDA jit compilation
print('CUDA jit compilation time is   : {}'.format((current_time-jit_time)))

# CUDA time
print('CUDA Matrix Multiplication time is   : {}'.format((cuda_time-current_time)/100.0))

# OpenCV Mat Pultiplication
print('OpenCV Matrix Multiplication time is : {}'.format((cpu_time-cuda_time)/100.0))

# NumPy Mat Multiplication
print('NumPy  Matrix Multiplication  time is  : {}'.format((np_time-cpu_time)/100.0))
