## Parallel workflow configuration class

`Config` is a class that stores parallel workflow configuration parameters. An instance of `Config` is input to the
`plantcv.parallel.run_workflow` function to execute a PlantCV workflow on an image dataset, in parallel.

*class* **plantcv.parallel.Config**(*input_dir, json, filename_metadata, output_dir=".", tmp_dir=None, processes=1, 
start_date=1, end_date=None, imgformat="png", delimiter="_", metadata_filters=None, 
timestampformat='%Y-%m-%d %H:%M:%S.%f', writeimg=False, other_args=None, coprocess=None*)

- **Parameters:**
    - input_dir (str, required): path/name of input images directory (validates that it exists)
    - json (str, required): path/name of output JSON data file (appends new data if it already exists)
    - filename_metadata (list, required): list of metadata terms used to construct filenames
    - output_dir (str, default = "."): path/name of output directory where images will be saved
    - tmp_dir (str, default = `None`): path/name of parent folder for the temporary directory, current working directory when `None`
    - processes (int, default = 1): number of parallel processes
    - start_date (int, default = 1): start date in Unix time used to filter images. Images will be analyzed that are newer than the start date
    - end_date (int, default = `None`): end date in Unix time used to filter images. Images will be analyzed that are older than the end date, unless `None`
    - imgformat (str, default = "png"): image file format/extension
    - delimiter (str, default = "_"): image filename metadata term delimiter character. Alternatively, a regular expression for parsing filename metadata
    - metadata_filters (dict, default = `None`): a dictionary of metadata terms (keys) and values, images will be analyzed that have the associated term and value
    - timestampformat (str, default = '%Y-%m-%d %H:%M:%S.%f'): a date format code compatible with strptime C library
    - writeimg (bool, default = `False`): save analysis images to `output_dir` if `True`
    - other_args (str, default = `None`): other arguments required by the workflow
    - coprocess (str, default = `None`): coprocess the specified imgtype with the imgtype specified in metadata_filters (e.g. coprocess NIR images with VIS)
- **Context:**
    - Used to configure parallelization of PlantCV workflows.

### Example

```python
import plantcv.parallel

config = plantcv.parallel.Config(input_dir="/path/to/images", json="plantcv.results.json", 
                                 filename_metadata=["imgtype", "camera", "frame", "zoom"], output_dir="/path/to/outdir",
                                 processes=10, metadata_filters={"imgtype": "VIS", "zoom": "z1000"})
plantcv.parallel.run_workflow(config=config, workflow=workflow)

```
