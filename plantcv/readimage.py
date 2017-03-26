# Read image

import os
import cv2
from . import fatal_error


def readimage(filename):
    """Read image from file.

    Inputs:
    filename = name of image file

    Returns:
    img      = image object as numpy array
    path     = path to image file
    img_name = name of image file

    :param filename: str
    :return img: numpy array
    :return path: str
    :return img_name: str
    """

    try:
        img = cv2.imread(filename)
    except:
        fatal_error("Cannot open " + filename)

    # Split path from filename
    path, img_name = os.path.split(filename)

    return img, path, img_name
