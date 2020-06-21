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
Dlib is easy to install. Once the source is downloaded, the python setup.py is the only file that you need to execute and it will find all the optimizations for your computer.

Some online posts have been consulted for this document.
* [1] http://dlib.net/compile.html
* [2] https://www.learnopencv.com/install-dlib-on-windows/

## Background Reading
An interview with Davis King.

https://www.pyimagesearch.com/2017/03/13/an-interview-with-davis-king-creator-of-the-dlib-toolkit/

## Obtaining Dlib Source

```
mkdir C:/dlib
cd C:/dlib
git clone https://github.com/davisking/dlib.git
git clone https://github.com/davisking/dlib-models.git
cd C:/dlib/dlib
```

## Uninstalling of Previous Installations

To make sure python finds your build you will want to remove any other installation of opencv.
```
pip3 uninstall dlib
```

## Preparing your Shell Build Environment

Open a command prompt (CMD) and enter the following commands with directories pointing to your installations:

```
set "DlibSource=C:\dlib\dlib"
set "DlibBuild=%DlibSource%\build"
set "buildType=Release"
set "generator=Visual Studio 16 2019"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
```

The last command is only applicable when you already built opencv.

## Build Python Wrapper
```
py -3 setup.py install
```

Fix dll not found errors

```
copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin\cublas64_10.dll" "C:\Python38\Lib\site-packages\dlib-19.19.99-py3.8-win-amd64.egg"

copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin\cudnn64_7.dll" "C:\Python38\Lib\site-packages\dlib-19.19.99-py3.8-win-amd64.egg"

copy "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2\bin\cublasLt64_10.dll" "C:\Python38\Lib\site-packages\dlib-19.19.99-py3.8-win-amd64.egg"
```

### Test

In a command shell:

```
py -3 -c "import dlib; print(f'Dlib: {dlib.__version__} for python installed and working')"
py -3 -c "import dlib; print(dlib.getBuildInformation())"
```

## Optional Build 

```
cd C:\dlib\dlib\build
"C:\Program Files\CMake\bin\cmake.exe" -B"%DlibBuild%/" ^
-H"%DlibSource%/" -G"%generator%" -T host=x64 ^
-DCMAKE_BUILD_TYPE=%buildType% ^
-DCMAKE_INSTALL_PREFIX="C:/dlib" ^
-DLIB_USE_MKL_WITH_TBB=ON ^
-DUSE_AVX_INSTRUCTIONS=ON ^
-DUSE_SSE2_INSTRUCTIONS=ON ^
-DUSE_SSE4_INSTRUCTIONS=ON ^
-DDLIB_JPEG_SUPPORT=ON ^
-DDLIB_PNG_SUPPORT=ON ^
-DDLIB_GIF_SUPPORT=ON ^
-DJPEG_INCLUDE_DIR=C:\dlib\dlib\dlib\external\libjpeg ^
-DJPEG_LIBRARY=C:\dlib\dlib\dlib\external\libjpeg ^
-DPNG_PNG_INCLUDE_DIR=C:\dlib\dlib\dlib\external\libpng ^
-DPNG_LIBRARY_RELEASE=C:\dlib\dlib\dlib\external\libpng ^
-DZLIB_INCLUDE_DIR=C:\dlib\dlib\dlib\external\zlib ^
-DZLIB_LIBRARY_RELEASE=C:\dlib\dlib\dlib\external\zlib
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
