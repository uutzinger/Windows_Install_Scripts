# Installing apckages from open-mmlab

MMCV require to be insgtalled inside **Windows Powershell**

## Build

## Dependencies

```
pip3 install addict pyyaml yapf
pip3 install regex;sys_platform=='win32'
```

### MMCV
Obtain source
```
cd C:\apps
git clone https://github.com/open-mmlab/mmcv.git mmcv
cd mmcv
```
Build
```
pip install -e .
```
Python wheel
```
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

# for instaboost
pip install instaboostfast
# for panoptic segmentation
pip install git+https://github.com/cocodataset/panopticapi.git
# for LVIS dataset
pip install git+https://github.com/lvis-dataset/lvis-api.git
# for albumentations
pip install albumentations>=0.3.2 --no-binary imgaug,albumentations

MMSegementation
MMClassification
MMTracking
MMPose
MMOcr
MMdetection3d