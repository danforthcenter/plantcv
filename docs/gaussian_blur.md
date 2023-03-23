## Gaussian Blur

Applies a gaussian blur filter. Applies median value to central pixel within a kernel size (ksize x ksize). 
The function is a wrapper for the OpenCV function [gaussian blur](http://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html?highlight=gaussianblur#gaussianblur).  

**plantcv.gaussian_blur**(*img, ksize, sigma_x=0, sigma_y=None*)

**returns** blurred image

- **Parameters:**
    - img - RGB or grayscale image data
    - ksize - Tuple of kernel dimensions, e.g. (5, 5). Must be odd integers.
    - sigma_x - standard deviation in X direction; if 0 (default), calculated from kernel size
    - sigma_y - standard deviation in Y direction; if sigma_Y is None (default), sigma_Y is taken to equal sigma_X
- **Context:**
    - Used to reduce image noise

**Original image**

![Screenshot](img/documentation_images/gaussian_blur/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Apply gaussian blur to a binary image that has been previously thresholded.
gaussian_img = pcv.gaussian_blur(img=img1, ksize=(51, 51), sigma_x=0, sigma_y=None)

```

**Gaussian blur (ksize = (51,51))**

![Screenshot](img/documentation_images/gaussian_blur/gaussian_blur51.jpg)

```python

# Apply gaussian blur to a binary image that has been previously thresholded.
gaussian_img = pcv.gaussian_blur(img=img1, ksize=(101, 101), sigma_x=0, sigma_y=None)

```

**Gaussian blur (ksize = (101,101))**

![Screenshot](img/documentation_images/gaussian_blur/gaussian_blur101.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/gaussian_blur.py)
