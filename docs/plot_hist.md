## Plot Histogram

This is a plotting method used to examine the distribution of signal within an image.

**plot_hist**(*img, 'hist_name'*)

**returns** no return value, makes a plot

- **Parameters:**
    - img = the original 2-dimensional grayscale image for anaysis.
    - name = the name of the output plot
- **Context:**
    - Examine the distribution of the signal, this help you select a value for binary thresholding.
- **Example use:**
    - [Use In NIR Tutorial](nir_tutorial.md)

**Grayscale image**

![Screenshot](img/documentation_images/plot_hist/grayscale_image.jpg) 

```python
import plantcv as pcv

# Examine signal distribution within an image
# prints out an image histogram of signal within image
pcv.plot_hist(img, 'histogram')
```

**Histogram of signal intensity**

![Screenshot](img/documentation_images/plot_hist/histogram.jpg) 
