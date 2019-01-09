## Combine Objects

Combine objects together for downstream analysis, usually done after object filtering.

**plantcv.object_composition**(*img, contours, hierarchy*)

**returns** grouped object, image mask

- **Parameters:**
    - img - RGB or grayscale image data for plotting
    - contours - Contour list
    - hierarchy - Contour hierarchy NumPy array
   
- **Context:**
    - This function combines objects together. This is important for downstream analysis of shape characteristics, if plant objects are not combined then one plant can appear to be many different objects.
- **Example use:**
    - [Use in VIS tutorial](vis_tutorial.md)
    - [Use in NIR tutorial](nir_tutorial.md)
    - [Use in PSII tutorial](psII_tutorial.md) 

**Original image**

![Screenshot](img/documentation_images/object_composition/original_image.jpg)

**Highlighted contours**

![Screenshot](img/documentation_images/object_composition/contours.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Combine objects so downstream analysis can be run on a single plant object
obj, mask = pcv.object_composition(img, roi_objects, hierarchy)
```

**Combined contours**

![Screenshot](img/documentation_images/object_composition/combined.jpg)
