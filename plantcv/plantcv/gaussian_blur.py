# Gaussian blur device

import cv2
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params


def gaussian_blur(img, ksize, sigma_x=0, sigma_y=None, roi=None):
    """
    Applies a Gaussian blur filter.

    Inputs:
    # img     = RGB or grayscale image data
    # ksize   = Tuple of kernel dimensions, e.g. (5, 5)
    # sigmax  = standard deviation in X direction; if 0, calculated from kernel size
    # sigmay  = standard deviation in Y direction; if sigmaY is None, sigmaY is taken to equal sigmaX
    # roi     = Optional rectangular ROI to apply gaussian blur in

    Returns:
    img_gblur = blurred image

    :param img: numpy.ndarray
    :param ksize: tuple
    :param sigma_x: int
    :param sigma_y: str or int
    :param roi: plantcv.plantcv.Objects
    :return img_gblur: numpy.ndarray
    """
    sub_img_gblur = _rect_filter(img, roi, cv2.GaussianBlur,
                                 **{"ksize": ksize, "sigmaX": sigma_x, "sigmaY": sigma_y})
    img_gblur = _rect_replace(img, sub_img_gblur, roi)
    if len(np.shape(img_gblur)) == 3:
        cmap = None
    else:
        cmap = 'gray'

    _debug(visual=img_gblur,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_gaussian_blur.png'),
           cmap=cmap)

    return img_gblur
