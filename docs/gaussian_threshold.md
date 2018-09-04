## Gaussian Adaptive Threshold

Creates a binary image from a grayscale image using the Gaussian adaptive thresholding method.

**plantcv.threshold.gaussian(*gray_img, max_value, object_type="light"*)**

**returns** thresholded/binary image

- **Parameters:**
    - gray_img - Grayscale image data
    - max_value - Value to apply above threshold (255 = white)
    - object_type - "light" or "dark" (default: "light"). If object is lighter than the background then standard 
    thresholding is done. If object is darker than the background then inverse thresholding is done
- **Context:**
    - Used to help differentiate plant and background
    

**Grayscale image (green-magenta channel)**

![Screenshot](img/documentation_images/auto_threshold/original_image1.jpg)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Create binary image from a gray image based
threshold_gaussian = pcv.threshold.gaussian(gray_img, 255, 'dark')
```

**Auto-Thresholded image (gaussian)**

![Screenshot](img/documentation_images/auto_threshold/gaussian_threshold.jpg)
