# Invert gray image

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def invert(gray_img):
    """Inverts grayscale images.

    Inputs:
    gray_img     = Grayscale image data

    Returns:
    img_inv = inverted image

    :param gray_img: numpy.ndarray
    :return img_inv: numpy.ndarray
    """

    params.device += 1
    img_inv = cv2.bitwise_not(gray_img)
    if params.debug == 'print':
        print_image(img_inv, os.path.join(params.debug_outdir, str(params.device) + '_invert.png'))
    elif params.debug == 'plot':
        plot_image(img_inv, cmap='gray')
    return img_inv
