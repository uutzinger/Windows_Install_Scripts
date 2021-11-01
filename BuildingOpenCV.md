# Compiling OpenCV on Windows With CUDA, MKL, TBB, GSTREAMER Support

- [Compiling OpenCV on Windows With CUDA, MKL, TBB, GSTREAMER Support](#compiling-opencv-on-windows-with-cuda--mkl--tbb--gstreamer-support)
  * [Motivation](#motivation)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Pre-Requisites](#pre-requisites)
  * [Obtaining OpenCV Source](#obtaining-opencv-source)
  * [Uninstalling of Previous opencv Installations](#uninstalling-of-previous-opencv-installations)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment)
- [Building OpenCV](#building-opencv)
  * [Debugging Missing Dependencies](#debugging-missing-dependencies)
  * [Build 1](#build-1)
    + [Configure Build](#configure-build)
    + [Configure and Generate](#configure-and-generate)
    + [Build](#build)
    + [Test](#test)
  * [Build 2 MKL,Video, Eigen, HDF, VTK](#build-2-mkl-video--eigen--hdf--vtk)
    + [Configure Build](#configure-build-1)
    + [Build](#build-1)
    + [DLL Fix](#dll-fix)
    + [Test](#test-1)
      - [Gstreamer Camera](#gstreamer-camera)
  * [BUILD 3, CUDA](#build-3--cuda)
    + [Build](#build-2)
    + [DLL Fix](#dll-fix-1)
    + [Test](#test-2)
  * [Create Wheel Install Package](#create-wheel-install-package)
- [DLL Summary](#dll-summary)
- [Build CMAKE Output](#build-cmake-output)
  * [Motivation](#motivation-1)
  * [Approach](#approach-1)
  * [Background Reading](#background-reading-1)
  * [Pre-Requisites](#pre-requisites-1)
  * [Obtaining OpenCV Source](#obtaining-opencv-source-1)
  * [Uninstalling of Previous opencv Installations](#uninstalling-of-previous-opencv-installations-1)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment-1)
- [Building OpenCV](#building-opencv-1)
  * [Debugging Missing Dependencies](#debugging-missing-dependencies-1)
  * [Build 1](#build-1-1)
    + [Configure Build](#configure-build-2)
    + [Configure and Generate](#configure-and-generate-1)
    + [Build](#build-3)
    + [Test](#test-3)
  * [Build 2 MKL,Video, Eigen, HDF, VTK](#build-2-mkl-video--eigen--hdf--vtk-1)
    + [Configure Build](#configure-build-3)
    + [Build](#build-4)
    + [DLL Fix](#dll-fix-2)
    + [Test](#test-4)
      - [Gstreamer Camera](#gstreamer-camera-1)
  * [BUILD 3, CUDA](#build-3--cuda-1)
    + [Build](#build-5)
    + [DLL Fix](#dll-fix-3)
    + [Test](#test-5)
  * [Create Wheel Install Package](#create-wheel-install-package-1)
- [DLL Summary](#dll-summary-1)
- [Build CMAKE Output](#build-cmake-output-1)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Motivation

There are many reasons to build your own OpenCV binaries; for example to enable hardware acceleration or gstreamer.

Building OpenCV beyond its default settings is notoriously difficlut. The
[python for engineers](https://www.pythonforengineers.com/installing-the-libraries-required-for-the-book/)
oline book calls people compiling it "masochists" and "If you get stuck, you will need to ask Stackoverflow, whereupon they will call you an idiot".

The main issues are the many temptations for enabling components that you don’t need but break your build. 
There is to my knowledge no list which version of dependencies compile with latest release version of OpenCV on Visual Studio. 

A build typically takes 10-30 minutes when CUDA is not enabled, taking time when you debug which option is not supported in your environment.
Some build options create a wrapper for external libraries which you need to download prior to the build, and others will download the modules for you. 
The documentation for building opencv beyond the default setting is sparse and google for the build options does not produce quality links.

Once you enable external libraries, you will need to have the corresponding dlls accessible. It is difficult to track which dlls are needed in your PATH or installation directory.

In the builds described here, I want to enable **gstreamer** and architecture specific accelerations. 
In particular **Intel optimized libraries** and **CUDA** support. 
I want architecture optimization because I will attempt using high frame rate cameras in my research.
I want to enable gstreamer because I want to develop python code for Jetson single board computers on my notebook computer. Nividia supports gstreamer with hardware acceleration on Jetson architecture. It does not support ffmpeg the default interface in OpenCV. 

## Approach

In this guide I propose to build OpenCV in several steps and with increasing complexity.

It is common that the activation of one component creates a set of issues that need to be solved. 
Also the activation of one component might not be reverted without clearing previous build cache and cleaning the build directory. 
It is also possible that the cmake and cmake-gui do not create the same build configuration. Make sure the cmake-gui version used in your command shell is from the same folder as cmake: `where cmake` and `where cmake-gui`.

Many online posts have been consulted for this document:

* [1] [James Bowley] (https://jamesbowley.co.uk/accelerate-opencv-4-5-0-on-windows-build-with-cuda-and-python-bindings/)
* [2] [dev.infohub.cc](https://dev.infohub.cc/build-opencv-430-with-cuda/) 
* [3] https://geeks-world.github.io/articles/464015/index.html 
* [4] https://docs.opencv.org/4.3.0/d3/d52/tutorial_windows_install.html 
* [5] https://www.learnopencv.com/install-opencv-4-on-windows/ 
* [6] https://lightbuzz.com/opencv-cuda/ 
* [7] https://pterneas.com/2018/11/02/opencv-cuda/
* [8] https://haroonshakeel.medium.com/build-opencv-4-5-1-with-gpu-cuda-support-on-windows-10-without-tears-cf0e55dc47f9

## Background Reading
The following article explains algorithm optimizations by Intel for opencv 
https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel 
pointing towards Halide and OpenCL.

This is excellent summary of the Halide algorithm development tools https://halide-lang.org/ 
It explains why some programs finish an image processing task much faster than others.

## Pre-Requisites

Prepare your system with 
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md.
I propose to work with dynamic link libraries and to copy some required dlls to a central location.

## Obtaining OpenCV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. 
I place them in the root folder C:/opencv but they can go anywhere. 
Its difficult to figure out which version works with your QT, VTK, and CUDA installation. 
Often the latest master branch solves build problems.
However for the dependencies, often the latest version is likely not yet supported in OpenCV.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir C:/apps/opencv
cd C:/apps/opencv
git clone https://github.com/opencv/opencv.git opencv
git clone https://github.com/opencv/opencv_contrib.git opencv_contrib
git clone https://github.com/opencv/opencv_extra.git opencv_extra
cd C:/apps/opencv/opencv_contrib
git checkout 4.5.3
REM git pull
REM git merge 4.5.4

cd C:/apps/opencv/opencv
git checkout 4.5.3
REM git pull
REM git merge 4.5.4
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
cd C:/apps/opencv/opencv/build
set "openCvSource=C:\apps\opencv\opencv"
set "openCVExtraModules=C:\apps\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you execute some of the vars script twice, it will throw an error the second time. You can ignore those.

**It is critical to run this setup each time in the shell window that you will use to start make, cmake, cmake-gui or ninja before you start configuring your build.**

# Building OpenCV
Here are several builds, each with increasing complexity. 
Its not a good idea to enable all settings at once and then to struggle through the errors. 
Its better to start with a smaller build and then expand.

## Debugging Missing Dependencies
In general this should help finding missing dependencies:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/debugMissingDLL.md

The solution to the dll load failures in OpenCV requires the patches outlined at the end of this document.  
If you already installed OpenCV and dont plan to create a pip install package you will need to apply the changes 
to `C:\Python38\Lib\site-packages` as listed after the build scenarios towards the end of this document.





## Build 1

With this first build, I will use cmake-gui. 
It is a light build with just the default settings, extra and non free modules and python.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:\apps\opencv\opencv\build
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Clear Build Cache. This will remove any previous configuration options.
-   Run configure. Select Visual Studio 16 2019 as your compiler environment. Select native compilers.

### Configure Build

The entries in RED need to be taken care off by running Configure again. 
But befor that, verify your settings with the ones below:

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
-   `BUILD_SHARED_LIBS = ON`, [2], when ON this will created DLLs, when OFF this will created static libraries (\*.lib), usually dlls are more memory and space efficient, but if you run into dll missing errors you might want this OFF
-   `BUILD_opencv_world = OFF`, ON [1,2,4], this will create single dll (SHARED_LIBS ON) or lib (SHARED_LIBS OFF) file, opencv_viz does not build with world.
-   `CPU_BASELINE`, should auto populate to your CPU
-   `BUILD_opencv_hdf = OFF`, HDF5 fileformat, recommended by [1]
-   `ENABLE_FAST_MATH = OFF`, recommended by cmake

Install location
-   `CMAKE_INSTALL_PREFIX = ` leave as is

Modify or create the variable:
-   `BUILD_opencv_python3 = ON` 
-   `BUILD_opencv_python_bindings_generator = ON` 
-   `CMAKE_CONFIGURATION_TYPES = "Release"`

If you have GLOG and GFLAGS on your system
-   `Glog_DIR = C:/apps/glog`
-   `Glog_LIBS = C:/apps/glog/lib/glog.lib`
-   `Gflags_DIR = C:/apps/gflags/lib/cmake/gflags`

### Configure and Generate

After successful configuration, CMAKE should have found python2 and python3 as
well as your java environment. If python or java environment is not found you
can attempt running the CMD line version below and then revisit it with
cmake-gui as shown above. Don't delete the cache. Just rerun configure in the
gui.

Run the Generate function to create your build project. If generate shows errors
and warnings but completes its process, you can continue building OpenCV.

### Build
And finally do first build using "Open_Project" in cmake-gui. Select build /
batch build and enable INSTALL and then click on build. If there are previously
compiled files in your build directory. you can clean them with the "clean"
button.

The command line equivalent is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build Time: 31 minutes 8:42

### Test
In a command shell:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Build 2 MKL,Video, Eigen, HDF, VTK

You should complete Build 1 before you start Build 2.

Now lets enable more features: 
* Intel optimizations 
  * Math Kernel Library 
  * Thread Building Blocks 
* Video features (optional)
  * Intel Media SDK (if you have intel cpu)
  * gstreamer
  * Intel Realsense (optional)
* EIGEN
* HDF file format (optional)
* GUI features
  *   VTK (optional)

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

**TBB**

Download the TBB source or the prebuilt binaries from Intel. The cmake configuration should list under Parallel framework: TBB (ver...) 

- `BUILD_TBB = OFF`, you want to use the pre-compiled files which we downloaded and installed earlier. BUILD TBB will create its own TBB binaries and I did not want that.
- `WITH_TBB = ON`, needed if you want to use TBB for thread acceleration, either with external libraries (preferred) or build when comppiling OpenCV

The following TBB folders should be set automatically: 
- `TBB_DIR           = C:/Program Files (x86)/Intel/oneAPI/tbb/2021.3.0/lib/cmake/tbb`
- `TBB_ENV_INCLUDE   = C:/Program Files (x86)/Intel.../tbb/include`
- `TBB_ENV_LIB       = C:/Program Files (x86)/Intel.../vc14/tbb.lib`
- `TBB_ENV_LIB_DEBUG = C:/Program Files (x86)/Intel.../vc14/tbb_debug.lib`
- `TBB_VER_FILE      = C:/Program Files (x86)/Intel/oneAPI/tbb/2021.3.0/include/oneapi/tbb/version.h`

**MKL**       

- `WITH_MKL = ON`, should find MKL automatically
- `MKL_ROOT_DIR = C:/Program Files (x86)/Intel.../mkl`
- `MKL_USE_MULTITHREAD = ON`, [1] , not available in 4.5.x
- `MKL_WITH_TBB = ON`, [1]

When executing the setup script it should configure automatically: 
- `MKL_INCLUDE_DRIS = C:/Program Files (x86)/Intel.../mkl/include` 
- `MKL_LIBRARIES ** =` 

If you have compilation issues you can try the **\_dll.lib** extension.

**LAPACK**

Please verify: 
- `LAPACK_INLCUDE_DIR = C:/Program Files (x86)/Intel.../mkl/include`
- `LAPACK_LIBRARIES =` 

**Intel Media SDK Support** (optional,only if you have Intel CPU)
-   `WITH_MFX = ON`
-   `WITH_MSMF = ON`
-   `WITH_MSMF_DXVA = ON`

Please check (you will need to rerun Configure in cmake first): 
- `MFX_LIBRARY = C:/Program Files (x86)/Intel.../lib/x64/libmfx_vs2015.lib` 
- `MFX_INCLUDE = C:/Program Files (x86)/Intel.../Software Development Kit/include`

**OPENCL**

This enables cv::ocl::resize() versus cv::resize() which provides hardware acceleration.

This should be set automatically. Please check: 
- `WITH_OPENCL = ON` 
- `WITH_OPENCLAMDBLAS = OFF` 
- `WITH_OPENCLEMDFFT = ON` 
- `WITH_OPENCL_D3D11_NV = ON` 
- `WITH_OPENCL_SVM = OFF`

**GSTREAMER**

-   `WITH_GSTREAMER=ON`

It automatically sets the path lib, include, glib, glib include, gobject, gstreamer library, gstreamer utils, riff library if GSTREAMER_DIR is set correctly.

**EIGEN**

When you turn EIGEN ON, you will need to provide the source code, its not automatically downloaded. 
I put the EIGEN code here:
```
cd C:\apps
git clone https://gitlab.com/libeigen/eigen
git checkout 3.3
```

Then I configured:
-   `WITH_EIGEN = ON`
-   `EIGEN_INCLUDE_PATH = "C:/apps/eigen"`, make sure to select the directory that is one level above Eigen. for examplpe I have `C:\eigen\Eigen\src` and the include path is `C:/eigen`.
-   `Eigen3_DIR` is not found which is ok

**Intel RealSense** (optional)

-   `WITH_LIBREALSENSE = ON`
You will need to rerun configure then:  
-   `realsense2_DIR = "C:/Program Files (x86)/Intel RealSense SDK 2.0"`
-   `LIBREALSENSE_INCLUDE_DIR = C:/Program Files (x86)/Intel RealSense SDK 2.0/include`
-   `LIBREALSENSE_LIBRARIES = C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib`

**VTK** (optional)
You can also use VTK python wrapper instead

- `VTK_DIR = C:\vtk\9.0\lib\cmake\vtk-9.0`
- `WITH_VTK = ON` 
- `BUILD_opencv_world = OFF`, cmake does not complete with world on, it fails configuring the viz module

**HDF** (optional
You can also use  HDF5 python wrapper

To include HDF5 support it is advised to build HDF5 on your computer first.
```
cd C:\apps\hdf5
git clone https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git
cd hdf5
git checkout hdf5_1_12
mkdir build
cd build
cmake-gui ..\
```
* CMAKE_INSTALL_PREFIX = C:/apps/hdf5/

Config->Generate->Open Project
Compile with BatchBuild and enable 64bit Release of INSTALL. When HDF5 build completes configure opencv for HDF5.

Set:

* `hdf5_c_library = C:/apps/hdf5/lib/hdf5.lib`
* `hdf5_include_dirs =  C:/apps/hdf5/include`

`libhdf5lib.lib` is for static build and `hdf5.lib` is for shared build.

Configure again and you should have following option
* `BUILD_opencv_hdf = ON`


**JAVA**

You will need ANT and JDK installed. Set ANT_HOME and JAVA_HOME

-   `BUILD_JAVA = ON` [2]
-   `BUILD_opencv_java = ON`
-   `BUILD_opencv_java_bindings_generator = ON`

**QT** (optional)

STATUS: ON HOLD, Windows interface works ok, but use separate QT wrapper if you need QT

-   `WITH_QT=ON`
-   `Qt5_DIR = C:/Qt/5.14.2/msvc2017_64/lib/cmake/Qt5`
-   `WITH_OPENGL=ON`, rgpd does not compile with opengl.

Rerun configure and generate in cmake-gui once the Qt5_DIR is set. QT allows several version to be installed simultanously, make sure you select version that works.

**Miscalaneous** 
-   `USE_WIN32_FILEIO = ON`windows file input output
-   `WITH_CUDA = OFF` keep this off for now
-   `OPENCV_DNN_CUDA = OFF`

### Build
Build using "Open_Project" in cmake-gui. Select `build / batch build` and enable `INSTALL` on `Release` version and then click on `build`.

### DLL Fix
Your installation now will depend on additional DLLs.

-   Modify `C:\Python38\Lib\site-packages\cv2\config.py` with example at end of document

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
C:\opencv\4.5.4\setup_vars_opencv4.cmd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Gstreamer Camera
Try to connect to rtsp stream initated on your local host for example with VLC Media Player:

- Media -\> Stream, Select Capture Device, Show more Options and reduce cache size.   
- Stream -\> Next,   
- Add Destination Device RTSP Add, 8554,   
- Activate Transcoding, Encapsulation=MPEG-TS, Video Codec = H-264, Audio off, Stream.

Check connection with standalone gstreamer application:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also connect to a Xiaomi Dafang Hack camera (https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the above with the gstreamer binaries work, test it with pyton program: test_rtsp_simplegstreamer.py





## BUILD 3, CUDA

Finally inlucde CUDA. This builds upon previous builds and enables CUDA support.
This is not useful if you dont have Nvidia GPU on your computer. 
The CUDA_Generation will need to match your GPU. This will be automatically selected.
CUDA support takes a long time to compile.

CUDA support doubles your build size and consumes much larger build time. It is better to figure out issues with other modules first because once you enable CUDA it takes a while to get compilation done.

Please make sure the selected CUDA_GENERATION matches the GPU you have installed: 
https://en.wikipedia.org/wiki/CUDA\#GPUs_supported. 
My notebook computer has a GeForce 960M which is GENERATION Maxwell and Compute Capability 5.0. 
For detailed coverage of CUDA_ARCH choices and GPU coverage refer to [1]. 
You can use CPUZ application to identify the hardware in your computer.
You can keep default setting which builds support for all CUDA architectures.

**CUDA**
-   `WITH_CUDA = ON`, enable CUDA
Run configure again, then the following should be available:    
-   `WITH_NVCUVID = ON`, [1] enable CUDA Video decodeing support
-   `WITH_CUFFT = ON`
-   `WITH_CUDNN = ON`
-   `WITH_CUBLAS = ON` [1,3,7]
-   `CUDA_FAST_MATH = OFF`, [2,3 have if ON], leave it OFF for accuracy
-   `CUDA_ARCH_BIN = 8.0,8.6`, selected from all options, for shorter compile time, select only the one you need, for compatibility, use the default list produced by configure (3.5;3.7;5.0;5.2;6.0;6.1;7.0;7.5;8.0;8.6)
-   `CUDA_ARCH_PTX = `, leave empty as is default or enter the lowest of ARCH_BIN
-   `CUDA_TOOLKIT_ROOT_DIR = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4"`
-   `CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4`
-   `CUDA_BUILD_EMULATION = OFF`, autopopulated
-   `CUDA_GENERATION = "Ampere"`, leave empty or select from list, match to the capability of your computer
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

Build Time: Many hours if all CUDA_ARCH_BINs are selected.

### DLL Fix

-   Modify `cv2/config.py`, see example at end of document

### Test
You can test CUDA performance according [1]:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\apps\opencv\opencv\build\install\x64\vc16\bin\ ..
"C:\opencv\opencv\x64\vc16\bin\opencv_perf_cudaarithm.exe" --gtest_filter=Sz_Type_Flags_GEMM.GEMM/29
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

You can test CUDA performance in python with:
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

jit_time = time.time()
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

# CUDA jit compilation
print('CUDA compilation time is   : {}'.format((current_time-jit_time)))

# CUDA time
print('CUDA execution time is   : {}'.format((cuda_time-current_time)/100.0))

# OpenCV Mat Pultiplication
print('OpenCV execution time is : {}'.format((cpu_time-cuda_time)/100.0))

# NumPy Mat Multiplication
print('NumPy execution time is  : {}'.format((np_time-cpu_time)/100.0))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my Dell Inspiron 15 7559 (core i7 6th gen, GTX960M) notebook setup with python the   
CUDA execution time is 9-29ms,  
CV2 execution time is 95-106ms,    
Numpy execution tims is 38-44ms   

RTX 3060 Laptop and Ryzen 7 Mobile 4800H  
CUDA execution time is 2.6-2.8ms  
OpenCV execution time is 95-97ms  
NumPy  execution time is 23ms  

Please note, that the first time the CUDA routine is called it undergoes jit compilation which takes more than 800ms. 
Also compared to compiled cuda performance test program, python implementation can take up to twice the time.

## Create Wheel Install Package

A few things will need to be prepared manually:

-   `cd C:\apps\opencv\opencv\build\python_loader`
-   `xcopy "..\lib\python3\Release\*.pyd" .\cv2\python-3.8 /i`
-   `xcopy "..\bin\Release\*.dll"         .\cv2\python-3.8 /i`
-   `xcopy "..\bin\Release\*.exe"         .\cv2\python-3.8 /i`
-   `xcopy "..\..\data\haarcascades\*"    .\cv2\python-3.8\data\ /i`
-   `echo graft cv2\python-3.8          > MANIFEST.in`

-   Modify `setup.py` so that lines 55-58 are:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ],
        # Additional Parameters
        include_package_data=True,
        zip_safe=False,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-   Change the name of the package in `setup.py` from `opencv` to `opencv-python`  

-   Modify cv2/config.py so that opencv can find additional dlls it needs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    # os.path.join('C:/apps/opencv/opencv/build/install', 'x64/vc16/bin'),
    os.path.join(os.getenv('CUDA_PATH', 'C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4'), 'bin'),
    os.path.join(os.getenv('TBB_PATH',  'C:/Program Files (x86)/Intel/oneAPI/tbb/latest/redist'),    'intel64/vc14'),
    os.path.join(os.getenv('MKL_PATH',  'C:/Program Files (x86)/Intel/oneAPI/mkl/latest/redist'),    'intel64'),
    os.path.join(os.getenv('GST_PATH',  'C:/apps/gstreamer/1.0'),                                    'msvc_x86_64/bin'),
    os.path.join(os.getenv('HDF5_PATH', 'C:/apps/hdf5'), 'bin'),
    # os.path.join(os.getenv('REALSENSE_PATH',  'C:/Program Files (x86)/Intel RealSense SDK 2.0'), 'bin/x64'),
    # os.path.join(os.getenv('INTELMEDIA_PATH', 'C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2020 R1/Software Development Kit'), 'bin/x64'),
    # os.path.join(os.getenv('VTK_PATH',        'C:/vtk/9.0'), 'bin'),
    # os.path.join(os.getenv('QT_PATH',         'C:/Qt/5.14.2/msvc2017_64'), 'bin')    
] + BINARIES_PATHS

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Modify cv2/config-3.8.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PYTHON_EXTENSIONS_PATHS = [
    os.path.join('C:/Python38/Lib/site-packages/cv2', 'python-3.8')
] + PYTHON_EXTENSIONS_PATHS

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   `py -3 setup.py bdist_wheel`

Your whl package is in `.\dist\` 
You can insall it with `pip3 install nameofthewheel.whl`

DLL Summary
===============

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Opencv DLLs
"C:\opencv\opencv\4.5.4\build\..

# TBB DDLs
"C:\Program Files (x86)\Intel...

# MKL DLLs
"C:\Program Files (x86)\Intel\..
#  VTK DLLs
"C:\vtk\9.0\bin\"

# CUDA DLLs

"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin\

# gstreamer DLLs
"C:\gstreamer\1.0\msvc_x86_64\bin\"     

# Realsense
"C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64

# Media
"C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2020 R1\Software Development Kit\bin\x64\

# HDF5
"C:\hdf5\1.12.1\bin\hdf5.dll" 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build CMAKE Output
==================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
eneral configuration for OpenCV 4.5.4 =====================================
  Version control:               4.5.4-dirty

  Extra modules:
    Location (extra):            C:/apps/opencv/opencv_contrib/modules
    Version control (extra):     4.5.4

  Platform:
    Timestamp:                   2021-10-01T03:17:14Z
    Host:                        Windows 10.0.19042 AMD64
    CMake:                       3.21.3
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1929
    Configuration:               Debug Release

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3
    Dispatched code generation:  SSE4_1 SSE4_2 FP16 AVX AVX2 AVX512_SKX
      requested:                 SSE4_1 SSE4_2 AVX FP16 AVX2 AVX512_SKX
      SSE4_1 (17 files):         + SSSE3 SSE4_1
      SSE4_2 (2 files):          + SSSE3 SSE4_1 POPCNT SSE4_2
      FP16 (1 files):            + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 AVX
      AVX (5 files):             + SSSE3 SSE4_1 POPCNT SSE4_2 AVX
      AVX2 (32 files):           + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2
      AVX512_SKX (8 files):      + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2 AVX_512F AVX512_COMMON AVX512_SKX

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/cl.exe  (ver 19.29.30133.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG 
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1 
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG 
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1 
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO 
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL 
    ccache:                      NO
    Precompiled headers:         YES
    Extra dependencies:          cudart_static.lib nppc.lib nppial.lib nppicc.lib nppidei.lib nppif.lib nppig.lib nppim.lib nppist.lib nppisu.lib nppitc.lib npps.lib cublas.lib cudnn.lib cufft.lib -LIBPATH:C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4/lib/x64
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 alphamat aruco barcode bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hdf hfs highgui img_hash imgcodecs imgproc intensity_transform java line_descriptor mcc ml objdetect optflow phase_unwrapping photo plot quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab wechat_qrcode xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    world
    Disabled by dependency:      -
    Unavailable:                 cvv julia matlab ovis sfm viz
    Applications:                tests perf_tests apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:                           WIN32UI
    Win32 UI:                    YES
    VTK support:                 NO

  Media I/O: 
    ZLib:                        build (ver 1.2.11)
    JPEG:                        build-libjpeg-turbo (ver 2.1.0-62)
    WEBP:                        build (ver encoder: 0x020f)
    PNG:                         build (ver 1.6.37)
    TIFF:                        build (ver 42 - 4.2.0)
    JPEG 2000:                   build (ver 2.4.0)
    OpenEXR:                     build (ver 2.3.0)
    HDR:                         YES
    SUNRASTER:                   YES
    PXM:                         YES
    PFM:                         YES

  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES (prebuilt binaries)
      avcodec:                   YES (58.134.100)
      avformat:                  YES (58.76.100)
      avutil:                    YES (56.70.100)
      swscale:                   YES (5.9.100)
      avresample:                YES (4.0.0)
    GStreamer:                   YES (1.18.5)
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES

  Parallel framework:            TBB (ver 2021.3 interface 12030)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/apps/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/apps/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_intel_lp64.lib C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_sequential.lib C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_core.lib)
    Eigen:                       YES (ver 3.4.0)
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  NVIDIA CUDA:                   YES (ver 11.4, CUFFT CUBLAS)
    NVIDIA GPU arch:             80 86
    NVIDIA PTX archs:

  cuDNN:                         YES (ver 8.2.4)

  OpenCL:                        YES (NVD3D11)
    Include path:                C:/apps/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.10)
    Libraries:                   NO
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.21.2)
    install path:                -

  Python (for build):            C:/Python38/python.exe

  Java:                          
    ant:                         C:/apps/ant/bin/ant.bat (ver 1.9.16)
    JNI:                         C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include/win32 C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include
    Java wrappers:               YES
    Java tests:                  YES

  Install to:                    C:/apps/opencv/opencv/build/install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Motivation

There are many reasons to build your own OpenCV binaries; for example to enable hardware acceleration or gstreamer.

Building OpenCV beyond its default settings is notoriously difficlut. The
[python for engineers](https://www.pythonforengineers.com/installing-the-libraries-required-for-the-book/)
oline book calls people compiling it "masochists" and "If you get stuck, you will need to ask Stackoverflow, whereupon they will call you an idiot".

The main issues are the many temptations for enabling components that you don’t need but break your build. 
There is to my knowledge no list which version of dependencies compile with latest release version of OpenCV on Visual Studio. 

A build typically takes 10-30 minutes when CUDA is not enabled, taking time when you debug which option is not supported in your environment.
Some build options create a wrapper for external libraries which you need to download prior to the build, and others will download the modules for you. 
The documentation for building opencv beyond the default setting is sparse and google for the build options does not produce quality links.

Once you enable external libraries, you will need to have the corresponding dlls accessible. It is difficult to track which dlls are needed in your PATH or installation directory.

In the builds described here, I want to enable **gstreamer** and architecture specific accelerations. 
In particular **Intel optimized libraries** and **CUDA** support. 
I want architecture optimization because I will attempt using high frame rate cameras in my research.
I want to enable gstreamer because I want to develop python code for Jetson single board computers on my notebook computer. Nividia supports gstreamer with hardware acceleration on Jetson architecture. It does not support ffmpeg the default interface in OpenCV. 

## Approach

In this guide I propose to build OpenCV in several steps and with increasing complexity.

It is common that the activation of one component creates a set of issues that need to be solved. 
Also the activation of one component might not be reverted without clearing previous build cache and cleaning the build directory. 
It is also possible that the cmake and cmake-gui do not create the same build configuration. Make sure the cmake-gui version used in your command shell is from the same folder as cmake: `where cmake` and `where cmake-gui`.

Many online posts have been consulted for this document:

* [1] [James Bowley] (https://jamesbowley.co.uk/accelerate-opencv-4-5-0-on-windows-build-with-cuda-and-python-bindings/)
* [2] [dev.infohub.cc](https://dev.infohub.cc/build-opencv-430-with-cuda/) 
* [3] https://geeks-world.github.io/articles/464015/index.html 
* [4] https://docs.opencv.org/4.3.0/d3/d52/tutorial_windows_install.html 
* [5] https://www.learnopencv.com/install-opencv-4-on-windows/ 
* [6] https://lightbuzz.com/opencv-cuda/ 
* [7] https://pterneas.com/2018/11/02/opencv-cuda/
* [8] https://haroonshakeel.medium.com/build-opencv-4-5-1-with-gpu-cuda-support-on-windows-10-without-tears-cf0e55dc47f9

## Background Reading
The following article explains algorithm optimizations by Intel for opencv 
https://www.slideshare.net/embeddedvision/making-opencv-code-run-fast-a-presentation-from-intel 
pointing towards Halide and OpenCL.

This is excellent summary of the Halide algorithm development tools https://halide-lang.org/ 
It explains why some programs finish an image processing task much faster than others.

## Pre-Requisites

Prepare your system with 
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md.
I propose to work with dynamic link libraries and to copy some required dlls to a central location.

## Obtaining OpenCV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. 
I place them in the root folder C:/opencv but they can go anywhere. 
Its difficult to figure out which version works with your QT, VTK, and CUDA installation. 
Often the latest master branch solves build problems.
However for the dependencies, often the latest version is likely not yet supported in OpenCV.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mkdir C:/apps/opencv
cd C:/apps/opencv
git clone https://github.com/opencv/opencv.git opencv
git clone https://github.com/opencv/opencv_contrib.git opencv_contrib
git clone https://github.com/opencv/opencv_extra.git opencv_extra
cd C:/apps/opencv/opencv_contrib
git checkout 4.5.3
REM git pull
REM git merge 4.5.4

cd C:/apps/opencv/opencv
git checkout 4.5.3
REM git pull
REM git merge 4.5.4
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
cd C:/apps/opencv/opencv/build
set "openCvSource=C:\apps\opencv\opencv"
set "openCVExtraModules=C:\apps\opencv\opencv_contrib\modules"
set "openCvBuild=%openCvSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you execute some of the vars script twice, it will throw an error the second time. You can ignore those.

**It is critical to run this setup each time in the shell window that you will use to start make, cmake, cmake-gui or ninja before you start configuring your build.**

# Building OpenCV
Here are several builds, each with increasing complexity. 
Its not a good idea to enable all settings at once and then to struggle through the errors. 
Its better to start with a smaller build and then expand.

## Debugging Missing Dependencies
In general this should help finding missing dependencies:
https://github.com/uutzinger/Windows_Install_Scripts/blob/master/debugMissingDLL.md

The solution to the dll load failures in OpenCV requires the patches outlined at the end of this document.  
If you already installed OpenCV and dont plan to create a pip install package you will need to apply the changes 
to `C:\Python38\Lib\site-packages` as listed after the build scenarios towards the end of this document.





## Build 1

With this first build, I will use cmake-gui. 
It is a light build with just the default settings, extra and non free modules and python.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:\apps\opencv\opencv\build
cmake-gui ..\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Clear Build Cache. This will remove any previous configuration options.
-   Run configure. Select Visual Studio 16 2019 as your compiler environment. Select native compilers.

### Configure Build

The entries in RED need to be taken care off by running Configure again. 
But befor that, verify your settings with the ones below:

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
-   `BUILD_SHARED_LIBS = ON`, [2], when ON this will created DLLs, when OFF this will created static libraries (\*.lib), usually dlls are more memory and space efficient, but if you run into dll missing errors you might want this OFF
-   `BUILD_opencv_world = OFF`, ON [1,2,4], this will create single dll (SHARED_LIBS ON) or lib (SHARED_LIBS OFF) file, opencv_viz does not build with world.
-   `CPU_BASELINE`, should auto populate to your CPU
-   `BUILD_opencv_hdf = OFF`, HDF5 fileformat, recommended by [1]
-   `ENABLE_FAST_MATH = OFF`, recommended by cmake

Install location
-   `CMAKE_INSTALL_PREFIX = ` leave as is

Modify or create the variable:
-   `BUILD_opencv_python3 = ON` 
-   `BUILD_opencv_python_bindings_generator = ON` 
-   `CMAKE_CONFIGURATION_TYPES = "Release"`

If you have GLOG and GFLAGS on your system
-   `Glog_DIR = C:/apps/glog`
-   `Glog_LIBS = C:/apps/glog/lib/glog.lib`
-   `Gflags_DIR = C:/apps/gflags/lib/cmake/gflags`

### Configure and Generate

After successful configuration, CMAKE should have found python2 and python3 as
well as your java environment. If python or java environment is not found you
can attempt running the CMD line version below and then revisit it with
cmake-gui as shown above. Don't delete the cache. Just rerun configure in the
gui.

Run the Generate function to create your build project. If generate shows errors
and warnings but completes its process, you can continue building OpenCV.

### Build
And finally do first build using "Open_Project" in cmake-gui. Select build /
batch build and enable INSTALL and then click on build. If there are previously
compiled files in your build directory. you can clean them with the "clean"
button.

The command line equivalent is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build Time: 31 minutes 8:42

### Test
In a command shell:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\opencv\opencv\build\install\setup_vars_opencv4.cmd
py -3 -c "import cv2; print(f'OpenCV: {cv2.__version__} for python installed and working')"
py -3 -c "import cv2; print(cv2.getBuildInformation())"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Build 2 MKL,Video, Eigen, HDF, VTK

You should complete Build 1 before you start Build 2.

Now lets enable more features: 
* Intel optimizations 
  * Math Kernel Library 
  * Thread Building Blocks 
* Video features (optional)
  * Intel Media SDK (if you have intel cpu)
  * gstreamer
  * Intel Realsense (optional)
* EIGEN
* HDF file format (optional)
* GUI features
  *   VTK (optional)

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

**TBB**

Download the TBB source or the prebuilt binaries from Intel. The cmake configuration should list under Parallel framework: TBB (ver...) 

- `BUILD_TBB = OFF`, you want to use the pre-compiled files which we downloaded and installed earlier. BUILD TBB will create its own TBB binaries and I did not want that.
- `WITH_TBB = ON`, needed if you want to use TBB for thread acceleration, either with external libraries (preferred) or build when comppiling OpenCV

The following TBB folders should be set automatically: 
- `TBB_DIR           = C:/Program Files (x86)/Intel/oneAPI/tbb/2021.3.0/lib/cmake/tbb`
- `TBB_ENV_INCLUDE   = C:/Program Files (x86)/Intel.../tbb/include`
- `TBB_ENV_LIB       = C:/Program Files (x86)/Intel.../vc14/tbb.lib`
- `TBB_ENV_LIB_DEBUG = C:/Program Files (x86)/Intel.../vc14/tbb_debug.lib`
- `TBB_VER_FILE      = C:/Program Files (x86)/Intel/oneAPI/tbb/2021.3.0/include/oneapi/tbb/version.h`

**MKL**       

- `WITH_MKL = ON`, should find MKL automatically
- `MKL_ROOT_DIR = C:/Program Files (x86)/Intel.../mkl`
- `MKL_USE_MULTITHREAD = ON`, [1] , not available in 4.5.x
- `MKL_WITH_TBB = ON`, [1]

When executing the setup script it should configure automatically: 
- `MKL_INCLUDE_DRIS = C:/Program Files (x86)/Intel.../mkl/include` 
- `MKL_LIBRARIES ** =` 

If you have compilation issues you can try the **\_dll.lib** extension.

**LAPACK**

Please verify: 
- `LAPACK_INLCUDE_DIR = C:/Program Files (x86)/Intel.../mkl/include`
- `LAPACK_LIBRARIES =` 

**Intel Media SDK Support** (optional,only if you have Intel CPU)
-   `WITH_MFX = ON`
-   `WITH_MSMF = ON`
-   `WITH_MSMF_DXVA = ON`

Please check (you will need to rerun Configure in cmake first): 
- `MFX_LIBRARY = C:/Program Files (x86)/Intel.../lib/x64/libmfx_vs2015.lib` 
- `MFX_INCLUDE = C:/Program Files (x86)/Intel.../Software Development Kit/include`

**OPENCL**

This enables cv::ocl::resize() versus cv::resize() which provides hardware acceleration.

This should be set automatically. Please check: 
- `WITH_OPENCL = ON` 
- `WITH_OPENCLAMDBLAS = OFF` 
- `WITH_OPENCLEMDFFT = ON` 
- `WITH_OPENCL_D3D11_NV = ON` 
- `WITH_OPENCL_SVM = OFF`

**GSTREAMER**

-   `WITH_GSTREAMER=ON`

It automatically sets the path lib, include, glib, glib include, gobject, gstreamer library, gstreamer utils, riff library if GSTREAMER_DIR is set correctly.

**EIGEN**

When you turn EIGEN ON, you will need to provide the source code, its not automatically downloaded. 
I put the EIGEN code here:
```
cd C:\apps
git clone https://gitlab.com/libeigen/eigen
git checkout 3.3
```

Then I configured:
-   `WITH_EIGEN = ON`
-   `EIGEN_INCLUDE_PATH = "C:/apps/eigen"`, make sure to select the directory that is one level above Eigen. for examplpe I have `C:\eigen\Eigen\src` and the include path is `C:/eigen`.
-   `Eigen3_DIR` is not found which is ok

**Intel RealSense** (optional)

-   `WITH_LIBREALSENSE = ON`
You will need to rerun configure then:  
-   `realsense2_DIR = "C:/Program Files (x86)/Intel RealSense SDK 2.0"`
-   `LIBREALSENSE_INCLUDE_DIR = C:/Program Files (x86)/Intel RealSense SDK 2.0/include`
-   `LIBREALSENSE_LIBRARIES = C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib`

**VTK** (optional)
You can also use VTK python wrapper instead

- `VTK_DIR = C:\vtk\9.0\lib\cmake\vtk-9.0`
- `WITH_VTK = ON` 
- `BUILD_opencv_world = OFF`, cmake does not complete with world on, it fails configuring the viz module

**HDF** (optional
You can also use  HDF5 python wrapper

To include HDF5 support it is advised to build HDF5 on your computer first.
```
cd C:\apps\hdf5
git clone https://bitbucket.hdfgroup.org/scm/hdffv/hdf5.git
cd hdf5
git checkout hdf5_1_12
mkdir build
cd build
cmake-gui ..\
```
* CMAKE_INSTALL_PREFIX = C:/apps/hdf5/

Config->Generate->Open Project
Compile with BatchBuild and enable 64bit Release of INSTALL. When HDF5 build completes configure opencv for HDF5.

Set:

* `hdf5_c_library = C:/apps/hdf5/lib/hdf5.lib`
* `hdf5_include_dirs =  C:/apps/hdf5/include`

`libhdf5lib.lib` is for static build and `hdf5.lib` is for shared build.

Configure again and you should have following option
* `BUILD_opencv_hdf = ON`


**JAVA**

You will need ANT and JDK installed. Set ANT_HOME and JAVA_HOME

-   `BUILD_JAVA = ON` [2]
-   `BUILD_opencv_java = ON`
-   `BUILD_opencv_java_bindings_generator = ON`

**QT** (optional)

STATUS: ON HOLD, Windows interface works ok, but use separate QT wrapper if you need QT

-   `WITH_QT=ON`
-   `Qt5_DIR = C:/Qt/5.14.2/msvc2017_64/lib/cmake/Qt5`
-   `WITH_OPENGL=ON`, rgpd does not compile with opengl.

Rerun configure and generate in cmake-gui once the Qt5_DIR is set. QT allows several version to be installed simultanously, make sure you select version that works.

**Miscalaneous** 
-   `USE_WIN32_FILEIO = ON`windows file input output
-   `WITH_CUDA = OFF` keep this off for now
-   `OPENCV_DNN_CUDA = OFF`

### Build
Build using "Open_Project" in cmake-gui. Select `build / batch build` and enable `INSTALL` on `Release` version and then click on `build`.

### DLL Fix
Your installation now will depend on additional DLLs.

-   Modify `C:\Python38\Lib\site-packages\cv2\config.py` with example at end of document

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
C:\opencv\4.5.4\setup_vars_opencv4.cmd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### Gstreamer Camera
Try to connect to rtsp stream initated on your local host for example with VLC Media Player:

- Media -\> Stream, Select Capture Device, Show more Options and reduce cache size.   
- Stream -\> Next,   
- Add Destination Device RTSP Add, 8554,   
- Activate Transcoding, Encapsulation=MPEG-TS, Video Codec = H-264, Audio off, Stream.

Check connection with standalone gstreamer application:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 playbin uri=rtsp://localhost:8554/camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also connect to a Xiaomi Dafang Hack camera (https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gst-launch-1.0 rtspsrc location=rtsp://192.168.11.26:1181/camera latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the above with the gstreamer binaries work, test it with pyton program: test_rtsp_simplegstreamer.py





## BUILD 3, CUDA

Finally inlucde CUDA. This builds upon previous builds and enables CUDA support.
This is not useful if you dont have Nvidia GPU on your computer. 
The CUDA_Generation will need to match your GPU. This will be automatically selected.
CUDA support takes a long time to compile.

CUDA support doubles your build size and consumes much larger build time. It is better to figure out issues with other modules first because once you enable CUDA it takes a while to get compilation done.

Please make sure the selected CUDA_GENERATION matches the GPU you have installed: 
https://en.wikipedia.org/wiki/CUDA\#GPUs_supported. 
My notebook computer has a GeForce 960M which is GENERATION Maxwell and Compute Capability 5.0. 
For detailed coverage of CUDA_ARCH choices and GPU coverage refer to [1]. 
You can use CPUZ application to identify the hardware in your computer.
You can keep default setting which builds support for all CUDA architectures.

**CUDA**
-   `WITH_CUDA = ON`, enable CUDA
Run configure again, then the following should be available:    
-   `WITH_NVCUVID = ON`, [1] enable CUDA Video decodeing support
-   `WITH_CUFFT = ON`
-   `WITH_CUDNN = ON`
-   `WITH_CUBLAS = ON` [1,3,7]
-   `CUDA_FAST_MATH = OFF`, [2,3 have if ON], leave it OFF for accuracy
-   `CUDA_ARCH_BIN = 8.0,8.6`, selected from all options, for shorter compile time, select only the one you need, for compatibility, use the default list produced by configure (3.5;3.7;5.0;5.2;6.0;6.1;7.0;7.5;8.0;8.6)
-   `CUDA_ARCH_PTX = `, leave empty as is default or enter the lowest of ARCH_BIN
-   `CUDA_TOOLKIT_ROOT_DIR = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4"`
-   `CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4`
-   `CUDA_BUILD_EMULATION = OFF`, autopopulated
-   `CUDA_GENERATION = "Ampere"`, leave empty or select from list, match to the capability of your computer
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

Build Time: Many hours if all CUDA_ARCH_BINs are selected.

### DLL Fix

-   Modify `cv2/config.py`, see example at end of document

### Test
You can test CUDA performance according [1]:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C:\apps\opencv\opencv\build\install\x64\vc16\bin\ ..
"C:\opencv\opencv\x64\vc16\bin\opencv_perf_cudaarithm.exe" --gtest_filter=Sz_Type_Flags_GEMM.GEMM/29
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

You can test CUDA performance in python with:
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

jit_time = time.time()
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

# CUDA jit compilation
print('CUDA compilation time is   : {}'.format((current_time-jit_time)))

# CUDA time
print('CUDA execution time is   : {}'.format((cuda_time-current_time)/100.0))

# OpenCV Mat Pultiplication
print('OpenCV execution time is : {}'.format((cpu_time-cuda_time)/100.0))

# NumPy Mat Multiplication
print('NumPy execution time is  : {}'.format((np_time-cpu_time)/100.0))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In my Dell Inspiron 15 7559 (core i7 6th gen, GTX960M) notebook setup with python the   
CUDA execution time is 9-29ms,  
CV2 execution time is 95-106ms,    
Numpy execution tims is 38-44ms   

RTX 3060 Laptop and Ryzen 7 Mobile 4800H  
CUDA execution time is 2.6-2.8ms  
OpenCV execution time is 95-97ms  
NumPy  execution time is 23ms  

Please note, that the first time the CUDA routine is called it undergoes jit compilation which takes more than 800ms. 
Also compared to compiled cuda performance test program, python implementation can take up to twice the time.

## Create Wheel Install Package

A few things will need to be prepared manually:

-   `cd C:\apps\opencv\opencv\build\python_loader`
-   `xcopy "..\lib\python3\Release\*.pyd" .\cv2\python-3.8 /i`
-   `xcopy "..\bin\Release\*.dll"         .\cv2\python-3.8 /i`
-   `xcopy "..\bin\Release\*.exe"         .\cv2\python-3.8 /i`
-   `xcopy "..\..\data\haarcascades\*"    .\cv2\python-3.8\data\ /i`
-   `echo graft cv2\python-3.8          > MANIFEST.in`

-   Modify `setup.py` so that lines 55-58 are:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ],
        # Additional Parameters
        include_package_data=True,
        zip_safe=False,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-   Change the name of the package in `setup.py` from `opencv` to `opencv-python`  

-   Modify cv2/config.py so that opencv can find additional dlls it needs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

BINARIES_PATHS = [
    # os.path.join('C:/apps/opencv/opencv/build/install', 'x64/vc16/bin'),
    os.path.join(os.getenv('CUDA_PATH', 'C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4'), 'bin'),
    os.path.join(os.getenv('TBB_PATH',  'C:/Program Files (x86)/Intel/oneAPI/tbb/latest/redist'),    'intel64/vc14'),
    os.path.join(os.getenv('MKL_PATH',  'C:/Program Files (x86)/Intel/oneAPI/mkl/latest/redist'),    'intel64'),
    os.path.join(os.getenv('GST_PATH',  'C:/apps/gstreamer/1.0'),                                    'msvc_x86_64/bin'),
    os.path.join(os.getenv('HDF5_PATH', 'C:/apps/hdf5'), 'bin'),
    # os.path.join(os.getenv('REALSENSE_PATH',  'C:/Program Files (x86)/Intel RealSense SDK 2.0'), 'bin/x64'),
    # os.path.join(os.getenv('INTELMEDIA_PATH', 'C:/Program Files (x86)/IntelSWTools/Intel(R) Media SDK 2020 R1/Software Development Kit'), 'bin/x64'),
    # os.path.join(os.getenv('VTK_PATH',        'C:/vtk/9.0'), 'bin'),
    # os.path.join(os.getenv('QT_PATH',         'C:/Qt/5.14.2/msvc2017_64'), 'bin')    
] + BINARIES_PATHS

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   Modify cv2/config-3.8.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PYTHON_EXTENSIONS_PATHS = [
    os.path.join('C:/Python38/Lib/site-packages/cv2', 'python-3.8')
] + PYTHON_EXTENSIONS_PATHS

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-   `py -3 setup.py bdist_wheel`

Your whl package is in `.\dist\` 
You can insall it with `pip3 install nameofthewheel.whl`

DLL Summary
===============

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Opencv DLLs
"C:\opencv\opencv\4.5.4\build\..

# TBB DDLs
"C:\Program Files (x86)\Intel...

# MKL DLLs
"C:\Program Files (x86)\Intel\..
#  VTK DLLs
"C:\vtk\9.0\bin\"

# CUDA DLLs

"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin\

# gstreamer DLLs
"C:\gstreamer\1.0\msvc_x86_64\bin\"     

# Realsense
"C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64

# Media
"C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2020 R1\Software Development Kit\bin\x64\

# HDF5
"C:\hdf5\1.12.1\bin\hdf5.dll" 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build CMAKE Output
==================

py -3 -c "import cv2; print(cv2.getBuildInformation())"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
eneral configuration for OpenCV 4.5.4 =====================================
  Version control:               4.5.4-dirty

  Extra modules:
    Location (extra):            C:/apps/opencv/opencv_contrib/modules
    Version control (extra):     4.5.4

  Platform:
    Timestamp:                   2021-10-01T03:17:14Z
    Host:                        Windows 10.0.19042 AMD64
    CMake:                       3.21.3
    CMake generator:             Visual Studio 16 2019
    CMake build tool:            C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/MSBuild/Current/Bin/MSBuild.exe
    MSVC:                        1929
    Configuration:               Debug Release

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3
    Dispatched code generation:  SSE4_1 SSE4_2 FP16 AVX AVX2 AVX512_SKX
      requested:                 SSE4_1 SSE4_2 AVX FP16 AVX2 AVX512_SKX
      SSE4_1 (17 files):         + SSSE3 SSE4_1
      SSE4_2 (2 files):          + SSSE3 SSE4_1 POPCNT SSE4_2
      FP16 (1 files):            + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 AVX
      AVX (5 files):             + SSSE3 SSE4_1 POPCNT SSE4_2 AVX
      AVX2 (32 files):           + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2
      AVX512_SKX (8 files):      + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2 AVX_512F AVX512_COMMON AVX512_SKX

  C/C++:
    Built as dynamic libs?:      YES
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/cl.exe  (ver 19.29.30133.0)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MD /O2 /Ob2 /DNDEBUG 
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MDd /Zi /Ob0 /Od /RTC1 
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   /MD /O2 /Ob2 /DNDEBUG 
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MDd /Zi /Ob0 /Od /RTC1 
    Linker flags (Release):      /machine:x64  /INCREMENTAL:NO 
    Linker flags (Debug):        /machine:x64  /debug /INCREMENTAL 
    ccache:                      NO
    Precompiled headers:         YES
    Extra dependencies:          cudart_static.lib nppc.lib nppial.lib nppicc.lib nppidei.lib nppif.lib nppig.lib nppim.lib nppist.lib nppisu.lib nppitc.lib npps.lib cublas.lib cudnn.lib cufft.lib -LIBPATH:C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.4/lib/x64
    3rdparty dependencies:

  OpenCV modules:
    To be built:                 alphamat aruco barcode bgsegm bioinspired calib3d ccalib core cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hdf hfs highgui img_hash imgcodecs imgproc intensity_transform java line_descriptor mcc ml objdetect optflow phase_unwrapping photo plot quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking ts video videoio videostab wechat_qrcode xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    world
    Disabled by dependency:      -
    Unavailable:                 cvv julia matlab ovis sfm viz
    Applications:                tests perf_tests apps
    Documentation:               NO
    Non-free algorithms:         YES

  Windows RT support:            NO

  GUI:                           WIN32UI
    Win32 UI:                    YES
    VTK support:                 NO

  Media I/O: 
    ZLib:                        build (ver 1.2.11)
    JPEG:                        build-libjpeg-turbo (ver 2.1.0-62)
    WEBP:                        build (ver encoder: 0x020f)
    PNG:                         build (ver 1.6.37)
    TIFF:                        build (ver 42 - 4.2.0)
    JPEG 2000:                   build (ver 2.4.0)
    OpenEXR:                     build (ver 2.3.0)
    HDR:                         YES
    SUNRASTER:                   YES
    PXM:                         YES
    PFM:                         YES

  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES (prebuilt binaries)
      avcodec:                   YES (58.134.100)
      avformat:                  YES (58.76.100)
      avutil:                    YES (56.70.100)
      swscale:                   YES (5.9.100)
      avresample:                YES (4.0.0)
    GStreamer:                   YES (1.18.5)
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      YES

  Parallel framework:            TBB (ver 2021.3 interface 12030)

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/apps/opencv/opencv/build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/apps/opencv/opencv/build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      YES (C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_intel_lp64.lib C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_sequential.lib C:/Program Files (x86)/Intel/oneAPI/mkl/latest/lib/intel64/mkl_core.lib)
    Eigen:                       YES (ver 3.4.0)
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  NVIDIA CUDA:                   YES (ver 11.4, CUFFT CUBLAS)
    NVIDIA GPU arch:             80 86
    NVIDIA PTX archs:

  cuDNN:                         YES (ver 8.2.4)

  OpenCL:                        YES (NVD3D11)
    Include path:                C:/apps/opencv/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38/python.exe (ver 3.8.10)
    Libraries:                   NO
    numpy:                       C:/Python38/lib/site-packages/numpy/core/include (ver 1.21.2)
    install path:                -

  Python (for build):            C:/Python38/python.exe

  Java:                          
    ant:                         C:/apps/ant/bin/ant.bat (ver 1.9.16)
    JNI:                         C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include/win32 C:/Program Files/AdoptOpenJDK/jdk-8.0.292.10-hotspot/include
    Java wrappers:               YES
    Java tests:                  YES

  Install to:                    C:/apps/opencv/opencv/build/install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
