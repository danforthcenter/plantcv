## Binary Threshold

Creates a binary image from a gray image based on the threshold values. 
The object target can be specified as dark or light.

**plantcv.threshold.binary(*gray_img, threshold, max_value, object_type="light"*)**

**returns** thresholded/binary image

- **Parameters:**
    - gray_img - Grayscale image data
    - threshold - Threshold value (0-255)
    - max_value - Value to apply above threshold (255 = white)
    - object_type - "light" or "dark" (default: "light"). If object is lighter than the background then standard 
                    thresholding is done. If object is darker than the background then inverse thresholding is done.
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md)
    
**Original image**

![Screenshot](img/documentation_images/binary_threshold/original_image.jpg)

**Grayscale image (saturation channel)**

![Screenshot](img/documentation_images/binary_threshold/saturation_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Create binary image from a gray image based on threshold values. Targeting light objects in the image.
threshold_light = pcv.threshold.binary(gray_img, 36, 255, 'light')
```

**Thresholded image**

![Screenshot](img/documentation_images/binary_threshold/thresholded_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Create binary image from a gray image based on threshold values. Targeting dark objects in the image.
threshold_dark = pcv.threshold.binary(gray_img, 36, 255, 'dark')
```

**Thresholded image (inverse)**

![Screenshot](img/documentation_images/binary_threshold/thresholded_inverse_image.jpg)
