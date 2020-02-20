## Visualize all potential colorspaces

This is a plotting method used to examine all potential colorspaces from available PlantCV functions.

**plantcv.visualize.colorspaces**(*rgb_img*)

**returns** fig_hist

- **Parameters:**
    - rgb_img - RGB image data, the original image for analysis.

- **Example use:**
    - Below

**Original image**

![Screenshot](img/tutorial_images/vis/original_image.jpg) 


```python

from plantcv import plantcv as pcv

# Examine all colorspaces at one glance
colorspace_img = pcv.visualize.colorspaces(rgb_img=img)

```

**Ouput**

![Screenshot](img/documentation_images/histogram/mask.jpg)

