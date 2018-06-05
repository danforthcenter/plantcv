## Find Objects within a Region of Interest

Find objects within a region of interest, either cut those objects to the region of interest 
or include objects that overlap with the region of interest.

**roi_objects**(*img, roi_type, roi_contour, roi_hierarchy, object_contour, obj_hierarchy, device, debug=None*)

**returns** device, kept objects, object hierarchy, object mask, object area

**Important Note:** If your ROI object detection does not perform first check that the ROI is 
completely within the image.

- **Parameters:**
    - img = img to display kept objects
    - roi_type = 'cutto' or 'partial' (include objects that are partially inside or overlapping with ROI)
    - roi_contour = contour of roi, output from "define_roi" function
    - roi_hierarchy = contour of roi, output from "define_roi" function
    - object_contour = contours of objects, output from "find_objects" function 
    - obj_hierarchy = hierarchy of objects, output from "find_objects" function
    - device = device number.  Used to count steps in the pipeline
    - device = Counter for image processing steps
    - debug = None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to find objects within a region of interest and decide which ones to keep.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 

```python
from plantcv import plantcv as pcv

# ROI objects allows the user to define if objects partially inside ROI are included or if objects are cut to ROI.
device, roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img, 'partial', roi, roi_hierarchy, objects, obj_hierarchy, device, debug="print")
```

**Object (green) that is identified as partially inside ROI**

![Screenshot](img/documentation_images/roi_objects/obj_on_img1.jpg)

**Mask of identified object**

![Screenshot](img/documentation_images/roi_objects/mask1.jpg)

**Kept objects**

![Screenshot](img/documentation_images/roi_objects/kept_objects1.jpg)

```python
from plantcv import plantcv as pcv

# Define region of interest in an image, there is a futher function 'ROI Objects' that allows the user to define if you want to include objects partially inside ROI or if you want to do cut objects to ROI.
device, roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img, 'cutto', roi, roi_hierarchy, objects, obj_hierarchy, device, debug="print")
```

**Object (green) that is cut to the ROI**

![Screenshot](img/documentation_images/roi_objects/obj_on_img2.jpg)

**Mask of identified object**

![Screenshot](img/documentation_images/roi_objects/mask2.jpg)

**Kept objects**

![Screenshot](img/documentation_images/roi_objects/kept_objects2.jpg)
