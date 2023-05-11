## Create labeled mask

Create a labeled mask for analyzing multiple objects in the same image

**plantcv.create_labels**(*mask, rois=None, roi_type="partial"*)

**returns** labeled mask, number of objects

- **Parameters:**
    - mask - Binary mask
    - rois - Objects class instance, typically output from [`pcv.roi.multi`](roi_multi.md) or [`pcv.roi.auto_grid`](roi_auto_grid.md), or `None` (default) in the case where each blob is to be treated as a separate object
    - roi_type - 'partial' (for partially inside, default), 'cutto' (hard cut off at ROI boundary), or 'largest' (keep only the largest contour). Will get ignored if `rois=None`. 
- **Context:**
    - Used to identify and separate multiple objects from a binary mask for downstream analysis. Such as grid of pots or seed scatter images. In the case of single plant and singular Region of Interest, see [`pcv.roi.filter`](roi_filter.md). 


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Label grid of seeds using ROIs
grid_rois = pcv.roi.multi(img=img, coord=(31,31), radius=20, spacing=(67, 67), nrows=4, ncols=7)
labeled_mask, num_seeds = pcv.create_labels(mask=clean_mask, rois=grid_rois, roi_type="partial")

# Don't use ROIs but instead assume one "object of interest" per contour
labeled_mask2, num_seeds2 = pcv.create_labels(mask=clean_mask)

```

**Debug Labeled Image**

![Screenshot](img/documentation_images/create_labels/colorful_labels.jpg)


**Output Mask Image**

![Screenshot](img/documentation_images/create_labels/grayscale_labeled_mask.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/create_labels.py)
