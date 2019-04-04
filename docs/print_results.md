## Print Measurement Results 

An `Outputs` class has been added that automatically stores measurements collected by the following 
functions:

* `analyze_bound_horizontal`
* `analyze_bound_vertical`
* `analyze_color`
* `analyze_nir_intensity`
* `analyze_object`
* `fluor_fvfm`
* `report_size_marker_area`
* `watershed`

The `print_results` function will take the measurements stored when running any (or all) of these functions, format, and 
print an output text file for data analysis. 

**plantcv.print_results**(*filename*)

**returns** none

- **Parameters:**
    - filename- Name of results text file
- **Context:**
    - Print out a result file containing all measurements recorded by functions included in the pipeline
      for each image processed.  
- **Example use:**
    - [Use In VIS Tutorial](vis_tutorial.md)  

```python
from plantcv import plantcv as pcv

# Read in image
img, path, img_filename = pcv.readimage("home/user/images/test-image.png")

######### Pipeline steps here 

pcv.print_results(filename='test_pipeline_results.txt')

```
