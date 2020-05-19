# Installing Software Development Tools on Windows 10
This write up perpares your Windows 10 computer for
* Python
* Visual Studio
* CMake
* Intel TBB, MKL, MPI, IPP, DAAL
* Intel Media SDK
* Intel RealSense
* GStreamer
* CUDA
* QT
* VTK
and attempts to provide the binaries, dlls and libs at a central location.

## Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.
OpenCV still supports python 2.7 but compilation fails at the final stages of the build if one version is 32bit and the other 64bit. 

## Install Visual Studio
Install Visual Studio Community from [Microsoft](https://visualstudio.microsoft.com/downloads/) and install the the option for develoment for desktop application in C.

## CMake
Install CMake with latest release version. [Kitware](https://github.com/Kitware/CMake/releases/). Cmake is update regularly. You might have multiple versions on your computer. You can find the one that is used with ```
where cmake.exe```. You would like it at the same location where cmake-gui is installed.

## Windows SDK 
When you install Visual Studio Compiler you can select Windows 10 SDK (e.g. 10.0.18362.0) in the Installer. Windows SDK includes DirectX SDK. When you rerun the Visual Studio installer you might want to add options to include Windows SDK and other compoenents that are not yet installed. [SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/).

## Ninja
NINJA can be faster than Visual Studio in building your projects.
You will still use the microsoft C compiler from Visual Studio but ninja will manage it.
Using ninja can inroduce additional issues and your build might not complete.

Install [Chocolatey](https://chocolatey.org/) then install Ninja with
```
choco install ninja
```

### Python Packages
Download get-pip.py from https://bootstrap.pypa.io/
Open a command shell and cd to the location of get-pip.py and execute following:
```
py -3 get-pip.py
py -3 -m pip install pip --upgrade
```

I recommend the following python packages rom https://www.lfd.uci.edu/~gohlke/pythonlibs download
* numpy‑1.18.3+mkl‑cp38‑cp38‑win_amd64.whl
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
* scikit-image
* pylint
* cython
* scipy
* pillow
* matplotlib
* pandas
* wave
* imutils 
in my python installation.

## Intel TBB, MKL, MPI, IPP, DAAL
To accelerate operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. 
[Intel libraries](https://software.seek.intel.com/performance-libraries). 
The chrome browser seems to have have issues with selecting the downloads unfortunately.

## LAPACK, BLAS
BLAS is part of the Intel Performance libraries which we installed above.
You dont need to build it. 
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

## cuDNN
Login to your NVIDIA account and download [cudnn](https://developer.nvidia.com/rdp/cudnn-download)
Open the archive and copy its content to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vxx.x where xx.x is your installed version.

## NVIDIA Video Codec SDK
Download the Video Codec SDK, extract and copy include and lib directories to 
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vxx.x
[VideoSDK](https://developer.nvidia.com/nvidia-video-codec-sdk/download)

## QT
Installing QT takes a very long time. In addition it can interfere with your current ninja and cmake setup.
Not all opencv components compile nicely when QT is enabled and unless you really need QT functionality enabled, I don't recommended it on Windows as a first time build. 

To install QT download it from https://www.qt.io/download-open-source. At the bottom is installer link in green. Login with your QT account. Once you have QT installed use the MaintenanceTool application in the QT folder to make sure you have a valid QT version installed. This can take a long time and might consume about 3GB of storage. I filter for LTS version.

I installed:
* MSVC 32/64bit
* UWP x86/x63
* Sources, QT Charts and all following QT Components
* QT Creator
* QT Debugging Tools for Windows

## VTK
For Visualization Tool Kit follow description here:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/InstallVTK.md

## INACTIVE Packages

### HDF5 STATUS: Disabled, does not compile.
If you are intersted in large datasets you might want to install the HDF library from HDF group. Often researchers use TIFF standard to create large image files, however for very large datasets hdf5 should be considered, especially when the data sets exceed the RAM capacity.
https://www.hdfgroup.org/downloads/hdf5/
Make an account and obtain the vs14.zip version.
I installed into C:/HDF5.
lib and include folders are in C:/HDF5/x.yy.z/lib/ and include folders.
OpenCV provides a wrapper for the libhdf5 library. If HDF5_DIR is set as environment variable it will find cmake files.

### JavaScript STATUS: Disabled, does not compile
OpenCV provides access to JavaScript. For BUILD_opencv_js=ON you need EMscripten.
WARNING: This will install a python and java interpreter. On my installation cmake picked up this Python 3 instead of the system wide one.
```
cd C:/opencv/oppencv_dep
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
emsdk install latest
emsdk activate latest
```
You will need to run 
```
C:/opencv/oppencv_dep/emsdk/emsdk_env.bat
``` 
in each shell/cmd window to activate the components.
This script set JAVA_HOME to a new location.
You can set it back with:
```
set "JAVE_HOME=C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\"
```

### Matlab STATUS: On hold.
WITH_MATLAB=ON requires mex builder and some libraries to be found. In matlab command prompt: mex -setup
This is not yet working in my setup as Matlab interface is not getting built. I assume I will need to activate additional components.

### EIGEN STATUS: Disabled, does not compile.
To active the EIGEN library you need to download it
```
git clone https://gitlab.com/libeigen/eigen.git
```

## Environment Variables

You will wan to update your path and environment variables. 
I added gstreamer to path. For other components I created a redistribution folder to hold all the dlls and libs from the different packages. There is a size limit for the PATH variable and exbanding the path can create a problem.

If you dont know how to do modify the PATH, Rapid Environment Editor is a tool that finds errors and can also help you deal with the PATH when it exceeds the size limit. There are two PATH variables. The global one and the one associated with your account. The one for your account is an addition to the global one.

Environment Variables

* INTELMEDIASDKROOT = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_ROOT_X86_64 = C:\gstreamer\1.0\x86_64
* GSTREAMER_DIR=C:\gstreamer\1.0\x86_64
* HDF5_DIR = C:\HDF5\1.12.0\cmake
* QT_PLUGIN_PATH = C:\Qt\5.x.y\msvc2017_64\plugins

PATH
* C:\Python38
* C:\Python38\Scripts
* C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\bin
* C:\Program Files (x86)\Windows Kits\8.1\bin\x64
* C:\gstreamer\1.0\x86_64\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin
* C:\PROGRA~1\NVIDIA GPU Computing Toolkit\CUDA\v10.2\libnvvp
* C:\opencv\opencv_redist

We will copy the dlls needed for our package to the "redist" folder.

## Colelcting dll and libs

Lets copy the dlls, libs in the redistribution folder to a central location. This needs about 3.5 GBytes.

```
REM   OpenCV ===========
copy  "C:\opencv\opencv\build\install\x64\vc16\bin\*" C:\opencv\opencv_redist /y
copy  "C:\opencv\opencv\build\install\x64\vc16\lib*" C:\opencv\opencv_redist /y
REM   Intel MPI ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\release\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\mpi\intel64\lib\*" C:\opencv\opencv_redist /y
REM   INTEL TBB ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc14\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\tbb\lib\intel64\vc14\*" C:\opencv\opencv_redist /y
REM   INTEL MKL ========
xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" C:\opencv\opencv_redist /s /h /i /e
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\mkl\lib\intel64\*" C:\opencv\opencv_redist /y
REM   INTEL IPP ========
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\ipp\*" C:\opencv\opencv_redist /y
xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\ipp\lib\intel64_win" C:\opencv\opencv_redist /s /h /i /e
REM   INTEL DAAL =======
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\daal\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\daal\lib\intel64\*" C:\opencv\opencv_redist /y
REM   INTEL compiler ===
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\compiler\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\compiler\lib\intel64\*" C:\opencv\opencv_redist /y
REM   INTEL Medi SDK ===
copy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\lib\x64\*" C:\opencv\opencv_redist /y
REM   INTEL RealSense ==
copy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*" C:\opencv\opencv_redist /y
copy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\lib\x64\*" C:\opencv\opencv_redist /y
REM QT =================
copy  "C:\Qt\5.14.1\msvc2017_64\bin\*" C:\opencv\opencv_redist /y
REM GSTREAMER ==========

REM copy  "C:\gstreamer\1.0\x86_64\bin\*" C:\opencv\opencv_redist /y
REM xcopy "C:\gstreamer\1.0\x86_64\lib"  C:\opencv\opencv_redist /s /h /i /e
```
