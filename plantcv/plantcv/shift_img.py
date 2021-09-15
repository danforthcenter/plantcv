# Crop position mask

import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


def shift_img(img, number, side="right"):
    """
    This function allows you to shift an image over without changing dimensions

    Inputs:
    img     = RGB or grayscale image data
    number  = number of rows or columns to add
    side   = "top", "bottom", "right", "left" where to add the rows or columns to

    Returns:
    newmask = image mask

    :param img: numpy.ndarray
    :param number: int
    :param side: str
    :return newmask: numpy.ndarray
    """

    number -= 1

    if number < 0:
        fatal_error("number cannot be 0, negative numbers, or non-integers")

    # get the sizes of the images
    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
        ori_img = np.copy(img)
        cmap = None
    else:
        ix, iy = np.shape(img)
        ori_img = np.dstack((img, img, img))
        cmap = 'gray'

    if side.upper() == "TOP":
        top = np.zeros((number, iy, 3), dtype=np.uint8)
        adjust = ix - number
        adjusted_img = np.vstack((top, ori_img[0:adjust, 0:]))
    elif side.upper() == 'BOTTOM':
        bottom = np.zeros((number, iy, 3), dtype=np.uint8)
        adjusted_img = np.vstack((ori_img[number:, 0:], bottom))
    elif side.upper() == 'RIGHT':
        right = np.zeros((ix, number, 3), dtype=np.uint8)
        adjusted_img = np.hstack((ori_img[0:, number:], right))
    elif side.upper() == 'LEFT':
        left = np.zeros((ix, number, 3), dtype=np.uint8)
        adjust = iy - number
        adjusted_img = np.hstack((left, ori_img[0:, 0:adjust]))
    else:
        fatal_error("side must be 'top', 'bottom', 'right', or 'left'")

    if len(np.shape(img)) == 2:
        adjusted_img = adjusted_img[:, :, 0]

    _debug(visual=adjusted_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_shifted_img.png"),
           cmap=cmap)

    return adjusted_img
