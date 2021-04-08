# Compiling TensorFlow on Windows 10 with CUDA or MKL

- [Compiling TensorFlow on Windows 10 with CUDA or MKL](#compiling-tensorflow-on-windows-10-with-cuda-or-mkl)
- [Motivation](#motivation)
- [Approach](#approach)
- [Pre-Requisites](#pre-requisites)
- [Configuring MSYS](#configuring-msys)
- [Updating Python Packages](#updating-python-packages)
- [Installing bazel](#installing-bazel)
- [CMD versus MSYS2 shell](#cmd-versus-msys2-shell)
  * [Configure MSYS2 build environment](#configure-msys2-build-environment)
  * [Configure the CMD shell build environment](#configure-the-cmd-shell-build-environment)
- [Obtaining TensorFlow Source](#obtaining-tensorflow-source)
- [Configuring TensorFlow](#configuring-tensorflow)
- [Building Tensor Flow](#building-tensor-flow)
  * [Build Configurations](#build-configurations)
  * [Clean previous build](#clean-previous-build)
  * [Default  build](#default--build)
  * [Building for GPU / Enable Eigen inline / Change AVX/AVX2](#building-for-gpu---enable-eigen-inline---change-avx-avx2)
  * [Building with MKL support](#building-with-mkl-support)
- [Creating the pip wheel](#creating-the-pip-wheel)
- [Installing the pip wheel](#installing-the-pip-wheel)
- [Testing Installation](#testing-installation)
- [Cleaning Up](#cleaning-up)
- [MKL + CUDA Error](#mkl---cuda-error)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Motivation

Reassons for compiling a custom version of tensorflow is either a hope for performance gain or compatibility for your installed libraries.

My tests show that custom built tensorflow increases training performance. The inference performance for the pre built pip packages is not significantly affected.

PyPi tensorflow-GPU uses cuda solver from CUDA 10 and works otherwise with CUDA 11. Installing and adding both CUDA bin-folders on the search path solves the issue of finding the appropriate solver.

PyPi tensorflow does not include Intel MKL acceleration. MKL improves traning performance.

# Approach

The following online posts have been consulted for this document:  
* [1] https://dev.infohub.cc/build-tensorflow-220rc0-gpu/
* [2] https://www.tensorflow.org/install/source_windows
* [3] https://software.intel.com/content/www/us/en/develop/articles/intel-optimization-for-tensorflow-installation-guide.html#wind_B_S
* [4] https://medium.com/vitrox-publication/deep-learning-frameworks-tensorflow-build-from-source-on-windows-python-c-cpu-gpu-d3aa4d0772d8

# Pre-Requisites

* Prepare your system with https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md 

* Install CUDA and cuDN. **Install both CUDA 10 and CUDA 11**, but make sure CUDA 11 is used by default.

* Install MSYS2 https://github.com/msys2/msys2-installer/releases, bazel uses bash from msys2 for some of its operation.

* Add ```C:\msys64\usr\bin``` to Windows path.

* Make sure you have long path names enabled https://superuser.com/questions/1119883/windows-10-enable-ntfs-long-paths-policy-option-missing

* Make sure you have the appropriate versions of python, cuDNN, CUDA, bazel as described here: https://www.tensorflow.org/install/source

* Make sure in ```Visual Studio Installer``` you select ```Desktop Development with C++``` and that ```Microsoft Visual C++ 2019 Redistributable``` is selected from Other Tools and Frameworks.

* Make sure in ```Microsoft Build Tools 2019``` you have selected ```C++ Build Tools```. 

# Configuring MSYS

Start the msys shell with ```C:\msys64\msys2_shell.cmd```   
Update packages:  
```
pacman -Syu
```
Restart the console and introduce required packages in a newly opened console.  
```
pacman -Su
pacman -S git patch zip unzip diffutils git
exit
```

If your windows username has a space in it, then you need to fix the username issue: https://sourceforge.net/p/msys2/discussion/general/thread/76612760/:  

```
/usr/bin/mkpasswd  >  /etc/passwd
```
Change your user name in /etc/passwd to a name without spaces.

# Updating Python Packages

Tensorflow needs numpy, keras-applications, keras-preprocessing, pip, six, wheel, mock. Numpy should already be installed. I use the numpy version built with Intel mkl from https://www.lfd.uci.edu/~gohlke/pythonlibs/ and the other packages from https://pypi.org/

In CMD shell:

```
pip3 install --upgrade pip
pip3 install six wheel mock
pip3 install keras_applications==1.0.8 --no-deps
pip3 install keras_preprocessing==1.1.2 --no-deps
```

# Installing bazel

Obtain latest release of baselisk from https://github.com/bazelbuild/bazelisk and copy it as bazel.exe into a folder in your path. bazelisk downloads and uses the apprpriate version of bazel for your build.

Bazel typical Windows related issues are mentioned on bazel website. I can not confirm wether enabling any of these suggestions solves them:  
- Use short pathnames when starting bazel```--output_user_root=C:/tensorflow/build```
- Enable short file names in 8.3 formant ```fsutil 8dot3name set 0```. Read about this tool first and query your current settings. This requires CMD shell run as Administrator. I did not modify my settings.
- Run bazel from CMD prompt or PowerShell. I use CMD or MSYS2.
- set BAZEL_VC=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC
- set BAZEL_SH=C:\msys64\usr\bin\bash.exe
- set BAZEL_VS=C:\Program Files (x86)\Microsoft Visual Studio
- Enable symbolic links by addding this to .bazelrc, however does not match my .bazelrc settings: ``` startup --windows_enable_symlinks```, ```build --enable_runfiles```. I did not modify .bazelrc.

# CMD versus MSYS2 shell

One can build tensorflow in CMD shell or in MSYS2 shell.

## Configure MSYS2 build environment

Start MSYS2 Shell:  

```
C:\msys64\msys2_shell.cmd
```

Setup environment inside MSYS2:  
```
cd C:/tensorflow/tensorflow
# Disable path conversion
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"
# Use Unix-style with ':' as separator
export PATH="/c/pool:$PATH"
export PATH="/c/Python36:$PATH"
# For CUDA add CUDA and CUDNN to the path
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin:$PATH"
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/extras/CUPTI/libx64:$PATH"
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/include:$PATH"
export PATH="$PATH:/c/tensorflow/tensorflow/bazel_out/external/mkl_windows/lib" 
export OneDNN_DIR="/c/tensorflow/tensorflow/bazel_out/one_dnn_dir"
export PATH=$PATH":$OneDNN_DIR
# Set Visual Studio Code Version, might decrease build time
export TF_VC_VERSION=16.9
```

## Configure the CMD shell build environment

```
cd C:\tensorflow\tensorflow
REM bazel executes the necessary compiler setup regradless of the calling shell.
REM Setup, bazel seems to take care of this by itself
REM "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
REM "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
REM "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019

REM BAZEL, if not already set in environment variables
REM I have these set as system variables
REM set BAZEL_SH='C:\msys64\usr\bin\bash.exe'
REM set BAZEL_VS='C:\Program Files (x86)\Microsoft Visual Studio'
REM  set BAZEL_VC='C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC'

REM Compile time reduction, this needs to be a float
REM Check Visual Studio Installer for current version
REM This is read when executing configure.py
set TF_VC_VERSION=16.9
```

After running the vcvars64 script I have invalid paths with "\\\\" instead of "\\'. You can fix this with:
```
echo | set /p=set > fixedpath.bat
path | sed 's/\\\\\\\/\\\/g' >> fixedpath.bat
fixedpath.bat
del fixedpath.bat
```
but the fix does not propagate to the bazel build scripts.

# Obtaining TensorFlow Source

```
mkdir C:/tensorflow
cd C:/tensorflow
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout v2.4.1
```

# Configuring TensorFlow

In CMD shell (with above enironment):
```
cd C:\tensorflow\tensorflow
py -3 configure.py
```

In MSYS shell (with above environment):
```
cd C:/tensorflow/tensorflow
python ./configure.py
```

* ROCm is AMDs GPU computation option.

* To minimize build time, I only enable the options my GPU and CPU support.
Compute Capabilities: [3.5] 5.0 [5.2,6.1,7.0,7.5,8.6], see https://en.wikipedia.org/wiki/CUDA  

* You can use CPCU-Z to check your supported CPU instruction set. ```/arch:AVX``` versus ```/arch:AVX2```.

* The "eigen strong inline" option significantly increase build time but result in slightly better performance.  You will need to disable optimization of large files as shown below. 

c:\tensorflow\tensorflow\.tf_configure.bazelrc should not have backward slashs in file paths. Check before continuing.

# Building Tensor Flow

Building tensorflow takes a long time and bazel spawns tasks that consume a lot of memory. To avoid that the build renders your computer unresponsive, one can limit the resources available to bazel:
```
--local_ram_resources=HOST_RAM*.6  
--local_cpu_resources=HOST_CPUS-5
```
The number of HOST_CPUS includes the virtual cpus. You will want to provide a number that is less than the number of actual cores. 

Some functions take more than 20hrs to compile (e.g. mkl_cwise_opps_common.cc, fused_batch_norm_op.cc) when the inline options is enabled. These compiler options reduce the amount of optimization on large functions: 

``` 
--copt=/d2ReducedOptimizeHugeFunctions
--host_copt=/d2ReducedOptimizeHugeFunctions   
```

If there was unintended input into shell/CMND window, for example by clicking inside the window with the mouse, job queueing might no longer update properly. Clear such input with "enter". 

To stop the build, open task manager and stop one of the MS C Compiler tasks. You might also be able to find bazel.exe in the list or the java server. ```ps -efW``` from MSYS2 shows all processes. ```Ctrl-C``` in the command window will stop tbe bazel build bot not the bazel server (java program running in background).

## Build Configurations

**CPU Version**

|        | Processor  | MKL     | Inst Set| Eigen inline | Build status     |
|  ---   | ---------- | ------- | ------- | ------------ | -----------------|
| PyPi   |  CPU       | unknown | unknown | unknown      | download         |
| Custom |  CPU       | No      | AVX     | No           | completed        |
| Custom |  CPU       | No      | AVX2    | No           | completed        |
| Custom |  CPU       | No      | AVX2    | Yes          | completed        |
| Custom |  CPU       | Yes     | AVX2    | Yes          | completed        |

**CUDA Version**
|        | Processor  | MKL     | AVX2    | Eigen inline | BUild status     |
|--------| -----------| ------- | ------- | ------------ | ---------------- |
| PyPi   |  CUDA      | unknown | unknown | unknown      | download         |
| Custom |  CUDA      | No      | AVX     | No           | completed        |
| Custom |  CUDA      | No      | AVX2    | No           | completed        |
| Custom |  CUDA      | No      | AVX2    | Yes          | completed        |
| Custom |  CUDA      | Yes     | AVX2    | Yes          | does not compile | 

# Cleaning Up / Clean previous build

After installing the package you might want to clear the output directories.
```
bazel --output_user_root=C:\tensorflow\build clean
```
This removes bazel_out, bazel_bin and frees about 17GB of data.

Some  build instructions recommend that whenever you change the build configuration, you should clean the build space before building a new one.

## Default  build

Accept the default settings in ```configure.py```, which will result in CPU version with AVX support and eigen inline optimizations turned off.

```
bazel --output_user_root=C:\tensorflow\build build^
 --config=opt ^
 --define=no_tensorflow_py_deps=true ^
 --local_ram_resources=HOST_RAM*.6 ^
 --local_cpu_resources=HOST_CPUS-5 ^
 //tensorflow/tools/pip_package:build_pip_package
```
## Building for GPU / Enable Eigen inline / Change AVX/AVX2

```
py -3 configure.py
```
You can:
- enabled CUDA and list the architecture of your GPU (see above).  
- enable instructions set optimization with ```/arch:AVX2```or ```/arch:AVX```   
- enable Eigen inline optimization (disable the override)

Build the configuration.
```
bazel --output_user_root=C:\tensorflow\build build ^
 --config=opt ^
 --define=no_tensorflow_py_deps=true ^
 --copt=-nvcc_options=disable-warnings ^
 --local_ram_resources=HOST_RAM*.6 ^
 --local_cpu_resources=HOST_CPUS-5 ^
 --copt=/d2ReducedOptimizeHugeFunctions ^
 --host_copt=/d2ReducedOptimizeHugeFunctions ^
 //tensorflow/tools/pip_package:build_pip_package
```

## Building with MKL support
For intel MKL support we need to use ```--config=opt ``` and ``` --config=mkl ``` .

```
bazel --output_user_root=C:\tensorflow\build build^
 --config=opt ^
 --config=mkl ^
 --define=no_tensorflow_py_deps=true ^
 --local_ram_resources=HOST_RAM*.6 ^
 --local_cpu_resources=HOST_CPUS-5 ^
 --copt=/d2ReducedOptimizeHugeFunctions ^
 --host_copt=/d2ReducedOptimizeHugeFunctions ^
 //tensorflow/tools/pip_package:build_pip_package
```

MKL increases build time.  
CUDA and MKL support are exclusive.  

# Creating the pip wheel
To build pip/wheel package we use the CMD shell and ```cd``` to the root directory:

```
cd C:\tensorflow\tensorflow
bazel-bin\tensorflow\tools\pip_package\build_pip_package pip_package
```

# Installing the pip wheel

You will want to remove any previous installation of tensorflow first. e.g.

```
pip3 uninstall tensorflow
pip3 uninstall tensorflow-gpu
```

Now we can install our custom tensorflow package:
```
cd pip_package
pip3 install tensorflow-2.x.y-cp38-cp38-win_amd64.whl
```

When you build several pip wheels, you dont want to change their filename but move them into subfolders. pip requires that the filename is not altered. 

# Testing Installation

Start python ```py -3``` and enter the following commands on command prompt:
```
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
import tensorflow as tf 
print("Tensorflow is build with CUDA support:", tf.test.is_built_with_cuda())
print("GPUs available:", tf.config.list_physical_devices('GPU'))
print("Tensorflow version:", tf.__version__)
print("Keras Version:",tf.keras.__version__)
print("Reduce Sum completed with:", tf.reduce_sum(tf.random.normal([1000, 1000])))
major_version = int(tf.__version__.split(".")[0])
if major_version >= 2:
   from tensorflow.python import _pywrap_util_port
   print("MKL enabled:", _pywrap_util_port.IsMklEnabled())
else:
   print("MKL enabled:", tf.pywrap_tensorflow.IsMklEnabled()) 
```

Also check out:
```
py -3 C:\tensorflow\tensorflow\tensorflow\python\framework\tensor_util_test.py

# This test results in something like:
# Ran 93 tests in 14.100s
# FAILED (failures=2, skipped=6)
# These Failed on (GeForce GTX 960M computeCapability: 5.0, 4GiB memory with 75GiB/s bandwidth): 
#    testLowRankSupported
#    testLongNpArray
```

# MKL + CUDA Error

 C:\tensorflow\tensorflow>bazel --output_user_root=C:\tensorflow\2.4.1 build ^
More?  --config=opt ^
More?  --config=mkl ^
More?  --define=no_tensorflow_py_deps=true ^
More?  --copt=-nvcc_options=disable-warnings ^
More?  --local_ram_resources=HOST_RAM*.6 ^
More?  --local_cpu_resources=HOST_CPUS-5 ^
More?  --copt=/d2ReducedOptimizeHugeFunctions ^
More?  --host_copt=/d2ReducedOptimizeHugeFunctions ^
More?  //tensorflow/tools/pip_package:build_pip_package
Starting local Bazel server and connecting to it...
INFO: Options provided by the client:
  Inherited 'common' options: --isatty=1 --terminal_columns=120
INFO: Reading rc options for 'build' from c:\tensorflow\tensorflow\.bazelrc:
  Inherited 'common' options: --experimental_repo_remote_exec
INFO: Options provided by the client:
  'build' options: --python_path=C:/Python38/python.exe
INFO: Reading rc options for 'build' from c:\tensorflow\tensorflow\.bazelrc:
  'build' options: --apple_platform_type=macos --define framework_shared_object=true --define open_source_build=true --java_toolchain=//third_party/toolchains/java:tf_java_toolchain --host_java_toolchain=//third_party/toolchains/java:tf_java_toolchain --define=tensorflow_enable_mlir_generated_gpu_kernels=0 --define=use_fast_cpp_protos=true --define=allow_oversize_protos=true --spawn_strategy=standalone -c opt --announce_rc --define=grpc_no_ares=true --noincompatible_remove_legacy_whole_archive --noincompatible_prohibit_aapt1 --enable_platform_specific_config --config=short_logs --config=v2
INFO: Reading rc options for 'build' from c:\tensorflow\tensorflow\.tf_configure.bazelrc:
  'build' options: --action_env PYTHON_BIN_PATH=C:/Python38/python.exe --action_env PYTHON_LIB_PATH=C:/Python38/lib/site-packages --python_path=C:/Python38/python.exe --config=xla --action_env CUDA_TOOLKIT_PATH=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2 --action_env TF_CUDA_COMPUTE_CAPABILITIES=5.0 --config=cuda --define=override_eigen_strong_inline=true --action_env TF_CONFIGURE_IOS=0
INFO: Found applicable config definition build:short_logs in file c:\tensorflow\tensorflow\.bazelrc: --output_filter=DONT_MATCH_ANYTHING
INFO: Found applicable config definition build:v2 in file c:\tensorflow\tensorflow\.bazelrc: --define=tf_api_version=2 --action_env=TF2_BEHAVIOR=1
INFO: Found applicable config definition build:xla in file c:\tensorflow\tensorflow\.bazelrc: --define=with_xla_support=true
INFO: Found applicable config definition build:cuda in file c:\tensorflow\tensorflow\.bazelrc: --config=using_cuda --define=using_cuda_nvcc=true
INFO: Found applicable config definition build:using_cuda in file c:\tensorflow\tensorflow\.bazelrc: --define=using_cuda=true --action_env TF_NEED_CUDA=1 --crosstool_top=@local_config_cuda//crosstool:toolchain --define=tensorflow_enable_mlir_generated_gpu_kernels=1
INFO: Found applicable config definition build:opt in file c:\tensorflow\tensorflow\.tf_configure.bazelrc: --copt=/arch:AVX2 --host_copt=/arch:AVX2 --define with_default_optimizations=true
INFO: Found applicable config definition build:mkl in file c:\tensorflow\tensorflow\.bazelrc: --define=build_with_mkl=true --define=enable_mkl=true --define=tensorflow_mkldnn_contraction_kernel=0 --define=build_with_openmp=true -c opt
INFO: Found applicable config definition build:windows in file c:\tensorflow\tensorflow\.bazelrc: --copt=/W0 --copt=/D_USE_MATH_DEFINES --host_copt=/D_USE_MATH_DEFINES --cxxopt=/std:c++14 --host_cxxopt=/std:c++14 --config=monolithic --copt=-DWIN32_LEAN_AND_MEAN --host_copt=-DWIN32_LEAN_AND_MEAN --copt=-DNOGDI --host_copt=-DNOGDI --copt=/experimental:preprocessor --host_copt=/experimental:preprocessor --linkopt=/DEBUG --host_linkopt=/DEBUG --linkopt=/OPT:REF --host_linkopt=/OPT:REF --linkopt=/OPT:ICF --host_linkopt=/OPT:ICF --experimental_strict_action_env=true --verbose_failures --distinct_host_configuration=false
INFO: Found applicable config definition build:monolithic in file c:\tensorflow\tensorflow\.bazelrc: --define framework_shared_object=false
INFO: Analyzed target //tensorflow/tools/pip_package:build_pip_package (412 packages loaded, 26756 targets configured).
INFO: Found 1 target...
INFO: Deleting stale sandbox base C:/tensorflow/2.4.1/wvk7snnt/sandbox
ERROR: C:/tensorflow/2.4.1/wvk7snnt/external/llvm_openmp/BUILD.bazel:176:1: C++ compilation of rule '@llvm_openmp//:libiomp5md.dll' failed (Exit 1): ml64.exe failed: error executing command
  cd C:/tensorflow/2.4.1/wvk7snnt/execroot/org_tensorflow
  SET CUDA_TOOLKIT_PATH=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2
    SET INCLUDE=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\ATLMFC\include;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\include;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\include\um;C:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\ucrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\shared;C:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\um;C:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\winrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.19041.0\cppwinrt
    SET LIB=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\ATLMFC\lib\x64;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\lib\x64;C:\Program Files (x86)\Windows Kits\NETFXSDK\4.8\lib\um\x64;C:\Program Files (x86)\Windows Kits\10\lib\10.0.19041.0\ucrt\x64;C:\Program Files (x86)\Windows Kits\10\lib\10.0.19041.0\um\x64
    SET PATH=C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\\Extensions\Microsoft\IntelliCode\CLI;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910\bin\HostX64\x64;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\VC\VCPackages;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\TestWindow;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\bin\Roslyn;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Team Tools\Performance Tools\x64;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Team Tools\Performance Tools;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Common\VSPerfCollectionTools\vs2019\\x64;C:\Program Files (x86)\Microsoft Visual Studio\Shared\Common\VSPerfCollectionTools\vs2019\;C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\devinit;C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64;C:\Program Files (x86)\Windows Kits\10\bin\x64;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\\MSBuild\Current\Bin;C:\Windows\Microsoft.NET\Framework64\v4.0.30319;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\;;C:\Windows\system32;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja
    SET PWD=/proc/self/cwd
    SET PYTHON_BIN_PATH=C:/Python38/python.exe
    SET PYTHON_LIB_PATH=C:/Python38/lib/site-packages
    SET RUNFILES_MANIFEST_ONLY=1
    SET TEMP=C:\Users\URSUTZ~1\AppData\Local\Temp
    SET TF2_BEHAVIOR=1
    SET TF_CONFIGURE_IOS=0
    SET TF_CUDA_COMPUTE_CAPABILITIES=5.0
    SET TF_NEED_CUDA=1
    SET TMP=C:\Users\URSUTZ~1\AppData\Local\Temp
  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.28.29910/bin/HostX64/x64/ml64.exe -B external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py /nologo /DCOMPILER_MSVC /DNOMINMAX /D_WIN32_WINNT=0x0600 /D_CRT_SECURE_NO_DEPRECATE /D_CRT_SECURE_NO_WARNINGS /D_SILENCE_STDEXT_HASH_DEPRECATION_WARNINGS /bigobj /Zm500 /J /Gy /GF /EHsc /wd4351 /wd4291 /wd4250 /wd4996 /Iexternal/llvm_openmp /Ibazel-out/x64_windows-opt/bin/external/llvm_openmp /Iexternal/bazel_tools /Ibazel-out/x64_windows-opt/bin/external/bazel_tools /Iexternal/llvm_openmp/runtime/src /Ibazel-out/x64_windows-opt/bin/external/llvm_openmp/runtime/src /Iexternal/llvm_openmp/include /Ibazel-out/x64_windows-opt/bin/external/llvm_openmp/include /showIncludes /MD /O2 /DNDEBUG /W0 /D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOGDI /experimental:preprocessor /arch:AVX2 -nvcc_options=disable-warnings /d2ReducedOptimizeHugeFunctions /Domp_EXPORTS /D_M_AMD64 /DOMPT_SUPPORT=0 /D_WINDOWS /D_WINNT /D_USRDLL /Fobazel-out/x64_windows-opt/bin/external/llvm_openmp/_objs/libiomp5md.dll/z_Windows_NT-586_asm.obj /c bazel-out/x64_windows-opt/bin/external/llvm_openmp/z_Windows_NT-586_asm.S
Execution platform: @local_execution_config_platform//:platform
Microsoft (R) Macro Assembler (x64) Version 14.28.29913.0
Copyright (C) Microsoft Corporation.  All rights reserved.

MASM : warning A4018:invalid command-line option : -B
 Assembling: external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(1) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(2) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(3) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(4) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(5) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(6) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(7) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(8) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(9) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(10) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(11) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(12) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(13) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(14) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(15) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(16) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(17) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(18) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(19) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(20) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(21) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(22) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(23) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(24) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(25) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(26) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(27) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(28) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(29) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(30) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(31) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(32) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(33) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(34) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(35) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(36) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(37) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(38) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(39) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(40) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(41) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(42) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(43) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(44) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(45) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(46) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(47) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(48) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(49) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(50) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(51) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(52) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(53) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(54) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(55) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(56) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(57) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(58) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(59) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(60) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(61) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(62) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(63) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(64) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(65) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(66) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(67) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(68) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(69) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(70) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(71) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(72) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(73) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(74) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(75) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(76) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(77) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(78) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(79) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(80) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(81) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(82) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(83) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(84) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(85) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(86) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(87) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(88) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(89) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(90) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(91) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(92) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(93) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(94) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(95) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(96) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(97) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(98) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(99) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(100) : error A2044:invalid character in file
external/local_config_cuda/crosstool/windows/msvc_wrapper_for_nvcc.py(101) : fatal error A1012:error count exceeds 100; stopping assembly
[10,724 / 14,833] Compiling tensorflow/compiler/xla/service/hlo_evaluator_typed_visitor_double.cc; 82986s local

Bazel Ctrl+C handler; shutting down.