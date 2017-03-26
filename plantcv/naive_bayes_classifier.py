# Classify pixels as plant or non-plant using the naive Bayes method written by Arash Abbasi,
# adapted for Python by Noah Fahlgren

import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import fatal_error


def naive_bayes_classifier(img, pdf_file, device, debug=None):
    """Use the Naive Bayes classifier to output a plant binary mask.

    Inputs:
    img      = image object (NumPy ndarray), BGR colorspace
    pdf_file = filename of file containing PDFs output from the Naive Bayes training method (see plantcv-train.py)
    device   = device number. Used to count steps in the pipeline
    debug    = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device   = device number
    mask     = binary mask (ndarray)

    :param img: ndarray
    :param pdf_file: str
    :param device: int
    :param debug: str
    :return device: int
    :return mask: ndarray
    """
    device += 1

    # Initialize PDF dictionary. There are two classes: plant and background (non-plant)
    pdfs = {"plant": {}, "background": {}}
    # Read the PDF file
    pf = open(pdf_file, "r")
    # Read the first line (header)
    pf.readline()
    # Read each line of the file and parse the PDFs, store in the PDF dictionary
    for row in pf:
        # Remove newline character
        row = row.rstrip("\n")
        # Split the row into columns on tab characters
        cols = row.split("\t")
        # Make sure there are the correct number of columns (i.e. is this a valid PDF file?)
        if len(cols) != 258:
            fatal_error("Naive Bayes PDF file is not formatted correctly. Error on line:\n" + row)
        # Store the PDFs. Column 0 is the class, Column 1 is the color channel, the rest are p at
        # intensity values 0-255. Cast text p values as float
        pdfs[cols[0]][cols[1]] = [float(i) for i in cols[2:]]

    # Split the input BGR image into component channels for BGR, HSV, and LAB colorspaces
    # b, g, r = cv2.split(img)
    h, s, v = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    # l, gm, by = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))

    # Calculate the dimensions of the input image
    width, height, depth = np.shape(img)

    # Initialize an empty ndarray for plant and background. These will be used to store the joint probabilities
    plant = np.zeros([width, height])
    bg = np.zeros([width, height])

    # Loop over the image coordinates (each i, j pixel)
    for i in range(0, width):
        for j in range(0, height):
            # Calculate the joint probability that this is a plant pixel
            plant[i][j] = pdfs["plant"]["hue"][h[i][j]] * pdfs["plant"]["saturation"][s[i][j]] * \
                          pdfs["plant"]["value"][v[i][j]]
            # Calculate the joint probability that this is a background pixel
            bg[i][j] = pdfs["background"]["hue"][h[i][j]] * pdfs["background"]["saturation"][s[i][j]] * \
                       pdfs["background"]["value"][v[i][j]]

    # Initialize an empty mask ndarray
    mask = np.zeros([width, height])
    # Set pixel intensities to 255 (white) where the probability of the pixel being plant is greater than the
    # probability of the pixel being background
    mask[np.where(plant > bg)] = 255

    # Print or plot the mask if debug is not None
    if debug == 'print':
        print_image(mask, (str(device) + '_naive_bayes_mask.jpg'))
    elif debug == 'plot':
        plot_image(mask, cmap='gray')

    return device, mask
