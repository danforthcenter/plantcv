# Fill in holes, flood fill

import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from scipy.ndimage import binary_fill_holes


def fill_holes(bin_img, roi=None):
    """
    Flood fills holes in a binary mask

    Inputs:
    bin_img      = Binary image data
    roi          = plantcv Objects class rectangular ROI

    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :param roi: plantcv.plantcv.Objects
    :return filtered_img: numpy.ndarray
    """
    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) > 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)
    # Flood fill holes
    bool_img = _rect_filter(bool_img, roi=roi, function=binary_fill_holes)
    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)
    # put subset back into original size image
    replaced_img = _rect_replace(bin_img.astype(bool) * 255, filtered_img, roi)

    _debug(visual=replaced_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_fill_holes' + '.png'),
           cmap='gray')

    return replaced_img
