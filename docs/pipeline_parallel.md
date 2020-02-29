## Tutorial: Workflow Parallelization

**Warning:** Workflows should be optimized to an image test-set before running a whole dataset.
See the [VIS workflow tutorial](vis_tutorial.md) or [VIS/NIR tutorial](vis_nir_tutorial.md).
Our [download tool](https://github.com/danforthcenter/pheno-data-service), which talks to a LemnaTec database system,
has a specific file structure, which may be different than yours unless you are using our tool, but we also have instructions
to run PlantCV over a flat file directory (just keep this in mind).

### Running PlantCV over PhenoFront image data-set structure

We normally execute workflows in a shell script or in in a condor job file (or dagman workflow if running multiple workflows into one json database)

* First call the plantcv-workflow.py script that does the parallelization
* -d is the --dir directory of images
* -p is the --workflow that you are going to run over the images, see the [VIS tutorial](vis_tutorial.md) and [PSII tutorial](psII_tutorial.md)
* -i is the --outdir your desired location for the output images
* -a is the --adaptor to indicate structure to grab the metadata from, either 'filename' or the default, which is 'phenofront' (lemnatec structured output)
* -t is the --type extension 'png' is the default. Any format readable by opencv is accepted such as 'tif' or 'jpg'
* -l is the --delimiter for the filename that is used to separate metadata, default is "_". Can also be a regular expression pattern (see below).
* -C is the --coprocess the specified imgtype with the imgtype specified in --match (e.g. coprocess NIR images with VIS).
* -f is the --meta (data) structure of image file names. Comma-separated list of valid metadata terms ( "camera","imgtype". "zoom", "exposure", "gain", 
    "frame", "lifter", "timestamp", "id", "plantbarcode", "treatment", "cartag", "measurementlabel", or "other").
* -M is the --match metadata option, for example to select a certain zoom or angle. For example: 'imgtype:VIS,camera:SV,zoom:z500'
* -D is the --dates option, to select a certain date range of data. YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date is excluded then the current date is assumed. Time can be excluded.
* -j is the --json, json database name
* -m is the --mask any image mask that you would like to provide
* -T is the --cpu # of cpu processes you would like to use.
* -s is the --timestampformat specify timestamp format for strptime C library. default is '%Y-%m-%d %H:%M:%S.%f' to parse '2010-10-10 10:10:10.123'. see 
    [strptime docs](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) for supported codes.
* -w is the --writeimg option, if True will write output images. default= False
* -c is the --create option to overwrite an json database if it exists, if you are creating a new database or appending to database, do NOT add the -c flag
* -o is the --other_args option, used to pass non-standard options to the workflow script. Must take the form `--other_args="--option1 value1 --option2 value2"`


#### If running as a command in a shell script

```bash
#!/bin/bash

# Here we are running a VIS top-view workflow

time \
/home/nfahlgren/programs/plantcv/plantcv-workflow.py \
-d /home/nfahlgren/projects/lemnatec/burnin2/images3 \
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z300_L1.py \
-t png \
-j burnin2.json \
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images \
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z300_L1.png \
-f imgtype,camera,frame,zoom,id \
-M imgtype:VIS,camera:TV,zoom:z300 \
-C NIR \
-T 10 \
-w


# Here we are running a second VIS top-view workflow at a second zoom level

time \
/home/nfahlgren/programs/plantcv/plantcv-workflow.py \
-d /home/nfahlgren/projects/lemnatec/burnin2/images3 \
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z1000_L1.py \
-t png \
-j burnin2.json \
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images \
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z1000_L1.png \
-f imgtype,camera,frame,zoom,id \
-M imgtype:VIS,camera:TV,zoom:z1000 \
-C NIR \
-T 10 \
-w 
```

### Example Batch Script (Windows)
If you are running on **Windows** (except with WSL), you will need to use a batch script. Assuming you are using Anaconda Prompt, make sure you `conda activate plantcv`,
 and `cd` to your project directory. There are no comments in batch scripts and `python` can only find files in you immediate working directory (even if the file is in your PATH). Also, the first argument needs to be on the same line `plantcv-workflow.py`.

```
python.exe ^
%CONDA_PREFIX%\Scripts\plantcv-workflow.py -d C:\Users\nfahlgren\Documents\projects\lemnatec\burnin2\images3 ^
-p C:\Users\nfahlgren\Documents\programs\plantcv\scripts\image_analysis\vis_tv\vis_tv_z300_L1.py ^
-t png ^
-j burnin2.json ^
-i C:\Users\nfahlgren\Documents\projects\lemnatec\burnin2\plantcv3\images ^
-m C:\Users\nfahlgren\Documents\programs\plantcv\masks\vis_tv\mask_brass_tv_z300_L1.png ^
-f imgtype,camera,frame,zoom,id ^
-M imgtype:VIS,camera:TV,zoom:z300 ^
-C NIR ^
-T 10 ^
-w
```

If saved as `run_workflow.cmd` you can then execute it in the Anaconda Prompt:
```
(plantcv) C:\Users\nfahlgren\Documents\projects\lemnatec> run_workflows.cmd
```

### Example Condor Jobfile

```
#################################
# HTCondor job description file #
#################################

universe         = vanilla
executable       = /home/mgehan/plantcv/plantcv-workflow.py
arguments        = -d /shares/tmockler_share/mgehan/LemnaTec/bnapus_phenotyping_katie/images-full -p /home/mgehan/kt-greenham-lemnatec/scripts/vis_nir_tv_z500_h2_e10000_brassica.py -j ktbrassica.json -i /home/mgehan/kt-greenham-lemnatec/output/output500 -f imgtype,camera,zoom,lifter,gain,exposure,id -M imgtype:VIS,camera:TV,zoom:z500 -T 16 -C NIR -w
log              = $(Cluster).$(Process).log
output           = $(Cluster).$(Process).out
error            = $(Cluster).$(Process).error
request_cpus     = 16
notification     = always
nice_user        = False
getenv           = true
####################

queue

```

### Running PlantCV workflows over a flat directory of images

**Note:** We will try and update PlantCV so that it can run over flat directories in a more flexible manner.
But for now please follow the instructions on Running PlantCV over a flat directory carefully.

In order for PlantCV to scrape all of the necessary metadata from the image files, image files need to be named in a particular way.

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

Valid metadata that can be collected from filenames are `camera`, `imgtype`, `zoom`, `exposure`, `gain`, `frame`, `lifter`, `timestamp`, `id`, `plantbarcode`, `treatment`, `cartag`, `measurementlabel`, and `other`. 

For a flat direcotory of images (`--adaptor = filename`) you are required to specify the timestamp format (`--timestampformat`, `-s`) code for the 
[strptime C library](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior). For the example above you would use `--timestampformat "%Y-%m-%d %H-%M-%S"`.

**Next, run images over a flat directory with images named as described above:**

We normally execute workflows as a shell script or as a condor jobfile (or dagman workflow)

```bash
#!/bin/bash

# Here we are running a VIS top-view workflow over a flat directory of images

# Image names for this example look like this: cam1_16-08-06-16:45_el1100s1_p19.jpg

/home/mgehan/plantcv/plantcv-workflow.py \
-d /shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1 \
-a filename \
-s %y-%m-%d-%H:%M
-l _
-p /home/mgehan/pat-edger/round1-python-pipelines/2016-08_pat-edger_brassica-cam1-splitimg.py \
-j edger-round1-brassica.json \
-i /shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1/output \
-f camera,timestamp,id,other \
-t jpg \
-T 16 \
-w

```

### Using a pattern matching-based filename metadata parser

If image filenames do not use a consistent delimiter (e.g. rgb_plant-1_2019-01-01 10_00_00.png) throughout, 
then using the `--delimiter` option with a single separator character will not split the filename properly
into the component metadata parts. An advanced option to extract metadata in this situation is to use pattern
matching, or [regular expressions](https://docs.python.org/3.7/library/re.html). The `--delimiter` option
will accept a regular expression in place of a delimiter character. Example:

Example filename: rgb_plant-1_2019-01-01 10_00_00.png
Metadata components: imgtype, plantbarcode, timestamp
Delimiter = "_" will not work because the timestamp contains _ characters.
Regular expression: '(.{3})_(.+)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})'

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
the `--meta` option.

```bash
plantcv-workflow.py \
--dir input_directory \
--workflow user-workflow.py \
--json output.json \
--outdir output_directory \
--meta camera,plantbarcode,timestamp \
--delimiter '(.{3})_(.+)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})'
--timestampformat "%Y-%m-%d %H_%M_%S"

```

If you need help building a regular expression, https://regexr.com/ is a useful site to help build and interpret
patterns. Also feel free to post an [issue](https://github.com/danforthcenter/plantcv/issues).

### Convert the output JSON file into CSV tables

```bash
plantcv-utils.py json2csv -j output.json -c result-table
```

This can be added as an additional line in the shell script that runs the workflow too.

See [Accessory Tools](tools.md) for more information.
