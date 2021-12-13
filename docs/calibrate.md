## Calibrate

Calibrate a raw hyperspectral image using white and dark reference images. 

**plantcv.hyperspectral.calibrate(*raw_data, white_reference, dark_reference*)**

**returns** calibrated [`Spectral_data` class instance](Spectral_data.md) 

- **Parameters:**
    - raw_data - Raw hyperspectral data instance of the `Spectral_data` class (read in with [pcv.readimage](read_image.md) with `mode='envi'`) 
    - white_reference - White reference data (read in with pcv.readimage with `mode='envi'`) 
    - dark_reference - Dark reference data (read in with pcv.readimage with `mode='envi'`) 

- **Context:**
    - Used to calibrate raw hyperspectral image data into reflectance values. Calibrate using `reflectance = (raw data - dark reference) / (white reference - dark reference)`
    based on [calibration protocol](https://docs.google.com/document/d/1w_zHHlrPVKsy1mnW9wrVzAU2edVqZH8i1IZa5BZxVpo/edit#heading=h.jjfbhbos05cc) posted by 
    [The TERRA-REF team](https://github.com/terraref). This process of calibration might look different depending on the hyperspectral camera used so we highly encourage 
    PlantCV users to reach out to the PlantCV developers/maintainers at the PlantCV [GitHub issues page](https://github.com/danforthcenter/plantcv/issues) to request to extend 
    the functionality of this function to handle data from different cameras. 
    
!!! note
    Calibrated values are clipped to the range 0-1 

- **Example use:**
    - Below
    


```python

from plantcv import plantcv as pcv

raw = pcv.readimage(filename=raw_spectral_filename)
white_reference = pcv.readimage(filename=white_reference_filename)
dark_reference = pcv.readimage(filename=dark_reference_filename)

calibrated_data = pcv.hyperspectral.calibrate(raw_data=raw, white_reference=white_reference, dark_reference=dark_reference)
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/hyperspectral/calibrate.py)
