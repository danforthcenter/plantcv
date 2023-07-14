## Otsu Auto Threshold

Creates a binary image from a gray image based on the threshold values. 

**plantcv.threshold.otsu**(*gray_img, object_type="light"*)

**returns** thresholded/binary image

- **Parameters:**
    - gray_img - Grayscale image data
    - object_type - "light" or "dark" (default: "light"). If object is lighter than the background then standard 
    thresholding is done. If object is darker than the background then inverse thresholding is done.
   
- **Context:**
    - Used to help differentiate plant and background

**Grayscale image (green-magenta channel)**

![Screenshot](img/documentation_images/otsu_threshold/original_image1.jpg)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Create binary image from a gray image based on threshold values. 
# Targeting dark objects in the image.
threshold_dark = pcv.threshold.otsu(gray_img=gray_img, object_type='dark')

```

**Thresholded image**

![Screenshot](img/documentation_images/otsu_threshold/thresholded_dark.jpg)

**Grayscale image (blue-yellow channel)**

![Screenshot](img/documentation_images/otsu_threshold/original_image.jpg)

```python

# Create binary image from a gray image based on threshold values. 
# Targeting light objects in the image.
threshold_light = pcv.threshold.otsu(gray_img=gray_img, object_type='light')

```

**Thresholded image (inverse)**

![Screenshot](img/documentation_images/otsu_threshold/thresholded_light.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/threshold/threshold_methods.py)
