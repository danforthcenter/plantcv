## X-axis Pseudolandmarks

Divide plant object into twenty equidistant bins and assign pseudolandmark points based upon their actual (not scaled) position.
Once this data is scaled this approach may provide some information regarding shape independent of size.

**plantcv.homology.x_axis_pseudolandmarks**(*img, mask, label=None*)

**returns** landmarks_on_top (top), landmarks_on_bottom (bottom), landmarks_at_center_along_the_vertical_axis (center_V)

- **Parameters:**
    - img - RGB or grayscale image data for plotting.
    - mask - This is a binary image. The object should be white and the background should be black.
    - label - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Context:**
    - Used to identify a set of sixty equidistant landmarks on the horizontal axis. Once scaled these can be used for shape analysis.
- **Output data stored:** Data ('top_lmk', 'bottom_lmk', 'center_v_lmk') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)
**Input object contour and image**

![Screenshot](img/documentation_images/x_axis_pseudolandmarks/xpl_example_image.jpg)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Identify a set of land mark points
# Results in set of point values that may indicate tip points
top, bottom, center_v = pcv.homology.x_axis_pseudolandmarks(img=img, mask=mask)

# Access data stored out from x_axis_pseudolandmarks
bottom_landmarks = pcv.outputs.observations['plant']['bottom_lmk']['value']

```

**Image of points selected**

![Screenshot](img/documentation_images/x_axis_pseudolandmarks/xap_output.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/homology/x_axis_pseudolandmarks.py)
