## Cluster Contours

This function take a image with multiple contours and clusters them based on user input of rows and columns

**cluster_contours**(*device,img, roi_objects, nrow=1,ncol=1,debug=None*)

**returns** device, grouped_contour_indexes, contours

- **Parameters:**
    - device- Counter for image processing steps
    - img = image object to be masked
    - roi_objects= object contours in an image that are needed to be clustered.
    - nrow= approximate number of rows
    - ncol= approximate number of columns
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Cluster contours based on number of approximate rows and columns
- **Example use:**
    - [Use In Multi-Plant Tutorial](multi-plant_tutorial.md)
    

**ROI Objects Output**

![Screenshot](img/documentation_images/cluster_contour/13_roi_mask.jpg)

```python
import plantcv as pcv

# clusters them based on user input of rows and columns
device, clusters_i, contours = pcv.cluster_contours(device, img, roi_objects, 4, 6, debug="print")
```

**Cluster Contour Image**

![Screenshot](img/documentation_images/cluster_contour/14_clusters.jpg)

