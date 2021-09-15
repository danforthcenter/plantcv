# Join images (OR)

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params


def logical_or(bin_img1, bin_img2):
    """
    Join two images using the bitwise OR operator.

    Inputs:
    bin_img1   = Binary image data to be compared to bin_img2
    bin_img2   = Binary image data to be compared to bin_img1

    Returns:
    merged     = joined binary image

    :param bin_img1: numpy.ndarray
    :param bin_img2: numpy.ndarray
    :return merged: numpy.ndarray
    """

    merged = cv2.bitwise_or(bin_img1, bin_img2)

    _debug(visual=merged,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_or_joined.png'),
           cmap='gray')

    return merged
