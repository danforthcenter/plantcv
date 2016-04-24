# RGB -> Gray

import cv2
from . import print_image


def rgb2gray(img, device, debug=False):
    """Convert image from RGB colorspace to Gray.

    Inputs:
    img    = image object, RGB colorspace
    device = device number. Used to count steps in the pipeline
    debug  = True/False. If True, print image

    Returns:
    device = device number
    gray   = grayscale image

    :param img: numpy array
    :param device: int
    :param debug: bool
    :return device: int
    :return gray: numpy array
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    device += 1
    if debug:
        print_image(gray, (str(device) + '_gray.png'))
    return device, gray
