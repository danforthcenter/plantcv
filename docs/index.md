# Welcome to the documentation for PlantCV

## Overview

[PlantCV](http://plantcv.danforthcenter.org) is composed of modular functions in order to be applicable to a 
variety of plant types and imaging systems. In the following documentation we will describe use of each function and 
provide tutorials on how each function is used in the context of an overall image-processing pipeline. The initial 
releases of PlantCV have been designed for processing images from visible spectrum cameras ('VIS'), near-infrared 
cameras ('NIR'), and excitation imaging fluorometers ('PSII'; see note below). Development of PlantCV is 
ongoing---we encourage input from the greater plant phenomics community. Please post questions and comments on the 
[GitHub issues page](https://github.com/danforthcenter/plantcv/issues).

**Note**: At the Danforth Center we refer to our excitation imaging 
fluorometer (PSII) camera system as 'FLU' internally. But others have 
previously published on their steady-state fluorescence imaging systems 
(a different type of fluorescence imaging system) and referred to it as 
'FLU'. We are working to make the naming changes of our functions from 
'FLU' to 'PSII' to try and prevent further confusion.

## Getting started

The documentation can be navigated using the sidebar table of contents. Documentation for individual PlantCV functions
are listed under the headings "Package plantcv" and "Package plantcv.learn." For general information on installation,
updating, and other questions, see:

* [Installing PlantCV](installation.md)
* [Updating PlantCV](updating.md)
* [Frequently Asked Questions](faq.md)
* [General Approaches to Image Analysis with PlantCV](analysis_approach.md)
* [Using Jupyter Notebooks with PlantCV](jupyter.md)
* [Summary of Output Measurements and Database Structure](output_measurements.md)

Also see our tutorials for more detailed overviews of using PlantCV for specific tasks:

* [VIS/RGB Image Processing](vis_tutorial.md)
* [Near-Infrared Image Processing](nir_tutorial.md)
* [PSII Image Processing](psII_tutorial.md)
* [VIS / NIR Dual Pipelines](vis_nir_tutorial.md)
* [Multi Plant Image Processing](multi-plant_tutorial.md)
* [Machine Learning Tutorial](machine_learning_tutorial.md)
* [Parallel Image Processing](pipeline_parallel.md)
* [Exporting Data for Downstream Analysis](db-exporter.md)

We have added interactive documentation (the link takes up to a few minutes to load so be patient please),
so you can test out pipelines and even upload your own images to test on.

* [Interactive Documentation](https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=index.ipynb)

If you are interested in contributing to PlantCV, please see:

* [Contribution Guide](CONTRIBUTING.md)
* [Documentation Guide](documentation.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

## Versions

The documentation defaults to the `latest` version of PlantCV which is the latest
commit in the `master` code branch.
Documentation for all releases from v1.1 on are also available
via the standard Read the Docs popup/pulldown menu (sidebar, bottom left).

[Return to the PlantCV homepage](http://plantcv.danforthcenter.org)
