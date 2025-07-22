import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _closing


def closing(gray_img, kernel=None):
    """Wrapper for scikit-image closing functions. Opening can remove small dark spots (i.e. pepper).

    Inputs:
    gray_img = input image (grayscale or binary)
    kernel   = optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.

    :param gray_img: ndarray
    :param kernel = ndarray
    :return filtered_img: ndarray
    """
    filtered_img = _closing(gray_img, kernel)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_opening' + '.png'),
           cmap='gray')

    return filtered_img
