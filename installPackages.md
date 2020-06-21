# Installing Software Development Tools on Windows 10
This write up prepares your Windows 10 computer for
* Python
* Visual Studio
* CMake
* Intel TBB, MKL, MPI, IPP, DAAL
* Intel Media SDK
* Intel RealSense
* GStreamer
* CUDA 10.2 (11 is not yet working)
* QT
* VTK

and attempts to provide the binaries, dlls and libs at a central location.

#  Table of Contents

- [Installing Software Development Tools on Windows 10](#installing-software-development-tools-on-windows-10)
- [Table of Contents](#table-of-contents)
  * [Install Python](#install-python)
  * [Install Visual Studio](#install-visual-studio)
  * [Windows SDK](#windows-sdk)
  * [CMake](#cmake)
  * [Ninja](#ninja)
    + [Python Packages](#python-packages)
  * [Intel TBB, MKL, MPI, IPP, DAAL](#intel-tbb--mkl--mpi--ipp--daal)
  * [LAPACK, BLAS](#lapack--blas)
  * [Intel Media SDK](#intel-media-sdk)
  * [Intel RealSense](#intel-realsense)
  * [Gstreamer & FFMPEG](#gstreamer---ffmpeg)
    + [Gstreamer](#gstreamer)
    + [FFMPEG](#ffmpeg)
  * [CUDA](#cuda)
  * [cuDNN](#cudnn)
  * [NVIDIA Video Codec SDK](#nvidia-video-codec-sdk)
  * [TensorFlow prebuilt](#tensorflow-prebuilt)
  * [QT](#qt)
  * [VTK](#vtk)
  * [DLIB](#dlib)
  * [Packages not yet ready](#packages-not-yet-ready)
    + [HD5](#hd5)
    + [JavaScript](#javascript)
    + [EIGEN STATUS](#eigen-status)
  * [Environment Variables](#environment-variables)
  * [Collecting dll and libs](#collecting-dll-and-libs)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.
OpenCV still supports python 2.7 but compilation fails at the final stages of the build if one version is 32bit and the other 64bit. 

## Install Visual Studio
Install Visual Studio Community from [Microsoft](https://visualstudio.microsoft.com/downloads/) and install the the option for Desktop Development with C++.

I also enable:
* Azure
* .Net
* Universal Windows Platform development

## Windows SDK 
When you install Visual Studio Compiler you can select Windows 10 SDK in the Installer. Windows SDK includes DirectX SDK. When you rerun the Visual Studio installer you might want to add options to include Windows SDK and other components that are not yet installed. You can also download directly: [SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/).

## CMake
Install CMake with latest release version. [Kitware](https://github.com/Kitware/CMake/releases/). Cmake is update regularly. You might have multiple versions on your computer. You can find the one that is used with ```
where cmake.exe```. You would like it at the same location where cmake-gui is installed.

## Ninja
NINJA can be faster than Visual Studio in building your projects.
You will still use the Microsoft C compiler from Visual Studio but ninja will manage it. Using ninja can introduce additional issues and your build might not complete.

Download from https://github.com/ninja-build/ninja/releases and copy to C:\pool\bin

### Python Packages
Download get-pip.py from https://bootstrap.pypa.io/
Open a command shell and cd to the location of get-pip.py and execute following:
```
py -3 get-pip.py
py -3 -m pip install pip --upgrade
```
Make sure you have the latest  Microsoft C++ 2015-2019 redistributable:
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
and the 2008 redistributale installed
https://www.microsoft.com/en-us/download/details.aspx?id=15336

I recommend the following python packages rom https://www.lfd.uci.edu/~gohlke/pythonlibs download
* numpy‑1.18.4+mkl‑cp38‑cp38‑win_amd64.whl
* numpy‑1.16.6+mkl‑cp27‑cp27m‑win_amd64.whl
* yappi‑1.2.5‑cp38‑cp38‑win_amd64.whl

```
py -3 -m pip install numpy‑1.18.3+mkl‑cp38‑cp38‑win_amd64.whl
py -2 -m pip install numpy‑1.16.6+mkl‑cp27‑cp27m‑win_amd64.whl
py -3 -m pip install pylint --upgrade
py -3 -m pip install flake8 --upgrade
py -3 -m pip install yappi‑1.2.5‑cp38‑cp38‑win_amd64.whl
```
I usually also have 
* cython
* scipy
* pillow
* scikit-image
* scikit-learn
* matplotlib
* pandas
* wave
* imutils 
* itk

in my python installation.

## Intel TBB, MKL, MPI, IPP, DAAL
To accelerate operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. 
[Intel libraries](https://software.seek.intel.com/performance-libraries). 
The chrome browser seems to have have issues with selecting the downloads unfortunately.

For openCV 4.3.0 the intel libraries should be:
* mkl 2019 Update 5 2019.5.281
* tbb 2019 Update 8 2019.8.281
* mpi 2019 Update 5 2019.5.281
* ipp 2019 Update 5 2019.5.281
* daal 2019 Update 5 2019.5.281
This will link libraries to 2019 folder.
If you want 2020 version you need to download the latest version of these packages. MPI 2019 update 6 and higher are 2020 version. This the versions are important because the folder C:\Program Files (x86)\IntelSWTools\compilers_and_libraries is a link the the installed liraries and it can not link simultanously to 2019 and 2020 libraries.


## LAPACK, BLAS
BLAS is part of the Intel Performance libraries which we installed above.
You don't need to build it. 
LA stands for linear algebra and is the backbone of computer vision and scientific computing.
If you want to build it you can download the source [LAPACK] (http://www.netlib.org/lapack/) and build it but you need a FORTRAN compiler (see Build Instructions for LAPACK 3.5.0 for Windows with Visual Studio in http://icl.cs.utk.edu/lapack-for-windows/lapack. 
You might also be able to use pre built libraries from https://icl.cs.utk.edu/lapack-for-windows/lapack/ using http://icl.cs.utk.edu/lapack-for-windows/lapack/LAPACKE_examples.zip.

## Intel Media SDK
To accelerate video decoding on Intel CPU’s, register, download and install [Intel Media SDK](https://software.intel.com/en-us/media-sdk)

## Intel RealSense
If you want to use an Intel Realsense cameras (3D or Tracking camera) you might want to install [Intel Realsense](https://www.intelrealsense.com/developers/). 

## Gstreamer & FFMPEG
FFMPEG or gstreamer are needed to receive, decode and encode compressed video streams. 
For example the rtsp web cam streams.
OpenCV comes with a wrapper for FFMPEG and distributes the necessary libraries and dlls.
If you use a Jetson single board computer, at the time of tis writting, FFMPEG is not GPU accelerated and you likely will want to 
become familiar with gstreamer which is supported by NVIDIA.

### Gstreamer
For Windows: https://gstreamer.freedesktop.org/download/ or https://gstreamer.freedesktop.org/data/pkg/windows/
Install both
* msvc
* devel msvc

The gst-python bindings are not available on Windows, unfortunately. 
If they were available we could access gstreamer pipelines directly in python. 
For now we can use opencv.
WARNING: Including gstreamer in a python builds can create many issues as there are numerous dlls that need to be accessible.

### FFMPEG
FFMPEG is auto downloaded with opencv and it builds a wrapper and does not build againts your own FFMPEG installation. 
There is a suggestion further below how to bypass the wrapper. 
I have not completed the bypass approach and can not recommend it at thist time.
You can obtain your ffmpeg binary and development files here:
From https://ffmpeg.zeranoe.com/builds/ download
Version:latest stable
Architecture: Windows 64 bit
Linking: Shared and Dev
Unzip and install in your ffmpeg folder 

## CUDA
Install CUDA Tookit from [NVIDIA](https://developer.nvidia.com/cuda-downloads)
This is only useful if you have an NVIDA GPU available. 
If you have a previously installed version, and want to upgrade, make sure to uninstall it first by removing following Program and Features:
* Nsight Visual Studio Integration
* CUDA Visual Studio Integration
* CUDA Samples
* CUDA Runtime
* CUDA Documentation
* CUDA Development

For OpenCV 4.3 you need QT 10.2.

## cuDNN
Login to your NVIDIA account and download [cudnn](https://developer.nvidia.com/rdp/cudnn-download)
Open the archive and copy its content to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2.

## NVIDIA Video Codec SDK
Download the Video Codec SDK, extract and copy include and lib directories to 
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2.
[VideoSDK](https://developer.nvidia.com/nvidia-video-codec-sdk/download)

## TensorFlow prebuilt
TensorFlow needs 
* CUDA 10.2 which you need to get from https://developer.nvidia.com/cuda-toolkit-archive
* cuDNN https://developer.nvidia.com/cudnn which needs to match version 10.2. 
Open the archive and copy its content to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2.

Make sure these are on the PATH
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin```
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\extras\CUPTI\lib64```
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\include```

```
pip3 install --upgrade tensorflow-gpu
```

Start python ```py -3```
Enthere following commands on command prompt
```
import tensorflow as tf 
tf.test.is_built_with_cuda()
tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None)
```

## QT
Installing QT takes a very long time. Make sure you install only the components you need to avoid interference with your current ninja and cmake setup.

Install QT from https://www.qt.io/download-open-source. At the bottom is the installer link in green. Login with your QT account. Once you have QT installed use the MaintenanceTool application in the QT folder to make sure you have a valid QT version installed. This can take a long time and might consume about 3GB of storage.

I installed:
* MSVC 32/64bit
* UWP x86/x64
* Sources, QT Charts and all following QT Components
* QT Creator
* QT Debugging Tools for Windows

For OpenCV you will need qt5.14.2. You can have both 5.14 and 5.15 installed.

## VTK
For Visualization Tool Kit follow description here:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/InstallVTK.md

OpenCV 4.3.0 needs VTK8.2

## DLIB
Machine learning
https://github.com/davisking/dlib

### HD5 [Optional]
If you are interested in large datasets you might want to install the HDF library from HDF group. Often researchers use TIFF standard to create large image files, however for very large datasets hdf5 should be considered, especially when the data sets exceed the RAM capacity.

```
cd C:\hdf5
git clone https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git
cd hdf5
git checkout hdf5_1_12
mkdir build
cd build
cmake-gui ..\
```
* CMAKE_INSTALL_PREFIX = C:/hdf5/1.12.1

Config->Generate->Open Project
Compile with BatchBuild and enable 64bit Release of INSTALL. When HDF5 build completes configure opencv for HDF5.

### JavaScript [Optional]
OpenCV provides access to JavaScript. For BUILD_opencv_js=ON you need EMscripten.
WARNING: This will install a python and java interpreter. On my installation cmake picked up this Python 3 instead of the system wide one.
```
cd C:/opencv/
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
emsdk install latest
emsdk activate latest
```
You will need to run 
```
C:/opencv/emsdk/emsdk_env.bat
``` 
in each shell/cmd window to activate the components.
This script set JAVA_HOME to a new location.
You can set it back with:
```
set "JAVE_HOME=C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\"
```

### EIGEN [Optional]
To active the EIGEN library you need to download it
```
cd C:\
git clone https://gitlab.com/libeigen/eigen.git
git checkout 3.3
```

## Environment Variables

You will wan to update your path and environment variables. 
I added gstreamer to path. For other components I created a redistribution folder to hold all the dlls and libs from the different packages. There is a size limit for the PATH variable and expanding the path can create a problem.

If you don't know how to do modify the PATH, Rapid Environment Editor is a tool that finds errors and can also help you deal with the PATH when it exceeds the size limit. There are two PATH variables. The global one and the one associated with your account. The one for your account is an addition to the global one.

Environment Variables

* INTELMEDIASDKROOT     = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_ROOT_X86_64 = C:\gstreamer\1.0\x86_64
* GSTREAMER_DIR         = C:\gstreamer\1.0\x86_64
* HDF5_DIR              = C:\HDF5\1.12.0\cmake
* QT_PLUGIN_PATH        = C:\Qt\5.x.y\msvc2017_64\plugins
* JAVA_HOME             = C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\
* DXSDK_DIR             = might be already set

PATH

* C:\Python38
* C:\Python38\Scripts
* C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\bin
* C:\Program Files (x86)\Windows Kits\8.1\bin\x64
* C:\gstreamer\1.0\x86_64\bin
* C:\Qt\5.12.8\msvc2017_64\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\libnvvp

This is the location where I copied all dlls and binaries. It will need to be added to the PATH:
* C:\pool\bin

## Collecting dll and libs
We will copy the dlls needed for our package to the "redist" folder. This needs about 3.5 GBytes.
When you build shared libs, dll files are needed, otherwise libraries (*.lib)
```
REM   Intel MPI ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\*" C:\pool\bin /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\release\*" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\lib\*" C:\pool\lib  /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\include\*" C:\pool\include  /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\etc\*" C:\pool\etc  /s/h/i/e/y

REM   INTEL TBB ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc14\*" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\lib\*" C:\pool\lib /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\include\*" C:\pool\include /s/h/i/e/y

REM   INTEL MKL ========
xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" C:\pool\bin /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\lib\*" C:\pool\lib /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\include\*" C:\pool\include /s/h/i/e/y

REM   INTEL IPP ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\ipp\*" C:\pool\bin /y
xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\lib\*" C:\pool\lib /s/h/i/e/y
xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\include\*" C:\pool\include /s/h/i/e/y

REM   INTEL DAAL =======
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\daal\*" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\lib\*" C:\pool\lib /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\include\*" C:\pool\include /s/h/i/e/y

REM   INTEL compiler ===
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\compiler\*" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\compiler\lib\*" C:\pool\lib  /s/h/i/e/y

REM   INTEL Media SDK ===
copy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\lib\*" C:\pool\lib /s/h/i/e/y
xcopy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\include\*" C:\pool\include /s/h/i/e/y

REM   INTEL RealSense ==
copy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" C:\pool\bin /y
xcopy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\lib\*" C:\pool\lib  /s/h/i/e/y
xcopy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\include\*" C:\pool\include  /s/h/i/e/y
```
