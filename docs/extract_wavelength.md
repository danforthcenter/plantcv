## Extract Wavelength 

This function extracts a single band from a hyperspectral data cube that is the closest to a user defined wavelength reflectance from a hyperspectral datacube, 
which is a [`Spectral_data` class](Spectral_data.md) instance created while reading in with [readimage](read_image.md)
with `mode='envi'`. This function is similar to the [`extract_index`](extract_index.md) which calculates and outputs standard spectral indices. 

**plantcv.hyperspectral.extract_wavelength**(*spectral_data, wavelength*)

**returns** index array (instance of the `Spectral_data` class)

- **Parameters:**
    - spectral_data      - Hyperspectral data instance
    - wavelength         - Target wavelength value for band for extraction 

- **Note:**
    - This function will print out which wavelength was found to be closest to the target wavelength value input. Additionally, this metadata is available
    since the function outputs a spectral data class instance which has a method that stores the array type. 
    
- **Example use:**
    - Below
    
```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

blue_array_obj = pcv.hyperspectral.extract_wavelength(spectral_data=spectral_array_obj, wavelength=400)

blue_array_obj.array_type

```

```python
> 
```

**Grayscale array image**

![Screenshot](img/tutorial_images/hyperspectral/NDVI_index.jpg)

```python
> The closest band found to 400nm is: 400.033
```