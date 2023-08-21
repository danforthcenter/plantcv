## Tutorial: Workflow Parallelization

!!! warning
    Workflows should be optimized to an image test-set before running a whole dataset.
    See the [VIS workflow tutorial](tutorials/vis_tutorial.md) or [VIS/NIR tutorial](tutorials/vis_nir_tutorial.md).
    Our [download tool](https://github.com/danforthcenter/pheno-data-service), which talks to a LemnaTec database system,
    has a specific file structure, which may be different than yours unless you are using our tool, but we also have instructions
    to run PlantCV over a flat file directory (just keep this in mind).

### Running PlantCV workflows over a dataset

We normally execute workflows in a shell script or in in a cluster scheduler job file. The parallelization tool
`plantcv-run-workflow` has many configuration parameters. To make it easier to manage the number of input parameters,
a configuration file can be edited and input.

### Configuration-based method

To create a configuration file, run the following:

```bash
plantcv-run-workflow --template my_config.txt

```

The code above saves a text configuration file in JSON format using the built-in defaults for parameters. The parameters can be modified
directly in Python as demonstrated in the [WorkflowConfig documentation](parallel_config.md). A configuration can be
saved at any time using the `save_config` method to save for later use. Alternatively, open the saved config
file with your favorite text editor and adjust the parameters as needed.

**Some notes on JSON format:**

* Like Python, string variables (e.g. "VIS") need to be in quotes but must be double `"` quotes.
* Unlike Python, `true` and `false` in JSON are lowercase.
* `None` in Python translates to `null` in JSON
* `\` characters need to be escaped in JSON e.g. `\d` in Python becomes `\\d` in JSON
* There are no comments in JSON

Differences between JSON and Python will be automatically converted appropriately if you make changes to the config in Python and then use `save_config`.

Once configured, a workflow can be run in parallel over a dataset using the command:

```bash
plantcv-run-workflow --config config.json

```

As noted on the [WorkflowConfig](parallel_config.md) page, `plantcv-run-workflow` can be configured to run PlantCV
workflows locally or distribute workflows to a cluster using a scheduler service (e.g. HTCondor, SLURM, etc.).

### Running PlantCV workflows over a flat directory of images

!!! note
    PlantCV can analyze images in parallel that are stored in a directory (including subdirectories). Our aim is to
    make this process as flexible as possible but consistency in naming images is key. Ideally image filenames are
    constructed of metadata information separated by a consistent delimiter (though we provide a regular
    expression-based parser if needed). Please follow the instructions below carefully.

In order for PlantCV to extract all of the necessary metadata from the image files, image files need to be named in
a particular way.

**Image name might include:**

1. Plant ID
2. Timestamp
3. Measurement/Experiment Label
4. Image Type
5. Camera Label
6. Zoom

**Example Name:**

AABA002948_2014-03-14 03-29-45_Pilot-031014_VIS_TV_z3500.png

1. Plant ID = AABA002948
2. Timestamp = 2014-03-14 03-29-45
3. Measurement Label = Pilot-031014
4. Image Type = VIS
5. Camera Label = TV
6. Zoom = z3500

**Valid Metadata**

Valid metadata that can be collected from filenames are `camera`, `imgtype`, `zoom`, `exposure`, `gain`, `frame`, `rotation`,
`lifter`, `timestamp`, `id`, `barcode`, `treatment`, `cartag`, `measurementlabel`, and `other`.

To correctly process timestamps, you need to specify the timestamp format (`timestampformat` configuration
parameter) code for the
[strptime C library](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior).
For the example above you would use `"timestampformat": "%Y-%m-%d %H-%M-%S"`.

#### Example configuration

Sample image filename: `cam1_16-08-06-16:45_el1100s1_p19.jpg`

```
{
    "input_dir": "/shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1",
    "json": "edger-round1-brassica.json",
    "filename_metadata": ["camera", "timestamp", "id", "other"],
    "workflow": "/home/mgehan/pat-edger/round1-python-pipelines/2016-08_pat-edger_brassica-cam1-splitimg.py",
    "img_outdir": "/shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1/output",
    "tmp_dir": null,
    "start_date": null,
    "end_date": null,
    "imgformat": "jpg",
    "delimiter": "_",
    "metadata_filters": {"camera": "cam1"},
    "timestampformat": "%y-%m-%d-%H:%M",
    "writeimg": true,
    "other_args": {},
    "groupby": ["filepath"],
    "group_name": "auto",
    "cleanup": true,
    "append": true,
    "cluster": "HTCondorCluster",
    "cluster_config": {
        "n_workers": 16,
        "cores": 1,
        "memory": "1GB",
        "disk": "1GB",
        "log_directory": null,
        "local_directory": null,
        "job_extra_directives": null
    },
    "metadata_terms": {
    ...
    }
}

```

Running `plantcv-run-workflow --config config.json` with the example configuration options above will run the PlantCV
workflow script `2016-08_pat-edger_brassica-cam1-splitimg.py` on the images in the input directory using an HTCondor
compute cluster with up to 16 worker jobs checked out of the cluster.

#### Using a pattern matching-based filename metadata parser

If image filenames do not use a consistent delimiter (e.g. rgb_plant-1_2019-01-01 10_00_00.png) throughout,
then using the `delimiter` parameter with a single separator character will not split the filename properly
into the component metadata parts. An advanced option to extract metadata in this situation is to use pattern
matching, or [regular expressions](https://docs.python.org/3.7/library/re.html). The `delimiter` parameter
will accept a regular expression in place of a delimiter character. Example:

Example filename: `rgb_plant-1_2019-01-01 10_00_00.png`
Metadata components: `imgtype`, `plantbarcode`, `timestamp`
Delimiter = `"_"` will not work because the timestamp contains `_` characters.
Regular expression: `'(.{3})_(.+)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})'`

**Interpreting the example pattern**

A key part of the pattern is the use of parenthesis because in regular expression syntax these
mark the start and end of a group that will be returned from a match (or in other words parsed
for our purposes). Regular expression patterns can be as general or specific as needed. The
pattern above reads as:

Group 1 (camera): any 3 characters

Underscore

Group 2 (plantbarcode): 1 or more of any character

Underscore

Group 3 (timestamp): 4 digits, dash, 2 digits, dash, 2 digits, space, 2 digits, underscore, 2 digits, underscore, 2 digits

Note that the number of groups returned by the regular expression must match the number of metadata terms provided to
in a list to the `filename_metadata` parameter.

**Example configuration:**

```bash
{
    "input_dir": "input_directory",
    "json": "output.json",
    "filename_metadata": ["camera", "plantbarcode", "timestamp"],
    "workflow": "user-workflow.py",
    "img_outdir": "output_directory",
    "tmp_dir": null,
    "start_date": null,
    "end_date": null,
    "imgformat": "jpg",
    "delimiter": '(.{3})_(.+)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})',
    "metadata_filters": {},
    "timestampformat": "%Y-%m-%d %H_%M_%S",
    "writeimg": true,
    "other_args": {},
    "groupby": ["filepath"],
    "group_name": "auto",
    "cleanup": true,
    "append": true,
    "cluster": "HTCondorCluster",
    "cluster_config": {
        "n_workers": 16,
        "cores": 1,
        "memory": "1GB",
        "disk": "1GB",
        "log_directory": null,
        "local_directory": null,
        "job_extra_directives": null
    },
    "metadata_terms": {
    ...
    }
}

```

If you need help building a regular expression, https://regexr.com/ is a useful site to help build and interpret
patterns. Also feel free to post an [issue](https://github.com/danforthcenter/plantcv/issues).

#### Grouping images for multi-image workflows

Advanced PlantCV workflows can co-analyze multiple images. For example, a dataset containing an RGB and grayscale
near-infrared image could be co-analyzed in a single workflow.

Sample image filenames: `rgb_16-08-06-16:45_el1100s1_p19.jpg` and `nir_16-08-06-16:45_el1100s1_p19.jpg`

Note in the example above, the two filenames are the same other than the indicated image type (rgb or nir).

In the example configuration below, we can group these images by `timestamp` because they share this metadata.
To identify each image within our workflow, we will name them based on the `imgtype` metadata values (rgb and nir).

```
{
    "input_dir": "/shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1",
    "json": "edger-round1-brassica.json",
    "filename_metadata": ["imgtype", "timestamp", "id", "other"],
    "workflow": "/home/mgehan/pat-edger/round1-python-pipelines/2016-08_pat-edger_brassica-cam1-splitimg.py",
    "img_outdir": "/shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1/output",
    "tmp_dir": null,
    "start_date": null,
    "end_date": null,
    "imgformat": "jpg",
    "delimiter": "_",
    "metadata_filters": {},
    "timestampformat": "%y-%m-%d-%H:%M",
    "writeimg": true,
    "other_args": {},
    "groupby": ["timestamp"],
    "group_name": "imgtype",
    "cleanup": true,
    "append": true,
    "cluster": "HTCondorCluster",
    "cluster_config": {
        "n_workers": 16,
        "cores": 1,
        "memory": "1GB",
        "disk": "1GB",
        "log_directory": null,
        "local_directory": null,
        "job_extra_directives": null
    },
    "metadata_terms": {
    ...
    }
}

### Convert the output JSON file into CSV tables

```bash
plantcv-utils json2csv -j output.json -c result-table

```

See [Accessory Tools](tools.md) for more information.

**Source Code:** [Here](https://github.com/danforthcenter/plantcv/blob/main/plantcv/parallel/cli.py)
