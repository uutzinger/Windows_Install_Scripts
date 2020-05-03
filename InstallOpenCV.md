# Compiling OpenCV on Windows 10
## Motivation
There are many reasons to build your own openCV binaries. The issue with building your own binaries are the many temptations of enabling components that you dont really need.

I want to enable gstreamer and processor specific accelerations. In particular Intel optimized libraries and CUDA support.
I need to eanble gstreamer because I want to develop code for Jetson single board computers on my notebook computer. Nividia supports gstreamer with hardware acceeration on Jetson architecture. I would like to be able to read rtsp camera streams because I have bandwidth caps on my applications. I want to be able to use the same USB cameras on arm based single board computers and my notebook computer. I also have projects that utilize the Intel Realsense platform. I need architeture optimization because I will attempt using high frame rate cameras in my research.

The temptations I encountered are: Enabling Eigen, Matlab, JavaScript, Java, HDF5. Intel TBB,IPP,MKL and CUDA are complex enough for architecture opimization. I dont program in Java nor JavaScript. I have over many years used Matlab for scientific computing but I dont need to build an opencv interface for Matlab, as I can obtain that through Mathworks when the need arises. If I have issue of needing to save and read very large files >2Gb, I can check into packages other than openCV that provide that functionality.

## Apparoach
This guide's purpose is to build openCV in several steps and with increasing complexity.

It is common that the activation of one component creates a set of issues that need to be solved. Also the activation of one component (e.g. gstreamer) can not be reverted even when attempting to turn off the component in the build script.
It is also common that the cmake and cmake-gui do not create the same build configuration. Often there is more than one cmake version installed on your computer.

I prefer building with Ninja because opencv build times are very long and Ninja reduces them significantly. 

Many online posts have been consulted for this script e.g. [James Bowley](https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd).

## Debug
Once you start more complex builds, the two main issues you will need to solve is to 
* a) find appropriate binaries and packages to include into your build and reference the appropraite directories and lib(s) 
* b) to make sure the dlls that those packages need are in the search path when cv2 is loaded 
Although you can enable world build which creates a single dll for opencv, the support packages still have their own dlls. I counted about 200 additional dll if you make a large build.

I enable opencv builds both for python 2 and python 3. I had builds that open in python 2 without errors and don't open in python 3. At this time I dont have a recipe that simply identfies the component that failed to load. However the following is my approach:

### Dumpbin
```
dumpbin C:\Python38\Lib\site-packages\cv2\python-3.8\cv2.cp38-win_amd64.pyd /IMPORTS | findstr dll
```
This lists all dlls your build is attempting to open. Make sure each dll listed is found in you CMD windows with:
```
where dllname_from_previous_output
```
This approach can take significant time, and is not guaranteed to find the culprit.

### procmon
[Procmon](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon) allows to monitor file system activity.
I start python and procmon and stop it from monitoring.  I clear the output. Then I start activity monitoring and type ```import cv2```  in python and stop monitoring as soon as the error appears. The I use find tool in procmon to locate python activity e.g. Find python.exe. I attempt to find the last python activity and then step backwards by locating activity that did not result in SUCCESS. There are many such activities. I can not say exactly how to navigate the FILE NOT FOUND or BUFFER OVERLOW activities to identify which ones caused cv2 to fail. The one that breaks your installation can be listed under an other task than python.exe as it could be an other component failing to load its dlls. The more components you activate in your openCV build, the more such components can cause a fail.

### Cleaning of previous build
You can clean the build configurtion in cmake-gui by clearing the cache. You can also clean previous builds by deleting the content of the build directory. If you modif the build with cmake or cmake-gui, it appears that only the necessary modules are rebuilt. If you can not complete an incremental build, start disabling features and when that does not help, you might need to clear the cache or start from scratch by deleting the build folder.

### Fun
This explains algorithm optimizations.
https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel
https://halide-lang.org/

## Pre Requisits

### Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.
OpenCV still supports python 2.7 but compilation fails at the final stages of the build if one version is 32bit and the other 64bit. 

### Install Visual Studio
Install Visual Studio Community from [Microsoft](https://visualstudio.microsoft.com/downloads/) and install the the option for develoment for desktop application in C.

### Open CV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. I place them in the root folder C:/opencv but they can go anywhere. I usually attempt installing release versions and not the latest version. At times in can be confusing in GitHub to identify the latest release. You can check openCV [Documentation](https://docs.opencv.org/) when you select Doxygen HTML you will have a pull down menu and can identify the highest version number that is not -dev -beta or -alpha. 

```
mkdir C:/opencv
cd C:/opencv
git clone https://github.com/opencv/opencv.git --branch 4.3.0
git clone https://github.com/opencv/opencv_contrib.git --branch 4.3.0
cd C:/opencv/opencv
mkdir build
```

### CMake
Install CMake with latest release version. [Kitware](https://github.com/Kitware/CMake/releases/)

### Windows SDK 
When you install Visual Studio Compiler you can select Windows 10 SDK (10.0.18362.0) in the Installer. Windows SDK includes DirectX SDK. When you rerun the Visual Studio installer you might want to add options to Windows SDK that are not yet installed. [SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)

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

## Unistall old opencv version
To make sure python finds your build you will want to remove any other installations of opencv.
```
pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
```

## Environment Variables
You might want to update your path and environment variables. If you dont know how to do that Rapid Environment Editor is a tool that finds errors and can also help you deal with the PATH when it exceeds the size limit. There are two PATH variables. THe global one and the one associated with your account. The one for your account is an addition to the global one.

PATH
* C:\Python38
* C:\Python38\Scripts
* C:\Program Files\AdoptOpenJDK\jdk-11.0.7.10-hotspot\bin
* C:\Program Files (x86)\Windows Kits\8.1\bin\x64

## Prepare your Shell Build Environment

Open command prompt and enter the following commands with directories pointing to your installations
```
cd C:/opencv/opencv/build
set "openCvSource=C:\opencv\opencv"
set "openCVExtraModules=C:\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Ninja"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
```

When you execute the vcvars script twice in a row, it will throw error the second time. You can ignore that.

## Build
Here it have 3 builds with increasing complexity. Its not a good idea to enable all settings at once and then to struggle through the errors. Its better to start with smaller build and then expand.

## Build 1
With this first build, I will not use the command line option. We will start directly with cmake-gui.
You should not need to worry about dlls. It is a light build with just the default settings, extra and non free modules and python.

### Let's Start Light (minimal)
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
* Clear Build Cache. This will remove any revious configuration options.
* Run configure. Select Ninja as your compiler environment. Select native compilers.

### Verify Build Variables
There will entries in RED, meaning cmake-gui would like you to take a look at them. 
Please verify:

For a light build, following options are usually off:
* WITH_GSTREAMER
* WITH_MFX
* WITH_MKL
* WITH_TBB
* WITH_EIGEN
* WITH_LIBREALSENSE
* BUILD_opencv_hdf
* D-DBUILD_EXAMPLES
* BUILD_DOCS
* BUILD_TESTS
* BUILD_PERF_TESTS
* INSTALL_PYTHON_EXAMPLES
* INSTALL_C_EXAMPLES
* INSTALL_TESTS

Make sure this is ON or set:
* BUILD_opencv_python3
* OPENCV_EXTRA_MODULES_PATH "C:/opencv/opencv_contrib/modules"
* OPENCV_ENABLE_NONFREE
* BUILD_SHARED_LIBS
* OPENCV_PYTHON3_VERSION
* PYTHON_DEFAULT_EXECUTABLE "C:\Python38\python.exe"

### Configure and Generate
After successful configuratin, CMAKE should have found python2 and python3 as well as your java environment. If python or java environment is not found you can attempt running the CMD line version below and then revisit it with cmake gui as shown above. Dont delete the cache. Just rerun configure in gui.

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
And finally do first build using Ninja:
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

### Test
```
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -2 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -2 -c "import cv2; print(cv2.getBuildInformation())"
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

STATUS: Completed Successfully.

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

This will activate many additional components. Each one having ability to break your build. It is difficult to ensure that installing anyone of them will not impact configurtions on individual computers. If something breaks, you can attempt removing compoents and go back to build 1 until it completes again.

First we will want to install additional components. Some of them I wilke to install outside of the opencv and opencv-contrib folder.
```
cd C:/opencv
mkdir opencv_dep
```

### Intel TBB, MKL, MPI, IPP, DAAL
To accelerate some OpenCV operations install both the Intel MKL and TBB by registering for community licensing, and downloading for free. [Intel libraries](https://software.seek.intel.com/performance-libraries). The chrome browser seems to have have issues with selecting the downloads unfortunately.

### LAPACK BLAS
BLAS is part of the Intel Performance libraries which we installed above.
You dont need to build it. 
LA stands for linear algebra and is the backbone of computer vision and scientific computing.
If you want to build it you can download the source [LAPACK] (http://www.netlib.org/lapack/) and build it but you need a FORTRAN compiler (see Build Instructions for LAPACK 3.5.0 for Windows with Visual Studio in http://icl.cs.utk.edu/lapack-for-windows/lapack. You might also be able to use pre built libraries from https://icl.cs.utk.edu/lapack-for-windows/lapack/ using http://icl.cs.utk.edu/lapack-for-windows/lapack/LAPACKE_examples.zip.

### Intel Media SDK
Optional: To accelerate video decoding on Intel CPU’s, register, download and install [Intel Media SDK](https://software.intel.com/en-us/media-sdk)

### Intel RealSense
Optional: If you want to use an Intel Realsense cameras (3D or Tracking camera) you might want to install [Intel Realsense](https://www.intelrealsense.com/developers/). You need to add realsense2.dll to system path. It is usully location in C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64

### Gstreamer & FFMPEG
FFMPEG or gstreamer are needed to receive, decode and encode compressed video streams. For example the rtsp web cam streams.
OpenCV comes with a wrapper for FFMPEG and distributes the necessary libraries.
If you use a Jetson single board computers you will need to get familiar with gstreamer as NVIDIA does not provide GPU support for FFMPEG. 

#### Gstreamer
For Windows: https://gstreamer.freedesktop.org/download/ or https://gstreamer.freedesktop.org/data/pkg/windows/
Install both
* msvc
* devel msvc
The gst-python bindings are not available on Windows unfortunately.

WARNING: Including gstreamer creates most issues with oppencv as there are numerous dlls that need to be accessible.

#### FFMPEG
FFMPEG is auto downloaded with opencv and it builds a wrapper and does not build againts your own FFMPPEG includes. 
There is suggestion further below how to bypass the wrapper. I have not completed the bypass approach and can not recommend it at thist time.
You can obtain your ffmpeg binary and development files here:
From https://ffmpeg.zeranoe.com/builds/ download
Version:latest stable
Architecture: Windows 64 bit
Linking: Shared and Dev
Unzip and install in your ffmpeg folder 

### HDF5
If you are intersted in large datasets you might want to install the HDF library from HDF group. Often researchers use TIFF standard to create large image files, however for very large datasets hdf5 should be considered, especially when the data sets exceed the RAM capacity.
https://www.hdfgroup.org/downloads/hdf5/
Make an account and obtain the vs14.zip version.
I installed into C:/HDF5.
lib and include folders are in C:/HDF5/x.yy.z/lib/ and include folders.
OpenCV provides a wrapper for the libhdf5 library. If HDF5_DIR is set as environment variable it will find cmake files.
STATUS: Disabled, does not comppile

### JavaScript
OpenCV provides access to JavaScript. For BUILD_opencv_js=ON you need EMscripten.
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
STATUS: Disabled, does not compile

### Matlab
WITH_MATLAB=ON requires mex builder and some libraries to be found. In matlab command prompt: mex -setup
This is not yet working in my setup as Matlab interface is not getting built. I assume I will need to activate additional components.
STATUS: In progress

### EIGEN
To active the EIGEN library you need to download it
```
git clone https://gitlab.com/libeigen/eigen.git
```
STATUS: Disabled, does not compile.

### Environment Variables
Your path and environment variables should include:

Environent Variables
* INTELMEDIASDKROOT = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_ROOT_X86_64 = C:\gstreamer\1.0\x86_64
* GSTREAMER_DIR=C:\gstreamer\1.0\x86_64\bin

* HDF5_DIR = C:\HDF5\1.12.0\cmake

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
Optional, needed for Build 2 and Build 3:
* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin
* C:\gstreamer\1.0\x86_64\bin"

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

#### cmake-gui
Start cmake-gui in the CMD shell that has the bat files from above executed.

```
cmake-gui ..\
```

Features to be turned on and variables to be set
* OPENCV_EXTRA_MODULES_PATH="C:/opencv/opencv_contrib/modules"
* OPENCV_ENABLE_NONFREE=ON
* BUILD_SHARED_LIBS=ON
* BUILD_opencv_python3=ON
* BUILD_opencv_python2=ON

Add Entry
* PYTHON_DEFAULT_EXECUTABLE="C:\Python38\python.exe"

EIGEN
* WITH_EIGEN=OFF
* EIGEN_INCLUDE_PATH="C:/opencv/dep/eigen/Eigen"
* Eigen3_DIR is not found

Intel RealSense
* WITH_LIBREALSENSE=ON
* LIBREALSENSE_INCLUDE_DIR="C:/Program Files (x86)/Intel RealSense SDK 2.0/include"
* LIBREALSENSE_LIBRARIES="C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib"
* realsense2_DIR is not found

GSTREAMER
* WITH_GSTREAMER=ON
It should automatically set the path lib, include, glib, glib include, gobject, gstreamer library, gstreamer utils, riff library.

TBB, Parallel framework should list TBB (ver...)
* BUILD_TBB=OFF, you want to use the precompiled files which we downloaded and installed above. This is not a wrapper.
* WITH_TBB=ON
The following TBB folders should be set automatically:
* TBB_DIR is not found
* TBB_ENV_INCLUDE C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include
* TBB_ENV_LIB  C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib
* TBB_ENV_LIB_DEBUG  C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb_debug.lib
* TBB_VER_FILE C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include/tbb/tbb_stddef.h

MKL 
* WITH_MFX
* WITH_MKL
* MKL_USE_MULTITHREAD
* MKL_WITH_TBB
When setting executing the setup script it should configure automatically:
* MKL_INCLUDE_DRIS = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include
* MKL_LIBRARIES = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_intel_lp64.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_sequential.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core.lib
* MKL_ROOT_DIR C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl

HDF

When the HDF5_DIR is set as environment variable it should find the directories and all the variables below should be set automatically.
* BUILD_opencv_hdf=OFF
* HDF5_C_LIBRARY="C:/HDF5/1.12.0/lib/libhdf5.lib"
* HDF5_INCLUDE_DIRS="C:/HDF5/1.12.0/include"

OPENCL

This should be set automatically.
* WITH_OPENCL=ON
* WITH_OPENCLAMDBLAS=ON
* WITH_OPENCLEMDFFT=ON
* WITH_OPENCL_D3D11_NV=ON
* WITH_OPENCL_SVM=ON support vector machine classified

JavaScript
* BUILD_opencv_js=OFF

Turn Following Features OFF
* USE_WIN32_FILEIO=OFF, this might enable bigTIFF or file acceess for >2GB.
* WITH_CUDA=OFF
* OPENCV_DNN_CUDA=OFF

#### CMD Shell Version
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
STATUS: In progress

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
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
```

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
Inlucde CUDA and QT. This builds upon previous two builds and enables CUDA support. This is not useful if you dont have Nvidia GPU on your computer. OpenCV built with CUDA support will not run on a computer without CUDA GPU. The QT build replaces GUI option.

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

### QT
Installing QT takes a very long time. In addition it might interfere with your current ninja and cmake setup.
Not all opencv components compile nicely when QT is enabled and unless you really need QT functionality enabled, I don't recommended it on Windows as first time build. 

To install QT download it from https://www.qt.io/download-open-source. At the bottom is installer link in green. Login with your QT account. One you have the QT installed use the MaintenanceTool application in the QT folder to make sure you have a valid QT version installed. This can take a long time and might consume 3GB of storage. I filter for LTS version.

### Environment Variables
You might want to update your path and environment variables:

CUDA
* C:\PROGRA~1\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin
* C:\PROGRA~1\NVIDIA GPU Computing Toolkit\CUDA\v10.2\libnvvp

```
cmake-gui ..\
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

### Graphics Libraries
* WITH_QT=ON
* Qt5_DIR = C:/Qt/5.x.y/msvc2017_64/lib/cmake/Qt5
With x.y the QT version you downloaded.
Rerun configure and generate in cmake-gui.

If you have previous builds you might want to rename build/install to build/install_noCUDA so you can preserve non_cuda version.

### Build
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

### Create single library to include all features
* BUILD_opencv_world=ON
