## class Outputs 

A global PlantCV output class.

*class* plantcv.**Outputs**

An `Outputs` class has been added that automatically stores measurements and images collected by the following 
functions:

* `analyze_bound_horizontal`
* `analyze_bound_vertical`
* `analyze_color`
* `analyze_nir_intensity`
* `analyze_object`
* `fluor_fvfm`
* `report_size_marker_area`
* `watershed`

An instance of `Outputs` is created on import automatically as `plantcv.outputs`. The function 
[pcv.print_results](print_results.md) will print out all the stored measurments data to a text file. 

### Methods

Methods are accessed as plantcv.outputs.*method*.

**clear**: Clears the contents of both measurements and image 

- **Example use:**
    - [Use In VIS/NIR Tutorial](vis_nir_tutorial.md)

### Example

```
from plantcv import plantcv as pcv

######## Pipeline steps here ########

# Find shape properties, output shape image (optional)
shape_header, shape_data, shape_img = pcv.analyze_object(img, obj, mask)

# Write shape data to results file
pcv.print_results(filename=args.result)

# Will will print out results again, so clear the outputs before running NIR analysis 
pcv.outputs.clear()

######## More pipeline steps here ########

nhist_header, nhist_data, nir_imgs = pcv.analyze_nir_intensity(nir2, nir_combinedmask, 256)
nshape_header, nshape_data, nir_hist = pcv.analyze_object(nir2, nir_combined, nir_combinedmask)

# Write the NIR and shape data to a file 
pcv.print_results(filename=args.coresult)
```
