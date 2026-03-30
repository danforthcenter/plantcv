# Read image

import os
import cv2
import numpy as np
import pandas as pd
import nd2
import flyr
from plantcv.plantcv import fatal_error
from plantcv.plantcv._globals import params
from plantcv.plantcv.hyperspectral.read_data import read_data
from plantcv.plantcv._debug import _debug


def readimage(filename, mode="native"):
    """Read image from file.

    Parameters
    ----------
    filename : str
        Name of image file
    mode : str
        Mode of readimage. Options: "native", "rgb", "rgba", "gray", "normalize",
        "csv", "envi", "arcgis", "nd2", "thermal"

    Returns
    -------
    img : numpy.ndarray
        Image object as numpy array
    path : str
        Path to image file
    img_name : str
        Name of image file
    """
    if mode.upper() in ("GRAY", "GREY"):
        img = cv2.imread(filename, 0)
    elif mode.upper() == "RGB":
        img = cv2.imread(filename)
    elif mode.upper() == "RGBA":
        img = cv2.imread(filename, -1)
    elif mode.upper() == "NORMALIZE":
        img = cv2.normalize(cv2.imread(filename, cv2.IMREAD_UNCHANGED), None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    elif mode.upper() == "CSV":
        inputarray = pd.read_csv(filename, sep=',', header=None)
        img = inputarray.values
    elif mode.upper() in ["ENVI", "ARCGIS"]:
        array_data = read_data(filename, mode=mode)
        return array_data
    elif mode.upper() == "ND2":
        img = nd2.imread(filename)
    elif mode.upper() == "THERMAL":
        img = flyr.unpack(filename).celsius
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
