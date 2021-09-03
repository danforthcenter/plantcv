## Interactive Polygon ROI 

Using [Jupyter Notebooks](jupyter.md) it is possible to interactively collect coordinates for the [`pcv.roi.custom`](roi_custom.md) function by clicking on
the plotted image.   

**plantcv.roi.CustomROI**(*img, figsize=(12, 6)*)

**returns** interactive image class

- **Parameters:**
    - img - Image data 
    - figsize - Interactive plot figure size (default = (12,6)) 
    
- **Context:**
    - Used to define coordinates for custom polygon region(s) of interest. Output of this function works upstream of the 
- **Example use:**
    - Below
    

```python
from plantcv import plantcv as pcv

# Create an instance of the Custom ROI class 
marker = pcv.roi.CustomROI(img=img, figsize=(12,6))

# Click on the plotted image to collect coordinates 

# Use the identified coordinates to create a custom polygon ROI 
roi_contour, roi_hierarchy = pcv.roi.custom(img=img, vertices = marker.points)

```

**Selecting Coordinates**

![screen-gif](img/documentation_images/interactive_roi/custom_roi.gif)

**Resulting ROI**

![Screenshot](img/documentation_images/interactive_roi/custom_roi.jpg)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/roi/roi_methods.py)
