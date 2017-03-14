## Tutorial: Machine Learning

Machine learning methods can be used to train a trainable classifier to detect features of interest. In the tutorial
below we describe how to train and use the first trainable classifier we have made available in PlantCV. See the 
[Naive Bayes Classifier](naive_bayes_classifier.md) documentation for more details on the methodology.

### Naive Bayes

The naive Bayes approach used here can be trained to label pixels as plant or background. In other words, it can be
trained to, given a color image, output a binary image where background is labeled as black (0) and plant is labeled
as white (255). The goal is to replace the need to set [binary threshold](binary_threshold.md) values manually.

To train the classifier, we need to label a relatively small set of images using a binary mask (just like above).
We can use PlantCV to create a binary mask for a set of input images using the methods described in the 
[VIS Tutorial](vis_tutorial.md).

For the purpose of this tutorial, we assume we are in a folder containing two subfolders, one containing original RGB
images, and one containing black and white masks that match the set of RGB images.

First, use `plantcv-train.py` to use the training images to output probability density functions (PDFs) for plant
and background.

```
plantcv-train.py --imgdir ./images --maskdir ./masks --method naive_bayes --outfile naive_bayes_pdfs.txt
```

The output file from `plantcv-train.py` will contain one row for each color channel (hue, saturation, and value) for
each class (plant and background). The first and second column are the class and channel label, respectively. The
remaining 256 columns contain the p-value from the PDFs for each intensity value observable in an 8-bit image (0-255).

Once we have the `plantcv-train.py` output file, we can classify pixels in a color image in PlantCV.

```python
import plantcv as pcv

# Read in a color image
img, path, filename = pcv.readimage("color_image.png")

# Classify the pixels as plant or background
device, mask = pcv.naive_bayes_classifier(img, pdf_file="naive_bayes_pdfs.txt", device=0, debug="print")
```

See the [Naive Bayes Classifier](naive_bayes_classifier.md) documentation for example input/output.
