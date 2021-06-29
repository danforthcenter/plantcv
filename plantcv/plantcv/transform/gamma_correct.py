# Gamma Correction Function Prototype

import os
import numpy as np
from skimage import exposure, img_as_float
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def gamma_correct(img, gamma=1, gain=1):
    """Wrapper for scikit-image gamma correction function. Performs Gamma Correction on the input image. Also known as
    Power Law Transform. This function transforms the input image pixelwise according to the equation O = I**gamma
    after scaling each pixel to the range 0 to 1.

    Inputs:
    img     = input image (RGB or grayscale)
    gamma   = Non negative real number. Default value is 1.
    gain    = The constant multiplier. Default value is 1.

    :param img: ndarray
    :param gamma = float
    :param gain = float
    :return corrected_img: ndarray
    """

    corrected_img = exposure.adjust_gamma(image=img, gamma=gamma, gain=gain)

    _debug(visual=corrected_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_gamma_corrected.png'))

    return corrected_img
