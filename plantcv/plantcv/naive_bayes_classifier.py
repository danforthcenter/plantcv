# Classify pixels as plant or non-plant using the naive Bayes method written by Arash Abbasi,
# adapted for Python by Noah Fahlgren

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def naive_bayes_classifier(rgb_img, pdf_file):
    """
    Use the Naive Bayes classifier to output a plant binary mask.

    Inputs:
    rgb_img      = RGB image data
    pdf_file = filename of file containing PDFs output from the Naive Bayes training method (see plantcv-train.py)

    Returns:
    mask     = Dictionary of binary masks

    :param rgb_img: numpy.ndarray
    :param pdf_file: str
    :return masks: dict
    """

    # Initialize PDF dictionary
    pdfs = {}
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
        class_name = cols[0]
        channel = cols[1]
        if class_name not in pdfs:
            pdfs[class_name] = {}
        pdfs[class_name][channel] = [float(i) for i in cols[2:]]

    # Split the input BGR image into component channels for BGR, HSV, and LAB colorspaces
    h, s, v = cv2.split(cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV))

    # Calculate the dimensions of the input image
    width, height, depth = np.shape(rgb_img)

    # Initialize an empty ndarray for plant and background. These will be used to store the joint probabilities
    px_p = {}
    for class_name in pdfs.keys():
        px_p[class_name] = np.zeros([width, height])

    # Loop over the image coordinates (each i, j pixel)
    for i in range(0, width):
        for j in range(0, height):
            for class_name in pdfs.keys():
                # Calculate the joint probability that this is in the class
                px_p[class_name][i][j] = pdfs[class_name]["hue"][h[i][j]] * pdfs[class_name]["saturation"][s[i][j]] * \
                    pdfs[class_name]["value"][v[i][j]]

    # Initialize empty masks
    masks = {}
    for class_name in pdfs.keys():
        masks[class_name] = np.zeros([width, height], dtype=np.uint8)
    # Set pixel intensities to 255 (white) for the mask where the class has the highest probability
    for class_name in masks:
        background_classes = []
        for name in masks:
            if class_name is not name:
                background_classes.append(px_p[name])
        background_class = np.maximum.reduce(background_classes)
        masks[class_name][np.where(px_p[class_name] > background_class)] = 255

    # Print or plot the mask if debug is not None
    if params.debug is not None:
        for class_name, mask in masks.items():
            _debug(visual=mask,
                   filename=os.path.join(params.debug_outdir, str(params.device) +
                                         "_naive_bayes_" + class_name + "_mask.png"),
                   cmap='gray')

    return masks
