## Filter a Mask using a Region of Interest with Connected Components

Filter connected regions of non-zero pixels within a region of interest. This function is similar to
[plantcv.roi.filter](roi_filter.md) and [plantcv.roi.quick_filter](roi_quick_filter.md), but uses OpenCV connected
components for a stripped down, faster ROI filtering path.

**plantcv.roi.fast_filter**(*mask, roi, roi_type="partial"*)

**returns** filtered_mask

- **Parameters:**
    - mask = binary image data to be filtered
    - roi = region of interest, an instance of the Objects class, output from one of the pcv.roi subpackage functions
    - roi_type = 'partial' (for partially inside, default), 'cutto' (cut objects to the inside of the ROI),
    'within' (keep only objects fully inside ROI), or 'largest' (keep only the largest object overlapping the ROI)

- **Context:**
    - Used to quickly keep objects inside one or more ROIs without the full contour filtering workflow.

- **Example use:**
    - Below

**RGB image**

![Screenshot](img/documentation_images/roi_filter/rgb_img.png)

**Thresholded image (mask)**

![Screenshot](img/documentation_images/roi_filter/bin_img.png)

**ROI visualization**

![Screenshot](img/documentation_images/roi_filter/roi_img.png)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# ROI filter keeps objects that are partially inside ROI
filtered_mask = pcv.roi.fast_filter(mask=mask, roi=roi)

```

**Filtered mask**

![Screenshot](img/documentation_images/roi_filter/mask_partial.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/roi/fast_filter.py)
