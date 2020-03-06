# Compiling OpenCV on Windows 10
This guide is adapted from [James Bowley] (https://jamesbowley.co.uk/accelerating-opencv-4-build-with-cuda-intel-mkl-tbb-and-python-bindings/#visual_studio_cmake_cmd).

## Pre Requisits

### Install Python
Install [python](https://www.python.org/downloads/windows/) Choose 64bit version if you run 64bit OS.

### Install Visual Studio
Install Visual Studio Community from [Microsoft] (https://visualstudio.microsoft.com/downloads/) and install the the option for develoment for desktop application in C.

### Open CV Source
Download the source files for both OpenCV and OpenCV contrib, available on GitHub. I place them in the root folder C:/ but they can go anywhere. Download the files under realeases and if build fails check on open issues and then decide if you need to switch to the current development version (what you get if you download directly from top level at github). If you include contrib and nonfree options you might end up with 1800-2200 modules to compile. A module takes about 2 sec to build.

```
cd C:/
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
```

### CMake
Install CMake that comes with CMake GUI. Install release version.
https://github.com/Kitware/CMake/releases/download/v3.16.5/cmake-3.16.5-win64-x64.msi

### CUDA
Install CUDA Tookit from NVIDIA. Useful only if you have NVIDA GPU.

### NVIDIA video codec SDK
Download the Video Codec SDK, extract and copy include and lib directories to C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\vx.x

### Intel Media SDK
To accelerate video decoding on Intel CPU’s register and download and install Intel Media SDK

### Windows SDK 
WIndows SDK includes DirectX SDK. When you rerun the installer you  might want to add options to Windows SDK that are not yet installed.

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
Download QT from https://www.qt.io/download-open-source
At the bottom is installer link in green
Login with QT account


### Environment Variables
You might want to update your path and environment variables
* INTELMEDIASDKROOT = C:\Program Files (x86)\IntelSWTools\Intel(R) Media SDK 2019 R1\Software Development Kit
* GSTREAMER_DIR = C:\gstreamer\1.0\x86_64

PATH
* C:\Python38
* C:\Python38\Scripts
* C:\gstreamer\1.0\x86_64\bin
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc_mt
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\redist\intel64_win\tbb\vc_mt;
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin;
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin;
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin;
* C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin;

## Prepare Shell Environment

Open command prompt and enter the following commands with directories pointing to your installations
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
"C:\Program Files\CMake\bin\cmake.exe" -B"%openCvBuild%/" -H"%openCvSource%/" -G"%generator%" -DCMAKE_BUILD_TYPE=%buildType% -DOPENCV_EXTRA_MODULES_PATH="%openCVExtraModules%/" -DOPENCV_ENABLE_NONFREE=ON -DWITH_GSTREAMER=ON
```
### Update Build Variables
Run configure with GUI 
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
and then make sure the following variables are set:
* PYTHON_DEFAULT_EXECUTABLE=C:\Python38\python.exe
* BUILD_SHARED_LIBS=OFF
* // CMAKE_BUILD_TYPE=Release
* // WITH_GSTREAMER=ON
* // OPENCV_ENABLE_NONFREE=ON
* // OPENC_EXTRA_MODULES_PATH=C:/opencv_contrib/modules
* // BUILD_EXAMPLES=OFF
* // BUILD_opencv_python3=ON 
* INSTALL_PYTHON_EXAMPLES=ON
* INSTALL_C_EXAMPLES=ON

Rerun configure and generate in cmake-gui.

And finally do first build using Ninja:
```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

## Build 2
Now lets enable more features and optimizations.
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```
If things dont build, delete the content of the build directory and start again with setting variables, then build again. If that does not conclude, check on error messages and the reported issues on gihub to find solutions.

###Create single library to include all features
* BUILD_opencv_world=ON

### Intel Optimization Thread Building Blocks
* WITH_TBB=ON

### Intel Optimization Math Kernel Library
* WITH_MKL=ON 
* // MKL_USE_MULTITHREAD=ON 
* // MKL_WITH_OPENMP=ON
* MKL_WITH_TBB=ON 

### MFX
* WITH_MFX=ON
sets include and libraries automatically 

### Graphics Libraries
* WITH_OPENGL=ON
* WITH_QT=ON
Qt5_DIR = C:/Qt/Qt5.14.1/5.14.1/msvc2017_64/lib/cmake/Qt5

Rerun configure and generate in cmake-gui.

* BUILD_opencv_rgbd=OFF, does not compile

```
"C:\Program Files\CMake\bin\cmake.exe" --build %openCvBuild% --target install
```

Python will need all gstreamer dlls from ```C:\gstreamer\1.0\x86_64\bin``` copied to ```C:/Python38\Lib\site-packages\cv2\python-3.8\```
Python will need all qt dlls from ```C:\Qt\5.14.1\msvc2017_64\bin``` copied to ```C:/Python38\Lib\site-packages\cv2\python-3.8\```

### ENv Variable
QT_PLUGIN_PATH = C:\Qt\5.14.1\msvc2017_64\plugins

If this worked ok, we can try to include CUDA support. CUDA compiled opencv will not run if there is no NVIDIA GPU on the system.

## Build 3
Hardware specific dependencies.
Inlucde CUDA and Intel Realsense.

### RealSense Camera Support
You will need to set the include and library manually as it does not auto populate.
* WITH_LIBREALSENSE=ON
* LIBREALSENSE_INCLUDE_DIR C:/Program Files (x86)/Intel RealSense SDK 2.0/include
* LIBREALSENSE_LIBRARIES C:/Program Files (x86)/Intel RealSense SDK 2.0/lib/x64/realsense2.lib


Include CUDA support in build scripts:
```
"C:\Program Files\CMake\bin\cmake-gui.exe"
```

There are issues with rgbd and nonfree modules. [Issue] (https://github.com/opencv/opencv_contrib/issues/2307)

Still working on that.

###CUDA
Use CUDA GPU for optimzed computation 
* WITH_CUDA=ON
* WITH_CUBLAS=ON 
* WITH_NVCUVID=ON
* CUDA_TOOLKIT_ROOT_DIR="C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2"
* CUDA_FAST_MATH=ON
* CUDA_ARCH_BIN=7.5 
* CUDA_ARCH_PTX=7.5 
* CUDA_nvcuvenc_LIBRARY=
* CUDA_SDK_ROOT_DIR = C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v10.2
* OPENCV_DNN_CUDA=ON
* CUDA_BUILD_EMULATION=OFF

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
