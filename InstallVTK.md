# Installing VTK in Windows

This script follows closely the description on infohub-Development [https://dev.infohub.cc/build-vtk-820]

## Pre-Requisits
Latest version of
* Windows OS 10
* Microsoft Visual Studio Community 2019 https://visualstudio.microsoft.com/downloads/
* CMAKE-gui https://cmake.org/
* VTK download https://vtk.org/download/

## Download
I donwloaded and unpacked the tar file to ```C:\VTK```

```
cd C:\VTK\VTK-9.0.0>
mkdir build
cd build
```

```
cmake-gui ..\
```

Configure for Visual Studio Compiler for x64 application.

Enable
* CMAKE_CXX_MP_FLAG = On
* CMAKE_CXX_MP_NUM_PROCESSORS8 = 8
* VTK_WRAP_PYTHON = On
* VTK_PYTHON_VERSION = 3
* CMAKE_INSTALL_PREFIX = C:\VTK
* VTK_USE_CUDA = ON

Open the project by clicking approriate button in cmake gui.
In Visual Studio open Build / Batch Build and make sure INSTALL is enabled and click Build.
It will take about 30 minutes.

## Copying files
```
xcopy C:\VTK\VTK-9.0.0\build\bin\Lib\site-packages C:\Python38\Lib\site-packages /s/h/i/e/y
copy C:\VTK\VTK-9.0.0\build\bin\Release\* C:\Python38\Lib\site-packages\vtkmodules /y
copy C:\VTK\VTK-9.0.0\build\lib\Release\* C:\Python38\Lib\site-packages\vtkmodules /y
```

## Testing
Run the QuadraticTetra.py program from https://github.com/lorensen/VTKExamples in command shell:
```
py -3 QuadraticTetra.py
```
