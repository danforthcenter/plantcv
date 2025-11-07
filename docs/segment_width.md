## Measure Width of Segments 

Measure the average width of segments. 

**plantcv.morphology.segment_width**(*segmented_img, skel_img, labeled_mask, n_labels=1, label=None*)

**returns** labeled_image  

- **Parameters:**
    - segmented_img - Segmented image (output either from [plantcv.morphology.segment_skeleton](segment_skeleton.md)
    or [plantcv.morphology.segment_id](segment_id.md)), used for creating the labeled image. 
    - Skeleton image (output from [plantcv.morphology.skeletonize](skeletonize.md) or output from [plantcv.morphology.prune](prune.md))
    - labeled_mask - Labeled mask of segments/objects to get analyzes (output from [plantcv.morphology.fill_segments](fill_segments.md),  [`pcv.create_labels`](create_labels.md), or [`pcv.roi.filter`](roi_filter.md))
    - label         - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Context:**
    - Calculates the geodesic distance of each segment. Users can pass only 
    leaf objects (returned from [plantcv.morphology.segment_sort](segment_sort.md)) to only collect lengths of leaves only.
- **Output data stored:** Data ('segment_path_length') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. Length type measurements can be scaled to real world units (e.g. cm and cm^2) using the `unit`, `px_height`, and `px_width` [parameters](params.md).
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Reference Image:** segmented_img 

![Screenshot](img/documentation_images/segment_path_length/segmented_img_mask.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

labeled_img = pcv.morphology.segment_path_length(segmented_img=segmented_img, objects=obj)

# Access data stored out from segment_path_length
path_lengths = pcv.outputs.observations['plant']['segment_path_length']['value']

```

*Labeled Image*

![Screenshot](img/documentation_images/segment_path_length/labeled_path_lengths.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/morphology/segment_path_length.py)
