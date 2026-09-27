# Correct for nonuniform illumination

import os
import cv2
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv import gaussian_blur
from plantcv.plantcv.transform import rescale
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray
from plantcv.plantcv.get_kernel import _format_kernel


def nonuniform_illumination(img, ksize):
    """Correct for non uniform illumination i.e. spotlight correction.

    Parameters:
    -----------
    img       = numpy.ndarray,
        RGB or grayscale image data
    ksize        = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.

    Returns:
    --------
    corrected_img = numpy.ndarray,
        rescaled image
    """
    if len(np.shape(img)) == 3:
        img = _rgb2gray(img)

    # Fill foreground objects
    kernel = _format_kernel(ksize, np.ndarray)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Heavily blurred image acts like a background image
    blurred_img = gaussian_blur(opening, ksize=ksize)
    img_mean = np.mean(blurred_img)
    corrected_img = img - blurred_img + img_mean
    corrected_img = rescale(gray_img=corrected_img, min_value=0, max_value=255)

    # Reset debug mode
    params.debug = debug

    _debug(visual=corrected_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_correct_illumination.png'))

    return corrected_img
