# Object fill device

import numpy as np
import os
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from skimage.morphology import remove_small_objects


def fill(bin_img, size):
    """
    Identifies objects and fills objects that are less than size.

    Inputs:
    bin_img      = Binary image data
    size         = minimum object area size in pixels (integer)


    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :param size: int
    :return filtered_img: numpy.ndarray
    """

    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) != 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Find and fill contours
    bool_img = remove_small_objects(bool_img, size)

    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_fill" + str(size) + '.png'))

    return filtered_img
