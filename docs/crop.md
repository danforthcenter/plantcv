## Crop

Crops image to user specified coordinates 

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
crop_img = pcv.crop(img=img, x=100, y=50, h=2000, w=1700)

```

**Debug Crop Image**

![Screenshot](img/documentation_images/crop/)


**Cropped Image**

![Screenshot](img/documentation_images/crop/)
