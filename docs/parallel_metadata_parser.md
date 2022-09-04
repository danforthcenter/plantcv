## Metadata Parser 

Reads metadata the from the input data directory.

**plantcv.parallel.metadata_parser**(*config*)

**returns** meta (dictionary of image metadata, one entry per image to be processed)

- **Parameters:**
    - config   - plantcv.parallel.WorkflowConfig object
- **Context:**
    - This is one of the first steps built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. 
    It reads metadata the from the input data directory and uses the outputs in the [job builder](parallel_job_builder.md) step. 


A helper function to convert datetimes/timestamps in string format to Unix/Epoch time (elapsed seconds from epoch).

**plantcv.parallel.convert_datetime_to_unixtime**(*timestamp_str, date_format*)

**returns** unix_time (integer value of elapsed seconds from epoch: 1970-01-01 00:00:00)

- **Parameters:**
    - timestamp_str - a datetime represented as a character string (e.g. 2020-01-01 00:00:00)
    - date_format - date format code for `strptime` (e.g. "%Y-%m-%d %H:%M:%S") See 
    [strptime docs](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) for supported codes.
- **Context:**
    - A timestamp is often an important piece of metadata associated with automated imaging. This function is used to
    convert between human and machine readable datetime formats within [Workflow Parallelization](pipeline_parallel.md).

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/parsers.py)
