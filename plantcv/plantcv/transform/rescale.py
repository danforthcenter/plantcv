# Rescale grayscale images to user defined range

import os
from plantcv.plantcv import params
from plantcv.plantcv._helpers import _rescale
from plantcv.plantcv._debug import _debug


def rescale(gray_img, min_value=0, max_value=255):
    """Rescale image.

    Inputs:
    gray_img  = Grayscale image data
    min_value = (optional) new minimum value for range of interest. default = 0
    max_value = (optional) new maximum value for range of interest. default = 255

    Returns:
    rescaled_img = rescaled image

    :param gray_img: numpy.ndarray
    :param min_value: int
    :param max_value: int
    :return c: numpy.ndarray
    """
    rescaled_img = _rescale(gray_img=gray_img, min_value=min_value, max_value=max_value)

    _debug(visual=rescaled_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_rescaled.png'))

    return rescaled_img
