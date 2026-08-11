# Gaussian blur device

import cv2
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def gaussian_blur(img, ksize, sigma_x=0, sigma_y=None, roi=None):
    """
    Applies a Gaussian blur filter.

    Parameters:
    -----------
    img     = numpy.ndarray,
        RGB or grayscale image data
    ksize        = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
        Here any input will be coerced to a tuple.
    sigmax  = int,
        standard deviation in X direction; if 0, calculated from kernel size
    sigmay  = int or None,
        standard deviation in Y direction; if sigmaY is None, sigmaY is taken to equal sigmaX
    roi     = plantcv.plantcv.Objects,
        Optional rectangular ROI to apply gaussian blur in

    Returns:
    --------
    img_gblur = numpy.ndarray,
        blurred image
    """
    k = _format_kernel(ksize, tuple)
    sub_img_gblur = _rect_filter(img, roi, cv2.GaussianBlur,
                                 **{"ksize": k, "sigmaX": sigma_x, "sigmaY": sigma_y})
    img_gblur = _rect_replace(img, sub_img_gblur, roi)
    if len(np.shape(img_gblur)) == 3:
        cmap = None
    else:
        cmap = 'gray'

    _debug(visual=img_gblur,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_gaussian_blur.png'),
           cmap=cmap)

    return img_gblur
