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
* MSYS2

and attempts to provide the binaries, dlls and libs at a central location.

#  Table of Contents

- [Installing Software Development Tools on Windows 10](#installing-software-development-tools-on-windows-10)
- [Table of Contents](#table-of-contents)
  * [Install Python](#install-python)
  * [Install Visual Studio](#install-visual-studio)
  * [Windows SDK](#windows-sdk)
  * [CMake](#cmake)
  * [Ninja](#ninja)
  * [Python Packages](#python-packages)
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
  * [GFLAGS](#gflags)
  * [GLOG Google Logging](#glog-google-logging)
  * [DLIB](#dlib)
  * [HD5](#hd5)
  * [JavaScript [Optional]](#javascript--optional-)
  * [EIGEN](#eigen)
  * [Environment Variables](#environment-variables)
  * [Collecting dll and libs](#collecting-dll-and-libs)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.
OpenCV still supports python 2.7 but compilation fails at the final stages of the build if one version is 32bit and the other 64bit. 

## Install Visual Studio
Install Visual Studio Community from [Microsoft](https://visualstudio.microsoft.com/downloads/) and install the the option for Desktop Development with C++. Make sure Windows 10 SDK and MSVC v142 is included in your selection.

If you already installed Visual Studio and want to update run the Visual Studio Installer.

Make sure Microsoft Visual C++ 2019 Redistributable is installed in Control Planel/Programs and Features

After completing the Visual Studio installation, download and install the Microsoft Build Tools 2019 https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019 Include C++ Windows Desktop Build Tools in installer selection.

## Windows SDK 
When you install Visual Studio Compiler you can select Windows 10 SDK in the Installer. Windows SDK includes DirectX SDK. When you rerun the Visual Studio installer you might want to add options to include Windows SDK and other components that are not yet installed. You can also download directly: [SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/).

## CMake
Install CMake with latest release version. [Kitware](https://github.com/Kitware/CMake/releases/). Cmake is update regularly. You might have multiple versions on your computer. You can find the one that is used with ```
where cmake.exe```. You would like it at the same location where cmake-gui is installed.

## Ninja
NINJA can be faster than Visual Studio in building your projects.
You will still use the Microsoft C compiler from Visual Studio but ninja will manage it. Using ninja can introduce additional issues and your build might not complete.

Download from https://github.com/ninja-build/ninja/releases and copy to C:\pool\bin

## Python Packages
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

I recommend the following python packages from  
https://www.lfd.uci.edu/~gohlke/pythonlibs  

* numpy‑*+mkl‑cp38‑cp38‑win_amd64.whl
* yappi‑*‑cp38‑cp38‑win_amd64.whl

```
dir *.whl
py -3 -m pip install numpy...+mkl‑cp38‑cp38‑win_amd64.whl
py -3 -m pip install pylint --upgrade
py -3 -m pip install flake8 --upgrade
py -3 -m pip install yappi*‑cp38‑cp38‑win_amd64.whl
```
I usually also use
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

## Intel TBB, MKL, MPI, IPP, DAAL
To accelerate operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. 

Download the [Intel oneAPI Base Toolkit](https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit/download.html)

The numpy-mkl build at https://www.lfd.uci.edu/~gohlke/pythonlibs/ uses its own copy in the DLL folder inside site-packages/numpy.  

You can check https://github.com/opencv/opencv/blob/master/cmake/OpenCVDetectTBB.cmake and https://github.com/opencv/opencv/blob/master/cmake/OpenCVFindMKL.cmake to figure out if the newest version of TBB supported now.  

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\Intel\oneAPI\mkl\latest\redist\intel64\*" "C:\Program Files (x86)\Intel\oneAPI\tbb\latest\redist\intel64\vc14\*"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## LAPACK, BLAS
BLAS is part of the Intel Performance libraries which we installed above.

You don't need to build it. 
LA stands for linear algebra and is the backbone of computer vision and scientific computing.  

## Intel Media SDK
To accelerate video decoding on Intel Graphics, register, download and install [Intel Media SDK](https://software.intel.com/content/www/us/en/develop/tools/media-sdk/choose-download/client.html)  

## Intel RealSense
If you want to use an Intel Realsense cameras (3D or Tracking camera) you might want to install [Intel Realsense](https://www.intelrealsense.com/developers/). 

## Gstreamer & FFMPEG
FFMPEG or gstreamer are needed to receive, decode and encode compressed video streams. 
For example the rtsp web cam streams.  
OpenCV comes with a wrapper for FFMPEG and distributes the necessary libraries and dlls.  
If you use a Jetson single board computer, at the time of this writting, FFMPEG is not GPU accelerated and you likely will want to 
become familiar with gstreamer which is supported by NVIDIA.  

### Gstreamer
For Windows:  
https://gstreamer.freedesktop.org/download/   
or  
https://gstreamer.freedesktop.org/data/pkg/windows/  

Install both
* msvc
* devel msvc

The gst-python bindings are not available on Windows, unfortunately. 
If they were available, we could access gstreamer pipelines directly in python. 

You will need to add `C:\gstreamer\1.0\msvc_x86_64\bin` to your Windows PATH.  
WARNING: Including gstreamer in a python builds can create issues as there are numerous dlls that need to be accessible.

### FFMPEG
FFMPEG is auto downloaded with opencv and it builds a wrapper and does not build againts your own FFMPEG installation. 
There is a suggestion further below how to bypass the wrapper. 
I have not completed the bypass approach and can not recommend it at thist time.
You can obtain your ffmpeg binary and development files here:  
https://ffmpeg.zeranoe.com/builds/ download  
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

For OpenCV 4.3 you need Cuda 10.2.  
For OpenCV 4.5 you need Cuda 11.1.  
For OpenCV 4.5.1 you can use Cuda 11.4

## cuDNN
Login to your NVIDIA account and download [cudnn](https://developer.nvidia.com/rdp/cudnn-download)
Open the archive and copy its content to e.g.   
```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4.```

## NVIDIA Video Codec SDK
Download the Video Codec SDK [VideoSDK](https://developer.nvidia.com/nvidia-video-codec-sdk/download), extract and copy include and lib directories to ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4.```

## TensorFlow prebuilt
TensorFlow needs 
* CUDA which you need to get from https://developer.nvidia.com/cuda-toolkit-archive
  * I recommend to get both lates CUDA 10 as well as
  * CUDA 11
* cuDNN https://developer.nvidia.com/cudnn which needs to match the versions
Open the corresponding archive and copy its content to ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2``` and ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4```

Make sure these are on the PATH
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin```
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\extras\CUPTI\lib64```
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include```
* ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin```

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

## QT [OPTIONAL]
Installing QT takes a very long time. Make sure you install only the components you need to avoid interference with your current ninja and cmake setup.

Install QT from https://www.qt.io/download-open-source. At the bottom is the installer link in green. Login with your QT account. Once you have QT installed use the MaintenanceTool application in the QT folder to make sure you have a valid QT version installed. This can take a long time and might consume about 3GB of storage.

I installed:
* MSVC 32/64bit
* UWP x86/x64
* Sources, QT Charts and all following QT Components
* QT Creator
* QT Debugging Tools for Windows

For OpenCV 4.3.0 you will need qt5.14.2. You can have both 5.14 and 5.15 installed.

## VTK [OPTIONAL]

For Visualization Tool Kit follow description here:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/InstallVTK.md

VTK works by itself and does not need opencv.
OpenCV 4.3.0 vtk interface works with VTK8.2  
OpenCV 4.5.1 vtk interface works with VTK9.0.1 but world needs to be off

## GFLAGS
Download gfalgs
```
cd C:\apps\
mkdir gflags
cd gflags
git clone https://github.com/gflags/gflags
```
```
mv BUILD BUILD.back
mkdir build
cd build
cmake-gui ..\
```
* `CMAKE_INSTALL_PREFIX = C:\apps\gflags\`  
In Visual Studio:  
BUILD All  
BUILD INSTALL

## GLOG Google Logging

Download glog
```
cd C:\apps
mkdir glog
git clone https://github.com/google/glog
```

```
cd glog
mv BUILD BUILD.back
mkdir build
cd build
cmake-gui ..\
```
* `CMAKE_INSTALL_PREFIX = C:\apps\glog\`  
In Visual Studio:   
Build ALL_BUILD  
Build INSTALL  

## DLIB
Machine learning
https://github.com/davisking/dlib
There is sepaarate document on hopw to install dlib.
You should be able to ```pip3 install dlib``` and the build occurs in the background.

## HD5
If you are interested in large datasets you might want to install the HDF library from HDF group. Often researchers use TIFF standard to create large image files, however for very large datasets hdf5 should be considered, especially when the data sets exceed the RAM capacity.

```
cd C:\apps\
git clone https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git
cd hdf5
mkdir build
cd build
cmake-gui ..\
```
* CMAKE_INSTALL_PREFIX = C:/apps/hdf5/

Config->Generate->Open Project
Compile with BatchBuild and enable 64bit Release of INSTALL. When HDF5 build completes configure opencv for HDF5.

## JAVA and ANT
Obtain JDK from https://adoptium.net/

Set JAVA_HOME=C:\Program Files\Eclipse Foundation\jdk-17.0.0.35-hotspot

Follow https://ant.apache.org/manual/install.html#getBinary and download ANT from https://ant.apache.org/bindownload.cgi

Set ANT_HOME=C:\apps\ant

## JavaScript [Optional]
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

## EIGEN
To active the EIGEN library you need to download it
```
cd C:\apps
git clone https://gitlab.com/libeigen/eigen.git
git checkout 3.4
```
## Windows Tools

### MSYS2
Download MSYS2. https://www.msys2.org/ 
Follow the installation instructions on the msys2 website. 

To make the Unix commands available in Power Shell and CMD, in start Windows Power Shell and enter:
```$Env:PATH > path_backup.txt```  This will backup your current path
```Start-Process powershell -Verb runAs```  This will open another powershell with administrator priviledge.  
```setx /M PATH "$ENV:PATH;C:\msys64\usr\bin"``` This will add the msys binaries to your path.

You might want to update and install more commands:  
```pacman -Syu``` updates installation  
```pacman -Su``` updates insytalled packages  
```pacman -S git``` installs git  

### Rapid Environment Editor
To better manage your system path and environmnet variables you might want to install Rapid Environment Editor: https://www.rapidee.com/en/download

### Dependencies
Download the distribution files from https://github.com/lucasg/Dependencies and load the dlls, e.g. opencv_worldxxx.dll and examine the dependencies.

Apparently the following dlls dependency errors can be ignroed:
* API-MS-WIN-*.dll
* EXT-MS-WIN-*.dll
* IESHIMS.dll
* EMCLIENT.dll
* DEVICELOCKHELPERS.dll
* EFSCORE.DLL
* WPAXHOLDER.DLL

## Environment Variables

You will wan to update your path and environment variables. 
I added gstreamer to path. For other components I created a redistribution folder to hold all the dlls and libs from the different packages. There is a size limit for the PATH variable and expanding the path can create a problem.

If you don't know how to do modify the PATH, Rapid Environment Editor is a tool that finds errors and can also help you deal with the PATH when it exceeds the size limit. There are two PATH variables. The global one and the one associated with your account. The one for your account is an addition to the global one.

Environment Variables (Rapid Environment Editor is useful)

* INTELMEDIASDKROOT     = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2020 R1\Software Development Kit
* GSTREAMER_ROOT_X86_64 = C:\apps\gstreamer\1.0\msvc_x86_64
* GSTREAMER_DIR         = C:\apps\gstreamer\1.0\msvc_x86_64
* HDF5_DIR              = C:\apps\HDF5\1.12.1\cmake
* QT_PLUGIN_PATH        = C:\Qt\5.14.2\msvc2017_64\plugins
* JAVA_HOME             = C:\Program Files\AdoptOpenJDK\jdk-11.0.8.10-hotspot\
* OpenBLAS_HOME = C:\apps\openBLAS

PATH

* C:\Python38
* C:\Python38\Scripts
* C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\bin
* C:\Program Files (x86)\Windows Kits\8.1\bin\x64
* C:\gstreamer\1.0\x86_64\bin
* C:\Qt\5.12.8\msvc2017_64\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\libnvvp
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\extras\CUPTI\lib64
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin

## Collecting dll and libs

When building new software packages, one can attempt a) storing libraries and dlls at central location, b) include them with the packages or c) add the location of the dlls to the package path. 
A) When storing them at central location, each time a library (e.g. CUDA) is updated one needs to rebuild the packages depending on them.  
B) If you copy the necessary libraries to the pacakge execution directory you will end up with many copies and need more storage space.
C) In OpenCV there is updated startup file where one can include any directory on the search path. This eliminates the need to "collect" the dlls, but if the original installation files are removed, the package will no longer work.  

For the case of a central repository:  
This is the location where I copied all dlls and binaries. It will need to be added to the PATH:

* C:\pool\bin

We will copy the dlls needed for our package to the "redist" folder. This needs about 3.5 GBytes. When you build shared libs, dll files are needed, otherwise libraries (*.lib)
```
REM   INTEL Media SDK ===
copy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2020 R1\Software Development Kit\bin\x64\*" C:\pool\bin /y

REM   INTEL RealSense ==
copy  "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" C:\pool\bin /y

REM   INTEL MKL ========
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" C:\pool\bin /s/h/i/e/y

REM   INTEL TBB ========
xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\*" C:\pool\bin /s/h/i/e/y

REM   INTEL compiler ===
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\compiler\*" C:\pool\bin /y

REM   Intel MPI ========
REM copy   "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\*" C:\pool\bin /y
REM copy   "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\release\*" C:\pool\bin /y
REM xcopy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\etc\*" C:\pool\etc  /s/h/i/e/y

REM   INTEL IPP ========
REM copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\ipp\*" C:\pool\bin /y

REM   INTEL DAAL =======
REM copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\daal\*" C:\pool\bin /y
```
