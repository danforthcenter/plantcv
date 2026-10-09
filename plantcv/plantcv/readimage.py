# Read image

import os
import cv2
import numpy as np
import pandas as pd
import nd2
import flyr
from PIL import Image
from pillow_heif import register_heif_opener
from plantcv.plantcv.fatal_error import fatal_error
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
        "csv", "envi", "arcgis", "nd2", "thermal", "heic"

    Returns
    -------
    img : numpy.ndarray
        Image object as numpy array
    path : str
        Path to image file
    img_name : str
        Name of image file
    """
    reader_function = {
        "GRAY" : _read_gray,
        "GREY" : _read_gray,
        "RGB" : _read_rgb,
        "RGBA" : _read_rgba,
        "NORMALIZE" : _read_normalize,
        "CSV" : _read_csv_image,
        "ND2" : _read_nd2,
        "THERMAL" : _read_thermal,
        "HEIC" : _read_heic,
        "NATIVE" : _read_native
    }

    if os.path.splitext(filename)[1].upper() == ".HEIC" and mode == "native":
        mode = "heic"
    # read image
    if mode.upper() in ["ENVI", "ARCGIS"]:
        img = read_data(filename, mode)
        return img
    img = reader_function.get(mode.upper())(filename)

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


def _read_gray(filename):
    """read gray image"""
    img = cv2.imread(filename, 0)
    return img


def _read_rgb(filename):
    """read rgb image"""
    img = cv2.imread(filename)
    return img


def _read_rgba(filename):
    """read rgba image"""
    img = cv2.imread(filename, -1)
    return img


def _read_normalize(filename):
    """read rgba image"""
    img = cv2.normalize(cv2.imread(filename, cv2.IMREAD_UNCHANGED), None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img


def _read_csv_image(filename):
    """read csv image"""
    inputarray = pd.read_csv(filename, sep=',', header=None)
    img = inputarray.values
    return img


def _read_nd2(filename):
    """read nd2 image"""
    img = nd2.imread(filename)
    return img


def _read_thermal(filename):
    """read thermal image"""
    img = flyr.unpack(filename).celsius
    return img


def _read_heic(filename):
    """read heic image"""
    register_heif_opener()
    image = Image.open(filename)
    image_array = np.asarray(image)
    img = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    return img


def _read_native(filename):
    """read default image"""
    img = cv2.imread(filename, -1)
    return img
