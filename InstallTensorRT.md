# TensorRT
TensorRT is described here: https://docs.nvidia.com/deeplearning/tensorrt/

## Installation 
https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html

Download https://developer.nvidia.com/tensorrt-getting-started   
Install the ZIP file: https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html#installing-zip  

### Choose option B  
Copy the dlls, libs and include files   
~~~~~~~~~~~~~~~~~~~~~~~~~~~
copy <installpath>\lib\*.dll C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin
copy <installpath>\lib\*.lib C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\lib\x64
copy <installpath>\include\* C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\include
~~~~~~~~~~~~~~~~~~~~~~~~~~~
### Python  
~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip3 install <installpath>\graphsurgeon\graphsurgeon-0.4.5-py2.py3-none-any.whl
pip3 install <installpath>\uff\uff-0.6.9-py2.py3-none-any.whl
pip3 install <installpath>\onnx_graphsurgeon\onnx_graphsurgeon-0.2.6-py2.py3-none-any.whl
~~~~~~~~~~~~~~~~~~~~~~~~~~~
