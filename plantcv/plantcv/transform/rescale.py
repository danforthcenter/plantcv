# Rescale grayscale images to user defined range

import os
import numpy as np
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._helpers import _rescale
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug


def rescale(gray_img, min_value=0, max_value=255):
    """Rescale image.

    Parameters:
    -----------
    gray_img  : numpy.ndarray,
        Grayscale image data
    min_value : int (optional),
        new minimum value for range of interest. default = 0
    max_value : int (optional),
        new maximum value for range of interest. default = 255

    Returns:
    rescaled_img : numpy.ndarray,
        rescaled image
    """
    rescaled_img = _rescale(gray_img, min_value, max_value)

    _debug(visual=rescaled_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_rescaled.png'))

    return rescaled_img
