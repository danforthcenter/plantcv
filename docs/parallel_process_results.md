## Process Results

Process a directory of results files from running PlantCV over as many images as needed and create a formatted, concatenated data output file. 

**plantcv.parallel.process_results**(*job_dir, json_file*)

**returns** none

- **Parameters:**
    - job_dir   - Path of the job directory
    - json_file - Path and name of the output combined json file
- **Context:**
    - This step is built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. Each image will likely print 
    hierarchical data files if [`print_results`](print_results.md) is a step in the workflow but the `process_results` step takes place after all
    images have been analyzed and combines these single image data files into one text file that can be used as input for the [`json2csv`](tools.md#convert-output-json-data-files-to-csv-tables)
    function. 
- **Example use:**
    - Below 

```python
from plantcv import parallel 

# Read in image
parallel.process_results(job_dir="home/user/parallel_results", json_file="combined_output.txt")


```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/process_results.py)
