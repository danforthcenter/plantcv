## Scale features

This is a function to to transform the coordiantes of landmark points onto a common scale (0-1.0)
Scaling is used to remove the influence of size on shape parameters. Returns a list of tuples.

**scale_features**(*obj, mask, points, boundary_line, device, debug=None*)

**returns** device, rescaled landmark points, a rescaled centroid point, a rescaled baseline point

- **Parameters:**
    - obj - A contour of the plant object (this should be output from the object_composition.py fxn)
    - mask - This is a binary image. The object should be white and the background should be black
    - points - A set of landmark points to be rescaled given the centroid of the object
    - boundary_line - A vertical coordinate that denotes the height of the plant pot, the coordinates of this reference point is also rescaled
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to rescale the point coordinates of landmark points, including centroid and boundary line
    
**Input contour of plant object, an mask that denotes plant outline and landmark points**

![Screenshot](img/documentation_images/scale_features/av_output.jpg)

```python
from plantcv import plantcv as pcv

device = 1

# Identify acute vertices (tip points) of an object
# Results in set of point values that may indicate tip points
device, points_rescaled, centroid_rescaled, bottomline_rescaled = pcv.scale_features(obj, mask, landmark_points, boundary_line, debug='print')
```

**Image of rescaled points in white, centroid is in gold and centroid at pot base is in blue**

![Screenshot](img/documentation_images/scale_features/sf_output.jpg)
