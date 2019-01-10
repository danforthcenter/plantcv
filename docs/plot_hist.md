## Plot Histogram

This is a plotting method used to examine the distribution of signal within an image.

**plantcv.plot_hist**(*img, name=False*)

**returns** bins, hist

- **Parameters:**
    - img - RGB or grayscale image data, the original image for analysis.
    - name - the name of the output plot as a string (default: name=False)
- **Context:**
    - Examine the distribution of the signal, this help you select a value for binary thresholding.
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Grayscale image**

![Screenshot](img/documentation_images/plot_hist/grayscale_image.jpg) 

```python

from plantcv import plantcv as pcv

# Examine signal distribution within an image
# prints out an image histogram of signal within image
bins, hist = pcv.plot_hist(img, 'histogram')
```

**Histogram of signal intensity**

![Screenshot](img/documentation_images/plot_hist/histogram.jpg) 
