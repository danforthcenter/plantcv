# SPICE
Sparsity Promoting Iterated Constrained Endmembers

***
NOTE: If the SPICE Algorithm is used in any publication or presentation, the following reference must be cited:

Zare, A.; Gader, P.; , "Sparsity Promoting Iterated Constrained Endmember Detection in Hyperspectral Imagery,"" IEEE Geoscience and Remote Sensing Letters, vol.4, no.3, pp.446-450, July 2007.

NOTE: If the code is used anywhere or in any presentation or publication, include the following reference:
Caleb Robey, Taylor Glenn, Alina Zare, & Paul Gader. (2018, October 24). GatorSense/SPICE_py v1.0 (Version v1.0). Zenodo. http://doi.org/10.5281/zenodo.1470878
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1470878.svg)](https://doi.org/10.5281/zenodo.1470878)


****

The SPICE Algorithm in Python is run using the function:

```python
from SPICE import *

endmembers, P = SPICE(inputData, parameters)
```

If you would like to use the default parameters (described below), use the command:

`parameters = SPICEParameters()`

The inputData input is a DxM matrix of M input data points with D dimensions.  Each of the M pixels has D spectral bands.  Each pixel is a column vector.   

This form can be achieved from a three-dimensional hyperspectral numpy array using the following commands:

```python
import numpy as np

inputData = np.reshape(inputData, (inputData.shape[0]*inputData.shape[1], inputData.shape[2]))

```

The parameters input is a struct with the following fields:

    parameters.u :  This is the regularization parameter that trades off between the RSS and SPT terms.
    parameters.gamma : Gamma constant for the SPT term, controls the degree of sparsity desired
    parameters.changeThresh : Stopping Criteria, Set this to the desired change threshold for the objective function
    parameters.M : Number of Initial Endmembers
    parameters.iterationCap : Maximum Number of Iterations
    parameters.endmemberPruneThreshold : This is the pruning threshold for endmembers
    parameters.produceDisplay : Set this to 1 if progress display is desired, 0 otherwise
    parameters.initEM = None : By setting this to None, the algorithm randomly selects initial endmembers from the input data. You can also provide initial endmembers by inputting a matrix of endmembers.  Every column is one endmember.  The number of endmembers should match parameters.M.

The parameters structure can be generated using the SPICEParameters.m function.  
unmix2, which is imported with ```from SPICE import *```, is a required helper function which unmixes the data points given the endmembers. 

**Note: Often the parameters must be adjusted for a particular data set. Generally, u is set to between 0.001 and 0.1 depending on noise levels in the data. gamma is generally set to a value between 1 and 10 depending on the data set.   We have also found that SPICE has improved performance if the data has been normalized between 0 and 1 before running SPICE (e.g. Subtracting the minimum and then dividing by the max OR normalizing each spectrum by its L2 norm).**

### Running the Demo
This repository includes sample data in the form of a pickle file called "hsi_data.pkl". This contains a hyperspectral data cube, which can be analyzed by the SPICE algorithm. 

To run the algorithm, use the command:

```python spice_py_demo.py```

The algorithm should run for no more than 40 iterations (typically much less) and will detect 4 or 5 endmembers, depending on 
the randomized endmember initialization parameter. After the algorithm is finished, you will be prompted to choose whether
you would like to graph the output. Choose yes (Y) and a figure will appear with the proportions of each endmember in 
the context of the original image. Expand this window for a cleaner view of the plots. After closing this figure window,
a plot of the wavelength and reflectance of each endmember will appear.

### Requirements

It is recommended that you use a python virtual environment for this project using the following commands from the 
SPICE_py directory:
* ```pip install virtualenv``` (If you don't have the package installed already)
* ```python3 -m venv spice_env``` (Linux/Mac OSX)
* ```source ./spice_env/bin/activate``` (Linux/Mac OSX)
* ```python -m venv spice_env``` (Windows)
* ```spice_env\Scripts\activate.bat``` (Windows)

This program uses the python packages in the requirements.txt file. Those can be installed using the command:

```pip install -r requirements.txt``` 

This must also be done from the SPICE_py directory. If you run into issues, particularly on Windows, you may want to
consider using conda forge and conda environments for the install.

Note: This code uses qpsolvers (see the QPP.py file) by Stephane Caron <stephane.caron@normalesup.org>


### Questions
If you have any questions, please contact:  

Alina Zare  
Electrical and Computer Engineering  
University of Florida    
azare [at] ufl.edu  

% This product is Copyright (c) 2018 
% All rights reserved.

