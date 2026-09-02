## class `MS_data`

A PlantCV data object class.

*class* plantcv.**MS_data**

`MS_data` is a class used to create instances of multispectral data objects for PlantCV analysis after using the Bellwether lemnatech facility from the Danforth Center for Plant Science's Phenotyping Core Facility, which collects multispectral images as several unique png files.

`MS_data` objects are made by reading data with [pcv.multispec.read_ms](multispec_read_ms.md)

### Attributes

Attributes are accessed as ms_data.*attribute*.

**array_data**: The actual data, stored as a Numpy array. 

**wavelength_dict**: A dictionary of wavelengths included in the `MS_data` object.

**max_wavelength**: The maximum wavelength in the `MS_data` object.

**min_wavelength**: The minimum wavelength in the `MS_data` object.

**pseudo_rgb**: Pseudo-RGB image

**filename**: The filename where the data originated from

**metadata**: Metadata in a dictionary. Includes directory and list of files originally read.

### Example

below


```python
from plantcv import plantcv as pcv      

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

#read in image
ms = pcv.multispec.read_ms(source="home/user/multispectral_images")

type(ms)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/classes.py)
