import os
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _closing


def closing(gray_img, kernel=None, roi=None):
    """Closes holes, removing small dark spots (i.e. pepper).

    Parameters:
    gray_img = np.ndarray,
        input image (grayscale or binary)
    kernel   = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
    roi      = plantcv.plantcv.Objects,
        optional rectangular ROI to apply closing within a region

    Returns:
    --------
    filtered_img = numpy.ndarray
        Closed image
    """
    filtered_img = _closing(gray_img, kernel, roi=roi)

    _debug(visual=filtered_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_closing' + '.png'),
           cmap='gray')

    return filtered_img
