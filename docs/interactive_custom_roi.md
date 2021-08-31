## Interactive Polygon ROI 

Using [Jupyter Notebooks](jupyter.md) it is possible to interactively collect coordinates for the [`pcv.roi.custom`](roi_custom.md) function by clicking on
the plotted image.   

**plantcv.CustomROI**(*img, figsize=(12, 6)*)

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

# 

```

**Combined image**

![Screenshot](img/documentation_images/interactive/joined.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/roi/roi_methods.py)
