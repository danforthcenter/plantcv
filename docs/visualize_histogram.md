## Plot Histogram

This is a plotting method used to examine the distribution of signal within an image.
**plantcv.visualize.histogram**(*img, mask=None, bins=None, lower_bound=None, upper_bound=None, title=None*)
**returns** fig_hist

- **Parameters:**
    - img - Image data which is numpy.ndarray, the original image for analysis.
    - mask - Optional binary mask made from selected contours (default mask=None).
    - bins - Number of class to divide spectrum into (default bins=256).
    - lower_bound - lower bound of range to be shown in the histogram (default lower_range=None). 
    - upper_bound - upper bound of range to be shown in the histogram. 
    - title - The title for the histogram (default title=None) 
    
**Context:**
    - Examine the distribution of the signal, this can help select a value for binary thresholding.
    
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Grayscale image**

![Screenshot](img/documentation_images/histogram/01_hsv_saturation.jpg)

**Mask**

![Screenshot](img/documentation_images/histogram/mask.jpg)

```python

from plantcv import plantcv as pcv
pcv.params.debug = "plot"

# Examine signal distribution within an image
# prints out an image histogram of signal within image
hist_figure1, hist_data1 = pcv.visualize.histogram(gray_img, mask=mask)

# Alternatively, users can change the `bins`, `lower_bound`, `upper_bound` and `title`.
hist_figure2, hist_data2 = histogram(img=gray_img, mask=mask, bins=256, title="Histogram with Customized Bins")
hist_figure3, hist_data3 = histogram(img=gray_img, mask=mask, lower_bound=10, upper_bound=200, title="Trimmed Histogram")

```

**Histogram of signal intensity**

![Screenshot](img/documentation_images/histogram/gray_histogram_default.png)
![Screenshot](img/documentation_images/histogram/gray_histogram_bins.png)
![Screenshot](img/documentation_images/histogram/gray_histogram_trimmed.png)

If input an RGB image, the histogram function can plot histograms for 3 bands automatically.
**RGB image**
![Screenshot](img/tutorial_images/vis/original_image.jpg)
```python

from plantcv import plantcv as pcv
pcv.params.debug = "plot"

# Examine signal distribution within an image
# prints out an image histogram of signal within image
hist_figure, hist_data = pcv.visualize.histogram(img=RGB_img, mask=mask)

```
![Screenshot](img/documentation_images/histogram/RGB_histogram.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/histogram.py)
