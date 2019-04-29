## Check for Cycles

Check for cycles within a skeletonized image. 

**plantcv.morphology.check_cycles**(*skel_img*)

**returns** cycle data headers, cycle data values, debugging cycle image

- **Parameters:**
    - skel_img - Skeleton image (output from [plantcv.morphology.skeletonize](skeletonize.md))
- **Context:**
    - Identifies cycles in a skeleton image

**Reference Image**
 
![Screenshot](img/documentation_images/check_cycles/skeleton.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# The cycle_img created for debugging purposes allows for line thickness 
# adjustments with the global line thickness parameter. Try setting 
# pcv.params.line_thickness = 8 for thicker lines (default 5)
cycle_header, cycle_data, cycle_img = pcv.morphology.check_cycles(skel_img=skeleton)

```

![Screenshot](img/documentation_images/check_cycles/plot_cycles.jpg)
