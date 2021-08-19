# Welcome to the documentation for PlantCV

## Overview

[PlantCV](http://plantcv.danforthcenter.org) is composed of modular functions in order to be applicable to a 
variety of plant types and imaging systems. In the following documentation we will describe use of each function and 
provide tutorials on how each function is used in the context of an overall image-processing workflow. PlantCV 
currently supports the analysis of standard RGB color images (aka "VIS"), standard grayscale images (e.g. 
near-infrared, "NIR"), thermal infrared images, grayscale images from chlorophyll fluorescence imaging systems 
("PSII"), and hyperspectral ("ENVI") images. Support for additional image types is under development. Development of 
PlantCV is ongoing---we encourage input from the greater plant phenomics community. Please post questions and comments 
on the [GitHub issues page](https://github.com/danforthcenter/plantcv/issues).

## Getting started

The documentation can be navigated using the sidebar table of contents. Documentation for individual PlantCV functions
are listed under the headings "PlantCV Namespace". For general information on installation,
updating, and other questions, see:

* [Installing PlantCV](installation.md)
* [Updating PlantCV](updating.md)
* [Frequently Asked Questions](faq.md)
* [General Approaches to Image Analysis with PlantCV](analysis_approach.md)
* [Using Jupyter Notebooks with PlantCV](jupyter.md)
* [Summary of Output Measurements and Database Structure](output_measurements.md)

## Tutorials 

We have added interactive documentation (the link takes up to a few minutes to load so be patient please),
so you can test out workflows and even upload your own images to test on.

* [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=index.ipynb) Check out our interactive tutorials! 

Also see our tutorials documentation pages for more detailed overviews of using PlantCV for specific tasks:

* [VIS/RGB Image Processing](tutorials/vis_tutorial.md)
* [Near-Infrared Image Processing](tutorials/nir_tutorial.md)
* [PSII Image Processing](tutorials/psII_tutorial.md)
* [VIS / NIR Dual Workflows](tutorials/vis_nir_tutorial.md)
* [Multi Plant Image Processing](tutorials/multi-plant_tutorial.md)
* [Morphology Package](tutorials/morphology_tutorial.md) 
* [Thermal Image Processing](tutorials/thermal_tutorial.md)
* [Hyperspectral Image Processing](tutorials/hyperspectral_tutorial.md)
* [Machine Learning Tutorial](tutorials/machine_learning_tutorial.md)
* [Parallel Image Processing](pipeline_parallel.md)
* [Exporting Data for Downstream Analysis](db-exporter.md)

## Contributing 

If you are interested in contributing to PlantCV, please see:

* [Contribution Guide](CONTRIBUTING.md)
* [Documentation Guide](documentation.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

## Versions

The documentation defaults to the `stable` version of PlantCV which is the current release version available from
PyPI and Bioconda. Documentation for all releases from v1.1 on are also available via the standard Read the Docs 
popup/pulldown menu (bottom right corner). Select the `latest` version to get the most up-to-date documentation
associated with the current code in GitHub.

[Return to the PlantCV homepage](http://plantcv.danforthcenter.org)
