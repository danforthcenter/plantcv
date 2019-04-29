## Measure Euclidean Distance of Segments  

Measure Euclidean distance of segments.

**plantcv.morphology.segment_euclidean_length**(*segmented_img, objects, hierarchies*)

**returns** euclidean length data headers, euclidean length data values, labeled image 

- **Parameters:**
    - segmented_img - Segmented image (output either from [plantcv.morphology.segment_skeleton](segment_skeleton.md)
    or [plantcv.morphology.segment_id](segment_id.md)), used for creating the labeled image. 
    - objects - Segment objects (output from either [plantcv.morphology.segment_skeleton](segment_skeleton.md) or
    [plantcv.morphology.segment_sort](segment_sort.md)).
    - hierarchies - Hierarchies of segment objects (output from either [plantcv.morphology.segment_sort](segment_skeleton.md) or
    [plantcv.morphology.segment_sort](segment_sort.md)).
- **Context:**
    - Calculates the euclidean distance of each segment. Users can pass only 
    leaf objects (returned from [plantcv.morphology.segment_sort](segment_sort.md)) to only collect lengths of leaves.

**Reference Image:** segmented_img

![Screenshot](img/documentation_images/segment_euclidean_length/segmented_img_mask.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

eu_header, eu_lengths, labeled_img = pcv.morphology.segment_euclidean_length(segmented_img=segmented_img, 
                                                                             objects=obj,
                                                                             hierarchies=hier)

```

*Labeled Image*

![Screenshot](img/documentation_images/segment_euclidean_length/labeled_eu_lengths.jpg)
