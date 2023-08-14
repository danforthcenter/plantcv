## Measure Segment Angles

Measure angles of segments. 

**plantcv.morphology.segment_angle**(*segmented_img, objects, label=None*)

**returns** labeled image   

- **Parameters:**
    - segmented_img - Segmented image (output either from [plantcv.morphology.segment_skeleton](segment_skeleton.md)
    or [plantcv.morphology.segment_id](segment_id.md)), used for creating the labeled image. 
    - objects - Segment objects (output from either [plantcv.morphology.segment_skeleton](segment_skeleton.md), or
    [plantcv.morphology.segment_sort](segment_sort.md)).
    - label         - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Context:**
    - Calculates angles of segments (in degrees) by fitting a linear regression line to each segment. Users can pass only 
    leaf objects (returned from [plantcv.morphology.segment_sort](segment_sort.md)) to only collect angles of leaves. 
- **Output data stored:** Data ('segment_angle') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Reference Image:** segmented_img 

![Screenshot](img/documentation_images/segment_angle/segmented_img_mask.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

labeled_img = pcv.morphology.segment_angle(segmented_img=segmented_img, objects=obj)

# Access data stored out from segment_angle
segment_angles = pcv.outputs.observations['plant']['segment_angle']['value']

```

*Labeled Image*

![Screenshot](img/documentation_images/segment_angle/labeled_angles.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/morphology/segment_angle.py)
