# Invert gray image

import cv2
from . import print_image


def invert(img, device, debug=False):
    """Inverts grayscale images.

    Inputs:
    img     = image object, grayscale
    device  = device number. Used to count steps in the pipeline
    debug   = True/False. If True, print image

    Returns:
    device  = device number
    img_inv = inverted image

    :param img: numpy array
    :param device: int
    :param debug: bool
    :return device: int
    :return img_inv: numpy array
    """

    device += 1
    img_inv = cv2.bitwise_not(img)
    if debug:
        print_image(img_inv, (str(device) + '_invert.png'))
    return device, img_inv
