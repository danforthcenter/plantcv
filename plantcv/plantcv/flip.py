# Flip image

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def flip(img, direction):
    """Flip image.

    Inputs:
    img       = RGB or grayscale image data
    direction = "horizontal" or "vertical"

    Returns:
    vh_img    = flipped image

    :param img: numpy.ndarray
    :param direction: str
    :return vh_img: numpy.ndarray
    """
    params.device += 1
    if direction.upper() == "VERTICAL":
        vh_img = cv2.flip(img, 1)
    elif direction.upper() == "HORIZONTAL":
        vh_img = cv2.flip(img, 0)
    else:
        fatal_error(str(direction) + " is not a valid direction, must be horizontal or vertical")

    if params.debug == 'print':
        print_image(vh_img, os.path.join(params.debug_outdir, str(params.device) + "_flipped.png"))
    elif params.debug == 'plot':
        if len(np.shape(vh_img)) == 3:
            plot_image(vh_img)
        else:
            plot_image(vh_img, cmap='gray')

    return vh_img
