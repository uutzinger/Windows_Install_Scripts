# Compiling TensorFlow on Windows 10 with CUDA

- [Compiling TensorFlow on Windows 10 with CUDA](#compiling-tensorflow-on-windows-10-with-cuda)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisites](#pre-requisites)
  * [Obtaining TensorFlow Source](#obtaining-tensorflow-source)
  * [Install bazel](#install-bazel)
  * [Uninstalling of previous Installations](#uninstalling-of-previous-installations)
  * [Preparing your MSYS Build Environment](#preparing-your-msys-build-environment)
  * [Configure tensorflow](#configure-tensorflow)
  * [Build tensorflow](#build-tensorflow)
  * [Build pip Package](#build-pip-package)
  * [Install the Package](#install-the-package)
  * [Test Installation](#test-installation)
  * [Cleanup](#cleanup)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Motivation
Tensorflow supports CUDA 10.1. If you installed the latest CUDA version which is 10.2 you either add 10.1 or build tensorflow with latest CUDA support. By building it you can enable CUDA and AVX support. I dont know if you can have both MKL and CUDA support built into one distribution.

## Approach

The following online posts have been consulted for this document.
* [1] https://dev.infohub.cc/build-tensorflow-220rc0-gpu/
* [2] https://www.tensorflow.org/install/source_windows
* [3] https://software.intel.com/content/www/us/en/develop/articles/intel-optimization-for-tensorflow-installation-guide.html

## Background Reading

## Pre-Requisites

* Prepare your system with https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md. The goal is to install CUDA and cuDN.
* Install MSYS2 https://github.com/msys2/msys2-installer/releases/download/2020-05-22/msys2-x86_64-20200522.exe
* Add C:\msys64\usr\bin to PATH

Start shell with ```C:\msys64\msys2_shell.cmd```

Update packages
```
pacman -Syu
# Restart the console 

# Introduce required packages in newly opened console
pacman -Su
pacman -S git patch unzip
exit
```

Tensorflow needs numpy, keras-applications, keras-preprocessing, pip, six, wheel, mock. Numpy should already be installed. I use the version built with Intel mkl.

```
python -m pip install --upgrade pip
pip install six wheel mock
pip install keras_applications==1.0.8 --no-deps
pip install keras_preprocessing==1.1.0 --no-deps
```

## Obtaining TensorFlow Source

```
mkdir C:/tensorflow
cd C:/tensorflow
git clone https://github.com/tensorflow/tensorflow.git
mkdir output_dir
cd tensorflow
git checkout v2.2.0
```

(or git checkout master)

## Install bazel

Check _TF_MIN_BAZEL_VERSION in configure.py of TensorFlow. For tf 2.2.0 it is min version is 2.0.0.  

* Download the min_version of bazel https://github.com/bazelbuild/bazel/releases/download/2.0.0/bazel-2.0.0-windows-x86_64.exe
* Rename the downloaded version to bazel.exe. 
* Copy it to C:\tensorflow\.

## Uninstalling of previous Installations

To make sure python finds your build you will want to remove any other installation of tensorflow.
```
pip3 uninstall tensorflow
pip3 uninstall tensorflow-gpu
```

## Preparing your MSYS Build Environment

We will be using MSYS. CMD has issues with number of characters in commands.

```
C:\msys64\msys2_shell.cmd
```

Continue working in the MSYS shell

```
cd C:/tensorflow/tensorflow
```

```
# Use Unix-style with ':' as separator
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"
export PATH="/c/tensorflow:$PATH" # where bazel is located
export PATH="/c/Python36:$PATH"       # where python is located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/bin:$PATH" # CUDA libraries are located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/extras/CUPTI/libx64:$PATH"
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/include:$PATH"
export PATH="$PATH:/c/tensorflow/tensorflow/bazel_out/external/mkl_windows/lib" 
```

## Configure tensorflow

It is difficult to run configure in CMD window as the configure script exceeds maximum number of characters for command line. You would need to backup the PATH variable and reduce it to minium.

MSYS shell does not have the problem.

```
py -3 ./configure.py
```

```
accept default locations for python
no ROCm support
yes CUDA
compute capabilities 5.0
/arch:AVX2
use default
```

## Build tensorflow

CUDA Support Option
```
bazel build --config=opt --config=cuda --define=no_tensorflow_py_deps=true --copt=-nvcc_options=disable-warnings //tensorflow/tools/pip_package:build_pip_package
```
When the build gets stuck about 98% through, you will need to reboot and execute the command above again. You will need to have simple_console_for_windows.zip in bazel-out\x64_windows-opt\bin\tensorflow\tools\pip_package. The script gets stuck usually slightly before that archive is built.

MKL Support Option [not tested]
```
bazel build --config=mkl --config=opt //tensorflow/tools/pip_package:build_pip_package
```

The options listed after config are:
```
Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.

        --config=mkl            # Build with MKL support.
        --config=monolithic     # Config for mostly static monolithic build.
        --config=ngraph         # Build with Intel nGraph support.
        --config=numa           # Build with NUMA support.
        --config=dynamic_kernels        # (Experimental) Build kernels into separate shared objects.
        --config=v2             # Build TensorFlow 2.x instead of 1.x.

Preconfigured Bazel build configs to DISABLE default on features:
        --config=noaws          # Disable AWS S3 filesystem support.
        --config=nogcp          # Disable GCP support.
        --config=nohdfs         # Disable HDFS support.
        --config=nonccl         # Disable NVIDIA NCCL support.
```

## Build pip Package

Build pip/whl package in MSYS shell.
```
./bazel-bin/tensorflow/tools/pip_package/build_pip_package pip_package
```

## Install the Package

In regular CMD Window:
```
cd pip_package
pip3 install tensorflow-2.2.0-cp38-cp38-win_amd64.whl
```

## Test Installation

Start python ```py -3``` Enter the following commands on command prompt:
```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
import tensorflow as tf 
print(tf.test.is_built_with_cuda())
print(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
print(tf.__version__)
print(tf.keras.__version__)
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
# print(tf.pywrap_tensorflow.IsMklEnabled()) #this was renamed 
```

Also check out
```
py -3 C:/tensorflow/tensorflow/tensorflow/python/framework/test_util_tests.py
```

## Cleanup
After installing the package you might want to clear the output directories.

```
bazel clean
```

This removes bazel_out, bazel_bin and frees about 17GB of data.
