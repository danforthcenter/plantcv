import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _closing


def closing(gray_img, kernel=None, roi=None):
    """Closes holes, removing small dark spots (i.e. pepper).

    Inputs:
    gray_img = input image (grayscale or binary)
    kernel   = optional neighborhood, expressed as an array of 1s and 0s. If None, use cross-shaped structuring element.
    roi      = optional rectangular ROI to apply closing within a region

    :param gray_img: np.ndarray
    :param kernel = np.ndarray
    :param roi: plantcv.plantcv.Objects
    :return filtered_img: np.ndarray
    """
    filtered_img = _closing(gray_img, kernel, roi=roi)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_closing' + '.png'),
           cmap='gray')

    return filtered_img
