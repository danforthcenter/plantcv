# Fill in holes, flood fill

import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from scipy.ndimage.morphology import binary_fill_holes


def fill_holes(bin_img):
    """
    Flood fills holes in a binary mask

    Inputs:
    bin_img      = Binary image data

    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :return filtered_img: numpy.ndarray
    """

    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) != 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Flood fill holes
    bool_img = binary_fill_holes(bool_img)

    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_fill_holes' + '.png'),
           cmap='gray')

    return filtered_img
