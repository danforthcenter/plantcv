## Read grayscale multispectral images into `MS_data` object

Reads one or more grayscale images into an `MS_data` instance using syntax from the Danforth Center for Plant Science's Phenotyping Core Facility.

**plantcv.multispec.read_ms**(*source, wavelengths=None*)

**returns** MS_data object

- **Parameters:**
    - source    - path to an image or directory. In either case the directory will be searched for (other) image files starting with `MS\\d+`. These files should be single channel grayscale images with the wavelength described in the filename.
	- wavelengths - list of wavelengths to include, defaults to None in which case all `MS\\d+` prefixed images will be used.
	
- **Context:**
    - Reads in files to process multispectral data from several source files.
- **Notes:**
    - This function is made to work with the metadata collected by the Danforth Center's Phenotyping Core Facility, if your multispectral images are stored in a different format then this will not work for your use case. Please feel free to make a feature request on Github


```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

#read in image
ms = pcv.multispec.read_ms(filename="home/user/multispectral_images")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/readimage.py)
