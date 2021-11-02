# Installing apckages from open-mmlab

## Pre Requisites

MMCV require to be insgtalled inside **Windows Powershell**   
**opencv**  
**PyTorch**  

## Dependencies

```
pip3 install addict pyyaml yapf psutils
pip3 install regex;sys_platform=='win32'
```

## MIM installation tool
```
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
````

```
cd C:\apps
git clone https://github.com/open-mmlab/mim.git mim
cd mim
pip install -e .
```

### MMCV
Obtain source  
In powershell:  

```
cd C:\apps
git clone https://github.com/open-mmlab/mmcv.git mmcv
cd mmcv
set TORCH_CUDA_ARCH_LIST="8.0 8.6"
set MMCV_WITH_OPS = 1
set MAX_JOBS = 8
python setup.py build_ext
python setup.py develop

pip install -e .
py -3 setup.py bdist_wheel
pip3 install .\distr\mmcv...
```

### MMDetection

cd C:\apps
git clone https://github.com/open-mmlab/mmdetection.git mmdetection
cd mmdetection

needs cython and numpy

pip install -v -e .
py -3 setup.py bdist_wheel
pip3 install .\dist\mmd...

#### for instaboost
`pip install instaboostfast`
#### for panoptic segmentation
`pip install git+https://github.com/cocodataset/panopticapi.git`
#### for LVIS dataset
`pip install git+https://github.com/lvis-dataset/lvis-api.git`
#### for albumentations
`pip install albumentations>=0.3.2 --no-binary imgaug,albumentations`

### MMSegementation, MMClassification, MMTracking
Obtain source
```
cd C:\apps
git clone https://github.com/open-mmlab/mmdetection.git mmdetection
git clone https://github.com/open-mmlab/mmclassification.git mmclassification
git clone https://github.com/open-mmlab/mmtracking.git mmtracking
git clone https://github.com/open-mmlab/mmocr.git mmocr
git clone https://github.com/open-mmlab/mmpose.git mmpose
git clone https://github.com/open-mmlab/mmdetection3d.git mmdetection3d
git clone https://github.com/jin-s13/xtcocoapi.git

cd xtcocoapi
pip3 install -e .

cd C:\apps\mmdetection
pip3 install -e .
cd C:\apps\mmclassification
pip3 install -e .
cd C:\apps\mmtracking
pip3 install -e .
cd C:\apps\mmocr
pip3 install -e .
cd C:\apps\mmpose
pip3 install -e .
# cd C:\apps\mmdetection3d this fails because it wants old versions
# pip3 install -e .
```



set "buildType=Release"
set "generator=Visual Studio 16 2019"
"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
"C:\Program Files (x86)\Intel\oneAPI\setvars.bat" intel64 vs2019
