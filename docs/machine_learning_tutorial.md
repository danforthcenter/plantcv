## Tutorial: Machine Learning

Machine learning methods can be used to train a trainable classifier to detect features of interest. In the tutorial
below we describe how to train and use the first trainable classifier we have made available in PlantCV. See the 
[naive Bayes classifier](naive_bayes_classifier.md) documentation for more details on the methodology.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danforthcenter/plantcv-binder.git/master?filepath=notebooks/machine_learning.ipynb) Check out our interactive machine learning tutorial! 

### Naive Bayes

The naive Bayes approach used here can be trained to label pixels as plant or background. In other words, given a color image it can be
trained to output a binary image where background is labeled as black (0) and plant is labeled
as white (255). The goal is to replace the need to set [binary threshold](binary_threshold.md) values manually.

To train the classifier, we need to label a relatively small set of images using a binary mask.
We can use PlantCV to create a binary mask for a set of input images using the methods described in the 
[VIS tutorial](vis_tutorial.md). Alternatively, you can outline and create masks by hand.

For the purpose of this tutorial, we assume we are in a folder containing two subfolders, one containing original RGB
images, and one containing black and white masks that match the set of RGB images.

First, use `plantcv-train.py` to use the training images to output probability density functions (PDFs) for plant
and background.

```
plantcv-train.py naive_bayes --imgdir ./images --maskdir ./masks --outfile naive_bayes_pdfs.txt --plots

```

The output file from `plantcv-train.py` will contain one row for each color channel (hue, saturation, and value) for
each class (e.g. plant and background). The first and second column are the class and channel label, respectively. The
remaining 256 columns contain the p-value from the PDFs for each intensity value observable in an 8-bit image (0-255).

Once we have the `plantcv-train.py` output file, we can classify pixels in a color image in PlantCV.

```python
from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file), 
# or "plot" (Jupyter Notebooks or X11)
pcv.params.debug = "print"

# Read in a color image
img, path, filename = pcv.readimage("color_image.png")

# Classify the pixels as plant or background
masks = pcv.naive_bayes_classifier(img, pdf_file="naive_bayes_pdfs.txt")

```

See the [naive Bayes classifier](naive_bayes_classifier.md) documentation for example input/output.

### Naive Bayes Multiclass

The naive Bayes multiclass approach is an extension of the naive Bayes approach described above. Just like the approach
above, it can be trained to output binary images given an input color image. Unlike the naive Bayes method above, the
naive Bayes multiclass approach can be trained to classify two or more classes, defined by the user. Additionally,
the naive Bayes multiclass method is trained using colors sparsely sampled from images rather than the need to label all
pixels in a given image.

To train the classifier, we need to build a table of red, green, and blue color values for pixels sampled evenly from
each class. *You need a minimum of 2 classes.* The idea here is to collect a relevant sample of pixel color data for each class. The size of the sample 
needed to build robust probability density functions for each class will depend on a number of factors, including the
variability in class colors and imaging quality/reproducibility. To collect pixel color data we currently use the [Pixel
Inspection Tool](https://imagej.nih.gov/ij/plugins/pixel-tool/index.html) in [ImageJ](https://imagej.nih.gov/ij/). 

To collect pixel samples, open the color image in ImageJ.

![Screenshot](img/tutorial_images/machine_learning/color_image.jpg)

Use the Pixel Inspector Tool to select regions of the image belonging to a single class. Clicking on a pixel in the image will give you a set of R,G,B values for a window of pixels around the central pixel. In this example, nine pixels are sampled with one click but the radius is adjustable in "Prefs".

![Screenshot](img/tutorial_images/machine_learning/imagej_pixel_inspector.jpg)

From the "Pixel Values" window you can copy the values and paste them into a text editor such as Notepad on Windows, TextEditor on MacOS, [Atom](https://atom.io/) or [VS Code](https://code.visualstudio.com/). The R,G,B values for a class should be proceeded with a line that contains the class name preceded by a `#`.
The file contents should look like this:

```
#plant
93,166,104	94,150,101	82,137,91
86,154,102	87,145,94	79,137,95
116,185,135	103,172,126	96,166,126
#postule
216,130,52	217,129,51	221,132,53
218,131,53	223,132,54	221,132,53
219,131,54	221,132,54	225,135,56
#chlorosis
255,242,89	255,241,90	255,239,87
254,239,87	255,241,90	254,238,88
255,241,88	253,238,87	255,240,90
#background
31,42,54	42,52,60	40,49,58
28,38,51	32,43,55	36,47,59
24,35,45	30,40,50	37,49,66
```

Next, each class needs to be in its own column for the `plantcv-train`. You can use a utility script provided with PlantCV in `plantcv-utils.py` that will convert the data from the Pixel Inspector to a table for the bayes training algorithm.

```
python plantcv-utils.py tabulate_bayes_classes -i pixel_inspector_rgb_values.txt -o bayes_classes.tsv
```

A note if you are using Windows you will need to specify the whole path to `plantcv-utils.py`. For example with an Anaconda installation it would be `python %CONDA_PREFIX%/Scripts/plantcv-utils.py tabulate_bayes_classes -i pixel_inspector_rgb_values.txt -o bayes_classes.tsv`

where `pixel_inspector_rgb_values.txt` is the file with the pixel values you created above and `bayes_classes.tsv` is the file with the table for `plantcv-train.py`.

An example table built from pixel samples for use in `plantcv-train.py` looks like this:

```
plant	postule	chlorosis	background
93,166,104	216,130,52	255,242,89	31,42,54
94,150,101	217,129,51	255,241,90	42,52,60
82,137,91	221,132,53	255,239,87	40,49,58
86,154,102	218,131,53	254,239,87	28,38,51
87,145,94	223,132,54	255,241,90	32,43,55
79,137,95	221,132,53	254,238,88	36,47,59
116,185,135	219,131,54	255,241,88	24,35,45
103,172,126	221,132,54	253,238,87	30,40,50
96,166,126	225,135,56	255,240,90	37,49,66
```

Each column in the tab-delimited table is a feature class (in this example, plant, pustule, chlorosis, or background)
and each cell is a comma-separated red, green, and blue triplet for a pixel.

Like the naive Bayes method described above, use `plantcv-train.py` to use the pixel samples to output probability density functions (PDFs)
for each class.

```
plantcv-train.py naive_bayes_multiclass --file pixel_samples.txt --outfile naive_bayes_pdfs.txt --plots

```

The output file from `plantcv-train.py` will contain one row for each color channel (hue, saturation, and value) for
each class. The first and second column are the class and channel label, respectively. The
remaining 256 columns contain the p-value from the PDFs for each intensity value observable in an 8-bit image (0-255).

Once we have the `plantcv-train.py` output file, we can classify pixels in a color image in PlantCV using the same
function described in the naive Bayes section above. A plotting function [pcv.visualize.colorize_masks](visualize_colorize_masks.md) 
allows users to choose colors for each class.

![Screenshot](img/tutorial_images/machine_learning/classified_image.jpg)

### Parallelizing a Workflow that uses a Bayes Classifier

To parallelize the naive Bayes methods described above, construct a workflow script following the guidelines in the 
[workflow parallelization tutorial](pipeline_parallel.md), but with an additional argument provided for the probability
density functions file output by `plantcv-train.py`. For example:

```python
#!/usr/bin/env python
import os 
import argparse
from plantcv import plantcv as pcv

# Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    parser.add_argument("-p", "--pdfs", help="Naive Bayes PDF file.", required=True)
    args = parser.parse_args()
    return args


def main():
    # Get options
    args = options()
    
    # Initialize device counter
    pcv.params.debug = args.debug
    
    # Read in the input image
    vis, path, filename = pcv.readimage(filename=args.image)
    
    # Classify each pixel as plant or background (background and system components)
    masks = pcv.naive_bayes_classifier(rgb_img=vis, pdf_file=args.pdfs)
    colored_img = pcv.visualize.colorize_masks(masks=[masks['plant'], masks['pustule'], masks['background'], masks['chlorosis']], 
                                               colors=['green', 'red', 'black', 'blue'])
                                               
    # Print out the colorized figure that got created 
    pcv.print_image(colored_img, os.path.join(args.outdir, filename))
    
    # Additional steps in the workflow go here
    
```

Then run `plantcv-workflow.py` with options set based on the input images, but where the naive Bayes PDF file is input
using the `--other_args` flag, for example:

```bash
plantcv-workflow.py \
--dir ./my-images \
--workflow my-naive-bayes-script.py \
--db my-db.sqlite3 \
--outdir . \
--meta imgtype_camera_timestamp \
--create \
--other_args="--pdfs naive_bayes_pdfs.txt"

```

*  Always test workflows (preferably with -D flag set to 'print') on a smaller dataset before running over a full image set.* You can create a sample of your images with [`plantcv-utils.py sample_images`](tools.md).
