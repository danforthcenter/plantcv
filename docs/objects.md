## class Objects

A PlantCV data object class.

*class* plantcv.**Objects**

`Objects` is a class that is used to manage image contours/objects and their hierarchical relationships. 
These attributes are used internally by PlantCV functions but also can be utilized by users. 

### Attributes

Attributes are accessed as Objects.*attribute*.

**contours**: A list of contours (all the points that form the outline of a shape. Based on [OpenCV contours](https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html))

**hierarchy**: A list of hierarchies (An array that contains the relationship between contours. Based on [OpenCV hierarchies](https://docs.opencv.org/4.x/d9/d8b/tutorial_py_contours_hierarchy.html))

### Methods

**save**(self, *filename*): Save objects to a file.

**load**(*filename*): Load objects from a file.

**append**(*contour, h*): Append a contour and hierarchy to the Objects instance.

### Example

PlantCV functions from the roi sub-package use `Objects` implicitly.

```python
from plantcv import plantcv as pcv

# Make a grid of ROIs 
roi_objects = pcv.roi.multi(img=img1, coord=(25,120), radius=20, 
                                      spacing=(70, 70), nrows=3, ncols=6)

roi_objects.save(filename="test.npz")

roi_object_copy = Objects.load(filename="test.npz")
```


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/classes.py)
