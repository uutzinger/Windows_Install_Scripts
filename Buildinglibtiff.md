# Compiling libtiff

- [Compiling libtiff](#compiling-libtiff)
  * [Prerequisites](#prerequisites)
  * [Obtaining libtiff Source](#obtaining-libtiff-source)
  * [Preparing your Shell Build Environment](#preparing-your-shell-build-environment)
- [Building libtiff](#building-libtiff)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Prerequisites
* Visual Studio C Compiler from https://visualstudio.microsoft.com/downloads/
* cmake from https://cmake.org/download/

## Obtaining libtiff Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:/apps/
git clone https://gitlab.com/libtiff/libtiff.git libtiff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## Preparing your Shell Build Environment
Open a command prompt (CMD) and enter the following commands with directories
pointing to your installations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cd C:/apps/libtiff/build
set "libtiffSource=C:\apps\libtiff"
set "libtiffBuild=%libtiffSource%\build"
set "buildType=Release"
set "CMAKE_BUILD_TYPE=Release"
set "generator=Visual Studio 16 2019"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IntelMath / oneAPI libraries might not be needed.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Building libtiff
In CMD windows with administrative priviledges:

```
cd C:/apps/libtiff/build
cmake-gui ..\
"C:\Program Files\CMake\bin\cmake.exe" --build %libtiffBuild% --target install
```

Add `C:\Program Files (x86)\tiff\bin` to PATH (e.g. with Rapid Environment Editor or in System Properties/Environment Variables)
