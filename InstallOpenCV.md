# Compiling OpenCV on Windows 10
This guide is adapted from [James Bowley] (https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd).

## Pre Requisits

### Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.

### Install Visual Studio
Install Visual Studio Community from [Microsoft] (https://visualstudio.microsoft.com/downloads/) and install the the option for develoment for desktop application in C.

### Open CV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. I place them in the root folder C:/ but they can go anywhere. 

```
cd C:/
git clone https://github.com/opencv/opencv.git --branch 4.2.0
git clone https://github.com/opencv/opencv_contrib.git --branch 4.2.0
```

### CMake
Install CMake that comes with CMake GUI. Install release version.
https://github.com/Kitware/CMake/releases/download/v3.16.5/cmake-3.16.5-win64-x64.msi

### CUDA
Install CUDA Tookit from NVIDIA. 
Useful only if you have NVIDA GPU.

### NVIDIA video codec SDK
Optional: Download the Video Codec SDK, extract and copy include and lib directories to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vx.x

### Intel Media SDK
Optional: To accelerate video decoding on Intel CPU’s register and download and install Intel Media SDK

### Windows SDK 
Windows SDK includes DirectX SDK. When you rerun the installer you  might want to add options to Windows SDK that are not yet installed.

### Intel TBB, MKL, MPI, IPP, DAAL
To accelerate some OpenCV operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. 

### Intel RealSense
If you want to use an Intel Realsense camera you might want to install [Intel Realsense] (https://www.intelrealsense.com/developers/)
Add realsense2.dll to path its in C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64

### Ninja
Install Chocolatey https://chocolatey.org/
Then install Ninka with
```
choco install ninja
```

### Python
Python 2.7 is no longer supported and when both 3.x and 2.x are installed the compilation might fail at the final stages of the build. Either make sure both versions of Python are 64bit or remove references to 2.7 in cmake-gui and remove python2.7 from your computer.

Download get-pip.py from https://bootstrap.pypa.io/
Open command shell and cd to location of get-pip.py and execute following

```
py -3 get-pip.py
py -3 -m pip install pip --upgrade
py -3 -m pip install numpy --upgrade
py -3 -m pip install pylint --upgrade
py -3 -m pip install flake8 --upgrade
```

## QT
Not recommended on Windows
Download QT from https://www.qt.io/download-open-source
At the bottom is installer link in green
Login with QT account

## Gstreamer
https://gstreamer.freedesktop.org/download/
https://gstreamer.freedesktop.org/data/pkg/windows/1.16.2/
* msvc
* devel msvc

The gst-python bindings are not available on Windows unfortunately.

## FFMPEG
From https://ffmpeg.zeranoe.com/builds/ download
Version:latest stable
Architecture: Windows 64 bit
Linking: Shared and Dev
Unzip and install in ffmpeg folder 

FFMPEG is autodownloaded with opencv and it builds a wrapper and does not directly include the FFMPPEG includes.

## Unistall old opencv version
```
pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
```

### Environment Variables
You might want to update your path and environment variables

* INTELMEDIASDKROOT = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_DIR = C:\gstreamer\1.0\x86_64
* GSTREAMER_ROOT_X86_64 = C:\gstreamer\1.0\x86_64

PATH
* C:\Python38
* C:\Python38\Scripts
* C:\ffmpeg\bin
* C:\gstreamer\1.0\x86_64\bin
* C:\Program Files (x86)\Windows Kits\8.1\bin\x64

## Prepare Shell Environment

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
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
set "generator=Ninja"
```

## Build 1

### Let's start light (defaults, with gstreamer)

```
"C:\Program Files\CMake\bin\cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" -DCMAKE_BUILD_TYPE=%buildType% -DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" -DOPENCV_ENABLE_NONFREE=ON -DBUILD_SHARED_LIBS=ON -DBUILD_opencv_python3=ON -DBUILD_EXAMPLES=OFF -DINSTALL_PYTHON_EXAMPLES=OFF -DINSTALL_C_EXAMPLES=OFF -DINSTALL_TESTS=OFF
```

### Update Build Variables
Run configure with GUI cmake to verify setup.
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
and then make sure the following variables are set:

* BUILD_SHARED_LIBS=ON
* BUILD_opencv_python3=ON 

This saves some time:

* BUILD_EXAMPLES=OFF **
* INSTALL_PYTHON_EXAMPLES=OFF **
* INSTALL_C_EXAMPLES=OFF **
* INSTALL_TESTS=OFF**

### Build

And finally do first build using Ninja:
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

### Test
#### Run some camera tests
```
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera

gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
```

#### Now test with opencv
Since this build included gstreamer we should copy the dlls to our search path
```
copy "C:\gstreamer\1.0\x86_64\bin\*" "C:\opencv\build\install\x64\vc16\bin"
xcopy "C:\gstreamer\1.0\x86_64\lib" "C:\opencv\build\install\x64\vc16\lib" /E/H
```

```
C:\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

Now check with test_rtsp_simplegstramer.py

## Build 2
Now lets enable Intel optimizations, Intel Media SDK and Intel Realsense.

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
"C:\Program Files\CMake\bin\cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" -DCMAKE_BUILD_TYPE=%buildType% -DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" -DOPENCV_ENABLE_NONFREE=ON -DBUILD_SHARED_LIBS=ON -DBUILD_opencv_python3=ON -DBUILD_EXAMPLES=OFF -DINSTALL_PYTHON_EXAMPLES=OFF -DINSTALL_C_EXAMPLES=OFF -DINSTALL_TESTS=OFF -DBUILD_opencv_world=OFF -DWITH_GSTREAMER=ON -DWITH_MFX=ON -DWITH_MKL=ON -DMKL_USE_MULTITHREAD=ON -DMKL_WITH_TBB=ON -DWITH_TBB=ON -DWITH_LIBREALSENSE=ON -DLIBREALSENSE_INCLUDE_DIR="C:/Program Files (x86)/Intel RealSense SDK 2.0/include" -DLIBREALSENSE_LIBRARIES="C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib"
```

### Build
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

### Test
Make sure dlls are in the search path:
```
C:\opencv\build\install\setup_vars_opencv4.cmd
copy "C:\gstreamer\1.0\x86_64\bin\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc_mt\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64\*" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" "C:\opencv\build\install\x64\vc16\bin"
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\compiler\*.dll" "C:\opencv\build\install\x64\vc16\bin"
```
Jeezz 200 dlls ...

## Build 3
Inlucde CUDA

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
QT_PLUGIN_PATH = C:\Qt\5.14.1\msvc2017_64\plugins

If this worked ok, we can try to include CUDA support. CUDA compiled opencv will not run if there is no NVIDIA GPU on the system.



### Create single library to include all features
* BUILD_opencv_world=ON


### Build against FFMPEG and not the opencv FFMPEG wrapper
You need to add the text below to beginning of
modules/videoio/cmake/detect_ffmpeg.cmake

'''
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
'''

* FFMPEG_ROOT_DIR="PATH_TO_FFMPEG_DEV"

## GSTREAMER
* WITH_GSTREAMER=ON

### Graphics Libraries
* WITH_OPENGL=ON
* WITH_QT=ON
* Qt5_DIR = C:/Qt/Qt5.14.1/5.14.1/msvc2017_64/lib/cmake/Qt5

Rerun configure and generate in cmake-gui.

* BUILD_opencv_rgbd=OFF, does not compile


Include CUDA support in build scripts:
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```

There are issues with rgbd and nonfree modules. [Issue] (https://github.com/opencv/opencv_contrib/issues/2307)

Still working on that.

You might want to rename build/install to build/install_noCUDA so you can compare or install on other computers without rebuilding.

```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

Wiil have many DLL interface warnings. Ignore them. It might take 3 hours to complete.

Now that we have dll and CUDA suport where does library need to go? Check variable script in install folder.


```
dumpbin C:\Python38\Lib\site-packages\cv2\python-3.8\cv2.cp38-win_amd64.pyd /IMPORTS | findstr dll
```
make sure each dll is found with
```
where dllname
```

