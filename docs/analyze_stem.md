## Analyze Stem Objects

Primary, or stem, objects identified during workflows that examine the [mmorphology](morphology_tutorial.md) of 
plants or plant organs can have specific characteristics measured about the stem segments of a skeleton. These measurement

**plantcv.morphology.analyze_stem**(*img, obj, mask*)

**returns** analysis_image

- **Parameters:**
    - img - RGB or grayscale image data for plotting.
    - obj - Single or grouped contour object.
    - mask - Binary image to use as mask for moments analysis.
- **Context:**
    - Used to output shape characteristics of an image, including height, object area, convex hull, convex hull area, 
    perimeter, extent x, extent y, longest axis, centroid x coordinate, centroid y coordinate, in bounds QC (if object 
    touches edge of image, image is flagged). 
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)


- **Output data stored:** Data ('stem_angle', 'stem_height', and 'stem_length') 
    automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow. For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)