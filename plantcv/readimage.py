# Read image

import os
import cv2
from . import fatal_error
from . import print_image
from . import plot_image


def readimage(filename, debug=None):
    """Read image from file.

    Inputs:
    filename = name of image file
    debug    = None, print, or plot. Print = save to file, Plot = print to screen.

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

    if debug == "print":
        print_image(img, "input_image.png")
    elif debug == "plot":
        plot_image(img)

    return img, path, img_name
