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
    - label           =  Optional label parameter, modifies the variable name of observations recorded. (default = `pcv.params.sample_label`) In PlantCV v4.9 and later, the 'label' parameter is no longer utilized, since size marker is now metadata.
- **Context:**
    - Allows user to add size marker data, so that shape data can be normalized between images/cameras
- **Output metadata stored:** Data ('marker_area', 'marker_ellipse_major_axis', 'marker_ellipse_minor_axis', 'marker_ellipse_eccentricity') 
    automatically gets stored to the 
    [`Outputs` class](outputs.md) when this function is ran. 
    These data can always get accessed during a workflow (example below). These measurements can be used with known size of the marker and the `unit`, `px_height`, and `px_width` [parameters](params.md) to scale length and area outputs to real world units (e.g. mm and mm<sup>2</sup>). [Summary of Output Observations](output_measurements.md#summary-of-output-observations)

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
marker_area = pcv.outputs.metadata['marker_area']['value']

# Scale length & area Outputs collected downstream by
# updating size scaling parameters if the marker is detected
if image: # function returns None if no marker detected
    pcv.params.unit = "cm"
# E.G. Given a square size marker, (3cm x 3cm) in size
if image: # function returns None if no marker detected
    pcv.params.px_width = 3 / marker_area**(1/2) 
    pcv.params.px_height = 3 / marker_area**(1/2)
# E.G. Given a circular size marker, 2cm in Diameter 
# by averaging ellipse axis lengths detetcted
marker_diameter_cm = 2
if image: # function returns None if no marker detected
    marker_diameter_px = (pcv.outputs.metadata['marker_ellipse_major_axis']['value'] + \
        pcv.outputs.metadata['marker_ellipse_minor_axis']['value']) / 2 
    pcv.params.px_width = marker_diameter_cm / marker_diameter_px
    pcv.params.px_height = marker_diameter_cm / marker_diameter_px

```

**Area selected to detect size markers**

![Screenshot](img/documentation_images/report_size_marker/15_marker_roi.jpg)

**Object (green) that is identified as size marker**

![Screenshot](img/documentation_images/report_size_marker/21_marker_shape.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/report_size_marker_area.py)
