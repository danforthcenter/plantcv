# Object fill device

import numpy as np
import os
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from skimage.morphology import remove_small_objects


def fill(bin_img, size, roi=None):
    """
    Identifies objects and fills objects that are less than size.

    Inputs:
    bin_img      = Binary image data
    size         = minimum object area size in pixels (integer)
    roi          = optional Objects class rectangular ROI

    Returns:
    filtered_img = image with objects filled

    :param bin_img: numpy.ndarray
    :param size: int
    :param roi: plantcv.plantcv.Objects
    :return filtered_img: numpy.ndarray
    """
    # Make sure the image is binary
    if len(np.shape(bin_img)) != 2 or len(np.unique(bin_img)) > 2:
        fatal_error("Image is not binary")

    # Cast binary image to boolean
    bool_img = bin_img.astype(bool)

    # Find and fill contours, possibly within bounding rectangle
    bool_img = _rect_filter(bool_img,
                            roi=roi,
                            function=remove_small_objects,
                            **{"min_size" : size})
    # Cast boolean image to binary and make a copy of the binary image for returning
    filtered_img = np.copy(bool_img.astype(np.uint8) * 255)
    # slice the subset image back into full size binary image
    replaced_img = _rect_replace(bin_img.astype(bool) * 255, filtered_img, roi)

    _debug(visual=replaced_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_fill" + str(size) + '.png'))

    return replaced_img
