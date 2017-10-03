## Tutorial: Pipeline Parallelization

**Warning:** Pipelines should be optimized to an image test-set before running a whole data-set.
See Pipeline Tutorial [here](vis_tutorial.md) or [here](vis_nir_tutorial.md).
Our image download tool, which talks to a LemnaTec database system can be found [here](https://github.com/danforthcenter/pheno-data-service).
Our download tool has a specific file structure, which may be different than yours unless you are using our tool, but we also have instructions
to run PlantCV over a flat file directory (just keep this in mind).

### Running PlantCV over PhenoFront image data-set structure

We normally execute pipelines in a shell script or in in a condor job file (or dagman workflow if running multiple pipelines into one sqlite database)

* First call the plantcv-pipeline.py script that does the parallelization
* -d is the --directory of images
* -p is the --pipeline that you are going to run over the images see [VIS tutorial here](vis_tutorial.md) and [PSII tutorial here](psII_tutorial.md)
* -i is the --outdir your desired location for the output images
* -a is the --adaptor to indicate structure to grab the metadata from, either 'filename' or the default, which is 'phenofront' (lemnatec structured output)
* -t is the --type extension 'png' is the default or 'jpg'
* -l is the --deliminator for the filename, default is "_"
* -C is the --coprocess Coprocess the specified imgtype with the imgtype specified in --match (e.g. coprocess NIR images with VIS).
* -f is the --meta (data) format map for example the default is "imgtype_camera_frame_zoom_id"
* -M is the --match metadata option, for example to select a certain zoom or angle. For example: 'imgtype:VIS,camera:SV,zoom:z500'
* -D is the --dates" option, to select a certain date range of data. YYYY-MM-DD-hh-mm-ss_YYYY-MM-DD-hh-mm-ss. If the second date is excluded then the current date is assumed.
* -s is the --db, sqlite database name
* -m is the --mask any image mask that you would like to provide
* -T is the --threads (cpus) you would like to use.
* -w is the --writeimg option, if True will write output images. default= False
* -c is the --create option to overwrite an sqlite database if it exists, if you are creating a new database or appending to database, do NOT add the -c flag
* -o is the --other_args option, used to pass non-standard options to the pipeline script. Must take the form `--other_args="--option1 value1 --option2 value2"`


####If running as a command in a shell script

```bash
#!/bin/bash

#Here we are running a VIS top-view pipeline

time \
/home/nfahlgren/programs/plantcv/plantcv-pipeline.py \
-d /home/nfahlgren/projects/lemnatec/burnin2/images3 \
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z300_L1.py \
-t png \
-s burnin2.sqlite3 \
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images \
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z300_L1.png \
-f imgtype_camera_frame_zoom_id \
-M imgtype:VIS,camera:TV,zoom:z300 \
-C NIR \
-T 10 \
-w


#Here we are running a second VIS top-view pipeline at a second zoom level

time \
/home/nfahlgren/programs/plantcv/plantcv-pipeline.py \
-d /home/nfahlgren/projects/lemnatec/burnin2/images3 \
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z1000_L1.py \
-t png \
-s burnin2.sqlite3 \
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images \
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z1000_L1.png \
-f imgtype_camera_frame_zoom_id \
-M imgtype:VIS,camera:TV,zoom:z1000 \
-C NIR \
-T 10 \
-w
```

### Example Condor Jobfile

```
####################
# HTCondor job description file
####################

universe         = vanilla
executable       = /home/mgehan/plantcv/plantcv-pipeline.py
arguments        = -d /shares/tmockler_share/mgehan/LemnaTec/bnapus_phenotyping_katie/images-full -p /home/mgehan/kt-greenham-lemnatec/scripts/vis_nir_tv_z500_h2_e10000_brassica.py -s ktbrassica.sqlite3 -i /home/mgehan/kt-greenham-lemnatec/output/output500 -f imgtype_camera_zoom_lifter_gain_exposure_id -M imgtype:VIS,camera:TV,zoom:z500 -T 16 -C NIR -w
log              = $(Cluster).$(Process).log
output           = $(Cluster).$(Process).out
error            = $(Cluster).$(Process).error
request_cpus     = 16
notification     = always
nice_user        =False
accounting_group = $ENV(CONDOR_GROUP)
getenv           = true
####################

queue
```

### Running PlantCV pipelines over a flat directory of images

**Note:** We will try and update PlantCV so that it can run over flat directories in a more flexible manner.
But for now please follow the instructions on Running PlantCV over a flat directory carefully.

In order for PlantCV to scrape all of the necessary metadata from the image files, image files need to be named in a particular way.

**Image name might include:**

1. Plant ID
2. Timestamp
3. Measurement/Experiment Label
4. Camera Label

**Example Name :**

AABA002948-2014-03-14 03_29_45-Pilot_031014-VIS_TV_z3500.png

1. Plant ID = AABA002948
2. Timestamp = 2014-03-14 03_29_45
3. Measurement Label = Pilot_031014
4. Camera Label = VIS_TV_z3500

**Next, run images over a flat directory with images named as described above:**

We normally execute pipelines as a shell script or as a condor jobfile (or dagman workflow)

```bash
#!/bin/bash

#Here we are running a VIS top-view pipeline over a flat directory of images

#Image names for this example look like this: cam1-16-08-06_16:45_el1100s1_p19.jpg

/home/mgehan/plantcv/plantcv-pipeline.py \
-d /shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1 \
-a filename \
-p /home/mgehan/pat-edger/round1-python-pipelines/2016-08_pat-edger_brassica-cam1-splitimg.py \
-s edger-round1-brassica.sqlite3 \
-i /shares/mgehan_share/raw_data/raw_image/2016-08_pat-edger/data/split-round1/split-cam1/output \
-f camera_timestamp_id_other \
-t jpg \
-T 16 \
-w 


```
