## Process Results

Process a directory of coco annotation files from running PlantCV over as many images as needed and create a formatted, concatenated data output file.


**plantcv.plantcv.process_coco_results**(*filename, source=".", pattern="_pcv_coco.json", mode="w"*)

**returns** none

- **Parameters:**
	- filename    - str, filename to write out, ignored if `input_dir` is a `WorkflowConfig` object
	- source - string or list, a string is used as a filepath to search for results that match the given apttern. A list is taken as a list of filepaths.
	- pattern - string or None, used to pick which files are coco results. None will include all plain text/json files. The `"_pcv_coco.json"` default matches the coco suffix that [`COCO.save`](coco_class.md) defaults to use.
	- mode - string, either "a" for append or "w" for write.

- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. Each workflow may save coco data using [`pcv.COCO.save`](coco_class.md). The `process_coco_results` step takes place after all images have been analyzed and combines these single workflow coco files into one text file that can be used as input for machine learning/AI applications. This function can also be called manually if you have run a jupyter notebook several times and want to combine COCO annotations.

- **Example use:**
    - Below 

```python
from plantcv import plantcv as pcv

pcv.process_coco_results("combined_coco_results.json")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/plantcv/process_coco_results.py)
