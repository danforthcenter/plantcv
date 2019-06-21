## Analyze Color

Extract color data of objects and produce pseudocolored images, can extract data for RGB (Red, Green, Blue), HSV (Hue, Saturation, Value) and LAB (Lightness, Green-Magenta, Blue Yellow) channels.

**plantcv.analyze_color**(*rgb_img, mask, hist_plot_type=None*)

**returns** Histogram image (if hist_plot_type is not `None`, otherwise returns `None` object)   

- **Parameters:**  
    - rgb_img - RGB image data
    - mask - binary mask of selected contours
    - hist_plot_type - None (default), 'all', 'rgb','lab' or 'hsv', this is the data to be printed to an SVG histogram file, however all (every channel) data is still stored to the database.
- **Context:**
    - Used to extract color data from RGB, LAB, and HSV color channels.
    - Generates histogram of color channel data. Data automatically gets stored into the [Outputs class](outputs.md). 
    Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original image**

![Screenshot](img/documentation_images/analyze_color/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Analyze Color
    
analysis_image = pcv.analyze_color(rgb_img, mask, 'all')

```

**Histograms of (R, G, B), (H, S, V), and (L, A, B) color channels**

![Screenshot](img/documentation_images/analyze_color/color_histogram.jpg)

**Pseudocolored value-channel image**

**Note:** The grayscale input image (e.g. value-channel) and object mask can be used with the [pcv.visualize.pseudocolor](visualize_pseudocolor.md) function
which allows the user to pick a colormap for plotting.

![Screenshot](img/documentation_images/analyze_color/pseudocolored_value_image.jpg)
