# Compiling TensorFlow on Windows 10

- [Compiling OpenCV on Windows 10](#compiling-opencv-on-windows-10)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisites](#pre-requisites)
  * [Obtaining OpenCV Source](#obtaining-opencv-source)
  * [Uninstalling of Previous opencv Installations](#uninstalling-of-previous-opencv-installations)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment)
  * [Debugging Missing Dependencies](#debugging-missing-dependencies)
- [Building OpenCV](#building-opencv)
  * [Build 1 [STATUS: Completed Successfully]](#build-1--status--completed-successfully-)
    + [Configure Build](#configure-build)
    + [Configure and Generate](#configure-and-generate)
    + [CMD Shell Equivalent](#cmd-shell-equivalent)
    + [Build](#build)
    + [Test](#test)
  * [Build 2 [STATUS: Completed Successfully]](#build-2--status--completed-successfully-)
    + [Configure Build](#configure-build-1)
    + [Build](#build-1)
    + [Test](#test-1)
  * [Build 3 [STATUS: Completed Successfully]](#build-3--status--completed-successfully-)
    + [Configure BUILD](#configure-build)
    + [Build](#build-2)
    + [Test](#test-2)
  * [Build 4](#build-4)
    + [Configure Build](#configure-build-2)
    + [Build](#build-3)
    + [Test](#test-3)
      - [Gstreamer Camera](#gstreamer-camera)
- [Build 1 CMAKE Output](#build-1-cmake-output)
- [Build 2 CMAKE Output](#build-2-cmake-output)
- [Build 3 CMAKE Output](#build-3-cmake-output)
- [Build 4 CMAKE Output](#build-4-cmake-output)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Motivation

## Approach

Many online posts have been consulted for this document.
* [1] https://dev.infohub.cc/build-tensorflow-220rc0-gpu/

## Background Reading


## Pre-Requisites

Prepare your system with https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md. I propose to work with dynamic link libraries and to copy all Intel related dlls to a central location to limit extension of the PATH variable.

Install MSYS2 https://github.com/msys2/msys2-installer/releases/download/2020-05-22/msys2-x86_64-20200522.exe
Add C:\msys64\usr\bin to PATH
C:\msys64\msys2_shell.cmd

# Package update (in console opened with C: \ msys64 \ msys2_shell.cmd)
pacman -Syu
# Restart the console (close it with the × button, etc.)
# Introduce required packages in newly opened console
pacman -Su
pacman -S git patch unzip
#After that, the console of MSYS2 is not used, so exit with exit
exit

Check _TF_MIN_BAZEL_VERSION and _TF_MAX_BAZEL_VERSION in configure.py of TensorFlow. For 2.2.0 it is 2.0.0 to 3.99.0
Install bazel https://github.com/bazelbuild/bazel/releases
https://github.com/bazelbuild/bazel/releases/download/2.0.0/bazel-2.0.0-windows-x86_64.exe

python -m pip install --upgrade pip
pip install six numpy wheel
pip install keras_applications==1.0.8 --no-deps
pip install keras_preprocessing==1.1.0 --no-deps

## Obtaining TensorFlow Source

```
mkdir C:/tensorflow
cd C:/tensorflow
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
git checkout v2.2.0
```

## Uninstalling of Previous opencv Installations

To make sure python finds your build you will want to remove any other installation of opencv.
```
pip3 uninstall tensorflow
pip3 uninstall tensorflow-gpu
```

## Preparing your Shell Build Environment

Open a command prompt (CMD) and enter the following commands with directories pointing to your installations:

```
cd C:/opencv/opencv/build
set "openCvSource=C:\opencv\opencv"
set "openCVExtraModules=C:\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
```

When you execute some of the vcvars script twice in a row, it will throw an error the second time. You can ignore those.

**It is critical to run this setup each time in the shell window that you will use make, cmake, cmake-gui or ninja before you start configuring your build.**

C:\msys64\msys2_shell.cmd
cd C:\tensorflow\tensorflow
py -3 ./configure.py

accept default locations for python
no ROCm support
yes CUDA
cumpute capabilities 5.0
/arch:AVX2



