## Median Blur

Applies a median blur filter. Applies median value to central pixel within a kernel size (ksize x ksize). 
The function is a wrapper for the SciPy function [median filter](https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.ndimage.filters.median_filter.html).

**plantcv.median_blur**(*gray_img, ksize*)**

**returns** blurred image

- **Parameters:**
    - gray_img - Grayscale image data
    - ksize - kernel size => integer or tuple, ksize x ksize box if integer, (n, m) size box if tuple 
- **Context:**
    - Used to reduce image noise
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

**Thresholded image**

![Screenshot](img/documentation_images/median_blur/thresholded_image.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Apply median blur to a binary image that has been previously thresholded.
blur_5 = pcv.median_blur(gray_img, 5)
```

**Median blur (k = 5)**

![Screenshot](img/documentation_images/median_blur/median_blur5.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Apply median blur to a binary image that has been previously thresholded.
blur_11 = pcv.median_blur(gray_img, (11, 11))
```

**Median blur (k = (11,11))**

![Screenshot](img/documentation_images/median_blur/median_blur11.jpg)
