## Analyze Thermal Values 

This function calculates the intensity of each pixel associated with the temperature and writes 
the values out to a file. Can also print out a histogram of pixel intensity.

**plantcv.analyze_thermal_values**(*thermal_array, mask, histplot=False*)

**returns** analysis_images

- **Parameters:**
    - thermal_array - Numpy array of thermal values (read in with [pcv.readimage](read_image.md) with `mode='flir'`)
    - mask          - Binary mask made from selected contours
    - histplot      - If True plots histogram of intensity values (default histplot = False)
- **Context:**
    - Data, such as  automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Example use:**
    - Below
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original thermal array image**

![Screenshot](img/documentation_images/analyze_thermal_values/scaled_thermal_img.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Caclulates the proportion of pixels that fall into a signal bin and writes the values to a file. Also provides a histogram of this data
thermal_hist  = pcv.analyze_thermal_values(thermal_img, mask, histplot=True)

```


**NIR signal histogram**

![Screenshot](img/documentation_images/analyze_thermal_values/thermal_hist.jpg)

**Note:** The grayscale input image and object mask can be used with the [pcv.visualize.pseudocolor](visualize_pseudocolor.md) function
which allows the user to pick a colormap for plotting.

```python

# Pseudocolor the thermal 
thermal_hist  = pcv.analyze_thermal_values(thermal_img, min_value=31, max_value=35, mask=mask)

```

![Screenshot](img/documentation_images/analyze_thermal_values/thermal_pseudocolored.jpg)
