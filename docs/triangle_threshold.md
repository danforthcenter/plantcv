## Triangle Auto Threshold

Creates a binary image from a gray image using adaptive thresholding.

**plantcv.triangle_auto_threshold(*img, maxvalue, object_type, xstep=1*)**

**returns** thresholded image

- **Parameters:**
    - img - grayscale img object
    - maxValue - value to apply above threshold (255 = white)
    - objecttype - 'light' or 'dark', is target image light or dark?
    - xstep - value to move along x-axis to determine the points from which to calculate distance
              recommended to start at 1 and change if needed)
- **Context:**
    - Used to help differentiate plant and background
    

**Grayscale image (green-magenta channel)**

![Screenshot](img/documentation_images/triangle_threshold/input_gray_img.jpg)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Create binary image from a gray image based
thresholded = pcv.triangle_auto_threshold(img, 255,'light', xstep=10)
```

**Triangle Auto-Thresholded image (xstep=10)**

![Screenshot](img/documentation_images/triangle_threshold/4_triangle_thresh_hist_30.0.jpg)
![Screenshot](img/documentation_images/triangle_threshold/4_triangle_thresh_img_30.0.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Create binary image from a gray image based 
thresholded = pcv.triangle_auto_threshold(img, 255,'light', xstep=1)
```

**Triangle Auto-Thresholded image (xstep=1)**

![Screenshot](img/documentation_images/triangle_threshold/11_triangle_thresh_hist_3.0.jpg)
![Screenshot](img/documentation_images/triangle_threshold/11_triangle_thresh_img_3.0.jpg)
