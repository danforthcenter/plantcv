# Invert gray image

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def invert(img):
    """Inverts grayscale images.

    Inputs:
    img     = image object, grayscale

    Returns:
    img_inv = inverted image

    :param img: numpy array
    :return img_inv: numpy array
    """

    params.device += 1
    img_inv = cv2.bitwise_not(img)
    if params.debug == 'print':
        print_image(img_inv, os.path.join(params.debug_outdir, str(params.device) + '_invert.png'))
    elif params.debug == 'plot':
        plot_image(img_inv, cmap='gray')
    return img_inv
