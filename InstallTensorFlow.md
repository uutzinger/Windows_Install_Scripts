# Compiling TensorFlow on Windows 10

- [Compiling TensorFlow on Windows 10](#compiling-tensorflow-on-windows-10)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisites](#pre-requisites)
  * [Obtaining TensorFlow Source](#obtaining-tensorflow-source)
  * [Install bazel](#install-bazel)
  * [Uninstalling of Previous Installations](#uninstalling-of-previous-installations)
  * [Preparing your MSYS Build Environment](#preparing-your-msys-build-environment)
  * [Configure tensorflow](#configure-tensorflow)
  * [Build tensorflow](#build-tensorflow)
  * [Build pip Package](#build-pip-package)
  * [Install the Package](#install-the-package)
  * [Test installation](#test-installation)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Motivation

## Approach

Many online posts have been consulted for this document.
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
```

Tensorflow needs numpy, keras-applications, keras-preprocessing, pip, six, wheel, mock. Numpy should already be installed and using Intel mkl.

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
cd tensorflow
git checkout v2.2.0
```

## Install bazel

Check _TF_MIN_BAZEL_VERSION in configure.py of TensorFlow. For tf 2.2.0 it is min version is 2.0.0.  

* Download the min_version of bazel https://github.com/bazelbuild/bazel/releases/download/2.0.0/bazel-2.0.0-windows-x86_64.exe
* Rename the downloaded version to bazel.exe. 
* Copy it to C:\tensorflow\bin.

## Uninstalling of Previous Installations

To make sure python finds your build you will want to remove any other installation of opencv.
```
pip3 uninstall tensorflow
pip3 uninstall tensorflow-gpu
```

## Preparing your MSYS Build Environment

We will be using MSYS. CMD has issues with number of characters in commands.

```
C:\msys64\msys2_shell.cmd
```
```
cd C:/tensorflow/tensorflow
```

In MSYS shell execute:

```
# Use Unix-style with ':' as separator
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"
export PATH="/c/tensorflow/bin:$PATH" # where bazel is located
export PATH="/c/Python36:$PATH"       # where python is located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/bin:$PATH" # CUDA libraries are located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/extras/CUPTI/libx64:$PATH"
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/include:$PATH"
```

?? set PATH=%PATH%;output_dir\external\mkl_windows\lib  

## Configure tensorflow

```
py -3 ./configure.py
```

```
accept default locations for python
no ROCm support
yes CUDA
cumpute capabilities 5.0
/arch:AVX2
default for rest
```

## Build tensorflow

```
bazel build --config=opt --config=mkl --config=cuda --define=no_tensorflow_py_deps=true --copt=-nvcc_options=disable-warnings //tensorflow/tools/pip_package:build_pip_package
```

bazel build --config = opt --config = cuda --define = no_tensorflow_py_deps = true --copt = -nvcc_options = disable-warnings // tensorflow / tools / pip_package: build_pip_package

./bazel build --output_base=output_dir build --config=opt --config=mkl --config=cuda --define=no_tensorflow_py_deps=true --copt=-nvcc_options=disable-warnings //tensorflow/tools/pip_package:build_pip_package

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

.\bazel-bin\tensorflow\tools\pip_package\build_pip_package C:\tensorflow\whl

## Clean up
%UserProfile%_bazel_%UserName%folder (for example C:\Users\Kurozumi_bazel_Kurozumi)

## Install the Package

pip install C:\temp\path_to_save_wheel\<wheel_name.whl>
pip install g:\tensorflow_pkg\tensorflow-2.2.0rc0-cp38-cp38-win_amd64.whl

## Test installation

Start python ```py -3``` Enter the following commands on command prompt:
```
import tensorflow as tf 
print(tf.test.is_built_with_cuda())
pprint(tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None))
print(tf.pywrap_tensorflow.IsMklEnabled())
```
python -c "import tensorflow as tf; print(tf.__version__); print(tf.keras.__version__)"
python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"