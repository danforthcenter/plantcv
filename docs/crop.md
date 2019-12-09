## Crop

Crops image to specified coordinates 

**plantcv.crop**(*img, x, y, h, w*)

**returns** image after cropping 

- **Parameters:**
    - img - RGB, grayscale, or hyperspectral image data
    - x - Starting X coordinate
    - y - Starting Y coordinate 
    - h - Height 
    - w - Width
- **Context:**
    - Crops image 
    
**Input image**

![Screenshot](img/documentation_images/auto_crop/2016-05-25_1031.chamber129-camera-01.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Crop image
crop_img = pcv.crop()

crop_img2 = pcv.crop()

```

**Debug Crop Images**

![Screenshot](img/documentation_images/crop/)

