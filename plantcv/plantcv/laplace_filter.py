# Laplace filtering

import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def laplace_filter(gray_img, ksize, scale=1, roi=None):
    """Apply a Laplacian filter to a grayscale image.

    The Laplacian filter highlights edges using the second derivative of the
    image. It is sensitive to fine edges but may also amplify background noise.
    The output has the same dimensions and data type as the input image.

    Parameters
    ----------
    gray_img : numpy.ndarray
        Grayscale image to filter.
    ksize : int, tuple, or numpy.ndarray
        Kernel size. Tuples and arrays are formatted as an integer for
        compatibility with ``cv2.Laplacian``. The resulting size must be odd.
    scale : int, optional
        Scale factor applied to the computed Laplacian values. The default is
        1, which leaves the values unscaled.
    roi : plantcv.plantcv.Objects, optional
        Rectangular region of interest in which to apply the filter.

    Returns
    -------
    numpy.ndarray
        Laplacian-filtered image.
    """
    k = _format_kernel(ksize, int)
    sub_lp_filtered = _rect_filter(gray_img, roi, cv2.Laplacian,
                                   **{"ddepth": -1, "ksize": k, "scale": scale})
    lp_filtered = _rect_replace(gray_img, sub_lp_filtered, roi)

    _debug(visual=lp_filtered, filename=os.path.join(params.debug_outdir, f"{params.device}_lp_out_k{ksize}_scale{scale}.png"),
           cmap='gray')

    return lp_filtered
