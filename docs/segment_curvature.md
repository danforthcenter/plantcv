## Segment Curvature

Measure the curvature of segments.   

**plantcv.morphology.segment_curvature**(*segmented_img, objects, hierarchies*)

**returns** segment curvature headers, list of segment curvatures, labeled image 

- **Parameters:**
    - segmented_img - Segmented image (output either from [plantcv.morphology.segment_skeleton](segment_skeleton.md)
    or [plantcv.morphology.segment_id](segment_id.md)), used for creating the labeled image. 
    - objects - Segment objects (output from either [plantcv.morphology.segment_sort](segment_skeleton.md) or
    [plantcv.morphology.segment_sort](segment_sort.md)).
    - hierarchies - Hierarchies of segment objects (output from either [plantcv.morphology.segment_skeleton](segment_skeleton.md) or
    [plantcv.morphology.segment_sort](segment_sort.md)).
- **Context:**
    - Calculates curvature of segments by taking the ratio of the geodesic distance ([plantcv.morphology.segment_path_length](segment_path_length.md))
    over the euclidean distance [plantcv.morphology.segment_euclidean_length](segment_euclidean_length.md)). Measurement of two-dimensional tortuosity.
    Values closer to 1 indicate that a segment is a straight line while larger values indicate the segment has more curvature.
    Users can pass only leaf objects (returned from [plantcv.morphology.segment_sort](segment_sort.md)) to only collect curvature of leaves.

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

curve_header, segment_curvature, labeled_img = pcv.morphology.segment_curvature(segmented_img=segmented_img, 
                                                                                objects=obj,
                                                                                hierarchies=hier)
# Pass just leaf objects and hierarchies (output from pcv.morphology.segment_sort) 
curve_header2, leaf_curvature, labeled_img2 = pcv.morphology.segment_curvature(segmented_img=leaf_segmented,
                                                                               objects=leaf_obj,
                                                                               hierarchies=leaf_hier)

```

*Labeled Image*

![Screenshot](img/documentation_images/segment_curvature/labeled_curvature.jpg)

*Labeled Image (only leaves)*

![Screenshot](img/documentation_images/segment_curvature/labeled_leaf_curvature.jpg)
