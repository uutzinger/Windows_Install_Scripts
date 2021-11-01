# Compiling Dlib on Windows 10

- [Compiling Dlib on Windows 10](#compiling-dlib-on-windows-10)
  * [Approach](#approach)
  * [Background Reading](#background-reading)
  * [Obtaining Dlib Source](#obtaining-dlib-source)
  * [Uninstalling of Previous Installations](#uninstalling-of-previous-installations)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment)
  * [Build Python Wrapper](#build-python-wrapper)
    + [Test](#test)
  * [Optional Build](#optional-build)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Approach
Dlib is easy to install:

```pip install dlib```

If you want to build it in separate folder, obtain source from github, then 

```py -3 setup.py install```

It will find all the optimizations for your computer.

Some online posts have been consulted for this document.
* [1] http://dlib.net/compile.html
* [2] https://www.learnopencv.com/install-dlib-on-windows/

## Background Reading
An interview with Davis King: 
https://www.pyimagesearch.com/2017/03/13/an-interview-with-davis-king-creator-of-the-dlib-toolkit/

## Obtaining Dlib Source
```
cd C:/apps
git clone https://github.com/davisking/dlib.git dlib
git clone https://github.com/davisking/dlib-models.git dlib-models
cd dlib
```

## Uninstalling of Previous Installations
To make sure python finds your build you will want to remove any other installation of opencv.
```
pip3 uninstall dlib
```

## Preparing your Shell Build Environment
Open a command prompt (CMD) and enter the following commands with directories pointing to your installations:

```
set "DlibSource=C:\apps\dlib"
set "DlibBuild=%DlibSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
```

## Build Python Wrapper
```
py -3 setup.py install
```

Fix dll not found errors

```
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin\cublas64_11.dll" "C:\python38\lib\site-packages\dlib-19.22.99-py3.8-win-amd64.egg"
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin\cudnn64_8.dll" "C:\python38\lib\site-packages\dlib-19.22.99-py3.8-win-amd64.egg"
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin\cublasLt64_11.dll" "C:\python38\lib\site-packages\dlib-19.22.99-py3.8-win-amd64.egg"
```

### Test

In a command shell:

```
py -3 -c "import dlib; print(f'Dlib: {dlib.__version__} for python installed and working')"
```

## Optional Build 

```
set "DlibSource=C:\apps\dlib\dlib"
set "DlibBuild=%DlibSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
cd C:\apps\dlib\build
cmake -H"%DlibSource%/" -G"%generator%" -T host=x64 ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DCMAKE_INSTALL_PREFIX="C:/apps/dlib" ^
-DUSE_AVX_INSTRUCTIONS=ON ^
-DUSE_SSE2_INSTRUCTIONS=ON ^
-DUSE_SSE4_INSTRUCTIONS=ON ^
-DDLIB_JPEG_SUPPORT=ON ^
-DDLIB_PNG_SUPPORT=ON ^
-DDLIB_GIF_SUPPORT=ON
```

This should find Intel MKL/BLAS, CUDA, cuDNN. 

Check Build Variables

```
"C:\Program Files\CMake\bin\cmake-gui.exe" ..\
```

The command line approach is:
```
cd C:\dlib\dlib\build
"C:\Program Files\CMake\bin\cmake.exe" --build . --config Release --target INSTALL
```
