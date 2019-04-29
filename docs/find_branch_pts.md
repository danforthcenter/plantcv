## Find Branch/Junction Points 

**plantcv.morphology.*find_branch_pts*(*skel_img, mask=None*)

**returns** Binary mask of branch points 

- **Parameters:**
    - skel_img - Skeleton image (output from [plantcv.morphology.skeletonize](skeletonize.md))
    - mask - Binary mask used for debugging (optional). If provided the debug image will be overlaid on the mask.
- **Context:**
    - Identifies branch/junction points in a skeleton image

**Skeleton Image**

![Screenshot](img/documentation_images/find_branch_pts/skeleton_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

branch_points_img = pcv.morphology.find_branch_pts(skel_img=skeleton)

# Adjust line thickness with the global line thickness parameter (default = 5),
# and provide binary mask of the plant for debugging. NOTE: the image returned
# will be exactly the same, but the debugging image will look different. 
pcv.params.line_thickness = 2

branch_points_img = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=None)
branch_points_img = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=plant_mask)

```

*Branch Points Image (image getting returned)*

![Screenshot](img/documentation_images/find_branch_pts/branch_pts.jpg)

*Debug Image without Mask*

![Screenshot](img/documentation_images/find_branch_pts/branch_pts_debug.jpg)

*Debug Image with Mask*

![Screenshot](img/documentation_images/find_branch_pts/branch_pts_debug_mask.jpg)
