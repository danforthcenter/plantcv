## Mean Adaptive Threshold

Creates a binary image from a grayscale image using the mean adaptive thresholding method.

Adaptive thresholds use a threshold value that varies across the image.
This local threshold depends on the local average, computed in a squared portion of the image of
*block_size* by *block_size* pixels, and on the *offset* relative to that local average.

In the mean adaptive threshold, the local average is the average of the pixel values in the block.

**plantcv.threshold.mean**(*gray_img, block_size, offset, object_type="light", max_value=255*)

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


**Grayscale image**

![Screenshot](img/documentation_images/adaptive_threshold/pollen_grains.png)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Adaptive threshold with different parameters
threshold_mean1 = pcv.threshold.mean(gray_img=gray_img, block_size=250, offset=25,
                                    object_type='dark', max_value=255)

threshold_mean2 = pcv.threshold.mean(gray_img=gray_img, block_size=15, offset=5,
                                    object_type='dark', max_value=255)

threshold_mean3 = pcv.threshold.mean(gray_img=gray_img, block_size=2000, offset=25,
                                    object_type='dark', max_value=255)
```

**Thresholded image**

![Screenshot](img/documentation_images/adaptive_threshold/pollen_grains_adaptive_mean_250-25_scaled.png)

**Thresholded image using a small block size**

![Screenshot](img/documentation_images/adaptive_threshold/pollen_grains_adaptive_mean_15-5_scaled.png)

**Thresholded image using a large block size**

![Screenshot](img/documentation_images/adaptive_threshold/pollen_grains_adaptive_mean_2000-25_scaled.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/threshold/threshold_methods.py)
