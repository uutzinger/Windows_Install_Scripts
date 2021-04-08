# Benchmarks
- [Benchmarks](#benchmarks)
  * [Hardware](#hardware)
    + [GPU](#gpu)
    + [CPU](#cpu)
- [Tensorflow](#tensorflow)
  * [Summary](#summary)
  * [Test Scenarios](#test-scenarios)
  * [Preparation for tensorflow v1 benchmarks](#preparation-for-tensorflow-v1-benchmarks)
    + [Choose which tensorflow version to test](#choose-which-tensorflow-version-to-test)
    + [Run CNN AlexNet test](#run-cnn-alexnet-test)
    + [CNN AlexNet test **Results**](#cnn-alexnet-test---results--)
  * [Preparation tensorflow v2 approach](#preparation-tensorflow-v2-approach)
    + [Conduct the test](#conduct-the-test)
    + [Tensroflow V2 Test **Results**](#tensroflow-v2-test---results--)
- [Numpy with MKL](#numpy-with-mkl)
- [OpenCV with MKL, TTB and CUDA](#opencv-with-mkl--ttb-and-cuda)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Hardware

### GPU
GeForce GTX 960M, compute capability: 5.0  
Core Clock: 1.176GHz  
Device Memory Size: 4.00GiB  
Device Memory Bandwidth: 74.65GiB/s  
Laptop needs some of GPU memory, usually only 2.9GB are available  

### CPU
i7 6700HQ, 2.6 GHz AVX2 4 cores 8 threads  
32Gbyte DDR3 800MHz CL11 

# Tensorflow

## Summary

If you plan to run tensorflow exclusively on the GPU there is no advantage of building your own version compared to downloading the PyPi verison.
On my setup, inference with CUDA is 4 times faster and training 3 times compared to running on CPU. 
On PyPi one can obtain tensorflow and tensorflow-gpu, but there appears to be no difference between them. 
If you plan to train or run models on the CPU, for example because they dont fit into your GPU memory, it is advisable to build your own tensorflow version with all optimzation options enabled.
AVX2 versus AVX instructions set gives about 3-5% performance boost, Eigen inline optimization gives an other 3-6% improvement. 
Intel Math Kernel Library affects training performance the most with a 40% performance increase but does not increase inference performance. 
When you build your own CPU optimized tensorflow version, it is best to enable MKL support which will result in about 10% inference improvement and 50% training improvement compared to installation from PyPi.
If you plan to use both GPU and CPU it is best to enable instruction set optimization and Eigen inline option which will result in about 10-15% performance boost on the CPU. 
Since its not possible to compile with MKL and CUDA support together, the best solution depends on your application.
Interestingly, when CUDA support is enabled, CPU performance also increases; inference is about 15% improved and training 10%.

## Test Scenarios

- pypi tensorflow  
- pypi tensorflow-gpu  
- default config options (AVX, no cuda, no mkl)
- custom avx2  
- custom avx2,  eigen inline  
- custom avx2, mkl  
- custom avx2, mkl, eigen inline  
- custom avx, cuda  
- custom avx2, cuda  
- custom avx2, cuda eigen inline  

## Preparation for tensorflow v1 benchmarks
```
cd C:\tensorflow
git clone https://github.com/tensorflow/benchmarks.git
cd benchmarks
pip3 install portpicker
```

Change benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py to include the following:   
```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
```

### Choose which tensorflow version to test

```
cd where you keep your own tensorflow wheel

# Test custom built
pip3 uninstall tensorflow
pip3 install tensorflow-2.4.1-cp38-cp38-win_amd64.whl

# Test default
pip3 uninstall tensorflow
pip3 install tensorflow --no-cache-dir

# Test default GPU
pip3 uninstall tensorflow-gpu
pip3 install tensorflow-gpu --no-cache-dir
```

### Run CNN AlexNet test

To run on CPU:
```
python benchmarks\scripts\tf_cnn_benchmarks\tf_cnn_benchmarks.py --batch_size=32 --model=alexnet --variable_update=parameter_server --device=cpu --data_format=NHWC
```

To run on GPU:
```
python benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py --model alexnet --batch_size 32  --device=gpu --data_format=NCHW 
```


### CNN AlexNet test **Results**

| Configuration | Proc | Instr | MKL | Eigen | Results [images/second] |
| ------------- | ---- | ----- | --- | ----- | ----------------------- |
| PyPi CPU      | CPU  |       |     |       |  28.99     | numpy 1.19.x
| PyPi GPU      | CPU  |       |     |       |  27.78     | numpy 1.19.x
| Custom CPU    | CPU  | AVX   | N   | N     |  27.63     | numpy 1.20.1 + mkl 
| Custom CPU    | CPU  | AVX2  | N   | N     |  27.61     | numpy 1.20.1 + mkl 
| Custom CPU    | CPU  | AVX2  | N   | Y     |  29.36     | numpy 1.20.1 + mkl 
| Custom CPU    | CPU  | AVX2  | Y   | Y     |  **39.49** | numpy 1.20.1 + mkl 
| Custom CPU    | CPU  | AVX2  | Y   | N     |  **39.58** | numpy 1.20.1 + mkl 
| Custom GPU    | CPU  | AVX   | N   | N     |  28.96     | numpy 1.20.1 + mkl
| Custom GPU    | CPU  | AVX2  | N   | N     |  28.30     | numpy 1.20.1 + mkl
| Custom GPU    | CPU  | AVX2  | N   | Y     |  29.57     | numpy 1.20.1 + mkl
| PyPi CPU      | GPU  |       |     |       | 235.08     | numpy 1.19.x
| PyPi GPU      | GPU  |       |     |       | **235.82** | numpy 1.19.x
| Custom GPU    | GPU  | AVX   | N   | N     | 233.48     | numpy 1.20.1 + mkl
| Custom GPU    | GPU  | AVX2  | N   | N     | 233.07     | numpy 1.20.1 + mkl
| Custom GPU    | GPU  | AVX2  | N   | Y     | 232.68     | numpy 1.20.1 + mkl

## Preparation for tensorflow v2 approach

For v2 I used https://pypi.org/project/ai-benchmark/ . It states that for inference testing you need 2GB memory and for training 4GB. 
However with 3GB available RAM not all inference tests can complete. 
Close all unnecessary programs and windows before running the benchmark. 
Reducing screen resolution on notbook computer might help to free more GPU memory.

Install the benchmark:  
```
pip3 install ai-benchmark
```

Example preparations for tensorflow:  
```
# PyPi default
pip3 install tensorflow --no-cache-dir
pip3 uninstall tensorflow

# PyPi default CUDA
pip3 install tensorflow-gpu --no-cache-dir
pip3 uninstall tensorflow

# Install custom built
cd where you keep your custom tensorflow wheel
pip3 uninstall tensorflow
pip3 install tensorflow-2.4.1-cp38-cp38-win_amd64.whl
```

### Conduct the test
Some of the older GPUs and noteboook computers dont run all the tests of the ai-benchmark. 
I edited config.py in the ai-benchmark folder and disableed ```Test 7, 8, 12, 15``` by commenting out the lines ```Test(test_id...)```.

Testing CPU version:
```
py -3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from ai_benchmark import AIBenchmark
benchmark = AIBenchmark(use_CPU=True)
results = benchmark.run()
```
Testing GPU version:
```
py -3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
from ai_benchmark import AIBenchmark
benchmark = AIBenchmark()
results = benchmark.run()
```

### Tensroflow V2 Test **Results**

Test configurations:  

|  | Source   | MKL     | AVX2    | Eigen Inline | Cuda  | run on |
| -|  ------- | ------- | ------- | ------------ | ----- | ------ |
| 1| PyPi     | No      | unknown | unknown      | Yes   | CPU    |
| 2| PyPi GPU | No      | unknown | unknown      | Yes   | CPU    |
| 3| Custom   | No      | AVX     | No           | No    | CPU    |
| 4| Custom   | No      | AVX     | No           | Yes   | CPU    |
| 5| Custom   | No      | AVX2    | No           | No    | CPU    |
| 6| Custom   | No      | AVX2    | No           | Yes   | CPU    |
| 7| Custom   | No      | AVX2    | Yes          | No    | CPU    |
| 8| Custom   | No      | AVX2    | Yes          | Yes   | CPU    |
| 9| Custom   | Yes     | AVX2    | Yes          | No    | CPU    |
|10| Custom   | Yes     | native  | No           | No    | CPU    |
|11| PyPi     | No      | unknown | unknown      | Yes   | GPU    |
|12| PyPi GPU | No      | unknown | unknown      | Yes   | GPU    |
|13| Custom   | No      | AVX     | No           | Yes   | GPU    |
|14| Custom   | No      | AVX2    | No           | Yes   | GPU    |
|15| Custom   | No      | AVX2    | Yes          | Yes   | GPU    |

Higher Score is better (Inference, Training, Ai) . Lower time is better. For explanation of the tests: https://ai-benchmark.com/tests.html . i stands for inference, t for training.

|  | Inference | Training | AI   | 1-i | 1-t  |  2-i | 2-t  | 3-i  | 3-t  | 4-i  | 4-t  | 5-i  | 5-t  | 6-i  | 6-t  | 9-i  | 9-i   | 9-t   | 10-i | 10-i | 10-t  | 11-i | 11-i  | 11-t  | 13-i | 13-t | 14-i | 14-t | 16-i | 16-t | 17-i |  17-t |  18-i |  18-t | 19-i | Configuration                          |
|- | --------- | -------- | ---- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ----  | ----  | ---- | ---- | ----  | ---- | ----  | ----  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ----  | ----  | ----  | ---- | -------------------------------------- |
| 1| 380       | 390      | 770  | 701 | 3242 | 1379 | 7320 | 1523 | 7346 | 1935 | 9742 | 1125 | 4851 | 1938 | 7616 | 7277 | 10744 | 25607 | 4699 | 4151 | 10960 | 7660 | 11868 | 13717 | 3756 | 3996 | 2525 | 5900 | 4134 | 4867 | 3383 |  9102 | 24438 | 24574 | 1195 | PyPi default - CPU                     |
| 2| 378       | 391      | 769  | 715 | 3134 | 1457 | 7380 | 1458 | 7156 | 1876 | 9559 | 1112 | 4864 | 1774 | 7450 | 6900 | 10189 | 25401 | 5482 | 4965 | 11391 | 7730 | 12027 | 14758 | 3571 | 3892 | 2356 | 5682 | 4276 | 4981 | 3640 |  8796 | 26037 | 25427 | 2021 | PyPi GPU - CPU                         |
| 3| 373       | 376      | 749  | 703 | 3325 | 1437 | 7615 | 1498 | 7754 | 1956 | 9626 | 1288 | 4870 | 1925 | 7806 | 6456 |  9378 | 25607 | 5393 | 4815 | 11453 | 7330 | 11397 | 14537 | 4036 | 4195 | 2820 | 6621 | 4420 | 5001 | 3670 |  9043 | 26151 | 26877 | 1817 | Custom CPU - CPU - AVX                 |
| 4| 442       | 421      | 863  | 738 | 3299 | 1381 | 7352 | 1499 | 7270 | 1873 | 7110 | 1065 | 4286 | 1561 | 6822 | 4032 |  6336 | 21411 | 3780 | 3605 |  9836 | 6174 |  9637 | 13357 | 3285 | 3591 | 2250 | 5328 | 3761 | 4852 | 3222 |  8575 | 24175 | 26083 | 1918 | Custom GPU - CPU - AVX                 |
| 5| 390       | 393      | 783  | 690 | 3262 | 1444 | 7455 | 1546 | 7450 | 1897 | 8916 | 1113 | 4651 | 1718 | 7464 | 6788 | 10028 | 26450 | 4741 | 4218 | 11056 | 7176 | 11462 | 14269 | 4005 | 3816 | 2587 | 6154 | 3908 | 4839 | 3348 |  8316 | 24882 | 25111 | 1834 | Custom CPU - CPU - AVX2                |
| 6| 445       | 426      | 871  | 719 | 3248 | 1412 | 7290 | 1505 | 6877 | 1805 | 6996 | 1005 | 4521 | 1630 | 6915 | 4363 |  7032 | 22868 | 3730 | 3431 | 10291 | 6059 |  9391 | 13488 | 3292 | 3525 | 2172 | 5166 | 3869 | 4545 | 3158 |  7855 | 24208 | 24186 | 1721 | Custom GPU - CPU - AVX2                |
| 7| 402       | 416      | 818  | 738 | 3258 | 1385 | 7241 | 1482 | 6986 | 1888 | 8068 | 1155 | 4644 | 1642 | 6996 | 6537 |  9755 | 23118 | 4342 | 3929 | 10154 | 7140 | 11064 | 13221 | 3482 | 3662 | 2332 | 5683 | 4071 | 4725 | 3520 |  8224 | 23609 | 23285 | 1747 | Custom CPU - CPU - AVX2 - Inline       |
| 8| 449       | 428      | 877  | 680 | 3063 | 1331 | 7065 | 1440 | 6810 | 1768 | 7029 | 1026 | 4458 | 1593 | 6825 | 3884 |  6154 | 21234 | 3723 | 3260 | 10056 | 6311 |  9837 | 13316 | 3324 | 3426 | 2356 | 5617 | 3693 | 4541 | 3545 |  8591 | 25005 | 24571 | 1772 | Custom GPU - CPU - AVX2 - Inline       |
| 9| 412       | 598      | 1010 | 613 | 1729 | 1344 | 4758 | 1461 | 5086 | 2277 | 5422 |  982 | 3218 | 1623 | 5320 | 3456 |  5419 |  9628 | 5174 | 4576 |  8764 | 8825 | 13538 |  9101 | 3524 | 2982 | 2716 | 7538 | 5770 | 4012 | 3168 |  3756 | 15082 | 15536 | 2354 | Custom CPU - CPU - AVX2 - Inline - MKL | 
|10| 413       | 594      | 1007 | 606 | 1848 | 1507 | 4637 | 1402 | 5061 | 2386 | 5272 |  958 | 3251 | 1522 | 5210 | 3342 |  5332 |  9326 | 4845 | 4387 |  8528 | 8881 | 13645 |  8811 | 3343 | 2976 | 2686 | 7762 | 5893 | 4484 | 3459 |  3897 | 14574 | 15479 | 2520 | Custom CPU - CPU - native - MKL        | 
|11| 1609      | 1613     | 3217 | 227 | 1386 |  421 | 1589 |  440 | 1699 |  575 | 1775 |  298 |  978 |  420 | 1442 |  831 |  2855 |  2892 |  881 |  999 |  1610 |  916 |  1863 |  1321 |  869 | 1280 |  717 | 1573 | 1015 | 1195 | 2769 | 15485 |  2460 |  6790 |  750 | PyPi default - CUDA                    |
|12| 1602      | 1608     | 3210 | 225 | 1384 |  422 | 1588 |  442 | 1686 |  578 | 1780 |  298 |  978 |  421 | 1452 |  831 |  2855 |  2737 |  884 |  996 |  1611 |  915 |  1866 |  1318 |  867 | 1276 |  712 | 1580 | 1018 | 1194 | 2787 | 16456 |  2465 |  7046 |  754 | PyPi GPU - CUDA                        |
|13| 1604      | 1620     | 3224 | 223 | 1337 |  420 | 1571 |  440 | 1688 |  577 | 1791 |  297 |  972 |  415 | 1461 |  831 |  2856 |  2892 |  888 | 1000 |  1617 |  914 |  1864 |  1238 |  871 | 1299 |  709 | 1554 | 1013 | 1197 | 2703 | 15688 |  2569 |  6912 |  759 | Custom GPU - CUDA - AVX                |
|14| 1605      | 1610     | 3215 | 228 | 1346 |  412 | 1576 |  438 | 1699 |  582 | 1805 |  297 |  973 |  413 | 1449 |  831 |  2865 |  2897 |  885 | 1001 |  1620 |  913 |  1871 |  1318 |  872 | 1302 |  705 | 1557 | 1015 | 1214 | 2722 | 15794 |  2501 |  6748 |  751 | Custom GPU - CUDA - AVX2               |
|15| 1608      | 1617     | 3225 | 224 | 1346 |  419 | 1569 |  439 | 1697 |  578 | 1782 |  296 |  974 |  415 | 1456 |  831 |  2855 |  2890 |  886 | 1000 |  1621 |  914 |  1862 |  1319 |  871 | 1305 |  703 | 1544 | 1015 | 1203 | 2692 | 15550 |  2508 |  6651 |  752 | Custom GPU - CUDA - AVX2 - Inline      |

# Numpy with MKL

Obtain numpy with mkl from https://www.lfd.uci.edu/~gohlke/pythonlibs/.
Obtain regular numpy from PyPi.

Run numpytest.py from https://gist.github.com/markus-beuckelmann

|                | M\*M   | v\*v   | SVD    | Cholesky | eig    |
| -              | ------ | ------ | ------ | -------- | ------ |
|                | 4096^2 | 524288 | 2048^2 | 2048^2   | 2048^2 |
| PyPi numpy     | 1.19   | 0.29   | 1.69   | 0.17     | 8.93   |  
| Numpy with MKL | 1.15   | 0.25   | 0.59   | 0.15     | 6.49   |

Singular Value Decomposition and Eigen value analysis is significnatly faster while "normal" multiplications are not.

# OpenCV with MKL, TTB and CUDA

https://www.renatocandido.org/2019/05/pure-python-vs-numpy-vs-tensorflow-performance-comparison/
