## Naive Bayes Classifier

Creates a binary (labeled) image from a color image based on the learned statistical information from
a training set. From the training set we calculate the probability density function (PDF) for the Random Variables
Plant (P) and Background (B), each containing the Random Variables Hue (H), Saturation (S), and Value (V)
(color channels). Given these PDFs, we calculate the joint probability a pixel is from the Random Variable P or B using
Bayes Theorem with the naive assumption that the Random Variables are independent (for convenience). Output pixels are
labeled as plant (255) or background (0) if P(Pixel = plant) > P(Pixel = background).

**naive_bayes_classifier(*img, pdf_file, device, debug=None*)**

**returns** device, mask

- **Parameters:**
    - img - (ndarray): color image (BGR)
    - pdf_file - (str): output file containing PDFs from `plantcv-train.py`
    - device - (int): counter for image processing steps
    - debug - (str): None, "print", or "plot". Print = save to file, Plot = print to screen. Default = None
- **Context:**
    - Used to help differentiate plant and background
- **Example use:**
    - [Use In Machine Learning Tutorial](machine_learning_tutorial.md)
    
**Original image**

![Screenshot](img/documentation_images/naive_bayes_classifier/original_image.jpg)


```python
from plantcv import plantcv as pcv

# Create binary image from a gray image based on threshold values. Targeting light objects in the image.
device, mask = pcv.naive_bayes_classifier(img, "naive_bayes_pdfs.txt", device=0, debug="print")
```

The output mask is a dictionary with the keys being the class names and the values being the corresponding binary masks.

**Binary mask image**

![Screenshot](img/documentation_images/naive_bayes_classifier/mask_image.jpg)
