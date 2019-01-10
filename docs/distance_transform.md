## Distance Transform

Perform distance transform on binary image

**plantcv.distance_transform**(*bin_img, distance_type, mask_size*)

**returns** distance transformed image normalized between 0 and 1

- **Parameters:**
    - bin_img - Binary image data
    - distance_type - Type of distance. It can be CV_DIST_L1, CV_DIST_L2 , or CV_DIST_C which are 1,2 and 3 respectively.
    - mask_size - Size of the distance transform mask. It can be 3, 5, or CV_DIST_MASK_PRECISE (the latter option is only supported by the first function). In case of the CV_DIST_L1 or CV_DIST_C distance type, the parameter is forced to 3 because a 3 by 3 mask gives the same result as 5 by 5 or any larger aperture.
- **Context:**
    - Used to perform object segmentation via thresholding and marker-aided [watershed segmentation](watershed.md).
- **Example use:**
    - See below.
    
**Input binary image**

![Screenshot](img/documentation_images/distance_transform/mask_img.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Perform dilation
# Results in addition of pixels to the boundary of object
distance_transform_img = pcv.distance_transform(mask, 1, 3)
```

**Image after distance transform**

![Screenshot](img/documentation_images/distance_transform/distance_transform_img.jpg)
