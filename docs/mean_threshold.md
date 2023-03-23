## Mean Adaptive Threshold

Creates a binary image from a grayscale image using the mean adaptive thresholding method.

**plantcv.threshold.mean**(*gray_img, max_value, object_type="light"*)

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

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Create binary image from a gray image based 
threshold_mean = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type='dark')

```

**Auto-Thresholded image (mean)**

![Screenshot](img/documentation_images/auto_threshold/mean_threshold.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/threshold/threshold_methods.py)
