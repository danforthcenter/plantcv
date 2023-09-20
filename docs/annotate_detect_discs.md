## Detect discs 

Detects disc-shaped regions in a binary image based on eccentricity.
A value of eccentricity between 0 and 1 corresponds to an ellipse.
The closer the value to 0 the closer the shape is to a circle.

**plantcv.annotate.detect_discs**(*bin_img, ecc_thresh=0*)

**returns** mask, coordinates of centroids

- **Parameters:**
    - bin_img - Binary image containing the connected regions to consider
    - ecc_thresh - Eccentricity threshold below which a region is detected
- **Context:**
    - Used to isolate disc-shaped objects of interest in a binary image. The output mask can be used for further analysis
    and the coordinates can be used for object counting along with the class `plantcv.annotate.ClickCount`.
- **Example use:**
    - Below

**Original image**

![ori_img](img/documentation_images/annotate_click_count/count_img.jpg)

**Mask generated using binary threshold in the blue channel**
![bin_img](img/documentation_images/annotate_detect_discs/discs_pre_scaled.png)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot"
pcv.params.debug = "plot"

# Apply detect discs to the binary image with an
# eccentricity threshold of 0.9
discs_mask, discs_coor = pcv.annotate.detect_discs(bin_img=binary_img, ecc_thresh=0.9)

# Apply detect discs to the binary image with an
# eccentricity threshold of 0.5
discs_mask, discs_coor = pcv.annotate.detect_discs(bin_img=binary_img, ecc_thresh=0.5)

```

**Mask of detected objects with eccentricity threshold of 0.9**
![count_img](img/documentation_images/annotate_click_count/count_mask.png)

**Mask of detected objects with eccentricity threshold of 0.5**
![count_img](img/documentation_images/annotate_detect_discs/discs_mask_scaled.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/annotate/detect_discs.py)
