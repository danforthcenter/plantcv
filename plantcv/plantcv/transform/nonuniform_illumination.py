# Correct for nonuniform illumination

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import rgb2gray
from plantcv.plantcv import gaussian_blur
from plantcv.plantcv.transform import rescale
from plantcv.plantcv._debug import _debug


def nonuniform_illumination(img, ksize):
    """Correct for non uniform illumination i.e. spotlight correction.

    Inputs:
    img       = RGB or grayscale image data
    ksize     = (optional) new minimum value for range of interest. default = 0

    Returns:
    corrected_img = rescaled image

    :param img: numpy.ndarray
    :param ksize: int
    :return corrected_img: numpy.ndarray
    """
    if len(np.shape(img)) == 3:
        img = rgb2gray(img)

    # Fill foreground objects
    kernel = np.ones((ksize, ksize), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Heavily blurred image acts like a background image
    blurred_img = gaussian_blur(opening, ksize=(ksize, ksize))
    img_mean = np.mean(blurred_img)
    corrected_img = img - blurred_img + img_mean
    corrected_img = rescale(gray_img=corrected_img, min_value=0, max_value=255)

    # Reset debug mode
    params.debug = debug

    _debug(visual=corrected_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_correct_illumination.png'))

    return corrected_img
