## Extract Wavelength 

This function extracts a single reflectance band that is the closest to a user defined wavelength from a hyperspectral datacube, 
which is a [`Spectral_data` class](Spectral_data.md) instance created while reading in with [`pcv.readimage`](read_image.md)
with `mode='envi'`. This function is similar to the [`pcv.spectral_index`](spectral_index.md) functions which calculates 
and outputs standard spectral indices from a hyperspectral datacubes. 

**plantcv.hyperspectral.extract_wavelength**(*spectral_data, wavelength*)

**returns** channel array (instance of the `Spectral_data` class)

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
pcv.params.debug = "plot"

# Many plants absorb 430nm wavelength light. 
blue_array_obj = pcv.hyperspectral.extract_wavelength(spectral_data=spectral_array_obj, wavelength=430)

blue_array_obj.array_type

```

```python
> The closest band found to 400nm is: 400.033

```

**Grayscale array image**

![Screenshot](img/documentation_images/extract_wavelength/430_grayscale.jpg)

**Array type**

```python
> 'index_430'

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/hyperspectral/extract_wavelength.py)
