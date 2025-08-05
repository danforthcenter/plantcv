# Laplace filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params


def laplace_filter(gray_img, ksize, scale, roi=None):
    """Apply the Lapace filter.
    This is a filtering method used to identify and highlight fine edges based on the 2nd derivative. A very
    sensetive method to highlight edges but will also amplify background noise. ddepth = -1 specifies that the
    dimensions of output image will be the same as the input image.

    Inputs:
    gray_img    = Grayscale image data
    ksize       = apertures size used to calculate 2nd derivative filter, specifies the size of the kernel
                  (must be an odd integer: 1,3,5...)
    scale       = scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
    roi         = Optional rectangular ROI to apply filter in.

    Returns:
    lp_filtered = laplacian filtered image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :param scale: int
    :param roi: plantcv.plantcv.Objects
    :return lp_filtered: numpy.ndarray
    """
    sub_lp_filtered = _rect_filter(gray_img, roi, cv2.Laplacian,
                                   **{"ddepth": -1, "ksize": ksize, "scale": scale})
    lp_filtered = _rect_replace(gray_img, sub_lp_filtered, roi)

    _debug(visual=lp_filtered,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_lp_out_k' + str(ksize) + '_scale' + str(scale) + '.png'),
           cmap='gray')

    return lp_filtered
