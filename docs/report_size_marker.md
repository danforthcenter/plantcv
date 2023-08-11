## Report Size Marker

Get and record the size of a size marker or set an area as a size marker.

**plantcv.report_size_marker_area**(*img, roi, marker='define', objcolor='dark', thresh_channel=None,
                            thresh=None, label=None*)

**returns** analysis_image

- **Parameters:**
    - img             = An RGB or grayscale image to plot the marker object on
    - roi             = A region of interest  (e.g. output from [pcv.roi.rectangle](roi_rectangle.md) or other methods)
    - marker          = 'define' (default) or 'detect'. If 'define' it means you set an area, if 'detect' it means you want to
                         detect within an area
    - objcolor        = Object color is 'dark' (default) or 'light' (is the marker darker or lighter than the background)
    - thresh_channel  = 'h', 's', or 'v' for hue, saturation or value, default set to None
    - thresh          = Binary threshold value (integer), default set to None.
    - label           =  Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`)
- **Context:**
    - Allows user to add size marker data, so that shape data can be normalized between images/cameras
- **Output data stored:** Data ('marker_area', 'marker_ellipse_major_axis', 'marker_ellipse_minor_axis', 'marker_ellipse_eccentricity') 
    automatically gets stored to the 
    [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

**Object (green) that is identified as partially inside ROI**

![Screenshot](img/documentation_images/report_size_marker/seed-image.jpg)


```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"
# Optionally, set a sample label name
pcv.params.sample_label = "marker"

# Define an ROI for the marker
roi = pcv.roi.rectangle(img=img1, x=3550, y=850, h=500, w=500)

# Detect and Measure Size Marker
image = pcv.report_size_marker_area(img=img1, roi=roi, marker='detect', 
                                    objcolor='light', thresh_channel='s', 
                                    thresh=120)

# Access data stored out from report_size_marker_area
marker_area = pcv.outputs.observations['marker']['marker_area']['value']

```

**Area selected to detect size markers**

![Screenshot](img/documentation_images/report_size_marker/15_marker_roi.jpg)

**Object (green) that is identified as size marker**

![Screenshot](img/documentation_images/report_size_marker/21_marker_shape.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/report_size_marker_area.py)
