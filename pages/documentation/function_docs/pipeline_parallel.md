---
layout: docs
title: Documentation
subtitle: Pipeline Parallel
---

## Tutorial: Pipeline Parallelization

**<font color='red'>Warning:</font>** Pipelines should be optimized to an image test-set before running a whole data-set.
See Pipeline Tutorial [here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html).
Our image download tool, which talks a LemnaTec database system can be found [here](https://github.com/danforthcenter/PhenoFront).
Our download tool has a specific file structure, which may be different than yours unless you are using our tool, but we also have instructions
to run PlantCV over a flat file directory (just keep this in mind).

**Running PlantCV over PhenoFront image data-set structure**

We normally execute pipelines in a shell script (remember run shell script in the background using screen or tmux)

* **First call the image\_analysis.pl script that does the parallelization**
* **-d flag is the directory of images**
* **-p flag is the pipeline that you are going to run over the images see [vis tutorial here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
and [flu tutorial here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/flu_tutorial.html)**
* **-t is the image type tag vis\_tv, vis\_sv, flu\_tv, nir\_sv, nir\_tv**
* **-z is the zoom level**
* **-s is the name of your sqlite database**
* **-i is your desired location for the output images**
* **-m is any image mask that you would like to provide**
* **-T is the number of threads you'd like to use (there seems to be a Python limitation of 10 threads)**
* **-c is to create the sqlite database, if you  are appending a database, do not add the -c flag**


```sh

#!/bin/bash

#Here we are running a VIS top-view pipeline

time\
/home/nfahlgren/programs/plantcv/scripts/image_analysis/image_analysis.pl\
-d /home/nfahlgren/projects/lemnatec/burnin2/images3\
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z300_L1.py\
-t vis_tv\
-z 300\
-s burnin2.sqlite3\
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images\
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z300_L1.png\
-T 10\
-c

#Here we are running a second VIS top-view pipeline at a second zoom level

time\
/home/nfahlgren/programs/plantcv/scripts/image_analysis/image_analysis.pl\
-d /home/nfahlgren/projects/lemnatec/burnin2/images3\
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z1000_L1.py\
-t vis_tv\
-z 1000\
-s burnin2.sqlite3\
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images\
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z1000_L1.png\
-T 10\

```

**To execute the shell script on the command line (in screen or tmux)**

<font color='orange'>[mgehan@pegasus LemnaTec]$</font> sh name\_of\_shell\_script.sh


**Running PlantCV piplines over a flat directory of images**

**<font color='blue'>Note:</font>** We will try and update PlantCV so that it can run over flat directories in a more flexible manner.
But for now please follow the instructions on Running PlantCV over a flat directory carefully.

In order for PlantCV to scrape all of the necessary metadata from the image files, image files need to be named in a particular way.

**Image name must include:**

1. Plant ID
2. Timestamp
3. Measurement/Experiment Label
4. Camera Label
5. Seperator should be a '-'

**Example Name :**

<font color='blue'>AABA002948</font>-<font color='red'>2014-03-14 03_29_45</font>-<font color='purple'>Pilot\_031014</font>-<font color='green'>VIS\_TV\_z3500</font>.png

1. <font color='blue'>Plant ID = AABA002948</font>
2. <font color='red'>Timestamp = 2014-03-14 03_29_45</font>
3. <font color='purple'>Measurement Label = Pilot\_031014</font>
4. <font color='green'>Camera Label = VIS\_TV\_z3500</font>

**Next, run images over a flat directory with images named as described above:**

We normally execute pipelines in a shell script (remember run shell script in the background using screen or tmux)

* **First call the image\_analysis.pl script that does the parallelization**
* **-d flag is the directory of images**
* **-p flag is the pipeline that you are going to run over the images see [vis tutorial here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/vis_tutorial.html)
and [flu tutorial here](http://plantcv.danforthcenter.org/pages/documentation/function_docs/flu_tutorial.html)**
* **-t is the image type tag vis\_tv, vis\_sv, flu\_tv, nir\_sv, nir\_tv**
* **-z is the zoom level**
* **-s is the name of your sqlite database**
* **-i is your desired location for the output images**
* **-m is any image mask that you would like to provide**
* **-T is the number of threads you'd like to use (there seems to be a Python limitation of 10 threads)**
* **-c is to create the sqlite database, if you  are appending a database, do not add the -c flag**
* **<font color='red'>-f is to run plantcv over a flat directory</font>**

```sh

#!/bin/bash

#Here we are running a VIS top-view pipeline

time\
/home/nfahlgren/programs/plantcv/scripts/image_analysis/image_analysis.pl\
-d /home/nfahlgren/projects/lemnatec/burnin2/images3\
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z300_L1.py\
-t vis_tv\
-z 300\
-s burnin2.sqlite3\
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images\
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z300_L1.png\
-T 10\
-c
-f

#Here we are running a second VIS top-view pipeline at a second zoom level

time\
/home/nfahlgren/programs/plantcv/scripts/image_analysis/image_analysis.pl\
-d /home/nfahlgren/projects/lemnatec/burnin2/images3\
-p /home/nfahlgren/programs/plantcv/scripts/image_analysis/vis_tv/vis_tv_z1000_L1.py\
-t vis_tv\
-z 1000\
-s burnin2.sqlite3\
-i /home/nfahlgren/projects/lemnatec/burnin2/plantcv3/images\
-m /home/nfahlgren/programs/plantcv/masks/vis_tv/mask_brass_tv_z1000_L1.png\
-T 10\
-f

```

**To execute the shell script on the command line (in screen or tmux)**

<font color='orange'>[mgehan@pegasus LemnaTec]$</font> sh name\_of\_shell\_script.sh