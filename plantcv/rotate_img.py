# RGB -> HSV -> Gray

import cv2
import numpy as np
from . import print_image
from . import plot_image
from . import fatal_error


def rotate_img(img, rotation_deg, device, debug=None):
    """Rotate image, sometimes it is necessary to rotate image, especially when clustering for multiple plants is needed.

    Inputs:
    img     = image object, RGB colorspace (either single or three channel)
    rotation_deg = rotation angle in degrees, should be an integer, can be a negative number, postive values move counter clockwise.
    device  = device number. Used to count steps in the pipeline
    debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    rotated_img = rotated image

    :param img: numpy array
    :param rotation_deg: int
    :param device: int
    :param debug: str
    :return device: int
    :return rotated_img: numpy array
    """
    device += 1

    if len(np.shape(img))==3:
        iy, ix, iz = np.shape(img)
    else:
        iy,ix=np.shape(img)

    M = cv2.getRotationMatrix2D((ix / 2, iy / 2), rotation_deg, 1)
    rotated_img = cv2.warpAffine(img, M, (ix, iy))

    if debug == 'print':
        print_image(rotated_img, (str(device) + '_hsv_value.png'))

    elif debug == 'plot':
        if len(np.shape(img))==3:
            plot_image(rotated_img)
        else:
            plot_image(rotated_img, cmap='gray')

    return device, rotated_img

