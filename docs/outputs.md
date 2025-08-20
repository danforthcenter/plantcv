## class Outputs 

A global PlantCV output class.

*class* plantcv.**Outputs**

An `Outputs` class has been added that automatically stores measurements and images collected by the following 
functions:

* `analyze.bound_horizontal`
* `analyze.bound_vertical`
* `analyze.color`
* `analyze.distribution`
* `analyze.grayscale`
* `analyze.npq`
* `analyze.size`
* `analyze.thermal` 
* `analyze.spectral_index`
* `analyze.spectral_reflectance`
* `analyze.yii`
* `homology.acute` 
* `homology.landmark_reference_pt_dist`
* `homology.x_axis_pseudolandmarks`
* `homology.y_axis_pseudolandmarks`
* `morphology.analyze_stem`
* `morphology.check_cycles`
* `morphology.euclidean_length`
* `morphology.fill_segments`
* `morphology.find_tips`
* `morphology.find_branch_pts`
* `morphology.segment_angle`
* `morphology.segment_curvature`
* `morphology.segment_euclidean_length`
* `morphology.segment_insertion_angle`
* `morphology.segment_path_length`
* `morphology.segment_tangent_angle` 
* `report_size_marker_area`
* `transform.detect_color_card`
* `transform.auto_correct_color`
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

* datatype: The type of data to be stored. See note below for supported data types.

* value: The data itself. Make sure the data type of value matches the data type stated in "datatype". 

* label:  The label for each value, which will be useful when the data is a frequency table (e.g. hues). 

**add_metadata**(*term, datatype, value*): Add metadata about the image or other information

* term: Metadata term/name

* datatype: The type of data to be stored. See note below for supported data types.

* value: The data itself. Make sure the data type of value matches the data type stated in "datatype". 

**save_results**(*filename, outformat="json"*): Save results to a file

* filename: Path and name of the output file

* outformat: Output file format (default = "json"). Supports "json" and "csv" formats

!!!note
    Supported data types for JSON output are: int, float, str, list, bool, tuple, dict, NoneType, numpy.float64.

**Example use:**
    - [Use In Seed Analysis Tutorial](https://plantcv.org/tutorials/seed-analysis-workflow)

### Examples

```python
from plantcv import plantcv as pcv
# Set a global sample label (optional)
pcv.params.sample_label = "plant"

######## workflow steps here ########

# Find shape properties, output shape image (optional)
shape_img = pcv.analyze.size(img=img, labeled_mask=mask, n_labels=1)

# Look at object area data without writing to a file 
plant_area = pcv.outputs.observations['plant_1']['pixel_area']['value']

######## More workflow steps here ########

nir_hist = pcv.analyze.grayscale(gray_img=nir2, labeled_mask=nir_combinedmask, n_labels=1, bins=100)

# Write the NIR and shape data to a file 
pcv.outputs.save_results(filename=args.result, outformat="json")

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

# Add metadata 
pcv.outputs.add_metadata(term="genotype", datatype=str, value="wildtype")

# Write custom data to results file
pcv.outputs.save_results(filename=args.result, outformat="json")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/classes.py)
