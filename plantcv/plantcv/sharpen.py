# Sharpen an image

import cv2
import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace


def sharpen(img, ksize, amount=1, threshold=0, sigma_x=0, sigma_y=None, roi=None):
    """Sharpen an image

    Parameters
    ----------
    img         = numpy.ndarray, RGB or grayscale image
    ksize       = tuple, kernel dimensions such as (5, 5)
    amount      = int, degree of sharpening, higher numbers will sharpen the image more
    threshold   = int, threshold on low contrast. Contrasts below this amount are removed.
    sigma_x     = int, standard deviation in X direction; if 0, calculated from kernel size
    sigma_y     = str or int, standard deviation in Y direction; if sigmaY is None, sigmaY is taken to equal sigmaX
    roi         = Optional rectangular ROI to apply sharpening in

    Returns
    -------
    sharp_img = numpy.ndarray,
                   sharpened image
    """
    sub_sharp_img = _rect_filter(img, roi, _unsharp_masking,
                                 **{"ksize": ksize,
                                    "sigma_x": sigma_x,
                                    "sigma_y": sigma_y,
                                    "amount": amount,
                                    "threshold": threshold})
    sharp_img = _rect_replace(img, sub_sharp_img, roi)

    _debug(visual=sharp_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_sharpen.png'))

    return sharp_img


def _unsharp_masking(img, ksize, amount=1, threshold=0, sigma_x=0, sigma_y=None):
    """Helper function to sharpen image using unsharp masking
    Parameters
    ----------
    img         = numpy.ndarray, RGB or grayscale image
    ksize       = tuple, kernel dimensions such as (5, 5)
    amount      = int, degree of sharpening, higher numbers will sharpen the image more
    threshold   = int, threshold on low contrast. Contrasts below this amount are removed.
    sigma_x     = int,
         passed to gaussian_blur. Standard deviation in X direction; if 0, calculated from kernel size
    sigma_y     = None or int,
         passed to gaussian blur. standard deviation in Y direction; if sigmaY is None, sigmaY is taken to equal sigmaX

    Returns
    -------
    sharpened = numpy.ndarray,
                   sharpened image
    """
    blurred = cv2.GaussianBlur(img, ksize=ksize, sigmaX=sigma_x, sigmaY=sigma_y)
    # subtract blurry image from "saturated" version of image
    sharpened_unscaled = float(amount + 1) * img - float(amount) * blurred
    # ensure image is [0, 255]
    sharpened_unscaled = np.maximum(sharpened_unscaled, np.zeros(sharpened_unscaled.shape))
    sharpened_float = np.minimum(sharpened_unscaled, 255 * np.ones(sharpened_unscaled.shape))
    # ensure image is uint8
    sharpened = sharpened_float.round().astype(np.uint8)
    # if threshold is greater than 0 then remove contrasts below that amount
    if threshold > 0:
        low_contrast_mask = np.absolute(img - blurred) < threshold
        np.copyto(sharpened, img, where=low_contrast_mask)

    return sharpened
