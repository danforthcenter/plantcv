# Read image

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv.hyperspectral import read_data
from plantcv.plantcv._debug import _debug


def readimage(filename, mode="native"):
    """Read image from file.

    Inputs:
    filename = name of image file
    mode     = mode of imread ("native", "rgb", "rgba", "gray", "csv", "envi")

    Returns:
    img      = image object as numpy array
    path     = path to image file
    img_name = name of image file

    :param filename: str
    :param mode: str
    :return img: numpy.ndarray
    :return path: str
    :return img_name: str
    """
    if mode.upper() == "GRAY" or mode.upper() == "GREY":
        img = cv2.imread(filename, 0)
    elif mode.upper() == "RGB":
        img = cv2.imread(filename)
    elif mode.upper() == "RGBA":
        img = cv2.imread(filename, -1)
    elif mode.upper() == "CSV":
        inputarray = pd.read_csv(filename, sep=',', header=None)
        img = inputarray.values
    elif mode.upper() == "ENVI":
        array_data = read_data(filename)
        return array_data
    else:
        img = cv2.imread(filename, -1)

    # Default to drop alpha channel if user doesn't specify 'rgba'
    if len(np.shape(img)) == 3 and np.shape(img)[2] == 4 and mode.upper() == "NATIVE":
        img = cv2.imread(filename)

    if img is None:
        fatal_error("Failed to open " + filename)

    # Split path from filename
    path, img_name = os.path.split(filename)

    # Debugging visualization
    _debug(visual=img, filename=os.path.join(params.debug_outdir, "input_image.png"))

    return img, path, img_name
