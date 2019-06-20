## Report Size Marker

Get and record the size of a size marker or set an area as a size marker.

**plantcv.report_size_marker_area**(*img, roi_contour, roi_hierarchy, marker='define', objcolor='dark', thresh_channel=None,
                            thresh=None*)

**returns** analysis_image

- **Parameters:**
    - img             = An RGB or grayscale image to plot the marker object on
    - roi_contour     = A region of interest contour (e.g. output from [pcv.roi.rectangle](roi_rectangle.md) or other methods)
    - roi_hierarchy   = A region of interest contour hierarchy (e.g. output from pcv.roi.rectangle or other methods)
    - marker          = 'define' (default) or 'detect'. If 'define' it means you set an area, if 'detect' it means you want to
                         detect within an area
    - objcolor        = Object color is 'dark' (default) or 'light' (is the marker darker or lighter than the background)
    - thresh_channel  = 'h', 's', or 'v' for hue, saturation or value, default set to None
    - thresh          = Binary threshold value (integer), default set to None.
- **Context:**
    - Allows user to add size marker data, so that shape data can be normalized between images/cameras
    - Data automatically gets stored into the [Outputs class](outputs.md). Users can look at the data collected at any point during 
    the workflow by using [pcv.print_results](print_results.md) which prints all stored data to a .json file.
- **Output data stored:** [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Object (green) that is identified as partially inside ROI**

![Screenshot](img/documentation_images/report_size_marker/seed-image.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Define an ROI for the marker
roi_contour, roi_hierarchy = pcv.roi.rectangle(img1, 3550, 850, 500, 500)

# Detect and Measure Size Marker
image = pcv.report_size_marker_area(img1, roi_contour, roi_hierarchy, marker='detect', objcolor='light', thresh_channel='s', thresh=120)

```

**Area selected to detect size markers**

![Screenshot](img/documentation_images/report_size_marker/15_marker_roi.jpg)

**Object (green) that is identified as size marker**

![Screenshot](img/documentation_images/report_size_marker/21_marker_shape.jpg)
