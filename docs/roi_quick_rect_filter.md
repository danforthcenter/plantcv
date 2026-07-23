## Filter a Mask using a Rectangular Region

Filter objects (connected regions of non-zero pixels) within a rectangle.

**plantcv.roi.quick_rect_filter**(*mask, roi, roi_type="partial"*)

**returns** filtered_mask

- **Parameters:**
    - mask = binary image data to be filtered
    - roi = region of interest specified as a list of (x, y, w, h) tuples.
	- roi_type = 'partial' (for partially inside, default), 'cutto' (cut objects to the inside of the ROI),
	'within' (keep only objects fully inside ROI), or 'largest' (largest object partially inside ROI)

- **Context:**
    - This might not end up being front facing?

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
filtered_mask = pcv.roi.quick_filter(mask=mask, roi=roi)

```

**Filtered mask**

![Screenshot](img/documentation_images/roi_filter/mask_partial.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/roi/quick_filter.py)
