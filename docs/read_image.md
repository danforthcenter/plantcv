## Read Image

Reads image into numpy ndarray and splits the path and image filename (*see note about when `mode='envi'`). Most modes of use of this function is a wrapper for the OpenCV function [imread](http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html).

**plantcv.readimage**(*filename, mode="native"*)

**returns** img, path, image filename

- **Parameters:**
    - filename - image file to be read (possibly including a path)
    - mode     - return mode of image ("native," "rgb", "rgba", "normalize", "csv", "envi", "arcgis", "gray", "nd2",
    or "thermal"), defaults to "native"
    
- **Context:**
    - Reads in file to be processed
- **Notes:**
    - In most cases, the alpha channel in RGBA image data is unused (and causes issue when used as RGB image data),
    so unless specificed, the `pcv.readimage()` function will read RGBA data in as an RGB image under
    default settings (`mode="native"`). However, if the alpha channel is needed users must specify `mode="rgba"`. 
    - Comma separated data can be read in with `mode="csv"` so that, for example, thermal data can 
    be used in downstream analysis, such as [`pcv.analyze.thermal`](analyze_thermal.md).
    - Nikon microscope images can be read in using `mode="nd2"`.
    - FLIR thermal images can be read in using `mode="thermal"`. 
    - Hyperspectral data can be read in with `mode="envi"` where the filename parameter is the raw data file. There is also support for 
    ArcGis style hyperspectral images (`mode="arcgis"`). These modes of 
    reading in data expects a `filename`.hdr file which gets used for shaping the hyperspectral datacube and labeling bands of data
    to the corresponding wavelength. An instance of the [`Spectral_data` class](Spectral_data.md) is created while reading in the data and this instance 
    is returned to the user rather than the usual `img, path, filename` that is returned under other modes of `pcv.readimage`. There is some flexibility 
    in formats of images supported but encourage people to reach out on [GitHub](https://github.com/danforthcenter/plantcv/issues) and collaborate with the
    PlantCV community to expand our support.
	- A wide variety of images can be read with `mode=normalize` which may be useful for special cases, such as 16-bit color images that otherwise may behave unexpectedly. This mode will normalize images to values to be between 0 and 255 using `cv2.normalize`.
- **Example use:**
    - [Use In Color Correction Tutorial](https://plantcv.org/tutorials/color-correction) 
    - [Use In Grayscale Tutorial](https://plantcv.org/tutorials/grayscale)

!!! note
  ENVI mode currently supports Band Interleaved by Line (BIL), Band Interleaved by Pixel (BIP) Band Sequential (BSQ) raw data formats.

```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

#read in image
img, path, img_filename = pcv.readimage(filename="home/user/images/test-image.png", mode="native")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/readimage.py)
