## Scale features

This is a function to to transform the coordiantes of landmark points onto a common scale (0-1.0)
Scaling is used to remove the influence of size on shape parameters. Returns a list of tuples.

**plantcv.homology.scale_features**(*mask, points, line_position*)

**returns** rescaled landmark points, a rescaled centroid point, a rescaled baseline point

- **Parameters:**
    - mask - This is a binary image. The object should be white and the background should be black
    - points - A set of landmark points to be rescaled given the centroid of the object
    - line_position - A vertical coordinate (int) that denotes the height of the plant pot, the coordinates of this reference point is also rescaled
- **Context:**
    - Used to rescale the point coordinates of landmark points, including centroid and boundary line
    
**Input contour of plant object, an mask that denotes plant outline and landmark points**

![Screenshot](img/documentation_images/scale_features/av_output.jpg)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "plot"

# Identify acute vertices (tip points) of an object
# Results in set of point values that may indicate tip points
points_rescaled, centroid_rescaled, base_rescaled = pcv.homology.scale_features(mask, landmark_points,
                                                                                boundary_line_position)
                                                                       
```

**Image of rescaled points in white, centroid is in gold and centroid at pot base is in blue**

![Screenshot](img/documentation_images/scale_features/sf_output.jpg)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/homology/scale_features.py)
