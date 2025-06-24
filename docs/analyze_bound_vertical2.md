## Vertical Boundary Line Tool

Set boundary line with boundary tool, this allows the user to find the extent-x ('width')
to the right and to the left as well as the area to the right and to the left of the set boundary line. This tool functions 
best if the pot size/position of the plant remains relatively constant.
 
**plantcv.analyze_bound_vertical**(*img, labeled_mask, line_position, n_labels=1, label=None*)

**returns** image with boundary data

- **Parameters:**
    - img - RGB or grayscale image data for plotting
    - labeled_mask - Labeled mask of objects (32-bit).
    - line_position - position of boundary line (a value of 0 would draw the line through the left of the image)
    - n_labels - Total number expected individual objects (default = 1).
    - label - Optional label parameter, modifies the variable name of observations recorded. Can be a prefix or list (default = pcv.params.sample_label).
- **Context:**
    - Used to define a boundary line for the image, to find the width to the right and to the left as well as area to the
    right and to the left of a boundary line.
- **Example use:**
    - [Use of horizontal companion tool in In VIS Tutorial](https://plantcv.org/tutorials/single-plant-rgb-workflow)
- **Output data stored:** Data ('vertical_reference_position', 'width_left_reference', 'width_right_reference',
'area_left_reference', 'percent_area_left_reference', 'area_right_reference', 'percent_area_right_reference') automatically
gets stored to the [`Outputs` class](outputs.md) when this function is ran. Width and area type measurements can be scaled to real world units (e.g. cm and cm^2) using the `unit`, `px_height`, and `px_width` [parameters](params.md). These data can always get accessed during a
workflow (example below). For more detail about data output see
[Summary of Output Observations](output_measurements.md#summary-of-output-observations)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Set Boundary Line    
boundary_image = pcv.analyze.bound_vertical(img=img, labeled_mask=bin_mask, line_position=1000, n_labels=1)

# Access data stored out from analyze_bound_vertical
area_right_reference = pcv.outputs.observations['plant_1']['area_right_reference']['value']

```

**Boundary tool output image (x = 1000)**

![Screenshot](img/documentation_images/analyze_bound_vertical/1_boundary_on_img1000.jpg)

Boundary line set at 1000, purple line is boundary line, blue line is extent x right of the boundary line, 
green is area right of boundary line. Green line is extent x left of the boundary line and red is area left
of the boundary line.

**Boundary tool output image (x = 1100)**

![Screenshot](img/documentation_images/analyze_bound_vertical/1_boundary_on_img1100.jpg)

Boundary line set at 1100, purple is boundary line, blue line is extent x right of the boundary line, 
green is area right of boundary line. Green line is extent x left of the boundary line and red is area left
of the boundary line.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/analyze/bound_vertical.py)
