## Create an elliptical Region of Interest (ROI)

**plantcv.roi.ellipse**(*img, x, y, r1, r2, angle*)

**returns** roi

- **Parameters:**
    - img - An RGB or grayscale image to plot the ROI on in debug mode.
    - x - The x-coordinate of the center of the ellipse.
    - y - The y-coordinate of the center of the ellipse.
    - r1 - The radius of the minor axis.
    - r2 - The radius of the major axis.
    - angle - The angle of rotation in degrees of the major axis.
- **Context:**
    - Used to define a region of interest in the image.

**Reference Image**

![Screenshot](img/documentation_images/ellipse/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

roi = pcv.roi.ellipse(img=rgb_img, x=200, y=200, r1=100, r2=80, angle=0)

```

![Screenshot](img/documentation_images/ellipse/image_with_roi.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/roi/roi_methods.py)
