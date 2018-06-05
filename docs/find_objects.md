## Find Objects

Find objects within the image.

**find_objects**(*img, mask, device, debug=None*)

**returns** device, objects, object hierarchy

- **Parameters:**
    - img - image that the objects will be overlayed
    - mask - what is used for object detection
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to identify objects (plant material) in an image.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

**Original image**

![Screenshot](img/documentation_images/find_objects/original_image.jpg)

**Input binary mask**

![Screenshot](img/documentation_images/find_objects/mask.jpg)

```python
from plantcv import plantcv as pcv

# Identify objects (plant material) in an image, all objects regardless of hierarchy are filled (e.g. holes between leaves).
device, id_objects, obj_hierarchy = pcv.find_objects(img, mask, device, debug="print")
```

**Image with contours highlighted**

![Screenshot](img/documentation_images/find_objects/contours.jpg)
