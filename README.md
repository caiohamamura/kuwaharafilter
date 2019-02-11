# kuwaharafilter
This algorithm was developed based on Kuwahara Filter. 

The Kuwahara filter is an edge-preserving filter which analyze subwindows around the central pixel, attributing the mean of the subwindow with the lowest variance.

There are two implementations of the filter available, one which will use only numpy for compatibility issues and another one for optimized for performance using *pyopencl*, which will take advantage of all devices compatible with opencl, including GPUs from the most common vendors. 

For using the optimized version you will need to install pyopencl and also the video/cpu drivers compatible with OpenCL. For instance in linux you should find the packages: beignet-opencl-icd (Intel), nvidia-opencl-icd (NVidia) and mesa-opencl-icd (AMD).

# Installing pyopencl

## Linux

### Requirements

#### Distro (available from package providers)
* opencl-headers: Header files for opencl
* ocl-icd-opencl-dev: Generic library for compiling opencl code

#### Python (available from pip)
* pybind11

### Example (Ubuntu)
```
sudo apt install opencl-headers
sudo apt install ocl-icd-opencl-dev
python3 -m pip install pybind11
python3 -m pip install pyopencl
```


## Windows

The best way to install pyopencl in windows is to download the compiled wheels from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopencl, then you just need to execute the downloaded wheel from the OSGeo4W Shell.

```
python3 -m pip install pyopencl‑[version]‑win_[architecture].whl
```
