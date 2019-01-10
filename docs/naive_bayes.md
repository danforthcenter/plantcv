## Naive Bayes Training Module

The modules in the `plantcv.learn` subpackage are not necessarily meant to be used directly. Instead,
each module is implemented in the `plantcv-train.py` script, but feel free to use these functions within your own
script if needed. See the [Machine Learning Tutorial](machine_learning_tutorial.md) for more details.

The naive_bayes function reads 8-bit RGB images from the input image directory and corresponding binary mask images
from the input mask directory. The input color images are converted the HSV colorspace, and using the masks, the input 
RGB images are split into foreground (plant) and background pixels. A random sampling of 10% of the foreground pixels 
and the same number of background pixels are kept. A Kernel Density Estimator (KDE) using a Gaussian kernel is used
to estimate the Probability Density Function (PDF) for each of the hue, saturation, and value channels for the
foreground and background classes. The PDFs, sampled at each of the possible 8-bit (256) intensity values are written
to the output file and can be used with the [naive Bayes classifier](naive_bayes_classifier.md) to segment plants.

**naive_bayes(*imgdir, maskdir, outfile, mkplots=False*)**

**returns** none

- **Parameters:**
    - imgdir  - (str): Path to a directory of original 8-bit RGB images.
    - maskdir - (str): Path to a directory of binary mask images. Mask images must have the same name as their 
    corresponding color images.
    - outfile - (str): Name of the output text file that will store the color channel probability density functions.
    - mkplots - (bool): Make PDF plots, True or False (default).
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In Machine Learning Tutorial](machine_learning_tutorial.md)
