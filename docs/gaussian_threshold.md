## Gaussian Adaptive Threshold

Creates a binary image from a grayscale image using the Gaussian adaptive thresholding method.

Adaptive thresholds use a threshold value that varies across the image.
This local threshold depends on the local average, computed in a squared portion of the image of
*block_size* by *block_size* pixels, and on the *offset* relative to that local average.

In the Gaussian adaptive threshold, the local average is a weighed average of the pixel values in the block, where the weights are a 2D Gaussian centered in the middle.

**plantcv.threshold.gaussian**(*gray_img, max_value, object_type="light"*)

**returns** thresholded/binary image

- **Parameters:**
    - gray_img - Grayscale image data
    - block_size - Size of the block of pixels used to compute the local average
    - offset - Value substracted from the local average to compute the local threshold.
    A negative offset sets the local threshold above the local average.
    - object_type - "light" or "dark" (default: "light").
      - "light" for objects brighter than the background, sets the pixels above
      the local threshold to max_value and the pixels below to 0.
      - "dark" for objects darker than the background, sets the pixels below the
      local threshold to max_value and the pixels above to 0.
    - max_value - Value to apply above threshold (default: 255 = white)
- **Context:**
    - Useful for unevenly illuminated images


**Grayscale image (green-magenta channel)**

![Screenshot](img/documentation_images/auto_threshold/original_image1.jpg)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Create binary image from a gray image based
threshold_gaussian = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type='dark')

```

**Auto-Thresholded image (gaussian)**

![Screenshot](img/documentation_images/auto_threshold/gaussian_threshold.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/threshold/threshold_methods.py)
