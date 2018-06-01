## Histogram Equalization

This is a method used to normalize the distribution of signal intensity values within an image. 
If the image has low contrast it will make it easier to threshold.

**hist_equalization**(*img, device, debug=None*)

**returns** device, normalized image

- **Parameters:**
    - img - the original 2 dimensional grayscale image for analysis.
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to normalize the distribution of a signal intensity within an image.

**Grayscale image**

![Screenshot](img/documentation_images/HistEqualization/grayscale_image.jpg)  

```python
from plantcv import plantcv as pcv

# Examine signal distribution within an image
# prints out an image histogram of signal within image
device, he_img = pcv.HistEqualization(img, device, debug="print")
```

**Normalized image**

![Screenshot](img/documentation_images/HistEqualization/normalized_image.jpg)  
