## Extract Wavelength 

This function extracts a single band of a user defined wavelength reflectance from a hyperspectral datacube, which is a [`Spectral_data` class](Spectral_data.md) instance created while reading in with [readimage](read_image.md)
with `mode='envi'`. This function is similar to the [`extract_index`](extract_index.md) which is alreado 

**plantcv.hyperspectral.extract_wavelength**(*spectral_data, wavelength*)

**returns** calculated index array (instance of the `Spectral_data` class)

- **Parameters:**
    - spectral_data      - 
    - wavelength         - 

- **Note:**
    - 
- **Example use:**
    - Below
```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"


```

**NDVI array image**

![Screenshot](img/tutorial_images/hyperspectral/NDVI_index.jpg)

