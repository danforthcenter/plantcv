# RGB -> Gray

import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray


def rgb2gray(rgb_img):
    """Convert image from RGB colorspace to Gray.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data

    Returns
    -------
    numpy.ndarray
        grayscale image
    """
    gray = _rgb2gray(rgb_img=rgb_img)

    _debug(visual=gray, filename=os.path.join(params.debug_outdir, f"{params.device}_gray.png"))

    return gray
