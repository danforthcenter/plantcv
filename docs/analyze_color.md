## Analyze Color

Extract color data of objects and produce pseudocolored images, can extract data for RGB (Red, Green, Blue), HSV (Hue, Saturation, Value) and LAB (Lightness, Green-Magenta, Blue Yellow) channels.

**plantcv.analyze_color**(*rgb_img, mask, hist_plot_type=None*)

**returns** data analysis images  

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
 
- **Units of Data Stored:**  
    - Red Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Green Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Blue Channel - histogram of object pixel intensity values 0 (unsaturated) to 255 (saturated)  
    - Hue Channel - histogram of object hue values 0 to 359 degrees
    - Saturation Channel - histogram of object pixel saturation values 0 (unsaturated) to 100% (saturated)
    - Value Channel - histogram of object pixel value/lightness values 0 (black) to 100% (bright)  
    - Lightness Channel - histogram of object pixel lightness values 0 (black) to 100% (bright)  
    - Green-Magenta Channel - histogram of object pixel green-magenta color component values -128 (green) to 127 (magenta)  
    - Blue-Yellow Channel - histogram of object pixel blue-yellow color component values -128 (blue) to 127 (yellow)  

**Original image**

![Screenshot](img/documentation_images/analyze_color/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Analyze Color
    
analysis_images = pcv.analyze_color(rgb_img, mask, 'all')

```

**Histograms of (R, G, B), (H, S, V), and (L, A, B) color channels**

![Screenshot](img/documentation_images/analyze_color/color_histogram.jpg)

**Pseudocolored value-channel image**

![Screenshot](img/documentation_images/analyze_color/pseudocolored_value_image.jpg)
