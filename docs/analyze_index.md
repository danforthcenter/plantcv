## Analyze a Hyperspectral Index

This function calculates the hyperspectral index statistics and writes the values  as observations out to
       the [Outputs class](outputs.md).
       
**plantcv.hyperspectral.analyze_index**(*thermal_array, mask, histplot=False*)

**returns** thermal histogram (if `histplot=True`, otherwise returns None object)

- **Parameters:**
    - thermal_array - Numpy array of thermal values (read in with [pcv.readimage](read_image.md) with `mode='csv'`)
    - mask          - Binary mask made from selected contours
    - histplot      - If True plots histogram of intensity values (default histplot = False)
- **Context:**
    - Data about image temperature within a masked region. 
- **Example use:**
    - Below
- **Output data stored:** Data ('max_temp', 'min_temp', 'mean_temp', 'median_temp', 'thermal_frequencies') automatically gets stored to the 
    [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original thermal array image**

![Screenshot](img/documentation_images/analyze_thermal_values/scaled_thermal_img.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Caclulates the proportion of pixels that fall into a signal bin and writes the values to a file. Also provides a histogram of this data
thermal_hist  = pcv.analyze_thermal_values(thermal_img, mask, histplot=True)

# Access data stored out from analyze_thermal_values
temp_range = pcv.outputs.observations['max_temp']['value'] - pcv.outputs.observations['min_temp']['value']

```
