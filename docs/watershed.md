## Watershed Segmentation

This function is based on code contributed by Suxing Liu, Arkansas State University.
For more information see [https://github.com/lsx1980/Leaf_count](https://github.com/lsx1980/Leaf_count).
This function uses the watershed algorithm to detect boundary of objects.
Needs a mask file which specifies area which is object is white, and background is black.

**plantcv.watershed_segmentation**(*rgb_img, mask, distance=10, label=None*)

**returns** labeled mask

- **Parameters:**
    - rgb_img - RGB image data
    - mask - Binary image, single channel, object in white and background black
    - distance - Minimum distance of local maximum, lower values are more sensitive, and segments more objects (default: 10)
    - label - Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Context:**
    - Used to segment image into parts
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.outputs.save_results](outputs.md) which saves all stored data to a .json file.
- **Output data stored:** Data ('estimated_object_count') automatically gets stored to the [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). For more detail about data output see [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Original image**

![Screenshot](img/documentation_images/watershed/cropped.jpg)

**Object mask**

![Screenshot](img/documentation_images/watershed/mask.jpg)

```python

import numpy as np
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "plant"

# Segment image with watershed function
labels = pcv.watershed_segmentation(rgb_img=crop_img, mask=bin_mask, distance=10)

# Utilize the labeled mask, n_labels -1 since we don't want to analyze background  
shape_img = pcv.analyze.size(img=crop_img, labeled_mask=labels, n_labels=np.unique(labels)-1)

```

**Watershed Segmentation**

![Screenshot](img/documentation_images/watershed/watershed.jpg)

**Downstream analysis e.g. `analyze.size`** 

![Screenshot](img/documentation_images/watershed/watershed_shape_measure.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/watershed.py)
