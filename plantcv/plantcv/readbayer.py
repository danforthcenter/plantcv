# Read image with bayer mosaic

import os
import cv2
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def readbayer(filename, bayerpattern='BG', alg='default'):
    """
    Read image from file that has a Bayer mosaic.

    Inputs:
    filename = name of image file
    bayerpattern = arrangement of the pixels. Often found by trial and error. ("BG","GB","RG","GR")
    alg = algorithm with which to demosaic the image. ("default","EdgeAware","VariableNumberGradients")

    Returns:
    img      = image object as numpy array
    path     = path to image file
    img_name = name of image file

    :param filename: str
    :param alg: str
    :param bayerpattern: str
    :return img: numpy.ndarray
    :return path: str
    :return img_name: str
    """
    # bayerpattern is defined as the colors of the pixels in the 2nd and 3rd column of the 2nd row.
    # see https://docs.opencv.org/3.2.0/de/d25/imgproc_color_conversions.html
    # COLOR_BayerBG2BGR
    # COLOR_BayerGB2BGR
    # COLOR_BayerRG2BGR
    # COLOR_BayerGR2BGR
    image_raw = cv2.imread(filename, flags=-1)

    if image_raw is None:
        fatal_error("Failed to open " + filename)

    # Itemize the Bayer pattern and algorithm
    converters = {
        "DEFAULT": {
            "BG": cv2.COLOR_BayerBG2BGR,
            "GB": cv2.COLOR_BayerGB2BGR,
            "RG": cv2.COLOR_BayerRG2BGR,
            "GR": cv2.COLOR_BayerGR2BGR
        },
        "EDGEAWARE": {
            "BG": cv2.COLOR_BayerBG2BGR_EA,
            "GB": cv2.COLOR_BayerGB2BGR_EA,
            "RG": cv2.COLOR_BayerRG2BGR_EA,
            "GR": cv2.COLOR_BayerGR2BGR_EA
        },
        "VARIABLENUMBERGRADIENTS": {
            "BG": cv2.COLOR_BayerBG2BGR_VNG,
            "GB": cv2.COLOR_BayerGB2BGR_VNG,
            "RG": cv2.COLOR_BayerRG2BGR_VNG,
            "GR": cv2.COLOR_BayerGR2BGR_VNG
        }
    }

    # Check if the algorithm is valid
    if alg.upper() not in converters:
        fatal_error(f"Invalid algorithm '{alg}'. Choose from {list(converters.keys())}.")
    # Check if the bayer pattern is valid
    if bayerpattern.upper() not in converters[alg.upper()]:
        fatal_error(f"Invalid Bayer pattern '{bayerpattern}'. Choose from {list(converters[alg.upper()].keys())}.")
    # Convert the image using the specified algorithm and Bayer pattern
    img = cv2.cvtColor(image_raw, converters[alg.upper()][bayerpattern.upper()])

    # Split path from filename
    path, img_name = os.path.split(filename)

    _debug(visual=img,
           filename=os.path.join(params.debug_outdir, "input_image.png"))

    return img, path, img_name
