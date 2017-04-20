## Landmark_reference_pt_dist

This is a function to measure the distance from user defined points to the centroid and a point defined by the centroid coordinate along the x-axis and baseline coordinate (top of pot) along the y-axis. Calculating the vertical distance between leaf tip points to the centroid of the plant object in side-view images may provide a proxy measure of turgor pressure.
 
**landmark_reference_pt_dist**(*points_rescaled, centroid_rescaled, baseline_rescaled, device, debug=None*)

**returns** device, ave_vertical_distance_from_centroid, ave_horizontal_distance_from_centroid, ave_euclidean_distance_from_centroid, average_angle_between_landmark_point_and_centroid, ave_vertical_distance_from_baseline, ave_horizontal_distance_from_baseline, ave_euclidean_distance_from_baseline, average_angle_between_landmark_point_and_baseline

- **Parameters:**
    - points_rescaled - A list of tuples representing rescaled landmark points
    - centroid_scaled - A tuple representing the rescaled centroid point
    - baseline_rescaled - A tuple representing the rescaled baseline point
    - device - Counter for image processing steps
    - debug- None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to estimate the distance and angles of landmark points relative to shape reference landmarks (centroid and pot height aka baseline)

**Input rescaled points, centroid and baseline points**

![Screenshot](img/documentation_images/landmark_reference_pt_dist/lrpd_example_image.jpg)

```python
import plantcv as pcv

device = 1

# Identify acute vertices (tip points) of an object
# Results in set of point values that may indicate tip points
device, vert_ave_c, hori_ave_c, euc_ave_c, ang_ave_c, vert_ave_b, hori_ave_b, euc_ave_b, ang_ave_b = pcv.landmark_reference_pt_dist(points_r, centroid_r, bline_r, device)
```

**Representation of many data points collected in two treatment blocks throughout time**

![Screenshot](img/documentation_images/landmark_reference_pt_dist/lrpd_output.jpg)
