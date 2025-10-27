# Sharpen an image

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace, _unsharp_masking
from plantcv.plantcv import params


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
