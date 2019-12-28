## Metadata Parser 

Reads metadata the from the input data directory.

**plantcv.parallel.metadata_parser**(*data_dir, meta_fields, valid_meta, meta_filters, date_format, 
                    start_date, end_date, delimiter="_", file_type="png", coprocess=None*)

**returns** jobcount (number of processing jobs), and meta (dictionary of image metadata, one entry per image to be processed)

- **Parameters:**
    - data_dir   - Input data directory
    - meta_fields - Dictionary of image filename metadata fields and index positions
    - valid_meta - Dictionary of valid metadata keys
    - meta_filters - Dictionary of metadata filters (key-value pairs)
    - date_format - Date format code for timestamp metadata to use with strptime
    - start_date - Analysis start date in Unix time
    - end_date - Analysis end date in Unix time
    - delimiter - Filename metadata delimiter string or regular expression pattern (default: "_") 
    - file_type - Image filetype extension (default: "png")
    - coprocess - Coprocess the specified imgtype with the imgtype specified in meta_filters (default: None) 
- **Context:**
    - This is one of the first steps built into the [PlantCV Workflow Parallelization](pipeline_parallel.md) feature. 
    It reads metadata the from the input data directory and uses the outputs in the [job builder](parallel_job_builder.md) step. 
