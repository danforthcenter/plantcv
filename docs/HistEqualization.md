## Histogram Equalization

This is a method used to normalize the distribution of signal intensity values within an image. 
If the image has low contrast it will make it easier to threshold.

**HistEqualization**(*img, device, debug=False*)

**returns** device, normalized image

- **Parameters:**
    - img - the original 2 dimensional grayscale image for analysis.
    - device - Counter for image processing steps
    - debug- Default value is False, if True, filled intermediate image will be printed
- **Context:**
    - Used to normalize the distribution of a signal intensity within an image.

**Grayscale image**

![Screenshot](img/documentation_images/HistEqualization/grayscale_image.jpg)  

```python
import plantcv as pcv

# Examine signal distribution within an image
# prints out an image histogram of signal within image
device, he_img = pcv.HistEqualization(img, device, debug=True)
```

**Normalized image**

![Screenshot](img/documentation_images/HistEqualization/normalized_image.jpg)  
