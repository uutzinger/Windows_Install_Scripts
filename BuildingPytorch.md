# Building or Installing PyTorch

- [Building or Installing PyTorch](#building-or-installing-pytorch)
- [Easy](#easy)
- [Build](#build)
  * [References](#references)
  * [Dependencies](#dependencies)
  * [Pytorch](#pytorch)
  * [Setup Build Environment](#setup-build-environment)
  * [Build](#build-1)
  * [Pytorch Vision](#pytorch-vision)
  * [Pytorch Audio, this failed on windows](#pytorch-audio--this-failed-on-windows)
  * [Pytorch Text](#pytorch-text)
  * [Test](#test)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Easy
pip3 install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio===0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html

# Build

## References
[1] https://dev.infohub.cc/build-torch15-cuda102-win10/


## Dependencies

**TensorRt**

You will need TensorRT installed. Check Nvidia instructions here: https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html

* Login with  your account an Nvidia.
* Obtain TensorRT 8.2 which is compatible with CUDA 11.4 on Windows  
* Extract to C:\app\temsorrt\8.2.0.6
* Add C:\temsorrt\8.2.0.6\lib to Windows PATH

```
pip3 install pycuda
cd C:\apps\temsorrt\8.2.0.6\graphsurgeon
pip3 install grahsurgeon*.whl
cd C:\apps\temsorrt\8.2.0.6\uff
pip3 install uff*.whl
```

**Visual Studio Build Tools**  
Obtain the Visual Studio Build Tools from https://visualstudio.microsoft.com/downloads/ under `Tools for Visual Studio 2019` listed as `Build Tools for Visual Studio 2019`

**libuv**  
This should install libuv to "C:\Program Files (x86)\libuv"
libuv is asynch input/output library.

The following approach is not yet working with regular python install script.

```
cd C:\apps
mkdir libuv
cd libuv
git clone https://github.com/libuv/libuv
cd libuv
mkdir -p build
(cd build && cmake .. -DBUILD_TESTING=ON)
cmake --build build -j 4
# elevated as administrator
cmake --install build
# test
(cd build && ctest -C Debug --output-on-failure)
```
you need to add the folder where uv.dll is stored to your path

Install **python packages**  

Check the available python packages
```
pip3 list
```

```
pip3 install astunparse ninja pyyaml mkl mkl-include setuptools cmake wheel cffi typing_extensions future six requests dataclasses
pip3 install intel-openmp pycparser pillow pyuv
```

**Test** your CMD shell for available programs.
```
where git
where cmake
where nvcc
where nvvp.exe
where cuda*.dll
where cudnn*.dll
these might fail
where cl*
where mkl*
```

## Pytorch

```
cd C:\apps
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
# if you are updating an existing checkout
git submodule sync
git submodule update --init --recursive --jobs 0
```

## Setup Build Environment
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
set USE_DISTRIBUTED=0
set DISTUTILS_USE_SDK=1
```

## Build

```
cd C:\apps\pytorch
py -3 setup.py build
```

a long time later

create wheel package

```
cd C:\apps\pytorch
py -3 setup.py bdist_wheel
```

install wheel
```
pip3 install "C:\apps\pytorch\dist\torch ...
```

## Pytorch Vision
```
cd C:\apps
git clone https://github.com/pytorch/vision torchvision
cd torchvision
git submodule update --init --recursive

```

```
cd C:\apps\torchvision
py -3 setup.py build
py -3 setup.py bdist_wheel
```

```
pip3 install "C:\apps\vision\dist\torchvision...
```

## Pytorch Audio, this failed on windows

```
cd C:\apps
git clone https://github.com/pytorch/audio torchaudio
cd torchaudio
git submodule update --init --recursive
```

```
cd C:\apps\torchaudio
py -3 setup.py build

failes here  
cmake C:/apps/torchaudio -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=C:/Python38/lib/site-packages/torch/share/cmake -DCMAKE_INSTALL_PREFIX=C:/apps/torchaudio/build/lib.win-amd64-3.8/torchaudio/ -DCMAKE_VERBOSE_MAKEFILE=ON -DPython_INCLUDE_DIR=C:/Python38/include -DBUILD_SOX:BOOL=OFF, -DBUILD_KALDI:BOOL=OFF -DBUILD_RNNT:BOOL=ON -DBUILD_TORCHAUDIO_PYTHON_EXTENSION:BOOL=ON -DUSE_ROCM:BOOL=OFF -DUSE_CUDA:BOOL=ON -DUSE_OPENMP:BOOL=ON -GNinja -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl -DPYTHON_VERSION=3.8

py -3 setup.py bdist_wheel
```

```
pip3 install "C:\apps\audio\dist\torchaudio...
```

## Pytorch Text

```
cd C:\apps
git clone https://github.com/pytorch/text torchtext
cd torchtext
git submodule update --init --recursive
```

```
cd C:\apps\torchtext
py -3 setup.py build
py -3 setup.py bdist_wheel
```

```
pip3 install "C:\apps\torchtext\dist\torchtext...
```

## Test
```
py -3 -c "import torch; print(torch.__version__)"
```

```
py -3 -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

```
py -3 -c "from __future__ import print_function; import torch; x = torch.rand(5, 3); print(x)"
```

```
py -3 -c "import torch;import torchvision;print(torchvision.__version__)"
```

```
py -3 -c "import torch;import torchtext;print(torchtext.__version__)"
```
