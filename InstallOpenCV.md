# Compiling OpenCV on Windows 10

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

There are many reasons to build your own OpenCV binaries; for example to enable
hardware acceleration or gstreamer.

Building OpenCV beyond its default settings is notoriously difficlut. The
[python for
engineers](https://www.pythonforengineers.com/installing-the-libraries-required-for-the-book/)
oline book calls people compiling it "masochists" and "If you get stuck, you
will need to ask Stackoverflow, whereupon they will call you an idiot".

The main issues are the many temptations for enabling components that you don’t
need but break your build and that figuring out which options are needed takes a
long time. There is to my knowledge no list which version of for example CUDA,
VTK and Visual Studio compile with latest release version of OpenCV. A build
typically takes 10-30 minutes when CUDA is not enabled. Some build options
create a wrapper for external libraries which you need to download prior to the
build, and others will download the modules for you. The documentation is sparse
and google the build options does not produce quality links.

In the builds described here, I want to enable gstreamer and architecture
specific accelerations. In particular Intel optimized libraries and CUDA
support. I need architecture optimization because I will attempt using high
frame rate cameras in my research.

I need to enable gstreamer because I want to develop python code for Jetson
single board computers on my notebook computer. Nividia supports gstreamer with
hardware acceleration on Jetson architecture. It does not support ffmpeg. I
would like to be able to read rtsp camera streams because I have applications
that limit network traffic.

I want to be able to use the same USB cameras on arm based single board
computers and my notebook computer. I also have projects that utilize the Intel
RealSense platform.

## Approach

In this guide I propose to build OpenCV in several steps and with increasing
complexity.

It is common that the activation of one component creates a set of issues that
need to be solved. Also the activation of one component might not be reverted
without clearing previous build cache and cleaning the build directory. It is
also possible that the cmake and cmake-gui do not create the same build
configuration. Make sure the cmake-gui version used in your command shell is
from the same folder as cmake: `where cmake` and `where cmake-gui`.

Many online posts have been consulted for this document. 
* [1] [James
Bowley](https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd)
and [opencv4.3
update](https://jamesbowley.co.uk/accelerate-opencv-4-3-0-build-with-cuda-and-python-bindings/)
* [2] https://dev.infohub.cc/build-opencv-410/ and
[update](https://dev.infohub.cc/build-opencv-430-with-cuda/) 
* [3]
https://geeks-world.github.io/articles/464015/index.html 
* [4]
https://docs.opencv.org/4.3.0/d3/d52/tutorial_windows_install.html 
* [5]
https://www.learnopencv.com/install-opencv-4-on-windows/ 
* [6]
https://lightbuzz.com/opencv-cuda/ 
* [7]
https://pterneas.com/2018/11/02/opencv-cuda/

## Background Reading
This explains algorithm optimizations by Intel for opencv
https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel
pointing towards Halide and OpenCL.

This is excellent summary of the Halide algorithm development tools
https://halide-lang.org/ It explains why some programs finish an image
processing task much faster than others.

## Pre-Requisites
Prepare your system with
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md.
I propose to work with dynamic link libraries and to copy all Intel related dlls
to a central location to limit extension of the PATH variable.

## Obtaining OpenCV Source
Download the source files for both OpenCV and OpenCV contrib, available on
GitHub. I place them in the root folder C:/opencv but they can go anywhere. Its
difficult to figure out which version works with your QT, VTK, and CUDA
installation. Often the latest master branch solves compiling problems.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir C:/opencv
cd C:/opencv
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
cd C:/opencv/opencv
mkdir build
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also work with latest branch: 
```git clone
https://github.com/opencv/opencv.git --branch 4.3.0`
```

## Uninstalling of Previous opencv Installations
To make sure python finds your build you will want to remove any other
installation of opencv.

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

"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\bin\daalvars.bat" intel64

"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\mpivars.bat"

"C:\opencv\setup_vars_opencv4.cmd"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you execute some of the vcvars script twice in a row, it will throw an
error the second time. You can ignore those.

**It is critical to run this setup each time in the shell window that you will
use make, cmake, cmake-gui or ninja before you start configuring your build.**

# Building OpenCV
Here are 4 builds, each with increasing complexity. Its not a good idea to
enable all settings at once and then to struggle through the errors. Its better
to start with a smaller build and then expand.

The first build is minimal. The second enables Intel Performance Libraries. The
third build enables CUDA. The forth build includes QT and few additional device
drivers.

## Debugging Missing Dependencies
In general this should help finding missing dependencies:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/debugMissingDLL.md

However the solution to the dll load failures in OpenCV 4.3 is described in [2]
as a python problem. It requires the patches outlined below [2]. These can be applied after you downloaded the OpenCV source and ran configure/generate in
CMAKE. If you already installed OpenCV you will need to apply the changes in `C:\Python38\Lib\site-packages`

-   Modify code in `cd C:\opencv\opencv\build\python_loader\`
-   Execute `echo graft cv2/python-3.8  > MANIFEST.in`
-   Modify setup.py so that lines 54-57 are:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ],
        # Additional Parameters
        include_package_data=True,
        zip_safe=False,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-   Modify cv2/config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    # 'C:/opencv/opencv/build/bin/Release'
    os.path.join(os.getenv("CV_PATH",    "C:/opencv"), "x64/vc16/bin"),
    os.path.join(os.getenv("INTEL_PATH", "C:/pool"), "bin"),    
    os.path.join(os.getenv("VTK_PATH"  , "C:/VTK" ), "bin"),
    os.path.join(os.getenv("QT_PATH"   , "C:/Qt/5.14.2/msvc2019_64"), "bin"),
    os.path.join(os.getenv("CUDA_PATH" , "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/V10.2"), "bin"),
    os.path.join(os.getenv("GST_PATH"  , "C:/gstreamer/1.0"), "x86_64/bin")
] + BINARIES_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change the folders to match your configuration. Adapted from [2]
-   Modify cv2/config-3.8.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
PYTHON_EXTENSIONS_PATHS = [
    # 'C:/opencv/opencv/build/lib/python3/Release'
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-3.8")
] + PYTHON_EXTENSIONS_PATHS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Build 1 [STATUS: Completed Successfully]
With this first build, I will not use the command line option. We will start
directly with cmake-gui. It is a light build with just the default settings,
extra and non free modules and python.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake-gui.exe"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Clear Build Cache. This will remove any previous configuration options.
-   Run configure. Select Visual Studio 16 2019 as your compiler environment.
    Select native compilers.

### Configure Build

The entries in RED need to be taken care off by running Configure again. But
bef0roe that verify your settings with the ones below:

Video

-   `WITH_GSTREAMER = OFF`
-   `WITH_MFX = OFF`, Intel Video Acceleration
-   `WITH_MKL = OFF`, Intel Math Library
-   `WITH_LIBREALSENSE = OFF`, Intel Real Sense Camera

Math Acceleration
-   `WITH_TBB = OFF`, Intel Thread building Blocks
-   `WITH_EIGEN = OFF`

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
-   `BUILD_opencv_python2 = OFF`
-   `OPENCV_EXTRA_MODULES_PATH = "C:/opencv/opencv_contrib/modules"`
-   `OPENCV_ENABLE_NONFREE = ON`
-   `BUILD_SHARED_LIBS = ON`, usually dlls are more memory and space efficient,
    but if you run into dll missing errors you might want this off
-   `BUILD_opencv_world = ON`, create single dll
-   `OPENCV_PYTHON3_VERSION = ON`, not sure, it might have issue with cmake-gui
-   `CPU_BASELINE`, should auto populate to your CPU
-   `BUILD_opencv_hdf = OFF`, HDF5 file format

Modify or create the variable:
-   `PYTHON_DEFAULT_EXECUTABLE = "C:\Python38\python.exe"`
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
py -2 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -2 -c "import cv2; print(cv2.getBuildInformation())"
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Build 2 [STATUS: Completed Successfully]
Now lets enable more features: 
* Intel optimizations 
* Math Kernel Library 
* Thread Building Blocks 
* IPP 
* Eigen
* Video features
* Intel Media SDK

This will activate many additional components. Each one having ability to break
your build. It is difficult to ensure that installing anyone of them will not
impact your build. If something breaks, you can go back to build one.

In this build, we only build wrapper for python 3. Building wrapper for both
python 2 and 3 simultaneously causes problems when loading the cv2 module. If
you need python 2 support, build it with separate project.

### Configure Build
Start cmake-gui in the CMD shell. Make sure the shell environment was configures
as shown above.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:\opencv\opencv\build
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Features to be turned ON/OFF and variables to be set:
-   `OPENCV_EXTRA_MODULES_PATH = "C:/opencv/opencv_contrib/modules"`
-   `OPENCV_ENABLE_NONFREE = ON`
-   `BUILD_SHARED_LIBS = ON`, [2], when on this will created DLLs, when off this
    will created static libraries (\*.lib)
-   `BUILD_opencv_world = ON`, [1,2,4], this will create single dll (SHARED_LIBS
    ON) or lib (SHARED_LIBS OFF) file
-   `BUILD_opencv_python3 = ON`
-   `BUILD_opencv_python2 = OFF`, if you need python 2 module, build it
    separately, when building both, the python 2 version often works but pyton 3
    import cv2 creates a dll error.
-   `OPENCV_PYTHON3_VERSION = ON`, apparently cmake-gui confuses this variable
    [4], [2] recommends it ON
-   `BUILD_opencv_hdf = OFF`, recommended by [1]
-   `ENABLE_FAST_MATH = OFF`, recommended by cmake

Add Entry \* `PYTHON_DEFAULT_EXECUTABLE="C:\Python38\python.exe"`, otherwise
python2 will be used to build opencv.

TBB [STATUS: WORKING]

You either download the TBB source or the prebuilt binaries from Intel. The
cmake configuration should list under Parallel framework: TBB (ver...) [1]
recommends the dlls from C:\Program Files
(x86)\IntelSWTools\compilers\_and_libraries\windows\redist\intel64_win\tbb\vc\_mt
which are statically linked to VC runtime. By default the vc14 versions are
picked up by cmake. The default vc14 works for me.

-   `BUILD_TBB = OFF`, you want to use the pre-compiled files which we
    downloaded and installed earlier. BUILT TBB will create its own TBB
    binaries.
-   `WITH_TBB = ON`, needed if you want to use TBB for thread acceleration,
    either with external libraries (preferred) or build when comppiling OpenCV

The following TBB folders should be set automatically: 
- `TBB_DIR` is not found
- `TBB_ENV_INCLUDE   = C:/Program Files
(x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include` \* `TBB_ENV_LIB
= C:/Program Files
(x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib`
- `TBB_ENV_LIB_DEBUG = C:/Program Files
(x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb_debug.lib`
- `TBB_VER_FILE      = C:/Program Files
(x86)/IntelSWTools/compilers_and_libraries/windows/tbb/include/tbb/tbb_stddef.h`

MKL [STATUS: WORKING] 
- `WITH_MKL = ON` 
- `MKL_USE_MULTITHREAD = ON`, [1] 
- `MKL_WITH_TBB = ON`, [1]

When executing the setup script it should configure automatically: 
- `MKL_INCLUDE_DRIS = C:/Program Files
(x86)/IntelSWTools/compilers_and_libraries/windows/mkl/include` 
- `MKL_LIBRARIES    =`

Make sure the libraries have \_dll.lib extension as the autopopulated one is for
static build:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_intel_lp64_dll.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_sequential_dll.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   `MKL_ROOT_DIR = "C:/Program Files
    (x86)/IntelSWTools/compilers_and_libraries/windows/mkl"`

LAPACK [STATUS: WORKING]

Please verify: 
- `LAPACK_LIBRARIES =`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_intel_lp64_dll.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_sequential_dll.lib;C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For shared library builds the dll.lib versions need to be selected.

Intel Media SDK Support [STATUS: WORKING]
-   `WITH_MFX = ON`
-   `WITH_MSMF = ON`
-   `WITH_MSMF_DXVA = ON`

Please check: 
- `MFX_LIBRARY = C:/Program Files (x86)/IntelSWTools/Intel(R)
Media SDK 2019 R1/Software Development Kit/lib/x64/libmfx_vs2015.lib` 
- `MFX_INCLUDE = C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2019
R1/Software Development Kit/include`

Enabling Intel MFX will create linker warning because libmfx_vs2015.pdb is not
provided in Intel Media SDK.

OPENCL [STATUS: WORKING]

This enables cv::ocl::resize() versus cv::resize() which provides hardware
acceleration.

This should be set automatically. Please check: 
- `WITH_OPENCL = ON` 
- `WITH_OPENCLAMDBLAS = ON` 
- `WITH_OPENCLEMDFFT = ON` 
- `WITH_OPENCL_D3D11_NV = ON` 
- `WITH_OPENCL_SVM = ON`, support vector machine classifier

MISC Features [STATUS: WORKING]
-   `USE_WIN32_FILEIO = ON`
-   `WITH_CUDA = OFF`
-   `OPENCV_DNN_CUDA = OFF`
-   `WITH_GSTREAMER=OFF`
-   `WITH_LIBREALSENSE = OFF`
-   `BUILD_opencv_hdf = OFF`, because its not compatible
-   `WITH_EIGEN = OFF`, because its not compaptible
-   `BUILD_opencv_js = OFF`, because no java wrapping

### Build
Build using "Open_Project" in cmake-gui. Select build / batch build and enable
INSTALL and then click on build.

The Command Shell equivalent is: (incomplete)
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
-DBUILD_opencv_world=ON ^
-DWITH_GSTREAMER=ON ^
-DWITH_MFX=ON ^
-DWITH_MKL=ON ^
-DMKL_USE_MULTITHREAD=ON ^
-DMKL_WITH_TBB=ON ^
-DWITH_TBB=ON ^
-DWITH_EIGEN=OFF ^
-DEIGEN_INCLUDE_PATH="C:/eigen/" ^
-DBUILD_opencv_hdf=OFF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Test
Run python 3 in command shell

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
py -3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Check the python path:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
print('\n'.join(sys.path))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
My output is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\Python38\python38.zip
C:\Python38\DLLs
C:\Python38\lib
C:\Python38
C:\Python38\lib\site-packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Build 3
These are additions to build 3. Do not clear the cache or delete previous build
files.

-   GUI features
    -   VTK
-   Video features
    -   gstreamer
    -   Intel Realsense
-   CPU/HW feature optimization

### Configure Build
CPU/HW feature optimization

Check with the CPU ID app if you have AVX2 and read on
https://github.com/opencv/opencv/wiki/CPU-optimizations-build-options what
baseline features you want to enable.

-   `CPU_BASELINE=AVX2`

VTK [STATUS: WORKING]

VTK 9.0 does not yet compile with release versions of opencv. There latest udates to opencv compiles with VTK 9.0 but you need to turn off world build.

- `VTK_DIR=C:/vtk/8.2/lib/cmake/vtk-8.2`
- `WITH_VTK=ON` 

Intel RealSense [STATUS: WORKING]
-   `WITH_LIBREALSENSE = ON`
-   `realsense2_DIR = "C:/Program Files (x86)/Intel RealSense SDK 2.0"`
-   `LIBREALSENSE_INCLUDE_DIR = "C:/Program Files (x86)/Intel RealSense SDK
    2.0/include"`
-   `LIBREALSENSE_LIBRARIES = "C:/Program Files (x86)/Intel RealSense SDK
    2.0/lib/x64/realsense2.lib"`

This breaks the build with "dll not found" error when importing cv2. At this
time I dont know which dll is not found besides the ones provided by the SDK.
Best appproach might be to build librealsense from source and check if building
the librealsense python wrapper creates the necessary dlls.

GSTREAMER [STATUS: WORKING]
-   `WITH_GSTREAMER=ON`

It automatically sets the path lib, include, glib, glib include, gobject,
gstreamer library, gstreamer utils, riff library if GSTREAMER_DIR is set
correcty.

JAVA [STATUS: ON HOLD]
-   `BUILD_JAVA = ON [2]`
-   `BUILD_opencv_java = OFF`
-   `BUILD_opencv_java_bindings_generator = OFF`

EIGEN [Status: WORKING]

When you turn EIGEN ON, you will need to provide the source code, its not
automatically downloaded. 
```
cd C:\
git clone https://gitlab.com/libeigen/eigen
git checkout 3.3
```

-   `WITH_EIGEN = ON`
-   `EIGEN_INCLUDE_PATH = "C:/eigen"`, make sure to select the directory that is one level above Eigen. for examplpe I have `C:\eigen\Eigen\src` and the include path is `C:/eigen`.
-   `Eigen3_DIR` is not found

### Build
If you build with Visual Studio C, open Build -\> Configuration Manager and
enable INSTALL and click build.

### Test

#### Gstreamer Camera
Try to connect to rtsp stream initated on your local host for example with VLC
Media Player:

Media -\> Stream, Select Capture Device, Show more Options and reduce cache
size. Stream -\> Next, Add Destination Device RTSP Add, 8554, Activate
Transcoding, Encapsulation=MPEG-TS, Video Codec = H-264, Audio off, Stream.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to a Xiaomi Dafang Hack camera
(https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the above with gstreamer binaries work, test it with pyton program:
test_rtsp_simplegstramer.py

## Build 4
QT [STATUS: WORKING]

OpenCV 4.3.0 needs QT 5.14.x

-   `WITH_QT=ON`
-   `Qt5_DIR = C:/Qt/5.14.2/msvc2017_64/lib/cmake/Qt5`
-   `WITH_OPENGL=OFF`, rgpd does not compile with opengl.

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

HDF [STATUS: WORKING]

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

Java [Status: ON HOLD]

If you need the java wrapper to be built, you might need to disable python3.
Somehow python2, python3 and java wrappers dont get along in cmake and OpenCV
and each one will need to be built separately.

JavaScript [STATUS: NOT WORKING]
-   `BUILD_opencv_js = OFF`

## Build 5 [STATUS: Completed Successfully]
Inlucde CUDA. This builds upon previous builds and enables CUDA support.
This is not useful if you dont have Nvidia GPU on your computer. The
CUDA_Generation will need to match your GPU.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Configure BUILD

CUDA support doubles your build size and consumes much larger build time. It is more efficient to figure out other module inclusions before you enable CUDA.

Please make sure the selected CUDA_GENERATION matches the GPU you have
installed: https://en.wikipedia.org/wiki/CUDA\#GPUs_supported. My notebook
computer has a GeForce 960M which is GENERATION Maxwell and Compute Capability
5.0. For detailed coverage of CUDA_ARCH choices and GPU coverage refer to [1]. You can use CPUZ application to identify the hardware in your computer.

CUDA [STATUS: Working]
-   `WITH_CUDA = ON`, enable CUDA
-   `WITH_NVCUVID = ON`, [1] enable CUDA Video decodeing support
-   `WITH_CUFFT = ON`
-   `WITH_CUBLAS = ON` [1,3,7]
-   `CUDA_FAST_MATH = ON`, [2,3]
-   `CUDA_ARCH_BIN = 5.0,5.2`, selected from all options, for shorter compile
    time, select only the one you need, for compatibility, use the default list
    produced by configure
-   `CUDA_ARCH_PTX = 5.0`, leave empty as is default or enter tothe lowest of ARCH_BIN
-   `CUDA_TOOLKIT_ROOT_DIR = "C:/Program Files/NVIDIA GPU Computing
    Toolkit/CUDA/v10.2"`
-   `CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing
    Toolkit/CUDA/v10.2`
-   `CUDA_BUILD_EMULATION = OFF`, autopopulated
-   `CUDA_GENERATION = "Maxwell"`, leave empty or select from list, match to the capability of your computer
-   `CUDA_HOST_COMPLIER =`, autopopulated
-   `CUDA_USE_STATIC_CUDA_RUNTIME = ON`, autopopulated
-   `OPENCV_DNN_CUDA = ON`,[2] Neural Network Classifiers on CUDA, per [1] its
    not necessary to downdload cuDNN from Nvidia and install it.
-   `BUILD_CUDA_STUBS = OFF`
-   `BUILD_opencv_cudev = ON`
-   `BUILD_opencv_cuda* = ON`

nvcuvid library
nvcuvenc library

TEST [STATUS: WORKING]
If you want to conduct performance tests enable these:
-   `INSTALL_TESTS = ON`
-   `BUILD_PERF_TESTS = ON`
-   `BUILD_TESTS = ON`
-   `BUILD_opencv_python_tests = ON`

This build creates a lot of warning: `warning : field of class type without a
DLL interface used in a class with a DLL interface` You can ignore them.

Make sure the PATH includes `C:\Program Files\NVIDIA GPU Computing
Toolkit\CUDA\v10.2\bin`

You might want to rename build/install to build/install_noCUDA so you can
preserve your non_cuda version.

### Build
If you build with Visual Studio C, open Build -\> Configuration Manager and
enable INSTALL and click build.

The command line equievalent is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Test
You can test CUDA performance according [1]:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\opencv\opencv\build\install\x64\vc16\bin\opencv_perf_cudaarithm.exe" --gtest_filter=Sz_Type_Flags_GEMM.GEMM/29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

My outpput is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[ RUN      ] Sz_Type_Flags_GEMM.GEMM/29, where GetParam() = (1024x1024, 32FC2, 0|cv::GEMM_1_T)
[ PERFSTAT ]    (samples=25   mean=12.49   median=12.48   min=11.99   stddev=0.27 (2.1%))
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
cuMat1 = cv.cuda_GpuMat()
cuMat2 = cv.cuda_GpuMat()
cuMat1.upload(npMat1)
cuMat2.upload(npMat2)

_ = cv.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)
current_time = time.time()

for i in range(20):
   _ = cv.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)

cuda_time = time.time()

for i in range(20):
   _ = cv.gemm(npMat1,npMat2,1,None,0,None,1)

cpu_time = time.time()

for i in range(20):
   _ = npMat3 @ npMat4

np_time = time.time()
# CUDA time
print('CUDA execution time is   : {}'.format((cuda_time-current_time)/20.0))
# OpenCV Mat Pultiplication
print('OpenCV execution time is : {}'.format((cpu_time-cuda_time)/20.0))
# NumPy Mat Multiplication
print('NumPy execution time is  : {}'.format((np_time-cpu_time)/20.0))
#
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my setup with python the CUDA routine takes 33ms, the cv2 routine 48ms and
the numpy routine 45ms. Please note, that the first time the CUDA routine is
called it undergoes jit compilation which takes more than 500ms. Also compared
to cuda performance test program, python implementation takes almost 3 times as
long.

## Build 6
Now lets attempt building a single DLL. The more modules you have enabled the less likely this will succeed. 

WORLD ON

Build 1 CMAKE Output
====================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General configuration for OpenCV 4.3.0-dev =====================================
  Version control:               4.3.0-294-ge96a58f091

  Extra modules:
    Location (extra):            C:/opencv/opencv_contrib/modules
    Version control (extra):     4.3.0-48-g1311b057

  Platform:
    Timestamp:                   2020-05-21T22:35:07Z
    Host:                        Windows 10.0.18362 AMD64
    CMake:                       3.17.2
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1926

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe  (ver 19.26.28805.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab world xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    hdf python2
    Disabled by dependency:      -
    Unavailable:                 alphamat cnn_3dobj cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv freetype java js matlab ovis sfm viz
    Applications:                tests perf_tests apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:
    Win32 UI:                    YES
    VTK support:                 NO

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
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES

  Parallel framework:            Concurrency

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      NO
    Eigen:                       NO
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  OpenCL:                        YES (NVD3D11)
    Include path:                C:/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.3)
    Libraries:                   C:/Python38/libs/python38.lib (ver 3.8.3)
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.18.4)
    install path:                C:/Python38/Lib/site-packages/cv2/python-3.8

  Python (for build):            C:/Python38/python.exe

  Java:
    ant:                         C:/ANT/bin/ant.bat (ver 1.10.7)
    JNI:                         C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include/win32 C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include
    Java wrappers:               NO
    Java tests:                  YES

  Install to:                    C:/opencv/opencv/build/install
-----------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build 2 CMAKE Output
====================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General configuration for OpenCV 4.3.0-dev =====================================
  Version control:               4.3.0-294-ge96a58f091

  Extra modules:
    Location (extra):            C:/opencv/opencv_contrib/modules
    Version control (extra):     4.3.0-48-g1311b057

  Platform:
    Timestamp:                   2020-05-21T22:35:07Z
    Host:                        Windows 10.0.18362 AMD64
    CMake:                       3.17.2
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1926

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe  (ver 19.26.28805.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab world xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    hdf python2 python_tests
    Disabled by dependency:      -
    Unavailable:                 alphamat cnn_3dobj cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv freetype java js matlab ovis sfm viz
    Applications:                apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:
    Win32 UI:                    YES
    VTK support:                 NO

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
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES
    Intel Media SDK:             YES (C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2019 R1/Software Development Kit/lib/x64/libmfx_vs2015.lib)

  Parallel framework:            TBB (ver 2020.2 interface 11102)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_intel_lp64_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_tbb_thread_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib)
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  OpenCL:                        YES (SVM NVD3D11)
    Include path:                C:/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.3)
    Libraries:                   C:/Python38/libs/python38.lib (ver 3.8.3)
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.18.4)
    install path:                C:/Python38/Lib/site-packages/cv2/python-3.8

  Python (for build):            C:/Python38/python.exe

  Java:
    ant:                         C:/ANT/bin/ant.bat (ver 1.10.7)
    JNI:                         C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include/win32 C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include
    Java wrappers:               NO
    Java tests:                  NO

  Install to:                    C:/opencv/opencv/build/install
-----------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build 3 CMAKE Output
====================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General configuration for OpenCV 4.3.0-dev =====================================
  Version control:               4.3.0-294-ge96a58f091

  Extra modules:
    Location (extra):            C:/opencv/opencv_contrib/modules
    Version control (extra):     4.3.0-48-g1311b057

  Platform:
    Timestamp:                   2020-05-21T22:35:07Z
    Host:                        Windows 10.0.18362 AMD64
    CMake:                       3.17.2
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1926

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe  (ver 19.26.28805.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:          cudart_static.lib nppc.lib nppial.lib nppicc.lib nppicom.lib nppidei.lib nppif.lib nppig.lib nppim.lib nppist.lib nppisu.lib nppitc.lib npps.lib cublas.lib cudnn.lib cufft.lib -LIBPATH:C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/lib/x64
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 aruco bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev datasets dnn dnn_objdetect dnn_superres dpm face features2d flann fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab world xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    hdf python2 python_tests
    Disabled by dependency:      -
    Unavailable:                 alphamat cnn_3dobj cvv freetype java js matlab ovis sfm viz
    Applications:                apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:
    Win32 UI:                    YES
    VTK support:                 NO

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
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES
    Intel Media SDK:             YES (C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2019 R1/Software Development Kit/lib/x64/libmfx_vs2015.lib)

  Parallel framework:            TBB (ver 2020.2 interface 11102)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_intel_lp64_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_tbb_thread_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib)
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  NVIDIA CUDA:                   YES (ver 10.2, CUFFT CUBLAS NVCUVID FAST_MATH)
    NVIDIA GPU arch:             75
    NVIDIA PTX archs:

  cuDNN:                         YES (ver 7.6.5)

  OpenCL:                        YES (SVM NVD3D11)
    Include path:                C:/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.3)
    Libraries:                   C:/Python38/libs/python38.lib (ver 3.8.3)
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.18.4)
    install path:                C:/Python38/Lib/site-packages/cv2/python-3.8

  Python (for build):            C:/Python38/python.exe

  Java:
    ant:                         C:/ANT/bin/ant.bat (ver 1.10.7)
    JNI:                         C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include/win32 C:/Program Files/AdoptOpenJDK/jdk-11.0.7.10-hotspot/include
    Java wrappers:               NO
    Java tests:                  NO

  Install to:                    C:/opencv/opencv/build/install
-----------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

C:\opencv\opencv\_contrib\modules\cvv\src\qtutil../util/observer_ptr.hpp(177,15):
error C2039: 'logic_error': is not a member of 'std' (compiling source file
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp) C:\Program
Files (x86)\Microsoft Visual
Studio\\2019\Community\VC\Tools\MSVC\\14.26.28801\include\memory(24): message :
see declaration of 'std' (compiling source file
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp)
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil../util/observer_ptr.hpp(174):
message : while compiling class template member function 'void
cvv::util::ObserverPtr::enforceNotNull(void) const' (compiling source file
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp)
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil../util/observer_ptr.hpp(96):
message : see reference to function template instantiation 'void
cvv::util::ObserverPtr::enforceNotNull(void) const' being compiled (compiling
source file C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp)
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.hpp(134): message :
see reference to class template instantiation 'cvv::util::ObserverPtr' being
compiled (compiling source file
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp)
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil../util/observer_ptr.hpp(177,1):
error C2065: 'logic_error': undeclared identifier (compiling source file
C:\opencv\opencv\_contrib\modules\cvv\src\qtutil\collapsable.cpp)

Build 4 CMAKE Output
====================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General configuration for OpenCV 4.3.0-dev =====================================
  Version control:               4.3.0-321-g515a06cedf

  Extra modules:
    Location (extra):            C:/opencv/opencv_contrib/modules
    Version control (extra):     4.3.0-57-g8fc6067b

  Platform:
    Timestamp:                   2020-05-21T22:35:07Z
    Host:                        Windows 10.0.18362 AMD64
    CMake:                       3.17.2
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1926

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe  (ver 19.26.28805.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.26.28801/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL
    ccache:                      NO
    Precompiled headers:         NO
    Extra dependencies:          cudart_static.lib nppc.lib nppial.lib nppicc.lib nppicom.lib nppidei.lib nppif.lib nppig.lib nppim.lib nppist.lib nppisu.lib nppitc.lib npps.lib cublas.lib cudnn.lib cufft.lib -LIBPATH:C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2/lib/x64
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 aruco bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev datasets dnn dnn_objdetect dnn_superres dpm features2d flann fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio world xfeatures2d ximgproc xobjdetect
    Disabled:                    cvv hdf java_bindings_generator photo python2
    Disabled by dependency:      face videostab xphoto
    Unavailable:                 alphamat cnn_3dobj freetype java js matlab ovis sfm viz
    Applications:                tests perf_tests apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:
    QT:                          YES (ver 5.15.0)
      QT OpenGL support:         NO
    Win32 UI:                    YES

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

  Parallel framework:            TBB (ver 2020.2 interface 11102)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_intel_lp64_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64/mkl_tbb_thread_dll.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/tbb/lib/intel64/vc14/tbb.lib C:/Program Files (x86)/IntelSWTools/compilers_and_libraries/windows/mkl/lib/intel64_win/mkl_core_dll.lib)
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
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.18.4)
    install path:                C:/Python38/Lib/site-packages/cv2/python-3.8

  Python (for build):            C:/Python38/python.exe

  Install to:                    C:/opencv
-----------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
