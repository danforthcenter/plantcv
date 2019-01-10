## Naive Bayes Multiclass Training Module

The modules in the `plantcv.learn` subpackage are not necessarily meant to be used directly. Instead,
each module is implemented in the `plantcv-train.py` script, but feel free to use these functions within your own
script if needed. See the [Machine Learning Tutorial](machine_learning_tutorial.md) for more details.

The naive_bayes_multiclass function reads a text file containing a tab-delimited table. Each column is a user-defined
feature class (e.g. plant, background, etc.). Each cell in the table is a comma-separated list of red, green, and blue
values for a single pixel that is representative of the class. The table needs to contain enough pixel samples (rows) so
that the training method can accurately estimate the true population distribution of color values for each class. The
naive_bayes_multiclass function converts the RGB values to the HSV colorspace. A Kernel Density Estimator (KDE) using a 
Gaussian kernel is used to estimate the Probability Density Function (PDF) for each of the hue, saturation, and value 
channels for the two or more input classes. The PDFs, sampled at each of the possible 8-bit (256) intensity values are 
written to the output file and can be used with the [naive Bayes classifier](naive_bayes_classifier.md) to segment the
user-defined classes. For more information about building the input sample file, see the 
[Machine Learning Tutorial](machine_learning_tutorial.md).

**naive_bayes_multiclass(*samples_file, outfile, mkplots=False*)**

**returns** none

- **Parameters:**
    - samples_file  - (str): Path to a text file containing a table of RGB values sampled for each feature class.
    - outfile       - (str): Name of the output text file that will store the color channel probability density functions.
    - mkplots       - (bool): Make PDF plots, True or False (default).
- **Context:**
    - Used to help differentiate two or more feature classes
- **Example use:**
    - [Use In Machine Learning Tutorial](machine_learning_tutorial.md)
