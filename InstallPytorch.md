
# Installing PyTorch

## References
[1] https://dev.infohub.cc/build-torch15-cuda102-win10/


## TensorRt
You will need TensorRT installed. Check Nvidia instructions here: https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html

* Login with  your account an Nvidia.
* Obtain TensorRT 7.0 which is compatible with CUDA 10.2 in windows  
* Extract to C:\temsorrt\7.0
* Add C:\temsorrt\7.0\lib to Windows PATH
```
pip3 install pycuda
cd C:\temsorrt\7.0\graphsurgeon
pip3 install grahsurgeon*.whl
cd C:\temsorrt\7.0\uff
pip3 install uff*.whl
```

## MKL

## Dependencies
```
pip3 install ninja pyyaml mkl mkl-include setuptools cmake cffi intel-openmp pycparser pyyaml setuptools wheel six pillow
```

```
pip3 list
```

```
where git
where cl
where cmake
where nvcc
where nvvp.exe
where cuda*102.dll
where cudnn*.dll
where mkl*
```

## Setup Build Environment
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"

"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\tbb\bin\tbbvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mkl\bin\mklvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\ipp\bin\ippvars.bat" intel64 vs2019
"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\daal\bin\daalvars.bat" intel64

"C:\Program Files (x86)\IntelSWTools\compilers_and_libraries\windows\mpi\intel64\bin\mpivars.bat"

"C:\opencv\4.3.0\setup_vars_opencv4.cmd"
```

## Pytorch
```
cd C:\
mkdir pytorch
cd pytroch
mkdir 1.5.1
cd c:\pytorch\1.5.1
git clone https://github.com/pytorch/pytorch
cd C:\pytorch\1.5.1\pytorch>
git checkout tags/v1.5.1
git submodule sync
git submodule update --init --recursive
```

```
C:\pytorch\1.7.0\pytorch
py -3 setup.py install
```
a few hours later
```
py -3 setup.py bdist_wheel
```

## Pytorch Vision
```
cd C:\pytorch\1.5.1
git clone https://github.com/pytorch/vision.git
git checkout tags/v0.6.1
```

```
cd C:\pytorch\1.5.1\vision
py -3 setup.py install
py -3 setup.py bdist_wheel
```


## Install Wheel Packages
```
pip3 install "C:\pytorch\1.5.1\pytorch\dist\torch ...
pip3 install "C:\pytorch\1.5.1\vision\dist\torchvision ...
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

## MMCV
```
pip3 install mmcv-full
```
```
git clone https://github.com/open-mmlab/mmcv.git
cd mmcv
git checkout tags/v1.0.2
set MMCV_WITH_OPS=1 
py -3 setup.py build
py -3 setup.py install
```