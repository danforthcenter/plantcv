## Rotate Hyperspectral Datacubes 

This function rotates a hyperspectral datacube counterclockwise in increments of 90 degrees.  The input and output is a [`Spectral_data` class](Spectral_data.md) 
instance created while reading in with [`pcv.readimage`](read_image.md) with `mode='envi'`. This function is similar to the [`pcv.transform.rotate`](rotate2.md) functions
but is specifically suitable for HSI image analysis. 

**plantcv.hyperspectral.rot90**(*spectral_data, k*)

**returns** rot_hsi (instance of the `Spectral_data` class)

- **Parameters:**
    - spectral_data      - Hyperspectral data instance
    - k                  - Number of times the array is rotated by 90 degrees


- **Example use:**
    - Below
    
    

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Rotate 90 degrees counterclockwise 
rot_hsi = pcv.hyperspectral.rot90(spectral_data=spectral_array_obj, k=1)

# Rotate 180 degrees
upside_down_hsi = pcv.hyperspectral.rot90(spectral_data=spectral_array_obj, k=2)

```


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/hyperspectral/rot90.py)
