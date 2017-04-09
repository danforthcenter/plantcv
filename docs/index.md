# Welcome to the documentation for PlantCV

## Getting started

[PlantCV](http://plantcv.danforthcenter.org) is composed of modular functions in order to be applicable to a 
variety of plant types and imaging systems.
In the following documentation
we will describe use of each function and provide tutorials on how each 
function is used in the context of an overall image-processing pipeline. 
The initial releases of PlantCV have been designed
for processing images
from visible spectrum cameras ('VIS'),
near-infrared cameras ('NIR'),
and excitation imaging fluorometers ('PSII'; see note below).
Development of PlantCV is ongoing---we encourage input
from the greater plant phenomics community.
Please post questions and comments on the [GitHub issues page](https://github.com/danforthcenter/plantcv/issues).

**Note**: At the Danforth Center we refer to our excitation imaging 
fluorometer (PSII) camera system as 'FLU' internally. But others have 
previously published on their steady-state fluorescence imaging systems 
(a different type of fluorescence imaging system) and referred to it as 
'FLU'. We are working to make the naming changes of our functions from 
'FLU' to 'PSII' to try and prevent further confusion.

## Versions

The documentation defaults to the `latest` version of PlantCV which is the latest
commit in the `master` code branch.
Documentation for all major releases from v1.1 on are also available.

[Return to the PlantCV homepage](http://plantcv.danforthcenter.org)
