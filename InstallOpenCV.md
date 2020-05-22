# Compiling OpenCV on Windows 10
## Motivation
There are many reasons to build your own openCV binaries. The issue with building your own binaries are the many temptations of enabling components that you dont really need but break your build.

I want to enable gstreamer and architecture specific accelerations. In particular Intel optimized libraries and CUDA support.
I need to eanble gstreamer because I want to develop python code for Jetson single board computers on my notebook computer. Nividia supports gstreamer with hardware acceeration on Jetson architecture. It does not support ffmpeg. I would like to be able to read rtsp camera streams because I have applications that limit network traffic. I want to be able to use the same USB cameras on arm based single board computers and my notebook computer. I also have projects that utilize the Intel RealSense platform. I need architeture optimization because I will attempt using high frame rate cameras in my research.

The temptations I encountered are: Enabling Eigen, Matlab, JavaScript, Java, HDF5. Intel TBB, IPP, MKL and CUDA are complex enough to build into opencv for architecture opimization. I don't program in Java nor JavaScript. I have over many years used Matlab for scientific computing but I dont need to build an opencv interface for Matlab, as I can obtain that through Mathworks when the need arises. If I have issue of needing to save and read very large files (>2Gb), I can check into packages other than opencv that provide that functionality.

## Approach
This guide's purpose is to build opencv in several steps and with increasing complexity.

It is common that the activation of one component creates a set of issues that need to be solved. Also the activation of one component (e.g. gstreamer) can not be reverted even when attempting to turn off the component in the build script.
It is also common that the cmake and cmake-gui do not create the same build configuration. Often there is more than one cmake version installed on your computer.

I prefer building with Ninja because opencv build times are very long and Ninja reduces them significantly. 

Many online posts have been consulted for this script e.g. [James Bowley](https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd) and https://dev.infohub.cc/build-opencv-410/ and
https://dev.infohub.cc/build-opencv-430-with-cuda/

### Fun
This explains algorithm optimizationsby Intel for opencv.
https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel
This is excellent summary of the Halide algorithm development tools https://halide-lang.org/ It explains why some programs finish an image processing task much faster than others.

## Pre Requisits

Prepare your system with https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md

### Open CV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. I place them in the root folder C:/opencv but they can go anywhere. I usually attempt installing release versions and not the latest version. At times it can be confusing on GitHub to identify the latest release. You can check openCV [Documentation](https://docs.opencv.org/) and when you select Doxygen HTML you will have a pull down menu and can identify the highest version number that is not -dev -beta or -alpha. 

```
mkdir C:/opencv
cd C:/opencv
git clone https://github.com/opencv/opencv.git --branch 4.3.0
git clone https://github.com/opencv/opencv_contrib.git --branch 4.3.0
cd C:/opencv/opencv
mkdir build
```

## Unistalling of Previous opencv Installtions
To make sure python finds your build you will want to remove any other installations of opencv.
```
pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
```

## Prepare your Shell Build Environment

Open a command prompt (CMD) and enter the following commands with directories pointing to your installations
```
cd C:/opencv/opencv/build
set "openCvSource=C:\opencv\opencv"
set "openCVExtraModules=C:\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
```

When you execute the vcvars script twice in a row, it will throw error the second time. You can ignore that.

## Build
Here I show 3 builds with increasing complexity. Its not a good idea to enable all settings at once and then to struggle through the errors. Its better to start with a smaller build and then expand.

## Build 1 STATUS: Completed Successfully.
With this first build, I will not use the command line option. We will start directly with cmake-gui.
You should not need to worry about dlls. It is a light build with just the default settings, extra and non free modules and python.

### Let's Start Light (minimal)
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
* Clear Build Cache. This will remove any revious configuration options.
* Run configure. Select Visual Studio 16 2019 as your compiler environment. Select native compilers.

### Verify Build Variables
There will entries in RED, meaning cmake-gui would like you to take a look at them. 
Please verify:

For a light build, many options are usually off such as:

Video
* WITH_GSTREAMER = OFF
* WITH_MFX = OFF, Intel Video Acceleration
* WITH_MKL = OFF, Intel Math Library
* WITH_LIBREALSENSE = OFF, Intel Real Sense Camera

Math Acceleration
* WITH_TBB = OFF, Intel Threadbuilding Blocks
* WITH_EIGEN = OFF

Examples and Tests
* BUILD_EXAMPLES = OFF
* BUILD_DOCS = OFF
* BUILD_TESTS = OFF
* BUILD_PERF_TESTS = OFF
* INSTALL_PYTHON_EXAMPLES = OFF
* INSTALL_C_EXAMPLES = OFF
* INSTALL_TESTS = OFF

Make sure this is ON or set:
* BUILD_opencv_python3 = ON
* BUILD_opencv_python2 = OFF
* OPENCV_EXTRA_MODULES_PATH = "C:/opencv/opencv_contrib/modules"
* OPENCV_ENABLE_NONFREE = ON
* BUILD_SHARED_LIBS = ON, usually dlls are more memory and space efficient, but if you run into dll missing errors you might want this off
* BUILD_opencv_world = ON, create single dll
* OPENCV_PYTHON3_VERSION = ON, not sure, it might have issue with cmake-gui
* CPU_BASELINE, should autopopulate to your CPU
* BUILD_opencv_hdf = OFF, HDF5 file format

Modify or create the variable:
* PYTHON_DEFAULT_EXECUTABLE = "C:\Python38\python.exe"
* CMAKE_CONFIGURATION_TYPES = "Release"

### Configure and Generate
After successful configuratin, CMAKE should have found python2 and python3 as well as your java environment. If python or java environment is not found you can attempt running the CMD line version below and then revisit it with cmake-gui as shown above. Dont delete the cache. Just rerun configure in the gui.

Run the Generate fucntion. Hopefully there will be no errors or the errors and warning allow you to still build opencv.

### CMD Shell Equivalent
The equivalent command in the CMD window is listed below. 
However for this first step, using the GUI version appears to be more reliable.

Optional:

```
"C:\Program Files\CMake\bin\cmake.exe" ^
-B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" ^
-DOPENCV_ENABLE_NONFREE=ON ^
-DBUILD_SHARED_LIBS=ON ^
-DOPENCV_PYTHON3_VERSION=ON ^
-DPYTHON_DEFAULT_EXECUTABLE="C:\Python38\python.exe" ^
-DBUILD_EXAMPLES=OFF ^
-DBUILD_DOCS=OFF ^
-DBUILD_TESTS=OFF ^
-DBUILD_PERF_TESTS=OFF ^
-DINSTALL_PYTHON_EXAMPLES=OFF ^
-DINSTALL_C_EXAMPLES=OFF ^
-DINSTALL_TESTS=OFF ^
-DWITH_GSTREAMER=OFF
```

### Build
And finally do first build using cmake in command line:
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```
or call the compiler with "Open_Project" in cmake-gui. Select build / batch build and enable INSTALL and build. If there are previous versions you can clean the files with "clean" button.

### Collect DLLs
If you had dlls built you  might want to collect them at single location and add that location to the PATH.

```
REM   OpenCV ===========
copy  "C:\opencv\opencv\build\install\x64\vc16\bin\*" C:\opencv\opencv_redist /y
REM copy  "C:\opencv\opencv\build\install\x64\vc16\lib\*" C:\opencv\opencv_redist /y
copy  "C:\opencv\opencv\build\install\java\*" C:\opencv\opencv_redist /y
REM copy  "C:\opencv\opencv\build\install\bin\*" C:\opencv\opencv_redist /y
```

### Test
```
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -2 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -2 -c "import cv2; print(cv2.getBuildInformation())"
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

## Build 2
Now lets enable more features:
* Intel optimizations
  * Math Kernel Library
  * Thread Building Blocks
  * IPP
* Eigen
* Video features
  * gstreamer 
  * Intel Media SDK
  * Intel Realsense

This will activate many additional components. Each one having ability to break your build. It is difficult to ensure that installing anyone of them will not impact specfic configurtions you already have. If something breaks, you can attempt removing compoents and go back to build 1 until it completes again.

First we will want to install additional components. Some of them I like to install outside of the opencv and opencv-contrib folder.
```
cd C:/opencv
mkdir opencv_dep
```

PATH Environment Variable
* C:\opencv\opencv\build\install\x64\vc16\bin"
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc14
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\mkl
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\ipp
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\daal
* C:\PROGRA~2\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\compiler
* C:\PROGRA~2\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit\bin\x64
* C:\PROGRA~2\Intel RealSense SDK 2.0\bin\x64
* C:\gstreamer\1.0\x86_64\bin"

### Setup Shell
```
set "openCvSource=C:\opencv\opencv"
set "openCVExtraModules=C:\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
set "generator=Ninja"
```
### Configure Build

#### cmake-gui
Start cmake-gui in the CMD shell that has the bat files from above executed.

```
cd C:\opencv\opencv\build
cmake-gui ..\
```

Features to be turned on and variables to be set
* OPENCV_EXTRA_MODULES_PATH = "C:/opencv/opencv_contrib/modules"
* OPENCV_ENABLE_NONFREE = ON
* BUILD_SHARED_LIBS = ON
* BUILD_opencv_python3 = ON
* BUILD_opencv_python2 = ON

Add Entry
* PYTHON_DEFAULT_EXECUTABLE="C:\Python38\python.exe"

EIGEN
* WITH_EIGEN = OFF
* EIGEN_INCLUDE_PATH = "C:/opencv/dep/eigen/Eigen"
* Eigen3_DIR is not found

Intel RealSense
* WITH_LIBREALSENSE = ON
* LIBREALSENSE_INCLUDE_DIR = "C:/Program Files (x86)/Intel RealSense SDK 2.0/include"
* LIBREALSENSE_LIBRARIES = "C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib"
* realsense2_DIR is not found

GSTREAMER
* WITH_GSTREAMER=ON

It automatically sets the path lib, include, glib, glib include, gobject, gstreamer library, gstreamer utils, riff library if GSTREAMER_DIR is set correcty.

TBB, Parallel framework should list TBB (ver...)
* BUILD_TBB = OFF, you want to use the precompiled files which we downloaded and installed above. This is not a wrapper.
* WITH_TBB = ON

The following TBB folders should be set automatically:
* TBB_DIR is not found
* TBB_ENV_INCLUDE = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include
* TBB_ENV_LIB = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib
* TBB_ENV_LIB_DEBUG = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb_debug.lib
* TBB_VER_FILE = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include/tbb/tbb_stddef.h

Intel Media SDK Support
* WITH_MFX = ON
* WITH_MSMF = ON
* WITH_MSMF_DXVA = ON

MKL 
* WITH_MKL = ON
* MKL_USE_MULTITHREAD = ON
* MKL_WITH_TBB = ON

When executing the setup script it should configure automatically:
* MKL_INCLUDE_DRIS = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include
* MKL_LIBRARIES = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_intel_lp64.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_sequential.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core.lib
* MKL_ROOT_DIR C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl

HDF

When the HDF5_DIR is set as environment variable it should find the directories and all the variables below should be set automatically.
* BUILD_opencv_hdf = OFF
* HDF5_C_LIBRARY = "C:/HDF5/1.12.0/lib/libhdf5.lib"
* HDF5_INCLUDE_DIRS = "C:/HDF5/1.12.0/include"

OPENCL

This should be set automatically.
* WITH_OPENCL = ON
* WITH_OPENCLAMDBLAS = ON
* WITH_OPENCLEMDFFT = ON
* WITH_OPENCL_D3D11_NV = ON
* WITH_OPENCL_SVM = ON support vector machine classified

JavaScript

* BUILD_opencv_js = OFF

Turn Following Features OFF
* USE_WIN32_FILEIO = OFF, this might enable bigTIFF or file acceess for >2GB.
* WITH_CUDA = OFF
* OPENCV_DNN_CUDA = OFF
* WITH_OPPENCL_SVM = not sure

#### CMD Shell Equivalent
STATUS: Not verified
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
-DWITH_EIGEN=OFF ^
-DEIGEN_INCLUDE_PATH="C:/opencv/opencv_dep/eigen/Eigen" ^
-DWITH_LIBREALSENSE=ON ^
-DLIBREALSENSE_INCLUDE_DIR="C:/Program Files (x86)/Intel RealSense SDK 2.0/include" ^
-DLIBREALSENSE_LIBRARIES="C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib" ^
-DBUILD_opencv_hdf=OFF ^
-DHDF5_C_LIBRARY="C:/HDF5/1.12.0/lib/libhdf5.lib" ^
-DHDF5_INCLUDE_DIRS="C:/HDF5/1.12.0/include"
```

### Build
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

### Test

We need to add the following directories to the search path so opencv can find the necessary dlls:
```
set "PATH=%PATH%;C:\opencv\opencv\build\install\x64\vc16\bin"
set "PATH=%PATH%;C:\gstreamer\1.0\x86_64\bin"
set "PATH=%PATH%;C:\PROGRA~2\Intel RealSense SDK 2.0\bin\x64
set "PATH=%PATH%;C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14"
```

Optional:
```
set "PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin"
set "PATH=%PATH%;C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\mkl"
set "PATH=%PATH%;C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\ipp"
set "PATH=%PATH%;C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\daal"
set "PATH=%PATH%;C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\compiler"
```

```
import sys
print('\n'.join(sys.path))
```

```
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -2 -c "import cv2; print('OpenCV: ' + cv2.__version__ + 'for python installed and working')"
py -2 -c "import cv2; print(cv2.getBuildInformation())"

STATUS: Completed

py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"

STATUS: In progress
```

#### Camera
```
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera

gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
```
Now check with test_rtsp_simplegstramer.py

## Build 3
Inlucde CUDA and QT. This builds upon previous two builds and enables CUDA support. This is not useful if you dont have Nvidia GPU on your computer. OpenCV built with CUDA support will not run on a computer without CUDA GPU. The QT build replaces GUI option.

```
cmake-gui ..\
```

### CUDA
* WITH_NVCUVID = ON, enable CUDA Video decodeing support
* WITH_CUDA = ON, enable CUDA
* WITH_CUFFT = ON
* WITH_CUBLAS = ON
* CUDA_FAST_MATH = ON 
* CUDA_ARCH_PTX = 7.5, selected from all options
* CUDA_ARCH_PTX = 7.5, selected from all options
* CUDA_TOOLKIT_ROOT_DIR = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2"
* CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2
* CUDA_BUILD_EMULATION = OFF, autopopulated
* CUDA_GENERATION = "Turing", autopopulated
* CUDA_HOST_COMPLIER = ... autopopulated
* CUDA_USE_STATIC_CUDA_RUNTIME = ON
* OPENCV_DNN_CUDA = ON, Neural Network Classifiers on CUDA
* ENABLE_FAST_MATH = ON
* BUILD_opencv_cudev = ON

Needs to be on path
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.0\bin

Python will need all qt dlls from ```C:\Qt\5.14.1\msvc2017_64\bin``` copied to ```C:/Python38\Lib\site-packages\cv2\python-3.8\```

### Graphical User Interfaces
* WITH_QT=ON
* Qt5_DIR = C:/Qt/5.x.y/msvc2017_64/lib/cmake/Qt5
With x.y the QT version you downloaded.
Rerun configure and generate in cmake-gui.

If you have previous builds you might want to rename build/install to build/install_noCUDA so you can preserve non_cuda version.

### Build

If you build with Visual Studio C, open Build -> Configuration Manager and enable INSTALL.

```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

This will create many DLL interface warnings. Ignore them. It might take 3 hours to complete.
Now that we have dll and CUDA suport where does library need to go? Check variable script in install folder.


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

### Building Dependencies from Source
It should not be necessary to build these dependencies
```
git clone https://github.com/oneapi-src/oneTBB.git
git clone https://github.com/AcademySoftwareFoundation/openexr.git
git clone git://code.qt.io/qt/qt5.git
cd qt5
git checkout 5.15.0
https://wiki.qt.io/Building_Qt_5_from_Git#Getting_the_source_code
https://structure.io/openni
```

### Create Single Library to Include all Features
* BUILD_opencv_world=ON

