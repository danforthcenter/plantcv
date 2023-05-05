## Create labeled mask

Create a labeled mask for analyzing multiple objects in the same image

**plantcv.create_labels**(*mask, rois, roi_type="partial"*)

**returns** labeled mask, number of objects

- **Parameters:**
    - mask - Binary mask
    - rois - Objects class instance, typically output from `pcv.roi.multi` or `pcv.roi.auto_grid`, or `None` in the case 
    - roi_type - 'partial' (for partially inside, default), 'cutto' (hard cut off at ROI boundary), 'largest' (keep only the largest contour), or 'auto' (use the mask alone withtout roi filtering)
    - h - Height 
    - w - Width
- **Context:**
    - Used to identify and separate multiple objects from a binary mask for downstream analysis. Such as grid of pots or seed scatter images.
    

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Crop image
labeled_mask, num_seeds = pcv.create_labels(mask=clean_mask, rois=grid_rois, roi_type="partial")

```

**Debug Labeled Image**

![Screenshot](img/documentation_images/ .jpg)


**Output Mask Image**

![Screenshot](img/documentation_images/ .jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/crop.py)
