## RGB to HSV

Convert image from RGB colorspace to gray-scale.

**plantcv.rgb2gray**(*img*)

**returns** gray-scale image 

- **Parameters:**
    - img- Image to be converted
   
- **Context:**
    - Used to help differentiate plant and background

**Original RGB image**

![Screenshot](img/documentation_images/rgb2gray/original_image.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# image converted from RGB to gray.
gray = pcv.rgb2gray(img)
```
**Gray-scale Image**

![Screenshot](img/documentation_images/rgb2gray/gray.jpg)
