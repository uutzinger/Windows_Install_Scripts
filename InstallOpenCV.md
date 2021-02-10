# Compiling OpenCV 4.5 on Windows 10 With CUDA, MKL, TBB, GSTREAMER Support

- [Compiling OpenCV 4.5 on Windows 10 With CUDA, MKL, TBB, GSTREAMER Support](#compiling-opencv-45-on-windows-10-with-cuda--mkl--tbb--gstreamer-support)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisites](#pre-requisites)
  * [Obtaining OpenCV Source](#obtaining-opencv-source)
  * [Uninstalling of Previous opencv Installations](#uninstalling-of-previous-opencv-installations)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment)
- [Building OpenCV](#building-opencv)
  * [Debugging Missing Dependencies](#debugging-missing-dependencies)
  * [Build 1 [STATUS: Completed Successfully]](#build-1--status--completed-successfully-)
    + [Configure Build](#configure-build)
    + [Configure and Generate](#configure-and-generate)
    + [CMD Shell Equivalent](#cmd-shell-equivalent)
    + [Build](#build)
    + [Test](#test)
  * [Build 2 [STATUS: Completed Successfully]](#build-2--status--completed-successfully-)
    + [Configure Build](#configure-build-1)
    + [Build](#build-1)
    + [DLL Fix](#dll-fix)
    + [Test](#test-1)
  * [Build 3 [STATUS: Completed Successfully]](#build-3--status--completed-successfully-)
    + [Configure Build](#configure-build-2)
    + [Build](#build-2)
    + [DLL Fix](#dll-fix-1)
    + [Test](#test-2)
      - [Gstreamer Camera](#gstreamer-camera)
  * [Build 4 [STATUS: OPTONAL]](#build-4--status--optonal-)
  * [Build 5 [STATUS: Completed Successfully]](#build-5--status--completed-successfully-)
    + [Configure BUILD](#configure-build)
    + [Build](#build-3)
    + [DLL Fix](#dll-fix-2)
    + [Test](#test-3)
  * [Build 6](#build-6)
  * [Create Wheel Install Package](#create-wheel-install-package)
- [Fix DDL Summary](#fix-ddl-summary)
- [Build CMAKE Output](#build-cmake-output)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Motivation

There are many reasons to build your own OpenCV binaries; for example to enable hardware acceleration or gstreamer.

Building OpenCV beyond its default settings is notoriously difficlut. The
[python for engineers](https://www.pythonforengineers.com/installing-the-libraries-required-for-the-book/)
oline book calls people compiling it "masochists" and "If you get stuck, you will need to ask Stackoverflow, whereupon they will call you an idiot".

The main issues are the many temptations for enabling components that you don’t need but break your build. 
There is to my knowledge no list which version of for example Intel Mathliraries and CUDA, compile with latest release version of OpenCV on Visual Studio. 

A build typically takes 10-30 minutes when CUDA is not enabled. Some build options create a wrapper for external libraries which you need to download prior to the build, and others will download the modules for you. The documentation is sparse and google the build options does not produce quality links.

In the builds described here, I want to enable **gstreamer** and architecture
specific accelerations. In particular **Intel optimized libraries** and **CUDA** support. 
I want architecture optimization because I will attempt using high frame rate cameras in my research.
I want to enable gstreamer because I want to develop python code for Jetson
single board computers on my notebook computer. Nividia supports gstreamer with
hardware acceleration on Jetson architecture. It does not support ffmpeg the default interface in OpenCV. 

## Approach

In this guide I propose to build OpenCV in several steps and with increasing complexity.

It is common that the activation of one component creates a set of issues that
need to be solved. Also the activation of one component might not be reverted
without clearing previous build cache and cleaning the build directory. It is
also possible that the cmake and cmake-gui do not create the same build
configuration. Make sure the cmake-gui version used in your command shell is
from the same folder as cmake: `where cmake` and `where cmake-gui`.

Many online posts have been consulted for this document. 

* [1] [James Bowley] (https://jamesbowley.co.uk/accelerate-opencv-4-5-0-on-windows-build-with-cuda-and-python-bindings/)
* [2] [dev.infohub.cc](https://dev.infohub.cc/build-opencv-430-with-cuda/) 
* [3] https://geeks-world.github.io/articles/464015/index.html 
* [4] https://docs.opencv.org/4.3.0/d3/d52/tutorial_windows_install.html 
* [5] https://www.learnopencv.com/install-opencv-4-on-windows/ 
* [6] https://lightbuzz.com/opencv-cuda/ 
* [7] https://pterneas.com/2018/11/02/opencv-cuda/
* [8] https://haroonshakeel.medium.com/build-opencv-4-5-1-with-gpu-cuda-support-on-windows-10-without-tears-cf0e55dc47f9

## Background Reading
The following article explains algorithm optimizations by Intel for opencv https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel pointing towards Halide and OpenCL.

This is excellent summary of the Halide algorithm development tools https://halide-lang.org/ It explains why some programs finish an image processing task much faster than others.

## Pre-Requisites

Prepare your system with
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md.
I propose to work with dynamic link libraries and to copy all required dlls
to a central location to limit extension of the PATH variable and to keep "parts together".

## Obtaining OpenCV Source
Download the source files for both OpenCV and OpenCV contrib, available on
GitHub. I place them in the root folder C:/opencv but they can go anywhere. 
Its difficult to figure out which version works with your QT, VTK, and CUDA
installation. Often the latest master branch solves compiling problems.
However for the dependencies often one version before the current release is likely to work.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir C:/opencv
cd C:/opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd C:/opencv/opencv_contrib
git checkout 4.5.1
cd C:/opencv/opencv
git checkout 4.5.1
mkdir build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Uninstalling of Previous opencv Installations
To make sure python finds your build you will want to remove any other installation of opencv.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip3 uninstall opencv-python
pip3 uninstall opencv-contrib-python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Preparing your Shell Build Environment
Open a command prompt (CMD) and enter the following commands with directories
pointing to your installations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:/opencv/opencv/build
set "openCvSource=C:\opencv\opencv"
set "openCVExtraModules=C:\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2019 and prior for Math acceleration and Thread Building Blocks:  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2019\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2019\windows\tbb\bin\tbbvars.bat" intel64 vs2019  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We dont need Intel daal, mpi and ipp for hardware optimization. OpenCV handles IPP automatically.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019  
# "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\bin\daalvars.bat" intel64  
# "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\mpivars.bat"  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Also intel libraries version 2021 do not work with opencv 4.5.1:  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you execute some of the vars script twice, it will throw an error the second time. You can ignore those.

**It is critical to run this setup each time in the shell window that you will use to start make, cmake, cmake-gui or ninja before you start configuring your build.**

# Building OpenCV
Here are several builds, each with increasing complexity. Its not a good idea to enable all settings at once and then to struggle through the errors. Its better to start with a smaller build and then expand.

## Debugging Missing Dependencies
In general this should help finding missing dependencies:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/debugMissingDLL.md

However the solution to the dll load failures in OpenCV 4.3 is described in [2] as a python problem. It requires the patches outlined at the end before the python package is built [2].  If you already installed OpenCV and dont plan to create a pip install package you will need to apply the changes in `C:\Python38\Lib\site-packages` as listed after all built scenarios towards the end of this document.

## Build 1 [STATUS: Completed Successfully]

With this first build, I will use cmake-gui. It is a light build with just the default settings, extra and non free modules and python.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake-gui.exe"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Clear Build Cache. This will remove any previous configuration options.
-   Run configure. Select Visual Studio 16 2019 as your compiler environment. Select native compilers.

### Configure Build

The entries in RED need to be taken care off by running Configure again. But befor that verify your settings with the ones below:

Video

-   `WITH_GSTREAMER = OFF`, off for now
-   `WITH_MFX = OFF`, Intel Video Acceleration
-   `WITH_MKL = OFF`, Intel Math Library
-   `WITH_LIBREALSENSE = OFF`, Intel Real Sense Camera

Math Acceleration
-   `WITH_TBB = OFF`, Intel Thread building Blocks
-   `WITH_EIGEN = OFF`, Linear Algebra Modules

Examples and Tests
-   `BUILD_EXAMPLES = OFF`
-   `BUILD_DOCS = OFF`
-   `BUILD_TESTS = OFF`
-   `BUILD_PERF_TESTS = OFF`
-   `INSTALL_PYTHON_EXAMPLES = OFF`
-   `INSTALL_C_EXAMPLES = OFF`
-   `INSTALL_TESTS = OFF`

Make sure this is ON or set:
-   `BUILD_opencv_python3 = ON`
-   `BUILD_opencv_python2 = OFF`, if you need python 2 module, build it separately. Its no longer supported.
-   `OPENCV_PYTHON3_VERSION = ON`, apparently cmake-gui confuses this variable [4], [2] recommends it ON
-   `OPENCV_EXTRA_MODULES_PATH = "C:/opencv/opencv_contrib/modules"`
-   `OPENCV_ENABLE_NONFREE = ON`
-   `BUILD_SHARED_LIBS = ON`, [2], when on this will created DLLs, when off this will created static libraries (\*.lib), usually dlls are more memory and space efficient, but if you run into dll missing errors you might want this off
-   `BUILD_opencv_world = ON`, [1,2,4], this will create single dll (SHARED_LIBS ON) or lib (SHARED_LIBS OFF) file
-   `CPU_BASELINE`, should auto populate to your CPU
-   `BUILD_opencv_hdf = OFF`, HDF5 fileformat, recommended by [1]
-   `ENABLE_FAST_MATH = OFF`, recommended by cmake

Install location
-   `CMAKE_INSTALL_PREFIX = C:\opencv\4.5.1`

Modify or create the variable:
-   `PYTHON_DEFAULT_EXECUTABLE = "C:\Python38\python.exe"` This makes sure it does not use python2 to configure and build
-   `CMAKE_CONFIGURATION_TYPES = "Release"`

### Configure and Generate

After successful configuration, CMAKE should have found python2 and python3 as
well as your java environment. If python or java environment is not found you
can attempt running the CMD line version below and then revisit it with
cmake-gui as shown above. Don't delete the cache. Just rerun configure in the
gui.

Run the Generate function to create your build project. If generate shows errors
and warnings but completes its process, you can continue building OpenCV.

### CMD Shell Equivalent
The equivalent command in the CMD window is listed below.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Build
And finally do first build using "Open_Project" in cmake-gui. Select build /
batch build and enable INSTALL and then click on build. If there are previously
compiled files in your build directory. you can clean them with the "clean"
button.

The command line equivalent is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Test
In a command shell:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Build 2 [STATUS: Completed Successfully]

You will need to complete Build 1 before you sart Build 2.

Now lets enable more features: 
* Intel optimizations 
  *  Math Kernel Library 
  * Thread Building Blocks 
* Video features
  * Intel Media SDK

### Configure Build
Start cmake-gui in the CMD shell. Make sure the shell environment was configures as shown above.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:\opencv\opencv\build
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**CPU optimization**

If you leave the default settings, cmake should configure the appropriate CPU architecture festures.
But you can check with the CPU ID app what features your CPU supports (e.g. AVX2) and read on
https://github.com/opencv/opencv/wiki/CPU-optimizations-build-options what
baseline features you want to enable.

Check if the following lines match your expected minimium (basline) and maximum (dispatch) cpu feature set:
-   `CPU_BASELINE= ...`
-   `CPU_DISPATCH= ...`
Your architecture should be listed at least in DISPATCH.

**Additional Build Features**

All settings from build 1 plus:

**TBB** [STATUS: WORKING]

Download the TBB source or the prebuilt binaries from Intel. The cmake configuration should list under Parallel framework: TBB (ver...) 

The dlls from C:\Program Files(x86)\IntelSWTools\compilers\_and_libraries\windows\redist\intel64_win\tbb\vc\_mt
are recommended in [1]  and linked to VC runtime. By default the vc14 versions are picked up by cmake and works for me.

-   `BUILD_TBB = OFF`, you want to use the pre-compiled files which we downloaded and installed earlier. BUILD TBB will create its own TBB binaries and I did not want that.
-   `WITH_TBB = ON`, needed if you want to use TBB for thread acceleration, either with external libraries (preferred) or build when comppiling OpenCV

The following TBB folders should be set automatically: 
- `TBB_DIR` is not found, even if you set the folder to "C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/tbb/" it will revert to not found
- `TBB_ENV_INCLUDE   = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/tbb/include` \* 
- `TBB_ENV_LIB = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/tbb/lib/intel64_win/vc14/tbb.lib`
- `TBB_ENV_LIB_DEBUG = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/tbb/lib/intel64_win/vc14/tbb_debug.lib`
- `TBB_VER_FILE      = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019.5.281/windows/tbb/include/tbb/tbb_stddef.h`

Opencv_gapi does not seem to compile with tbb. Its a new feature and actively developed. You can turn it off with
- `BUILD_opencv_gapi = OFF`

**MKL** [STATUS: WORKING]        

- `WITH_MKL = ON` I had to add this manually
- `MKL_ROOT_DIR = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl`
- `MKL_USE_MULTITHREAD = ON`, [1] , not available in 4.5.1
- `MKL_WITH_TBB = ON`, [1]

When executing the setup script it should configure automatically: 
- `MKL_INCLUDE_DRIS = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/include` 
- `MKL_LIBRARIES **   =` see below for the following 3 libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_core.lib  
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_intel_lp64.lib  
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_sequential.lib  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have compilation issues you can try the **\_dll.lib** extension.

**LAPACK** [STATUS: WORKING]

Please verify: 
- `LAPACK_INLCUDE_DIR = C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/include`
- `LAPACK_LIBRARIES =` should look like below:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_intel_lp64.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_sequential.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries_2019/windows/mkl/lib/intel64/mkl_core.lib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Intel Media SDK Support** [STATUS: WORKING]
-   `WITH_MFX = ON`
-   `WITH_MSMF = ON`
-   `WITH_MSMF_DXVA = ON`

Please check: 
- `MFX_LIBRARY = C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2020 R1/Software Development Kit/lib/x64/libmfx_vs2015.lib` 
- `MFX_INCLUDE = C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2020 R1/Software Development Kit/include`

**OPENCL** [STATUS: WORKING]

This enables cv::ocl::resize() versus cv::resize() which provides hardware acceleration.

This should be set automatically. Please check: 
- `WITH_OPENCL = ON` 
- `WITH_OPENCLAMDBLAS = ON` 
- `WITH_OPENCLEMDFFT = ON` 
- `WITH_OPENCL_D3D11_NV = ON` 
- `WITH_OPENCL_SVM = ON`, support vector machine classifier

**Miscalaneous** Features [STATUS: WORKING]
-   `USE_WIN32_FILEIO = ON`windows file input output
-   `WITH_CUDA = OFF` keep this off for now
-   `OPENCV_DNN_CUDA = OFF`
-   `WITH_GSTREAMER=OFF` keep this off for now
-   `WITH_LIBREALSENSE = OFF` keep this off for now
-   `BUILD_opencv_hdf = OFF`, keep this off for now
-   `WITH_EIGEN = OFF`, keep this off for now
-   `BUILD_opencv_js = OFF`, only on if you work with Java instead of Python

### Build
Build using "Open_Project" in cmake-gui. Select build / batch build and enable INSTALL and then click on build.

The Command Shell equivalent is: (incomplete, need to update)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
-DBUILD_opencv_hdf=OFF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### DLL Fix
Your installation now will dend on additional DLLs.
I recommend creating a directory in C:\Python38\Lib\site-packages\cv2\python-3.8\dlls and copying the dlls there.
These are the DLLs you need:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
copy "C:\opencv\4.5.1\x64\vc16\bin\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbb.dll"       C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbbmalloc.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Modify `C:\Python38\Lib\site-packages\cv2\config.py`   
Make sure the directory names are updated.  

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    os.path.join('C:/Python38\Lib/site-packages/cv2', 'python-3.8/dlls')
]  + BINARIES_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Modify `C:\Python38\Lib\site-packages\cv2\config-3.8.py`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
PYTHON_EXTENSIONS_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-3.8")
] + PYTHON_EXTENSIONS_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Test
Run python 3 in command shell

Check the python path:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
py -3 -c "import sys; print('\n'.join(sys.path))"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

My output is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\Python38\Lib\site-packages
C:\Python38\python38.zip
C:\Python38\DLLs
C:\Python38\lib
C:\Python38
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try to load opencv:  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If it does not work, close python and execute the following line and then rerun above lines:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\opencv\4.5.1\setup_vars_opencv4.cmd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Build 3 [STATUS: Completed Successfully]

These are additions to build 2. Do NOT clear the cache or delete previous build files.

-   EIGEN
-   HDF file format
-   GUI features
    -   VTK
-   Video features
    -   gstreamer
    -   Intel Realsense

### Configure Build

**GSTREAMER** [STATUS: WORKING]

-   `WITH_GSTREAMER=ON`

It automatically sets the path lib, include, glib, glib include, gobject, gstreamer library, gstreamer utils, riff library if GSTREAMER_DIR is set correctly.

**EIGEN** [Status: WORKING]

When you turn EIGEN ON, you will need to provide the source code, its not automatically downloaded. 
I put the EIGEN code here:
```
cd C:\
git clone https://gitlab.com/libeigen/eigen
git checkout 3.3
```

Then I configured:
-   `WITH_EIGEN = ON`
-   `EIGEN_INCLUDE_PATH = "C:/eigen"`, make sure to select the directory that is one level above Eigen. for examplpe I have `C:\eigen\Eigen\src` and the include path is `C:/eigen`.
-   `Eigen3_DIR` is not found

**Intel RealSense** [STATUS: WORKING]

-   `WITH_LIBREALSENSE = ON`
-   `realsense2_DIR = "C:/Program Files (x86)/Intel RealSense SDK 2.0"`
-   `LIBREALSENSE_INCLUDE_DIR = C:/Program Files (x86)/Intel RealSense SDK 2.0/include`
-   `LIBREALSENSE_LIBRARIES = C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib`

**VTK** [STATUS: WORKING, but just import VTK python wrapper instead]

- `VTK_DIR=C:/vtk/8.2/lib/cmake/vtk-8.2`
- `WITH_VTK=ON` 

**HDF** [STATUS: WORKING, but just import HDF5 python wrapper instead]

To include HDF5 support it is advised to build HDF5 on your computer first.
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

Set:

* `BUILD_opencv_hdf = ON`
* `hdf5_c_library = C:/hdf5/1.12.1/lib/hdf5.lib`
* `hdf5_include_dirs =  C:/hdf5/1.12.1/include`

`libhdf5lib.lib` is for static build and `hdf5.lib` is for shared build.

### Build
If you build with Visual Studio C, open Build -\> Configuration Manager and enable INSTALL and click build.

### DLL Fix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OpenCV dlls
copy "C:\opencv\4.5.1\x64\vc16\bin\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
# TBB dlls
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbb.dll"       C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbbmalloc.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
# gstreamer DLLs
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gst*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\glib*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gobject*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\intl*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gmodule*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\ffi*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\orc*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\z*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
# Realsense dlls
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

and the same as in BUILD 3.

### Test

#### Gstreamer Camera
Try to connect to rtsp stream initated on your local host for example with VLC Media Player:

Media -\> Stream, Select Capture Device, Show more Options and reduce cache size.   
Stream -\> Next,   
Add Destination Device RTSP Add, 8554,   
Activate Transcoding, Encapsulation=MPEG-TS, Video Codec = H-264, Audio off,   
Stream.

Check connection with standalone gstreamer application:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also connect to a Xiaomi Dafang Hack camera (https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the above with gstreamer binaries work, test it with pyton program: test_rtsp_simplegstreamer.py

## Build 4 [STATUS: OPTONAL]

Here I keep additional features I did not bother to completely debug.

**JAVA** [STATUS: ON HOLD]
-   `BUILD_JAVA = ON` [2]
-   `BUILD_opencv_java = OFF`
-   `BUILD_opencv_java_bindings_generator = OFF`

If you need the java wrapper to be built, you might need to disable python3.
Somehow python2, python3 and java wrappers dont get along in cmake and OpenCV
and each one will need to be built separately.

JavaScript [STATUS: NOT WORKING]
-   `BUILD_opencv_js = OFF`

**QT** [STATUS: ON HOLD, Windows interface works ok, use separate QT wrapper if you need QT]

OpenCV 4.3.0 needs QT 5.14.x
OpenCV 4.5.1 needs QT 5.??.?? (latest version is 5.15.2 with Qt6 coming)

-   `WITH_QT=ON`
-   `Qt5_DIR = C:/Qt/5.14.2/msvc2017_64/lib/cmake/Qt5`
-   `WITH_OPENGL=ON`, rgpd does not compile with opengl.

Rerun configure and generate in cmake-gui once the Qt5_DIR is set. QT allows several version to be installed simultanously, make sure you select version that works.

In order for opencv_cvv to compile you need to change:
`C:\opencv\opencv_contrib\modules\cvv\src\util\observer_ptr.hpp`

by adding
``` #include <stdexcept> // ```

at the end of 
```
#include <cstddef>   // size_t
#include <cstdint>   // [u]intXX_t
#include <algorithm> // since some people like to forget that one
```

OPENGL [STATUS: NOT WORKING ]
-   `WITH_OPENGL=OFF`, rgpd does not compile with opengl.

## Build 5 [STATUS: Completed Successfully]

Finally inlucde CUDA. This builds upon previous builds and enables CUDA support.
This is not useful if you dont have Nvidia GPU on your computer. 
The CUDA_Generation will need to match your GPU. This will be automatically selected.
CUDA support takes a long time to compile.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Configure BUILD

CUDA support doubles your build size and consumes much larger build time. It is better to figure out issues with other modules first because once you enable CUDA it takes a while to get compilation done.

Please make sure the selected CUDA_GENERATION matches the GPU you have installed: 
https://en.wikipedia.org/wiki/CUDA\#GPUs_supported. 
My notebook computer has a GeForce 960M which is GENERATION Maxwell and Compute Capability 5.0. 
For detailed coverage of CUDA_ARCH choices and GPU coverage refer to [1]. 
You can use CPUZ application to identify the hardware in your computer.
You can keep default setting which builds support for all CUDA architectures.

**CUDA** [STATUS: Working]
-   `WITH_CUDA = ON`, enable CUDA
-   `WITH_NVCUVID = ON`, [1] enable CUDA Video decodeing support
-   `WITH_CUFFT = ON`
-   `WITH_CUBLAS = ON` [1,3,7]
-   `CUDA_FAST_MATH = ON`, [2,3]
-   `CUDA_ARCH_BIN = 5.0,5.2`, selected from all options, for shorter compile time, select only the one you need, for compatibility, use the default list produced by configure
-   `CUDA_ARCH_PTX = 5.0`, leave empty as is default or enter to the lowest of ARCH_BIN
-   `CUDA_TOOLKIT_ROOT_DIR = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2"`
-   `CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2`
-   `CUDA_BUILD_EMULATION = OFF`, autopopulated
-   `CUDA_GENERATION = "Maxwell"`, leave empty or select from list, match to the capability of your computer
-   `CUDA_HOST_COMPLIER =`, autopopulated
-   `CUDA_USE_STATIC_CUDA_RUNTIME = ON`, autopopulated
-   `OPENCV_DNN_CUDA = OFF`,[2] Neural Network Classifiers on CUDA, per [1] its not necessary to downdload cuDNN from Nvidia and install it, but if you did this needs to be OFF to depend on cuDNN
-   `BUILD_CUDA_STUBS = OFF`
-   `BUILD_opencv_cudev = ON`
-   `BUILD_opencv_cuda* = ON`

TEST [STATUS: WORKING]
If you want to conduct performance tests enable these:
-   `INSTALL_TESTS = ON`
-   `BUILD_PERF_TESTS = ON`
-   `BUILD_TESTS = ON`
-   `BUILD_opencv_python_tests = ON`

This build creates a lot of warnings (>6,000): `warning : field of class type without a DLL interface used in a class with a DLL interface` You can ignore them.

### Build
If you build with Visual Studio C, open Build -\> Configuration Manager and enable INSTALL and click build.

The command line equievalent is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### DLL Fix
Now you will need to copy the CUDA dlls to the dll repository. With CUDA and gstreamer there are now a lot of dlls.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CUDA DLLs
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppc*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppia*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppicc*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppide*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppif*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppig*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppim*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppist*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppitc*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cublas*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cufft*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cudart*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cudnn*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cuinj*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\curand*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cusolver*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cusparse*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvblas*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvjpeg*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvrtc*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Test
You can test CUDA performance according [1]:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\opencv\4.5.1\x64\vc16\bin\opencv_perf_cudaarithm.exe" --gtest_filter=Sz_Type_Flags_GEMM.GEMM/29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

My outpput is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from Sz_Type_Flags_GEMM
[ RUN      ] Sz_Type_Flags_GEMM.GEMM/29, where GetParam() = (1024x1024, 32FC2, 0|cv::GEMM_1_T)
[ PERFSTAT ]    (samples=75   mean=9.23   median=9.25   min=8.48   stddev=0.27 (2.9%))
[       OK ] Sz_Type_Flags_GEMM.GEMM/29 (1299 ms)
[----------] 1 test from Sz_Type_Flags_GEMM (1308 ms total)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can test CUDA performance in pyton with:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import cv2 as cv
import time

npTmp = np.random.random((1024, 1024)).astype(np.float32)
npMat1 = np.stack([npTmp,npTmp],axis=2)
npMat2 = npMat1
npMat3 = npTmp + npTmp*1j
npMat4 = npMat3
cuMat1 = cv2.cuda_GpuMat()
cuMat2 = cv2.cuda_GpuMat()
cuMat1.upload(npMat1)
cuMat2.upload(npMat2)

_ = cv2.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)
current_time = time.time()

for i in range(100):
   _ = cv2.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)

cuda_time = time.time()

for i in range(100):
   _ = cv2.gemm(npMat1,npMat2,1,None,0,None,1)

cpu_time = time.time()

for i in range(100):
   _ = npMat3 @ npMat4

np_time = time.time()
# CUDA time
print('CUDA execution time is   : {}'.format((cuda_time-current_time)/100.0))
# OpenCV Mat Pultiplication
print('OpenCV execution time is : {}'.format((cpu_time-cuda_time)/100.0))
# NumPy Mat Multiplication
print('NumPy execution time is  : {}'.format((np_time-cpu_time)/100.0))
#
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my setup with python the   
CUDA execution time is 10-29ms,  
CV2 execution time is 100-106ms,  
Numpy execution tims is 42ms  

Please note, that the first time the CUDA routine is called it undergoes jit compilation which takes more than 500ms. 
Also compared to cuda performance test program, python implementation unfortunately takes much longer.

## Build 6

## Create Wheel Install Package

-   Modify code in `cd C:\opencv\opencv\build\python_loader\`
-   `xcopy "..\lib\python3\Release\*.pyd" .\cv2\python-3.8 /i`
-   Execute `echo graft cv2/python-3.8  > MANIFEST.in`
-   Modify setup.py so that lines 54-57 are:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ],
        # Additional Parameters
        include_package_data=True,
        zip_safe=False,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
also change the name of the package in setup.py from opencv to opencv-python  

I do not yet know how to get the dlls copied to dll repository automatically with wheel package.
If you know where they are on the computer you can follow these modifications:
Adapted from [2]

-   Modify cv2/config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    os.path.join(os.getenv("CV_PATH",    "C:/opencv/4.5.1"), "x64/vc16/bin"),
    os.path.join(os.getenv("INTEL_PATH", "C:/pool"), "bin"),    
    os.path.join(os.getenv("VTK_PATH"  , "C:/VTK/8.2" ), "bin"),
    os.path.join(os.getenv("QT_PATH"   , "C:/Qt/5.14.2/msvc2017_64"), "bin"),
    os.path.join(os.getenv("CUDA_PATH" , "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/V11.2"), "bin"),
    os.path.join(os.getenv("GST_PATH"  , "C:/gstreamer/1.0"), "x86_64/bin"),
    os.path.join(os.getenv("HDF5_PATH" , "C:/hdf5/1.12.1"), "bin")
] + BINARIES_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Modify cv2/config-3.8.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
PYTHON_EXTENSIONS_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-3.8")
] + PYTHON_EXTENSIONS_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   `pip3 install wheel`
-   `py -3 setup.py bdist_wheel`

Your whl package is in `.\dist\*.whl` 
You can insall it with `pip3 install nameofthewheel.whl`

Fix DDL Summary
===============

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Opencv DLLs
copy "C:\opencv\4.5.1\x64\vc16\bin\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y

# TBB DDLs
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbb.dll"       C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64\tbb\vc14\tbbmalloc.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y

# MKL DLLs
# xcopy "C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2019\windows\redist\intel64_win\mkl\*"        C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /s/h/i/e/y

# CUDA DLLs
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppc*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppia*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppicc*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppide*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppif*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppig*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppim*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppist*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nppitc*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cublas*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cufft*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cudart*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cudnn*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cuinj*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\curand*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cusolver*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\cusparse*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvblas*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvjpeg*.dll"   C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin\nvrtc*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y

# gstreamer DLLs
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gst*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\glib*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gobject*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\intl*.dll"    C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\gmodule*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\ffi*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\orc*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
copy "C:\gstreamer\1.0\msvc_x86_64\bin\z*.dll"     C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y

# Realsense
copy "C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y

# Media
# copy "C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2020 R1\Software Development Kit\bin\x64\*.dll" C:\Python38\Lib\site-packages\cv2\python-3.8\dlls /y
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Modify cv2/config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    os.path.join('C:/Python38\Lib/site-packages/cv2', 'python-3.8/dlls')
]  + BINARIES_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Modify cv2/config-3.8.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
PYTHON_EXTENSIONS_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-3.8")
] + PYTHON_EXTENSIONS_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Build CMAKE Output
==================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General configuration for OpenCV 4.3.0 =====================================
  Version control:               4.3.0

  Extra modules:
    Location (extra):            C:/opencv/opencv_contrib/modules
    Version control (extra):     4.3.0-dirty

  Platform:
    Timestamp:                   2020-06-13T06:07:45Z
    Host:                        Windows 10.0.19041 AMD64
    CMake:                       3.17.3
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1926

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3 SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2
      requested:                 AVX2
    Dispatched code generation:  AVX512_SKX
      requested:                 SSE4_1 SSE4_2 AVX FP16 AVX2 AVX512_SKX
      AVX512_SKX (6 files):      + AVX_512F AVX512_COMMON AVX512_SKX

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe  (ver 19.26.28806.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise         /arch:AVX  /arch:AVX /arch:AVX2 /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise         /arch:AVX  /arch:AVX /arch:AVX2 /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise         /arch:AVX  /arch:AVX /arch:AVX2 /MP   /MD /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise         /arch:AVX  /arch:AVX /arch:AVX2 /MP /MDd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:          cudart_static.lib nppc.lib nppial.lib nppicc.lib nppicom.lib nppidei.lib nppif.lib nppig.lib nppim.lib nppist.lib nppisu.lib nppitc.lib npps.lib cublas.lib cudnn.lib cufft.lib -LIBPATH:C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/lib/x64
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 alphamat aruco bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv datasets dnn dnn_objdetect dnn_superres dpm face features2d flann fuzzy gapi hdf hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab viz xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    java_bindings_generator python2 world
    Disabled by dependency:      -
    Unavailable:                 cnn_3dobj freetype java js matlab ovis sfm
    Applications:                tests perf_tests apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:
    QT:                          YES (ver 5.14.2)
      QT OpenGL support:         NO
    Win32 UI:                    YES
    VTK support:                 YES (ver 8.2.0)

  Media I/O:
    ZLib:                        build (ver 1.2.11)
    JPEG:                        build-libjpeg-turbo (ver 2.0.4-62)
    WEBP:                        build (ver encoder: 0x020f)
    PNG:                         build (ver 1.6.37)
    TIFF:                        build (ver 42 - 4.0.10)
    JPEG 2000:                   build Jasper (ver 1.900.1)
    OpenEXR:                     build (ver 2.3.0)
    HDR:                         YES
    SUNRASTER:                   YES
    PXM:                         YES
    PFM:                         YES

  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES (prebuilt binaries)
      avcodec:                   YES (58.54.100)
      avformat:                  YES (58.29.100)
      avutil:                    YES (56.31.100)
      swscale:                   YES (5.5.100)
      avresample:                YES (4.0.0)
    GStreamer:                   YES (1.16.2)
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES
    Intel RealSense:             YES (2.33.1)
    Intel Media SDK:             YES (C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2019 R1/Software Development Kit/lib/x64/libmfx_vs2015.lib)

  Parallel framework:            TBB (ver 2019.0 interface 11008)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_intel_lp64_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_sequential_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib)
    Eigen:                       YES (ver 3.3.7)
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  NVIDIA CUDA:                   YES (ver 10.2, CUFFT CUBLAS NVCUVID FAST_MATH)
    NVIDIA GPU arch:             50 52
    NVIDIA PTX archs:

  cuDNN:                         YES (ver 7.6.5)

  OpenCL:                        YES (SVM NVD3D11)
    Include path:                C:/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.3)
    Libraries:                   C:/Python38/libs/python38.lib (ver 3.8.3)
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.18.5)
    install path:                C:/Python38/Lib/site-packages/cv2/python-3.8

  Python (for build):            C:/Python38/python.exe

  Install to:                    C:/opencv/4.3.0
-----------------------------------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
