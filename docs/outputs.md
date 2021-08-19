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
* `analyze_thermal_values` 
* `fluor_fvfm`
* `hyperspectral.analyze_spectral`
* `hyperspectral.analyze_index`
* `report_size_marker_area`
* `morphology.check_cycles`
* `morphology.segment_angle`
* `morphology.segment_curvature`
* `morphology.euclidean_length`
* `morphology.segment_insertion_angle`
* `morphology.segment_path_length`
* `morphology.segment_tangent_angle` 
* `within_frame`
* `watershed`

An instance of `Outputs` is created on import automatically as `plantcv.outputs`. The method 
`Outputs.save_results` will save all the stored measurement data to a text file. 

### Methods

Methods are accessed as plantcv.outputs.*method*.

**clear**(): Clears the contents of both measurements and image 

**add_observation**(*sample, variable, trait, method, scale, datatype, value, label*): Add new measurement or other information

* sample: A sample name or label. Observations are organized by sample name.

* variable: A local unique identifier of a variable, e.g. a short name, that is a key linking the definitions of variables with observations.

* trait: A name of the trait mapped to an external ontology; if there is no exact mapping, an informative description of the trait.

* method: A name of the measurement method mapped to an external ontology; if there is no exact mapping, an informative description of the measurement procedure.

* scale: Units of the measurement or a scale in which the observations are expressed; if possible, standard units and scales should be used and mapped to existing ontologies; in case of a non-standard scale a full explanation should be given.

* datatype: The type of data to be stored. In JSON, values must be one of the following data types:
    - a string
    - a number
    - an array
    - a boolean
    - null
    - a JSON object
    
    They are equilvalent to python data types of the following:
    - 'str'
    - 'int' or 'float'
    - 'list' or 'tuple'
    - 'bool'
    - 'NoneType'
    - 'dict'

* value: The data itself. Make sure the data type of value matches the data type stated in "datatype". 

* label:  The label for each value, which will be useful when the data is a frequency table (e.g. hues). 

**save_results**(*filename, outformat="json"*): Save results to a file

* filename: Path and name of the output file

* outformat: Output file format (default = "json"). Supports "json" and "csv" formats

**Example use:**
    - [Use In VIS/NIR Tutorial](tutorials/vis_nir_tutorial.md)

### Examples

```python
from plantcv import plantcv as pcv

######## workflow steps here ########

# Find shape properties, output shape image (optional)
shape_img = pcv.analyze_object(img, obj, mask, label="default")

# Look at object area data without writing to a file 
plant_area = pcv.outputs.observations['default']['pixel_area']['value']

# Write shape data to results file
pcv.outputs.save_results(filename=args.result, outformat="json")

# Will will print out results again, so clear the outputs before running NIR analysis 
pcv.outputs.clear()

######## More workflow steps here ########

nir_imgs = pcv.analyze_nir_intensity(nir2, nir_combinedmask, 256, label="default")
shape_img = pcv.analyze_object(nir2, nir_combined, nir_combinedmask, label="default")

# Write the NIR and shape data to a file 
pcv.outputs.save_results(filename=args.coresult, outformat="json")

```

```python
import numpy as np
from plantcv import plantcv as pcv

# Use Naive-Bayes to make masks for each classes 
mask = pcv.naive_bayes_classifier(img, pdf_file="naive_bayes_pdfs.txt")

# Calculate percent of the plant found to be diseased 
sick_plant = np.count_nonzero(mask['diseased'])
healthy_plant = np.count_nonzero(mask['plant'])
percent_diseased = sick_plant / (sick_plant + healthy_plant)

# Create a new measurement
pcv.outputs.add_observation(sample='default', variable='percent_diseased', 
                            trait='percent of plant detected to be diseased',
                            method='ratio of pixels', scale='percent', datatype=float,
                            value=percent_diseased, label='percent')

# Write custom data to results file
pcv.outputs.save_results(filename=args.result, outformat="json")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/master/plantcv/plantcv/classes.py)
