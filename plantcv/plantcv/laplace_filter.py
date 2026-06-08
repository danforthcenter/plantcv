# Laplace filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def laplace_filter(gray_img, ksize, scale, roi=None):
    """Apply the Lapace filter.
    This is a filtering method used to identify and highlight fine edges based on the 2nd derivative. A very
    sensetive method to highlight edges but will also amplify background noise. ddepth = -1 specifies that the
    dimensions of output image will be the same as the input image.

    Parameters:
    -----------
    gray_img    = numpy.ndarray,
        Grayscale image data
    ksize       = int, tuple, or numpy.ndarray,
        tuples or numpy arrays are simplified to be an integer for compatibility with cv2.Laplacian.
        Must be an odd integer (1,3,5...)
    scale       = int,
        scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
    roi         = plantcv.plantcv.Objects,
        Optional rectangular ROI to apply filter in.

    Returns:
    --------
    lp_filtered = numpy.ndarray,
        laplacian filtered image
    """
    k = _format_kernel(ksize, int)
    sub_lp_filtered = _rect_filter(gray_img, roi, cv2.Laplacian,
                                   **{"ddepth": -1, "ksize": k, "scale": scale})
    lp_filtered = _rect_replace(gray_img, sub_lp_filtered, roi)

    _debug(visual=lp_filtered,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_lp_out_k' + str(ksize) + '_scale' + str(scale) + '.png'),
           cmap='gray')

    return lp_filtered
