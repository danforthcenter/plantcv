## RGB to HSV

Convert image from RGB colorspace to gray-scale.

**plantcv.rgb2gray**(*rgb_img*)

**returns** grayscale image 

- **Parameters:**
    - img - RGB image data
   
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
