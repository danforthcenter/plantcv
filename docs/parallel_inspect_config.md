## Inspect data for a parallel workflow configuration

### inspect_dataset

Once you have a [`WorkflowConfig` class object](parallel_config.md), a saved configuration file, or at the very least an input directory of image data, you may want to check which and how many images would be used running that workflow. This can be helpful in troubleshooting metadata filters among other configuration options.

**plantcv.parallel.inspect_dataset**(*config*)

**returns** summary_df, df
	- summary_df shows whether images were kept and if not where they why they were removed (status column) then groups images by status and any metadata from `config.metadata_filters` and returns how many unique values each term has and what they are (if there are 3 or fewer unique values).
	- df shows all the images collected by the workflow, including the same status information as in summary_df.


- **Parameters:**
	- config - Plantcv.parallel.WorkflowConfig object or str. String input should be a filepath to a configuration json file or a path to be used in place of `config.input_dir`. Note that there are several useful defaults expected from a `WorkflowConfig` object, so results from using just a file path may be less detailed.
- **Context:**
	- Used to check what would be collected by a given workflow configuration.
- **Example use:**
	- See below

```python
from plantcv import parallel as pcvpar

config = pcvpar.WorkflowConfig()
config.input_dir("./my_images")

summary, meta = pcvpar.inspect_dataset(config)
```

#### Command Line Interface

`plantcv.parallel.inspect_dataset` can also be run from the command line using `plantcv-run-workflow --dryrun configfile.json`. Used this way it will save the summary and metadata DataFrames to csv files named for your configuration file with `_summary_df.csv` and `_metadata_df.csv` replacing the `.json` extension.

```bash
plantcv-run-workflow --dryrun configfile.json
```
