## Vertical Boundary Line Tool

Set boundary line with boundary tool, this allows the user to find the extent-x ('width')
to the right and to the left as well as the area to the right and to the left of the set boundary line. This tool functions 
best if the pot size/position of the plant remains relatively constant.
 
**plantcv.analyze_bound_vertical**(*img, obj, mask, line_position*)

**returns** images with boundary data

- **Parameters:**
    - img - RGB or grayscale image data for plotting
    - obj - single or grouped contour object
    - mask - binary mask of selected contours
    - line_position = position of boundary line (a value of 0 would draw the line through the left of the image)
- **Context:**
    - Used to define a boundary line for the image, to find the width to the right and to the left as well as area to the right and to the left of a boundary line.
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Example use:**
    - [Use of horizontal companion tool in In VIS Tutorial](vis_tutorial.md)
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Set Boundary Line    
boundary_images = pcv.analyze_bound_vertical(img, obj, mask, 1000)

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
