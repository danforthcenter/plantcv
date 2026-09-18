## Read grayscale multispectral images into `MS_data` object

Reads one or more grayscale images into an `MS_data` instance using syntax from the Danforth Center for Plant Science's Phenotyping Core Facility.

**plantcv.multispec.read_ms**(*source, wavelengths=None, pattern="MS(\\\\d+)_((SV|TV))_BP0_(\\\\d+).\*"*)

**returns** MS_data object

- **Parameters:**
    - source    - path to an image or directory. In either case the directory will be searched for (other) image files starting with `MS\\d+`. These files should be single channel grayscale images with the wavelength described in the filename. Note that using a directory is ambiguous compared to a filename or a list of files since the first file read from that directory will be treated as the reference to compare other images against, see the `pattern` argument.
	- wavelengths - list of wavelengths to include, defaults to None in which case all matching images will be used.
	- pattern - Regular expression used to match images that are of the same subject from the same angle, etc. This should include a capture group for the wavelength, which is expected to be the *first* capture group. Subsequent capture groups are used to match against other candidate image files. For example if the source file is `MS455_SV_BP0_90_other1_metadata0_0.png` and our pattern were the default (`MS(\\d+)_((SV|TV))_BP0_(\\d+).*`) then we would keep any image file with `MS\\d+` (MS followed by digits) but would require `SV` and `90` for the camera-position and angle but be agnostic to any other metadata terms.

- **Context:**
    - Reads in files to process multispectral data from several source files.
- **Notes:**
    - This function is made to work with the metadata collected by the Danforth Center's Phenotyping Core Facility, if your multispectral images are stored in a different format then this may not work for your use case. Please feel free to make a feature request on Github.


```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

#read in image
ms = pcv.multispec.read_ms(filename="home/user/multispectral_images")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/readimage.py)
