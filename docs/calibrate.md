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
- **Example use:**
    - Below
    


```python

from plantcv import plantcv as pcv

raw = pcv.readimage(filename=raw_spectral_filename)
white_reference = pcv.readimage(filename=white_reference_filename)
dark_reference = pcv.readimage(filename=dark_reference_filename)

calibrated_data = pcv.hyperspectral.calibrate(raw_data=raw, white_reference=white_reference, dark_reference=dark_reference)
```

