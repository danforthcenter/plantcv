## Create a circular Region of Interest (ROI)

**plantcv.roi.circle**(*x, y, r, img*)

**returns** roi_contour, roi_hierarchy

- **Parameters:**
    - x - The x-coordinate of the center of the circle.
    - y - The y-coordinate of the center of the circle.
    - r - The radius of the circle.
    - img - An RGB or grayscale image to plot the ROI on in debug mode.
- **Context:**
    - Used to define a region of interest in the image.

**Reference Image**

![Screenshot](img/documentation_images/circle/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

roi_contour, roi_hierarchy = pcv.roi.circle(x=200, y=225, r=75, img=rgb_img)
```

![Screenshot](img/documentation_images/circle/image_with_roi.jpg)
