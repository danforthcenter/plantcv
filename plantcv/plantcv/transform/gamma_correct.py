# Gamma Correction Function

import os
from skimage import exposure
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def gamma_correct(img, gamma=1, gain=1):
    """
    Apply a gamma correction to the input image.

    Inputs:
    img     = input image (RGB or grayscale)
    gamma   = Non negative real number. Default value is 1.
    gain    = The constant multiplier. Default value is 1.

    :param img: numpy.ndarray
    :param gamma: float
    :param gain: float
    :return corrected_img: numpy.ndarray
    """
    corrected_img = exposure.adjust_gamma(image=img, gamma=gamma, gain=gain)

    _debug(visual=corrected_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_gamma_corrected.png'))

    return corrected_img
