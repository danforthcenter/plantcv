## Analyze the Size and Shape Characteristics of Objects

Size and shape analysis outputs numeric properties for individual plants, seeds, leaves, etc.
 
**plantcv.analyze.size**(*img, labeled_mask, n_labels=1, label="default"*)

**returns** analysis_image

- **Parameters:**
    - img - RGB or grayscale image data for plotting.
    - labeled_mask - Labeled mask of objects (32-bit).
    - n_labels - Total number expected individual objects (default = 1).
    - label - Optional label parameter, modifies the variable name of observations recorded. (default `label="default"`)
- **Context:**
    - Used to output size and shape characteristics of individual objects (labeled regions). 
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)
    - [Use In NIR Tutorial](tutorials/nir_tutorial.md)
    - [Use In PSII Tutorial](tutorials/psII_tutorial.md)
- **Output data stored:** Data ('area', 'convex_hull_area', 'solidity', 'perimeter', 'width', 'height', 'longest_path',
'center_of_mass, 'convex_hull_vertices', 'object_in_frame', 'ellipse_center', 'ellipse_major_axis', 'ellipse_minor_axis',
'ellipse_angle', 'ellipse_eccentricity') automatically gets stored to the [`Outputs` class](outputs.md) when this function is
run. These data can be accessed during a workflow (example below). For more detail about data output see
[Summary of Output Observations](output_measurements.md#summary-of-output-observations)
    
**Original image**

![Screenshot](img/documentation_images/analyze_shape/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "plot"

# Characterize object shapes
    
shape_image = pcv.analyze.size(img=img, labeled_mask=mask, n_labels=1, label="default")

# Save returned images with more specific naming
pcv.print_image(shape_image, '/home/malia/setaria_shape_img.png')

# Access data stored out from analyze_object
plant_solidity = pcv.outputs.observations['default1']['solidity']['value']

```

**Image with identified objects**

![Screenshot](img/documentation_images/analyze_shape/objects_on_image.jpg)

**Image with shape characteristics**

![Screenshot](img/documentation_images/analyze_shape/shapes_on_image.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/analyze/size.py)