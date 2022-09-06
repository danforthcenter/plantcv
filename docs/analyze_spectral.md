## Analyze Spectral Values 

This function calculates the reflectance frequencies associated with a hyperspectral datacube and writes 
the values out as observations to get saved out. Can also print out a histogram of average reflectance intensity.

**plantcv.hyperspectral.analyze_spectral**(*array, mask, histplot=False, label="default"*)

**returns** reflectance histogram (if `histplot=True`, otherwise returns None object)

- **Parameters:**
    - array         - A hyperspectral datacube object, an instance of the `Spectral_data` class (read in with [pcv.readimage](read_image.md) with `mode='envi'`)
    - mask          - Binary mask made from selected contours
    - histplot      - If True plots histogram of reflectance intensity values (default histplot = False)
    - label         - Optional label parameter, modifies the variable name of observations recorded. (default `label="default"`)
- **Example use:**
    - Below 
- **Output data stored:** Data ('max_reflectance', 'min_reflectance', 'median_reflectance', 'spectral_std', 'spectral_frequencies', 'global_mean_reflectance', 'global_median_reflectance', 'global_spectral_std') automatically gets stored to the 
    [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Calculates reflectance frequencies and writes the values as observations. Also provides a histogram of this data
spectral_hist  = pcv.hyperspectral.analyze_spectral(array=spectral_data, mask=mask, histplot=True, label="default")

# Access data stored 
reflectance_range = max(pcv.outputs.observations['default']['max_reflectance']['value']) - min(pcv.outputs.observations['default']['min_reflectance']['value'])

```

**Spectral Reflectance Intensity Histogram**

![Screenshot](img/tutorial_images/hyperspectral/spectral_histogram.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/hyperspectral/analyze_spectral.py)
