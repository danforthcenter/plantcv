## Find Endpoints/Tips

Find endpoints of a skeletonized image.

**plantcv.morphology.find_tips**(*skel_img, mask=None, label=None*)

**returns** Binary mask of endpoints 

- **Parameters:**
    - skel_img - Skeleton image (output from [plantcv.morphology.skeletonize](skeletonize.md))
    - mask     - Binary mask used for debugging (optional). If provided the debug image will be overlaid on the mask.
    - label    - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
    
- **Context:**
    - Identifies endpoints/tips in a skeleton image
    
- **Output data stored:** Data ('tips') 
    automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    All data stored in the Outputs class gets printed out while running [pcv.outputs.save_results](outputs.md) but
    these data can always get accessed during a workflow. For more detail about data output see 
    [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Skeleton Image**

![Screenshot](img/documentation_images/find_tips/skeleton_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Adjust line thickness with the global line thickness parameter (default = 5),
# and provide binary mask of the plant for debugging. NOTE: the image returned
# will be exactly the same, but the debugging image will look different. 
pcv.params.line_thickness = 3

tips_img = pcv.morphology.find_tips(skel_img=skeleton)
tips_img = pcv.morphology.find_tips(skel_img=skeleton, mask=plant_mask, label=rep1)


```

*Tip Points Image (image getting returned)*

![Screenshot](img/documentation_images/find_tips/tip_pts.jpg)

*Debug Image without Mask*

![Screenshot](img/documentation_images/find_tips/tips_debug.jpg)

*Debug Image with Mask*

![Screenshot](img/documentation_images/find_tips/tips_debug_mask.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/morphology/find_tips.py)
