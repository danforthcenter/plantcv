# Fill in holes, flood fill

import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from skimage.segmentation import flood_fill


def floodfill(bin_img, points, value=0):
    """
    Flood fills holes in a binary mask

    Inputs:
    bin_img = Binary image data
    points = list of seed points to start flood fill e.g. ([(x,y)])
    value  = value from 0-255 (default value=0)

    Returns:
    filled_img = image with objects filled

    :param bin_img: numpy.ndarray
    :param points: list
    :param value: float
    :return filled_img: numpy.ndarray
    """
    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) != 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Flood fill holes
    points1 = list(map(lambda sub: (sub[1], sub[0]), points))

    for x in points1:
        bool_img = flood_fill(bool_img, x, value)

    # Cast boolean image to binary and make a copy of the binary image for returning
    filled_img = np.copy(bool_img.astype(np.uint8) * 255)

    _debug(visual=filled_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_flood_fill' + '.png'),
           cmap='gray')

    return filled_img
