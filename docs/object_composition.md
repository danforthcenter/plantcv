## Combine Objects

Combine objects together for downstream analysis, usually done after object filtering.

**plantcv.object_composition**(*img, objs*)

**returns** grouped object, image mask

- **Parameters:**
    - img - RGB or grayscale image data for plotting
    - objs - an Objects instance with a contour list and hierarchy NumPy array
   
- **Context:**
    - This function combines objects together. This is important for downstream analysis of shape characteristics, if plant objects are not combined then one plant can appear to be many different objects.
- **Example use:**
    - [Use in VIS tutorial](tutorials/vis_tutorial.md)
    - [Use in NIR tutorial](tutorials/nir_tutorial.md)
    - [Use in PSII tutorial](tutorials/psII_tutorial.md)

**Original image**

![Screenshot](img/documentation_images/object_composition/original_image.jpg)

**Highlighted contours**

![Screenshot](img/documentation_images/object_composition/contours.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Combine objects so downstream analysis can be run on a single plant object
obj, mask = pcv.object_composition(img, objs)

```

**Combined contours**

![Screenshot](img/documentation_images/object_composition/combined.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/object_composition.py)
