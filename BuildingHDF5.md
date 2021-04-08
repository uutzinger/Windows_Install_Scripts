# Building HDF5

## References

## Obtain Source Code
From https://www.hdfgroup.org/downloads/hdf5/source-code/
donwload the cmake version
Unpack to C:\HDF5

## Pre-Rrequisites
Install https://www.perl.org/get.html#win32
and other tools as listed in https://github.com/uutzinger/Windows_Install_Scripts/blob/master/installPackages.md

Prepare your CMD shell with
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
```

## Configure
```
cd C:/hdf5/CMake-hdf5-1.12.0
mkdir build
cd build
cmake-gui ..\
```
Where to build binaries is C:/hdf5/CMake-hdf5-1.12.0/build  
Where is the source code is: C:/hdf5/CMake-hdf5-1.12.0/hdf5-1.12.0  

Optioinal change
```
CMAKE_INSTALL_PREFIX = C:/Program Files/HDF_Group/HDF5/1.12.0
````
to
```
C:/hdf5
```

And in GUI click Config and select Visual Studio as compiler. After completion select Generate and then Open Project when it becomes available.

When Perl is found there should be no errors when you run config as well as Generate. If perl is not found clear the chache in cmake-gui and try again.

## Build

Make sure HDF5 from HDF_GROUP is not already installed in C:/Program Files/HDF_Group/. Unintstall of necessary.  

Visual Studio-> Batch Build: enable "Install Release 64" and then select build.  
The build will take about 20 minutes.  

## Environment Variable
Set HDF5_DIR as environment variable to the directory you selected as INSTALL_PREFIX.
