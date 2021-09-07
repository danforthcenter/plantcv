## Print Measurement Results 

!!! warning
    `plantcv.print_results` is deprecated and will be removed in a future version.

An [Outputs](outputs.md) class has been added that automatically stores measurements collected by the following 
functions:

* `analyze_bound_horizontal`
* `analyze_bound_vertical`
* `analyze_color`
* `analyze_nir_intensity`
* `analyze_object`
* `analyze_thermal_values`
* `fluor_fvfm`
* `hyperspectral.analyze_index`
* `hyperspectral.analyze_spectral`
* `morphology.check_cycles`
* `morphology.segment_angle`
* `morphology.segment_curvature`
* `morphology.segment_euclidean_length`
* `morphology.segment_insertion_angle`
* `morphology.segment_path_length`
* `morphology.segment_tangent_angle`
* `report_size_marker_area`
* `watershed`

Users can also add measurements to the `Outputs` class with the `pcv.outputs.add_observation` method.


The `print_results` function will take the measurements stored when running any (or all) of these functions, format, and 
print an output .json file for data analysis. 

**plantcv.print_results**(*filename*)

**returns** none

- **Parameters:**
    - filename- Name of results text file
- **Context:**
    - Print out a result file containing all measurements recorded by functions included in the workflow
      for each image processed.  
- **Example use:**
    - [Use In VIS Tutorial](tutorials/vis_tutorial.md)  

```python
from plantcv import plantcv as pcv

# Read in image
img, path, img_filename = pcv.readimage("home/user/images/test-image.png")

######### Workflow steps here 

pcv.print_results(filename='test_workflow_results.txt')

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/print_results.py)
