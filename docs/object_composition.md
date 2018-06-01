## Combine Objects

Combine objects together for downstream analysis, usually done after object filtering.

**object_composition**(*img, contours, hierarchy, device, debug=None*)

**returns** device, grouped object, image mask

- **Parameters:**
    - contours- object list
    - device- device number. Used to count steps in the pipeline
    - debug - None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - This function combines objects together. This is important for downstream analysis of shape characteristics, if plant objects are not combined then one plant can appear to be many different objects.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

**Original image**

![Screenshot](img/documentation_images/object_composition/original_image.jpg)

**Highlighted contours**

![Screenshot](img/documentation_images/object_composition/contours.jpg)

```python
from plantcv import plantcv as pcv

# Combine objects so downstream analysis can be run on a single plant object
device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy, device, debug="print")
```

**Combined contours**

![Screenshot](img/documentation_images/object_composition/combined.jpg)
