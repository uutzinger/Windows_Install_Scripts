# Installing VTK in Windows

This script follows closely the description on infohub-Development [https://dev.infohub.cc/build-vtk-820]

## Pre-Requisits
Latest version of
* Windows OS 10
* Microsoft Visual Studio Community 2019 https://visualstudio.microsoft.com/downloads/
* CMAKE-gui https://cmake.org/

## Download
Obtain the source. Although VTK 9.0 is available only 8.2 version works with opencv. Lets attempt building both. We can use 9.0 python interface and 8.2 to compile opencv.

```
mkdir C:\vtk
cd C:\vtk
git clone https://gitlab.kitware.com/vtk/vtk.git --branch v8.2.0
cp vtk VTK-8.2.0
mv vtk VTK-latest
cd VTK-latest
git checkout master
git pull
mkdir C:\vtk\VTK-8.2.0\build
mkdir C:\vtk\VTK-latest\build
cd build
```

Configure VTK
```
cd C:\vtk\VTK-latest\build
cmake-gui ..\
```
After verifyng source and source directory settings, click Configure.
Select Visual Studio Compiler for x64 application.

Enable
* ```CMAKE_CXX_MP_FLAG = ON```
* ```CMAKE_CXX_MP_NUM_PROCESSORS8 = 8```
* ```VTK_WRAP_PYTHON = ON```
* ```VTK_PYTHON_VERSION = 3```
* ```CMAKE_INSTALL_PREFIX = C:\vtk\9.0```
* ```VTK_Group_Enable_QT=Default```, creates errors unortunately
* ```VTK_Group_Enable_Views=Default```
* ```VTK_Group_Standalone=Want```
* ```VTK_Group_Rendering=Want```
* ```VTK_Group_Imaging=Default```
* ```HDF5_ENABLE_HDFS = OFF```, creates errors
* ```VTK_USE_CUDA = ON```
* ```CMAKE_CUDA_ARCHITECTURES = compute_52```, this takes care of many warnings

For the CUDA architectures, check https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html and search for Virtual Architecture Feature List. Alternatively Maxwell might work also. 

Open the project by clicking approriate button in cmake gui.
In Visual Studio open Build / Batch Build and make sure INSTALL is enabled and click Build.
It will take about 30 minutes.

For python 3.8 you will need to download the patch mentioned in: https://gitlab.kitware.com/vtk/vtk/-/issues/17670
If you dont have patch you can use Msys or patch for gitbash "C:\Program Files\Git\usr\bin\patch.exe".

```
cd C:\vtk\VTK-8.2.0
patch -p 1 -i 0001-Compatibility-for-Python-3.8.patch
```
```-p 1 ``` removes the first directory which in this patch is "a/"

```
cd C:\vtk\VTK-8.2.0\build
cmake-gui ..\
```
After verifyng source and source directory settings, click Configure.
Select Visual Studio Compiler for x64 application.

Enable
* ```CMAKE_CXX_MP_FLAG = On```
* ```CMAKE_CXX_MP_NUM_PROCESSORS8 = 8```
* ```VTK_WRAP_PYTHON = Off```, creates errors with VS2019
* ```VTK_PYTHON_VERSION = 3```
* ```CMAKE_INSTALL_PREFIX = C:\vtk\8.2```
* ```VTK_Group_QT=Off```, creates errors unortunately
* ```VTK_Group_Views=Off```
* ```VTK_Group_Standalone=On```
* ```VTK_Group_Rendering=On```
* ```VTK_Group_Imaging=Off```
* ```VTK_USE_SYSTEM_HDF = Off```, creates errors
* ```BUILD_TESTING= Off```

Generate and Open Project. (There is implicit '8' to STRING conversion warning)
In Visual Studio open Build / Batch Build and make sure INSTALL is enabled and click Build.
It will take about 30 minutes. 8:27

## Copying files for python
```
xcopy C:\vtk\VTK-latest\build\bin\Lib\site-packages C:\Python38\Lib\site-packages /s/h/i/e/y
copy C:\vtk\VTK-latest\build\bin\Release\* C:\Python38\Lib\site-packages\vtkmodules /y
```

## Testing
Run the QuadraticTetra.py program from https://github.com/lorensen/VTKExamples in command shell:
```
py -3 QuadraticTetra.py
```
