# Compiling TensorFlow on Windows 10 with CUDA

- [Compiling TensorFlow on Windows 10 with CUDA](#compiling-tensorflow-on-windows-10-with-cuda)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisitemsyss](#pre-requisitemsyss)
    + [Configure MSYS](#configure-msys)
    + [Update Python Packages](#update-python-packages)
  * [Obtaining TensorFlow Source](#obtaining-tensorflow-source)
  * [Install bazel](#install-bazel)
  * [Uninstalling of previous Installations](#uninstalling-of-previous-installations)
  * [Preparing your MSYS Build Environment](#preparing-your-msys-build-environment)
  * [Configure tensorflow](#configure-tensorflow)
  * [Build tensorflow](#build-tensorflow)
    + [Setup your command shell](#setup-your-command-shell)
    + [Build tensorflow](#build-tensorflow-1)
    + [MKL Support Option [not tested]](#mkl-support-option--not-tested-)
  * [Build pip wheel](#build-pip-wheel)
  * [Install the pip wheel](#install-the-pip-wheel)
  * [Test Installation](#test-installation)
  * [Cleanup](#cleanup)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Motivation
By building it yourself you can enable lastest CUDA and AVX2 support.

## Approach

The following online posts have been consulted for this document.
* [1] https://dev.infohub.cc/build-tensorflow-220rc0-gpu/
* [2] https://www.tensorflow.org/install/source_windows
* [3] https://software.intel.com/content/www/us/en/develop/articles/intel-optimization-for-tensorflow-installation-guide.html

## Background Reading
NA

## Pre-Requisitemsyss

* Prepare your system with https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md and install CUDA and cuDN.
* Install MSYS2 https://github.com/msys2/msys2-installer/releases/download/2020-11-09/msys2-x86_64-20201109.exe
* Add C:\msys64\usr\bin to PATH

* Make sure you have long path names enabled https://superuser.com/questions/1119883/windows-10-enable-ntfs-long-paths-policy-option-missing
* Make sure you have the appropriate versions of python, cuDNN, CUDA, bazel, gcc as described here: https://www.tensorflow.org/install/source

### Configure MSYS
Start shell with ```C:\msys64\msys2_shell.cmd```   
Update packages   
```
pacman -Syu
```
Restart the console   
Introduce required packages in newly opened console  
```
pacman -Su
pacman -S git patch unzip
exit
```

If your windows username has a space in it, then you need to fix username issue: https://sourceforge.net/p/msys2/discussion/general/thread/76612760/:  
```
/usr/bin/mkpasswd  >  /etc/passwd
```
change user name in first column of /etc/passwd to a name without spaces.

### Update Python Packages
Tensorflow needs numpy, keras-applications, keras-preprocessing, pip, six, wheel, mock. Numpy should already be installed. I use the version built with Intel mkl.
Check for latest version on https://pypi.org/

```
pip3 install --upgrade pip
pip3 install six wheel mock
pip3 install keras_applications==1.0.8 --no-deps
pip3 install keras_preprocessing==1.1.2 --no-deps
```

## Obtaining TensorFlow Source

This runs best in CMD window:  

```
mkdir C:/tensorflow
cd C:/tensorflow
git clone https://github.com/tensorflow/tensorflow.git
mkdir output_dir
cd tensorflow
git checkout v2.4.1
```

## Install bazel

Check _TF_MIN_BAZEL_VERSION in configure.py of TensorFlow.  

* Download the min_version of bazel ```https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-windows-x86_64.exe```
* Rename the downloaded version to bazel.exe. 
* Copy it to C:\tensorflow\tensorflow

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
export PATH="/c/Python36:$PATH"   # where python is located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin:$PATH" # CUDA libraries are located
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/extras/CUPTI/libx64:$PATH"
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/include:$PATH"
export PATH="$PATH:/c/tensorflow/tensorflow/bazel_out/external/mkl_windows/lib" 
```

## Configure tensorflow

It is difficult to run configure in CMD window as the configure script exceeds the maximum number of characters for the command line. You would need to backup the PATH variable and reduce it to minium.

MSYS shell does not have that problem.

Run the following in MSYS:

```
py -3 ./configure.py
```

```
accept default locations for python
ROCm support: select No
CUDA support: select Yes
compute capabilities: type 3.5,5.0,5.2,7.0
optimization flags: type /arch:AVX2
rest of config: use default suggestions
```

The build options listed after above config complted is:
```
Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.
        --config=mkl            # Build with MKL support.
        --config=mkl_aarch64    # Build with oneDNN support for Aarch64.
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

## Build tensorflow

### Setup your command shell
In CMD window:

```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"

"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019

# Dont need these:
# "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
# "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\bin\daalvars.bat" intel64
#"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\mpivars.bat"

# Dont need this:
# "C:\opencv\4.3.0\setup_vars_opencv4.cmd"

# This is arelady on my path:
# SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\bin;%PATH%

# This is not on my pathy by default:
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\extras\CUPTI\lib64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include;%PATH%
```

### Build tensorflow

Building tensorflow can take a long time. Your build can get stuck. Sometimes restrating the build comamnd complets the build, sometimes you need to restrat the computer and when it produces compiler errors you need to clean the build folder and start over again.

If you have ```bazel-out\x64_windows-opt\bin\tensorflow\tools\pip_package\simple_console_for_windows.zip``` you are almost there. Often the build gets stuck about 98-99% into the build.

In CMD window:

```
cd C:/tensorflow/tensorflow

bazel --output_user_root=C:\tensorflow\2.4.1 build --config=opt --config=cuda --define=no_tensorflow_py_deps=true --copt=-nvcc_options=disable-warnings //tensorflow/tools/pip_package:build_pip_package
```

To stop the build, start other cmd shell
```
cd C:/tensorflow/tensorflow
bazel --output_user_root=C:\tensorflow\2.4.1 shutdown
````
Then hit ctrl-c in the build cmd window. Sometimes you need to hit Enter a few times. Sometimes the bezel server will not stop and you need to reboot the computer to free the task.

```ps -efW``` will show all processes but I have norecipe to find the one to shutdown bazel.

### MKL Support Option [not tested]
```
bazel --output_user_root=C:\tensorflow\2.4.1 build --config=mkl --config=opt //tensorflow/tools/pip_package:build_pip_package
```

## Build pip wheel

Build pip/wheel package in MSYS shell.

```
cd C:/tensorflow/tensorflow
bazel-bin/tensorflow/tools/pip_package/build_pip_package pip_package
```

## Install the pip wheel

```
cd pip_package
pip3 install tensorflow-2.4.1-cp38-cp38-win_amd64.whl
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
# should result in True
print(tf.test.is_built_with_cuda())
# should result in something similar to [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
print(tf.config.list_physical_devices('GPU'))
# should result in 2.4.1
print(tf.__version__)
# should result in 2.4.0
print(tf.keras.__version__)
# should result in something like tf.Tensor(-629.5367, shape=(), dtype=float32)
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
```

Also check out
```
# Results in something like:
# Ran 93 tests in 14.100s
# FAILED (failures=2, skipped=6)
# These Failed on (GeForce GTX 960M computeCapability: 5.0, 4GiB memory with 75GiB/s bandwidth): 
#    testLowRankSupported
#    testLongNpArray

py -3 C:\tensorflow\tensorflow\tensorflow\python\framework\tensor_util_test.py
```

## Cleanup
After installing the package you might want to clear the output directories.

```
bazel --output_user_root=C:\tensorflow\2.4.1 clean
```

This removes bazel_out, bazel_bin and frees about 17GB of data.
