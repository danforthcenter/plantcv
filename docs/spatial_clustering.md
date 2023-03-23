## Spatial Clustering

Segment features of images based on their distance to each other.

**plantcv.spatial_clustering**(*mask, algorithm="DBSCAN", min_cluster_size=5, max_distance=None*)

**returns** image showing all clusters colorized, individual masks for each cluster.

- **Parameters:**
    - mask - Mask/binary image to segment into clusters.
    - algorithm - Algorithm to use to segregate feature in image.  Currently, "DBSCAN" and "OPTICS" are supported.  
    "OPTICS" is slower but has better resolution for smaller objects, and "DBSCAN" is faster and useful for larger 
    features in the image (like separating two plants from each other).
    - min_cluster_size - The minimum size an feature of the image must be (in pixels) before it can be considered its 
    own cluster.
    - max_distance - The maximum distance between two pixels before they can be considered a part of the same cluster.  
    When using "DBSCAN," this value must be between 0 and 1.  When using "OPTICS," the value is the pixels and depends 
    on the size of your image. 

- **Context:**
    - This function automatically separates multiple features in an image into separate masks.  These masks can be 
    used for downstream analyses. 

**Original image**

![Screenshot](img/documentation_images/spatial_clustering/13_roi_mask.png)

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

clust_img, clust_masks = pcv.spatial_clustering(mask=mask, algorithm="DBSCAN", min_cluster_size=5, max_distance=None)

```

**Highlighted contours**

![Screenshot](img/documentation_images/spatial_clustering/Full_Image_Mask.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/spatial_clustering.py)
