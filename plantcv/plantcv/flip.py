# Flip image

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def flip(img, direction):
    """
    Flip image.

    Inputs:
    img       = RGB or grayscale image data
    direction = "horizontal" or "vertical"

    Returns:
    vh_img    = flipped image

    :param img: numpy.ndarray
    :param direction: str
    :return vh_img: numpy.ndarray
    """
    if direction.upper() == "VERTICAL":
        vh_img = cv2.flip(img, 1)
    elif direction.upper() == "HORIZONTAL":
        vh_img = cv2.flip(img, 0)
    else:
        fatal_error(str(direction) + " is not a valid direction, must be horizontal or vertical")

    if len(np.shape(vh_img)) == 3:
        cmap = None
    else:
        cmap = 'gray'

    _debug(visual=vh_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_flipped.png"),
           cmap=cmap)

    return vh_img
