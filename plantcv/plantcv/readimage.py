# Read image

import os
import cv2
from plantcv.plantcv import fatal_error
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params

def readimage(filename):
    """Read image from file.

    Inputs:
    filename = name of image file

    Returns:
    img      = image object as numpy array
    path     = path to image file
    img_name = name of image file

    :param filename: str
    :param debug: str
    :return img: numpy array
    :return path: str
    :return img_name: str
    """

    img = cv2.imread(filename)

    if img is None:
        fatal_error("Failed to open " + filename)

    # Split path from filename
    path, img_name = os.path.split(filename)

    if params.debug == "print":
        print_image(img, os.path.join(params.debug_outdir, "input_image.png"))
    elif params.debug == "plot":
        plot_image(img)

    return img, path, img_name
