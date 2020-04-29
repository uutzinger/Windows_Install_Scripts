# Compiling OpenCV on Windows 10
This guide is adapted from [James Bowley] (https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd).

## Debug
The two main issues you will need to solve is to a) find appropriate binaries and packages to include into your build and reference the appropraite directories and libs b) and to make sure the dlls that those packages need are in the search path when cv2 is loaded. Although you can enable world build which creates a single dll for opencv, the support packages still have their own dlls. I counted about 200 additional dll if you make a large build.

There are two ways to find missing dlls:
### Dumpbin
```
dumpbin C:\Python38\Lib\site-packages\cv2\python-3.8\cv2.cp38-win_amd64.pyd /IMPORTS | findstr dll
```
Make sure each dll listed is found in you CMD windows with:
```
where dllname_from_previous_output
```
There is issue that pyd file can fail to complete loading of dll because dlls outside of it fail to load.

### procmon
[Procmon](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) allows to monitor file system activity.
I start python and stop procmon minitoring and cleart the output. Then I start activity monitoring and type import cv2 in python and stop monitoring as soon as the error appears. The I use filter and find tool in procmon [Filter Result is not SUCCESS]. Find python.exe, step backwards.

## Pre Requisits

### Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.
OpenCV still supports python 2.7 but compilation fails at the final stages of the build if one version is 32bit and the other 64bit. 

### Install Visual Studio
Install Visual Studio Community from [Microsoft](https://visualstudio.microsoft.com/downloads/) and install the the option for develoment for desktop application in C.

### Open CV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. I place them in the root folder C:/ but they can go anywhere. 

```
cd C:/
git clone https://github.com/opencv/opencv.git --branch 4.2.0
git clone https://github.com/opencv/opencv_contrib.git --branch 4.2.0
```

### CMake
Install CMake with latest release version. [Kitware](https://github.com/Kitware/CMake/releases/)

### CUDA
Install CUDA Tookit from [NVIDIA](https://developer.nvidia.com/cuda-downloads)
This is only useful if you have an NVIDA GPU.

### cuDNN
Login to your NVIDIA account and download [cudnn](https://developer.nvidia.com/rdp/cudnn-download)
Open the archive and copy its content to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vxx.x

### NVIDIA video codec SDK
Optional: Download the Video Codec SDK, extract and copy include and lib directories to 
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vx.x
[VideoSDK](https://developer.nvidia.com/nvidia-video-codec-sdk/download)

### Intel Media SDK
Optional: To accelerate video decoding on Intel CPU’s, register, download and install [Intel Media SDK](https://software.intel.com/en-us/media-sdk)

### Windows SDK 
When you install Visual Studio Compiler you can select Windows 10 SDK (10.0.18362.0) in the Installer. Windows SDK includes DirectX SDK. When you rerun the Visual Studio installer you might want to add options to Windows SDK that are not yet installed. [SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)

### Intel TBB, MKL, MPI, IPP, DAAL
To accelerate some OpenCV operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. [Intel libraries](https://software.seek.intel.com/performance-libraries). Use Microsoft Edge to download as website has issues with Chrome.

### LAPACK BLAS
BLAS is part of the Intel Performance libraries. You dont need to build it. If you want to build it you can download the source [LAPACK] (http://www.netlib.org/lapack/) and build it but you need a FORTRAN compiler (see Build Instructions for LAPACK 3.5.0 for Windows with Visual Studio in http://icl.cs.utk.edu/lapack-for-windows/lapack. You might also be able to use pre built libraries from https://icl.cs.utk.edu/lapack-for-windows/lapack/ using http://icl.cs.utk.edu/lapack-for-windows/lapack/LAPACKE_examples.zip.

### Intel RealSense
If you want to use an Intel Realsense cameras (3D or Tracking camera) you might want to install [Intel Realsense] (https://www.intelrealsense.com/developers/). You need to add realsense2.dll to system path. It is location in C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64

### Ninja
To speed up the build, NINJA is preferred tool over Visual Studio as it speeds up the build significantly. You will still use the microsoft compiler from Visual Studio but ninja will call it.

Install [Chocolatey](https://chocolatey.org/) then install Ninja with
```
choco install ninja
```

### Python Packages
Download get-pip.py from https://bootstrap.pypa.io/
Open command shell and cd to location of get-pip.py and execute following
```
py -3 get-pip.py
py -3 -m pip install pip --upgrade
py -3 -m pip install numpy --upgrade
py -3 -m pip install pylint --upgrade
py -3 -m pip install flake8 --upgrade
```

### QT
Not all opencv components compile nicely when QT is enabled and unless you really need QT functionality enabled, I don't recommended it on Windows as first build. To insgtall QT download it from https://www.qt.io/download-open-source. At the bottom is installer link in green. Login with your QT account. One you have the QT installed use the MaintenanceTool application in the QT folder to make sure you have a valid QT version installed. This can take a long time and might consume 3GB of storage.

### Gstreamer
OpenCV can use gstreamer and comes with wrapper for FFMPEG. If you use Jetson single board computers you will need to get familiar with gstreamer as NVIDIA does not provide support for FFMPEG. You need those tools for creating, receiving and modifing video streams. For example the rtsp web cam streams.
https://gstreamer.freedesktop.org/download/
or
https://gstreamer.freedesktop.org/data/pkg/windows/
Install both
* msvc
* devel msvc
The gst-python bindings are not available on Windows unfortunately.

### FFMPEG
FFMPEG is auto downloaded with opencv and it builds a wrapper and does not build againts your own FFMPPEG includes. There is suggestion below how to bypass the wrapper. If you want to test FFMPEG you can get the packages as following:
From https://ffmpeg.zeranoe.com/builds/ download
Version:latest stable
Architecture: Windows 64 bit
Linking: Shared and Dev
Unzip and install in your ffmpeg folder 

### HDF5
If you are intersted in large datasets you might want to install the HDF library from HDF group.
https://www.hdfgroup.org/downloads/hdf5/
Make an account and obtain the vs14.zip version.
lib and include folders are in C:/Program Files/HDF_Group/HDF5/x.yy.z/lib/ and include folders.

### js
BUILD_opencv_js=ON requires EMscripten.
```
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
emsdk install latest
emsdk activate latest
emsdk_env.bat
```
You will need to run emsdk_env.bat in each shell/cmd window to activate the components.

### Matlab
WITH_MATLAB=ON requires mex and some libraries to be found. In matlab command prompt: mex -setup
This is not yet working in my setup as Matlab interface is not built.

### EIGEN
To active the EIGEN library you need to download it
git clone https://gitlab.com/libeigen/eigen.git
and set 
WITH_EIGEN=ON
EIGEN_INCLUDE_PATH="path_to_eigen/eigen/Eigen"

### Building Dependencies from Source
It should not be necessary to build these dependencies
```
git clone https://gitlab.com/libeigen/eigen.git
git clone https://github.com/oneapi-src/oneTBB.git
git clone https://github.com/AcademySoftwareFoundation/openexr.git
git clone git://code.qt.io/qt/qt5.git
cd qt5
git checkout 5.15.0
https://wiki.qt.io/Building_Qt_5_from_Git#Getting_the_source_code
https://structure.io/openni
```

## Unistall old opencv version
To make sure python finds your build you will want to remove any other installations of opencv.
```
pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
```

## Environment Variables
You might want to update your path and environment variables:

* INTELMEDIASDKROOT = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_DIR = C:\gstreamer\1.0\x86_64
* GSTREAMER_ROOT_X86_64 = C:\gstreamer\1.0\x86_64

PATH
Programming
* C:\Python38
* C:\Python38\Scripts
* C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\bin

Streamers
* C:\gstreamer\1.0\x86_64\bin
* C:\gstreamer\1.0\x86_64\lib\gstreamer-1.0
* C:\gstreamer\1.0\x86_64\lib
* C:\ffmpeg\bin

Intel
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2020.1.216\windows\mpi\intel64\bin
* C:\PROGRA~2\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries_2020.0.166\windows\mpi\intel64\bin
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc_mt
* C:\PROGRA~2\Intel RealSense SDK 2.0\bin\x64

CUDA
* C:\PROGRA~1\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin
* C:\PROGRA~1\NVIDIA GPU Computing Toolkit\CUDA\v10.2\libnvvp

* C:\Program Files (x86)\Windows Kits\8.1\bin\x64

## Prepare your Shell Build Environment

Open command prompt and enter the following commands with directories pointing to your installations
```
cd C:/opencv
mkdir build
cd build
```

```
set "openCvSource=C:\opencv"
set "openCVExtraModules=C:\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Ninja"
```

```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
```

When you execute the vcvars script twice in a row, it will throw error the second time. You can ignore that.

## Build
Here it have 3 builds with increasing complexity. Its not a good idea to enable all settings at once and then to struggle through the errors. Its better to start with smaller build and then expand.

## Build 1

### Let's Start Light (minimal)
```
"C:\Program Files\CMake\bin\cmake.exe" ^
-B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" ^
-DOPENCV_ENABLE_NONFREE=ON ^
-DBUILD_SHARED_LIBS=ON ^
-DOPENCV_PYTHON3_VERSION=ON ^
-DPYTHON_DEFAULT_EXECUTABLE="C:\Python38\python.exe"
-DBUILD_EXAMPLES=OFF ^
-DBUILD_DOCS=OFF ^
-DBUILD_TESTS=OFF ^
-DBUILD_PERF_TESTS=OFF ^
-DINSTALL_PYTHON_EXAMPLES=OFF ^
-DINSTALL_C_EXAMPLES=OFF ^
-DINSTALL_TESTS=OFF
```

### Update Build Variables
Run configure with GUI cmake to verify setup.
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
There might be entries in RED, meaning cmake-gui would like you to reconfigure them. If you start this process you need to complete it as it will overwrite your previous cmake call.

For a light build, following options are usually off:
* WITH_GSTREAMER
* WITH_MFX
* WITH_MKL
* WITH_TBB
* WITH_EIGEN
* WITH_LIBREALSENSE
* BUILD_opencv_hdf

Make sure this is on:
* BUILD_opencv_python3

### Build
And finally do first build using Ninja:
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

### Test

#### DLLs
Copy all necessary dlls into the installation path in the opencv build directory. This is in the range of 1GB.

It is likely cmake picked up the intel libraries:
```
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc_mt\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\compiler\*.dll" "C:\opencv\build\install\x64\vc16\bin"
```
It is also possible that gstreamer was picked up without you enabeling it. This will copy a lot of files:
```
copy "C:\gstreamer\1.0\x86_64\bin\*" "C:\opencv\build\install\x64\vc16\bin"
xcopy "C:\gstreamer\1.0\x86_64\lib" "C:\opencv\build\install\x64\vc16\lib" /E/H
```
Likely the realsense camera was not automatically includes but you might want to copy dlls anyway:
```
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" "C:\opencv\build\install\x64\vc16\bin"
```

HDF has bin in path but not lib
C:/Program Files/HDF_Group/HDF5/1.12.0/lib/

Intel Media SDK is not on path
CUDA bin is on path bot not lib

C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include
C:/Program Files/AdoptOpenJDK/jdk-11.0.6.10-hotspot/include
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core.lib

#### Test opencv
```
C:\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

## Build 2
Now lets enable Intel optimizations, Intel Media SDK and Intel Realsense and Eigen.

### Setup Shell
```
set "openCvSource=C:\opencv"
set "openCVExtraModules=C:\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
set "generator=Ninja"
```
### Configure Build
```
"C:\Program Files\CMake\bin\cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" ^
-DOPENCV_ENABLE_NONFREE=ON ^
-DBUILD_SHARED_LIBS=ON ^
-DBUILD_opencv_python3=ON ^
-DBUILD_EXAMPLES=OFF ^
-DBUILD_DOCS=OFF ^
-DBUILD_TESTS=OFF ^
-DBUILD_PERF_TESTS=OFF ^
-DINSTALL_PYTHON_EXAMPLES=OFF ^
-DINSTALL_C_EXAMPLES=OFF ^
-DINSTALL_TESTS=OFF ^
-DBUILD_opencv_world=OFF ^
-DWITH_GSTREAMER=ON ^
-DWITH_MFX=ON ^
-DWITH_MKL=ON ^
-DMKL_USE_MULTITHREAD=ON ^
-DMKL_WITH_TBB=ON ^
-DWITH_TBB=ON ^
-DWITH_EIGEN=ON ^
-DEIGEN_INCLUDE_PATH="C:/opencv/dep/eigen/Eigen" ^
-DWITH_LIBREALSENSE=ON ^
-DLIBREALSENSE_INCLUDE_DIR="C:/Program Files (x86)/Intel RealSense SDK 2.0/include" ^
-DLIBREALSENSE_LIBRARIES="C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib" ^
-DBUILD_opencv_hdf=ON ^
-DHDF5_C_LIBRARY="C:/Program Files/HDF_Group/HDF5/1.12.0/lib/libhdf5.lib" ^
-DHDF5_INCLUDE_DIRS="C:/Program Files/HDF_Group/HDF5/1.12.0/include"
```
### Intel Optimization Thread Building Blocks
* WITH_TBB=ON

### Intel Optimization Math Kernel Library
* WITH_MKL=ON **
* MKL_WITH_TBB=ON 
* MKL_USE_MULTITHREAD=ON

### MFX
* WITH_MFX=ON

### Real
* WITH_LIBREALSENSE=ON
* LIBREALSENSE_INCLUDE_DIR C:/Program Files (x86)/Intel RealSense SDK 2.0/include
* LIBREALSENSE_LIBRARIES C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib

### Build
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```
### Test
Make sure dlls are in the search path:
```
copy "C:\gstreamer\1.0\x86_64\bin\*" "C:\opencv\build\install\x64\vc16\bin"
xcopy "C:\gstreamer\1.0\x86_64\lib" "C:\opencv\build\install\x64\vc16\lib" /E/H
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc_mt\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy  "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" "C:\opencv\build\install\x64\vc16\bin"
copy  "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\compiler\*.dll" "C:\opencv\build\install\x64\vc16\bin"
```
Jeezz 200 dlls ...

### Test
#### Camera
```
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera

gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
```

#### OpenCV
```
C:\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

Now check with test_rtsp_simplegstramer.py

## Build 3
Inlucde CUDA. This builds upon previous two builds and enables most features

```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```

### CUDA
* WITH_NVCUVID=OFF 
* WITH_CUDA=ON
* CUDA_FAST_MATH=ON 
* WITH_CUBLAS=ON 
* CUDA_ARCH_PTX=7.5
* CUDA_ARCH_PTX=7.5 
* CUDA_TOOLKIT_ROOT_DIR="C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2"
* CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2
* OPENCV_DNN_CUDA=ON
* CUDA_BUILD_EMULATION=OFF

Needs to be on path
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin

Python will need all qt dlls from ```C:\Qt\5.14.1\msvc2017_64\bin``` copied to ```C:/Python38\Lib\site-packages\cv2\python-3.8\```

### Env Variable
QT_PLUGIN_PATH = C:\Qt\5.x.y\msvc2017_64\plugins

If this worked ok, we can try to include CUDA support. CUDA compiled opencv will not run if there is no NVIDIA GPU on the system.

### Create single library to include all features
* BUILD_opencv_world=ON

## GSTREAMER
* WITH_GSTREAMER=ON

### HDF
* BUILD_opencv_HDF=ON
* HDF5_C_LIBRARY = C:/Program Files/HDF_Group/HDF5/1.12.0/lib/libhdf5.lib
* HDF5_INCLUDE_DIRS = C:/Program Files/HDF_Group/HDF5/1.12.0/include/static
Not tested yet.

### Graphics Libraries
* WITH_OPENGL=ON
* WITH_QT=ON
* Qt5_DIR = C:/Qt/5.x.y/msvc2017_64/lib/cmake/Qt5
With x.y the QT version you downloaded.
Rerun configure and generate in cmake-gui.

You will need to disable rgbd as it does not compile with rgbd. [Issue] (https://github.com/opencv/opencv_contrib/issues/2307)

* BUILD_opencv_rgbd=OFF

If you have previous builds you might want to rename build/install to build/install_noCUDA so you can preserve non_cuda version.

### Build
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

This will create many DLL interface warnings. Ignore them. It might take 3 hours to complete.
Now that we have dll and CUDA suport where does library need to go? Check variable script in install folder.

```
dumpbin C:\Python38\Lib\site-packages\cv2\python-3.8\cv2.cp38-win_amd64.pyd /IMPORTS | findstr dll
```
make sure each dll is found with
```
where dllname
```

### Optional: Build against FFMPEG and not the opencv FFMPEG wrapper
You need to add the text below to beginning of
modules/videoio/cmake/detect_ffmpeg.cmake

```
if(FFMPEG_ROOT_DIR AND WIN32 AND NOT ARM)
  find_path(AVCODEC_INCLUDE_DIR libavcodec/avcodec.h PATHS ${FFMPEG_ROOT_DIR}/include/)
  find_library(AVCODEC_LIBRARY lib/avcodec.lib PATHS ${FFMPEG_ROOT_DIR})
  set(FFMPEG_INCLUDE_DIRS ${AVCODEC_INCLUDE_DIR})
  set(FFMPEG_LIBRARIES ${AVCODEC_LIBRARY})

  find_path(AVFORMAT_INCLUDE_DIR libavformat/avformat.h PATHS ${FFMPEG_ROOT_DIR}/include/)
  find_library(AVFORMAT_LIBRARY lib/avformat.lib PATHS ${FFMPEG_ROOT_DIR})
  list(APPEND FFMPEG_INCLUDE_DIRS ${AVFORMAT_INCLUDE_DIR})
  list(APPEND FFMPEG_LIBRARIES ${AVFORMAT_LIBRARY})

  find_path(AVUTIL_INCLUDE_DIR libavutil/avutil.h PATHS ${FFMPEG_ROOT_DIR}/include/)
  find_library(AVUTIL_LIBRARY lib/avutil.lib PATHS ${FFMPEG_ROOT_DIR})
  list(APPEND FFMPEG_INCLUDE_DIRS ${AVUTIL_INCLUDE_DIR})
  list(APPEND FFMPEG_LIBRARIES ${AVUTIL_LIBRARY})

  find_path(AVDEVICE_INCLUDE_DIR libavdevice/avdevice.h PATHS ${FFMPEG_ROOT_DIR}/include/)
  find_library(AVDEVICE_LIBRARY lib/avdevice.lib PATHS ${FFMPEG_ROOT_DIR})
  list(APPEND FFMPEG_INCLUDE_DIRS ${AVDEVICE_INCLUDE_DIR})
  list(APPEND FFMPEG_LIBRARIES ${AVDEVICE_LIBRARY})

  find_path(SWSCALE_INCLUDE_DIR libswscale/swscale.h PATHS ${FFMPEG_ROOT_DIR}/include/)
  find_library(SWSCALE_LIBRARY lib/swscale.lib PATHS ${FFMPEG_ROOT_DIR})
  list(APPEND FFMPEG_INCLUDE_DIRS ${SWSCALE_INCLUDE_DIR})
  list(APPEND FFMPEG_LIBRARIES ${SWSCALE_LIBRARY})

  set(HAVE_FFMPEG TRUE)
endif()
```

* FFMPEG_ROOT_DIR="PATH_TO_FFMPEG_DEV"


# Complete Build Script

```
set "openCvSource=C:\opencv"
set "openCVExtraModules=C:\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
set "generator=Ninja"

cd C:/opencv
mkdir build
cd build

"C:\Program Files\CMake\bin\cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" ^
-DOPENCV_ENABLE_NONFREE=ON ^
-DBUILD_SHARED_LIBS=ON ^
-DBUILD_opencv_python3=ON ^
-DBUILD_EXAMPLES=OFF ^
-DINSTALL_PYTHON_EXAMPLES=OFF ^
-DINSTALL_C_EXAMPLES=OFF ^
-DINSTALL_TESTS=OFF ^
-DBUILD_opencv_world=ON ^
-DWITH_GSTREAMER=ON ^
-DWITH_MFX=ON ^
-DWITH_MKL=ON ^
-DMKL_USE_MULTITHREAD=ON ^
-DMKL_WITH_TBB=ON ^
-DWITH_TBB=ON ^
-DWITH_LIBREALSENSE=ON ^
-DLIBREALSENSE_INCLUDE_DIR="C:/Program Files (x86)/Intel RealSense SDK 2.0/include" ^
-DLIBREALSENSE_LIBRARIES="C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib" ^
-DWITH_NVCUVID=OFF ^
-DWITH_CUDA=ON ^
-DCUDA_FAST_MATH=ON ^
-DWITH_CUBLAS=ON ^
-DCUDA_ARCH_BIN=7.5 ^
-DCUDA_ARCH_PTX=7.5 ^
-DCUDA_TOOLKIT_ROOT_DIR="C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2" ^
-DCUDA_SDK_ROOT_DIR="C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2" ^
-DOPENCV_DNN_CUDA=ON ^
-DCUDA_BUILD_EMULATION=OFF ^
-DBUILD_opencv_HDF=ON ^
-DHDF5_C_LIBRARY="C:/Program Files/HDF_Group/HDF5/1.12.0/lib/libhdf5.lib" ^
-DHDF5_INCLUDE_DIRS="C:/Program Files/HDF_Group/HDF5/1.12.0/include" ^
-DWITH_OPENGL=ON ^
-DBUILD_opencv_rgbd=OFF ^
-DWITH_QT=ON ^
-DQt5_DIR="C:/Qt/5.14.2/msvc2017_64/lib/cmake/Qt5" ^
-DQT_PLUGIN_PATH="C:\Qt\5.14.2\msvc2017_64\plugins"

"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install

C:\opencv\build\install\setup_vars_opencv4.cmd
copy "C:\gstreamer\1.0\x86_64\bin\*" "C:\opencv\build\install\x64\vc16\bin"
xcopy "C:\gstreamer\1.0\x86_64\lib" "C:\opencv\build\install\x64\vc16\lib" /E/H
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc_mt\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\compiler\*.dll" "C:\opencv\build\install\x64\vc16\bin"
```
