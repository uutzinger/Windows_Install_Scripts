# Install DeepFace

https://github.com/serengil/deepface 
https://pypi.org/project/deepface/

## Requirements

numpy>=1.14.0  
pandas>=0.23.4  
gdown>=3.10.1  
tqdm>=4.30.0  
Pillow>=5.2.0  
opencv-python>=4.2.0.34  
opencv-contrib-python>=4.3.0.36  
tensorflow>=1.9.0  
keras>=2.2.0  
Flask>=1.1.2  
mtcnn>=0.1.0  
lightgbm>=2.3.1  
dlib>=19.20.0  

### Pre-Compiled Libraries
https://www.lfd.uci.edu/~gohlke/pythonlibs/  

pip3 install numpy‑1.19.5+mkl‑cp38‑cp38‑win_amd64.whl
pip3 install pandas‑1.2.2‑cp38‑cp38‑win_amd64.whl
pip3 install Pillow‑8.1.0‑cp38‑cp38‑win_amd64.whl
pip3 install lightgbm‑3.1.1‑cp38‑cp38‑win_amd64.whl

### Pypi
pip3 install gdown --upgrade
pip3 install tqdm -- upgrade
pip3 install keras_applications==1.0.8 
pip3 install keras_preprocessing==1.1.2 
pip3 install Flask --upgrade
pip3 install mtcnn --upgrade
pip3 install retina-face --upgrade

### Build Yourself, might improve performance
- opencv  
- dlib  
- tensorflow  

#### LightGBM
Download from https://www.microsoft.com/en-us/download/details.aspx?id=100593  
* `msmpisetup.exe`
* `msmpisdk.msi`

Prepare the CMD shell for building:
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
```

Build LightGBM:
```
git clone --recursive https://github.com/microsoft/LightGBM
cd LightGBM
```
Open windows/LightGBM.sln in Visual Studio
Select Release_mpi configuration
Build Solution

## Install
pip3 install deepface

It wants to overwrite cuda support. Need to fix python install script
