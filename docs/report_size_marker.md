## Report Size Marker

Get and record the size of a size marker or set an area as a size marker.

**plantcv.report_size_marker**(*img, shape, marker='define', x_adj=0, y_adj=0, w_adj=0, h_adj=0,
                            base='white', objcolor='dark', thresh_channel=None, thresh=None, filename=False*)

**returns** marker_header,marker_data,analysis_images

- **Parameters:**
    - img             = image object (most likely the original), color(RGB)
    - shape           = 'rectangle', 'circle', 'ellipse'
    - marker          = define or detect, if define it means you set an area, if detect it means you want to detect within an area
    - x_adj           = x position of shape, integer
    - y_adj           = y position of shape, integer
    - w_adj           = width
    - h_adj           = height
    - base            = background color 'white' is default
    - objcolor        = object color is 'dark' or 'light'
    - thresh_channel  = 'h', 's','v'
    - thresh          = integer value
    - filename        = name of file
    
- **Context:**
    - Allows user to add size marker data, so that shape data can be normalized between images/cameras

**Output Data Units:**
    - Marker-Area - area of marker, pixels (units)
    - Marker Bounding Ellipse Major Axis - length of major axis of bounding ellipse, pixels (units)  
    - Marker Bounding Ellipse Minor Axis - length of minor axis of bounding ellipse, pixels (units)  
    - Marker Bounding Ellipse Eccentricity - ratio, 'roundness' of object (a perfect circle is 0, ellipse is greater than 0 but less than 1)  

**Object (green) that is identified as partially inside ROI**

![Screenshot](img/documentation_images/report_size_marker/seed-image.jpg)


```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Detect and Measure Size Marker
marker_header,marker_data,images = pcv.report_size_marker_area(img1, 'rectangle', marker='detect', x_adj=3500, y_adj=600, w_adj=-100, h_adj=-1500, base='white', objcolor='light', thresh_channel='s', thresh=120, filename=False)
```

**Area selected to detect size markers**

![Screenshot](img/documentation_images/report_size_marker/15_marker_roi.jpg)

**Object (green) that is identified as size marker**

![Screenshot](img/documentation_images/report_size_marker/21_marker_shape.jpg)