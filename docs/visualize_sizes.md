## Visualize object sizes

This function plots separate objects as different colors and annotates the largest objects with their respective sizes. 

**plantcv.visualize.sizes**(*img, mask, num_objects=100*)

**returns** plotting_img 

- **Parameters:**
    - img         - RGB or grayscale image data for plotting annotations.
    - mask        - Binary mask made from selected contours.
    - num_objects - Optional parameter to limit the number of objects that will get annotated, default `num_objects=100`).

- **Context:**
    - Used to annotate object sizes in a binary mask. This visualization aims to streamline the workflow building process, 
    especially while deciding the `size` threshold for a [fill](fill.md) step.  
- **Example use:**
    - Below

**Original image:**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_rgb.png)

**Binary mask:**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_bin.png)


```python

from plantcv import plantcv as pcv

pcv.params.debug='plot'

plotting_img = pcv.visualize.sizes(img=rgb_img, mask=mask, num_objects=100)

```

**Output Visualization**

![Screenshot](img/documentation_images/visualize_overlay_two_imgs/overlay_result.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/visualize/sizes.py)
