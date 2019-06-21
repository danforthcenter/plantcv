## Analyze Shape Characteristics of Object

Shape analysis outputs numeric properties for an input object (contour or grouped contours), works best on grouped contours.
 
**plantcv.analyze_object**(*img, obj, mask*)

**returns** analysis_image

- **Parameters:**
    - img - RGB or grayscale image data for plotting.
    - obj - Single or grouped contour object.
    - mask - Binary image to use as mask for moments analysis.
- **Context:**
    - Used to output shape characteristics of an image, including height, object area, convex hull, convex hull area, 
    perimeter, extent x, extent y, longest axis, centroid x coordinate, centroid y coordinate, in bounds QC (if object 
    touches edge of image, image is flagged). 
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)
    - [Use In NIR Tutorial](nir_tutorial.md)
    - [Use In PSII Tutorial](psII_tutorial.md) 
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)
    
**Original image**

![Screenshot](img/documentation_images/analyze_shape/original_image.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)

pcv.params.debug = "print"

# Characterize object shapes
    
shape_image = pcv.analyze_object(img, objects, mask)

# Save returned images with more specific naming
pcv.print_image(shape_image, '/home/malia/setaria_shape_img.png')

```

**Image with identified objects**

![Screenshot](img/documentation_images/analyze_shape/objects_on_image.jpg)

**Image with shape characteristics**

![Screenshot](img/documentation_images/analyze_shape/shapes_on_image.jpg)
