## Read Image

Reads image into numpy ndarray and splits the path and image filename (*see note about when `mode='envi'`). Most modes of use of this function is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**plantcv.readimage**(*filename, mode="native"*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - mode     - return mode of image ("native," "rgb,", "rgba", "csv", "envi", or "gray"), defaults to "native"
    
- **Context:**
    - Reads in file to be processed
- **Notes:**
    - In most cases, the alpha channel in RGBA image data is unused (and causes issue when used as RGB image data),
    so unless specificed as `mode='rgba'` the `pcv.readimage()` function will read RGBA data in as an RGB image under
    default settings (`mode='native'`). However, if the alpha channel is needed users can specify `mode='rgba'`. 
    - Comma separated data can be read in with `mode='csv'` so that, for example, [thermal](tutorials/thermal_tutorial.md) data can 
    be used in downstream analysis, such as [pcv.analyze_thermal_values](analyze_thermal_values.md) 
    - ENVI hyperspectral data can be read in with `mode="envi"` where the filename parameter is the raw data file. This mode of 
    reading in data expects a `filename`.hdr file which gets used for shaping the hyperspectral datacube and labeling bands of data
    to the corresponding wavelength. An instance of the [`Spectral_data` class](Spectral_data.md) is created while reading in the data and this instance 
    is returned to the user rather than the usual `img, path, filename` that is returned under other modes of `pcv.readimage`. 
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md) 
    - [Use In Thermal Tutorial](tutorials/thermal_tutorial.md)
    - [Use In Hyperspectral Tutorial](tutorials/hyperspectral_tutorial.md)

!!! note
  ENVI mode currently supports Band Interleaved by Line (BIL) and Band Sequential (BSQ) raw data formats.

```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

#read in image
img, path, img_filename = pcv.readimage(filename="home/user/images/test-image.png", mode="native")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/readimage.py)
