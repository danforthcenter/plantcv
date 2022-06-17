## Write data

Write a hyperspectral image in ENVI format to the specified file.
It creates a text header file with extension .hdr and a binary file with
extension .raw.  This function only supports Band-Interleaved-by-Line (BIL)
interleave.

**plantcv.hyperspectral.write_data**(*filename, spectral_data*):


- **Parameters:**
    - filename- desired name of the hyperspectral image file. The extensions are ignored and .hdr and .raw are used.
    - spectral_data- Hyperspectral data object

- **Context:**
    - Used to save a modified hyperspectral image

- **Example use:**

```python
from plantcv import plantcv as pcv

modified_spectral = pcv.Spectral_data(array_data=modified_array_data,
                          max_wavelength=list(source_spectral.wavelength_dict.keys())[-1],
                          min_wavelength=list(source_spectral.wavelength_dict.keys())[0],
                          max_value=float(np.amax(modified_array_data)),
                          min_value=float(np.amin(modified_array_data)),
                          d_type=modified_array_data.dtype,
                          wavelength_dict=source_spectral.wavelength_dict,
                          samples=modified_array_data.shape[1],
                          lines=modified_array_data.shape[0], interleave='bil',
                          wavelength_units=source_spectral.wavelength_units,
                          array_type="datacube",
                          pseudo_rgb=None,
                          filename=source_spectral.filename,
                          default_bands=None)

pcv.hyperspectral.write_data('test-hyperspectral', modified_spectral)
```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/hyperspectral/write_data.py)
