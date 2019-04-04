## Find Endpoints/Tips

**plantcv.morphology.*find_tips*(*skel_img*)

**returns** Binary mask of endpoints 

- **Parameters:**
    - skel_img - Skeleton image (output from [plantcv.morphology.skeletonize](morph_skeletonize.md))
- **Context:**
    - Identifies endpoints/tips in a skeleton image

**Reference Image**

![Screenshot](img/documentation_images/find_tips/skel_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

tips_img = pcv.morphology.find_tips(skel_img=skeleton)

# Adjust line thickness with the global line thickness parameter (default = 5)
pcv.params.line_thickness = 8
tips_img2 = pcv.morphology.find_tips(skel_img=skeleton)

```
*Default Thickness (5)*

![Screenshot](img/documentation_images/find_tips/tip_image.jpg)

*pcv.params.line_thickness = 8*

![Screenshot](img/documentation_images/find_tips/thick_tip_img.jpg)
