## Filter on object eccentricity 

Detects more circular regions in a binary image based on eccentricity.
A value of eccentricity between 0 and 1 corresponds to an ellipse.
The closer the value to 0 the closer the shape is to a circle.

**plantcv.filter.eccentricity**(*bin_img, ecc_thresh=0*)

**returns** mask

- **Parameters:**
    - bin_img - Binary image containing the connected regions to consider
    - ecc_thresh - Eccentricity threshold below which a region is detected
- **Context:**
    - Used to isolate disc-shaped objects of interest in a binary image. The output mask can be used for further analysis.
- **Example use:**
    - Below

**Original image**

![ori_img](img/documentation_images/filter_eccentricity/count_img.jpg)

**Mask generated using binary threshold in the blue channel**

![bin_img](img/documentation_images/filter_eccentricity/discs_pre_scaled.png)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot"
pcv.params.debug = "plot"

# Apply detect discs to the binary image with an
# eccentricity threshold of 0.9
mask_9 = pcv.filter.eccentricity(bin_img=binary_img, ecc_thresh=0.9)

# Apply detect discs to the binary image with an
# eccentricity threshold of 0.5
mask_5 = pcv.filter.eccentricity(bin_img=binary_img, ecc_thresh=0.5)

```

**Mask of detected objects with eccentricity threshold of 0.9**

![count_img](img/documentation_images/filter_eccentricity/count_mask.png)

**Mask of detected objects with eccentricity threshold of 0.5**

![count_img](img/documentation_images/filter_eccentricity/discs_mask_scaled.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/filter/eccentricity.py)