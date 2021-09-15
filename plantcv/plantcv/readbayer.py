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

    if alg.upper() == 'DEFAULT':
        if bayerpattern.upper() == 'BG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerBG2BGR)
        elif bayerpattern.upper() == 'GB':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGB2BGR)
        elif bayerpattern.upper() == 'RG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerRG2BGR)
        elif bayerpattern.upper() == 'GR':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGR2BGR)
    elif alg.upper() == 'EDGEAWARE':
        if bayerpattern.upper() == 'BG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerBG2BGR_EA)
        elif bayerpattern.upper() == 'GB':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGB2BGR_EA)
        elif bayerpattern.upper() == 'RG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerRG2BGR_EA)
        elif bayerpattern.upper() == 'GR':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGR2BGR_EA)
    elif alg.upper() == 'VARIABLENUMBERGRADIENTS':
        if bayerpattern.upper() == 'BG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerBG2BGR_VNG)
        elif bayerpattern.upper() == 'GB':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGB2BGR_VNG)
        elif bayerpattern.upper() == 'RG':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerRG2BGR_VNG)
        elif bayerpattern.upper() == 'GR':
            img = cv2.cvtColor(image_raw, cv2.COLOR_BayerGR2BGR_VNG)

    # Split path from filename
    path, img_name = os.path.split(filename)

    _debug(visual=img,
           filename=os.path.join(params.debug_outdir, "input_image.png"))

    return img, path, img_name
