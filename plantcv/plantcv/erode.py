# Erosion filter

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _erode
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def erode(gray_img, ksize, i=1, roi=None):
    """Apply morphological erosion filtering.

    Parameters
    ----------
    gray_img : numpy.ndarray
        Grayscale image data, usually binary.
    ksize : int, numpy.ndarray, or tuple
        Kernel specification: a binary array for an arbitrary shape, a tuple
        for a rectangular shape, or an integer for a square shape.
    i : int, optional
        Number of consecutive filtering passes. Default is 1.
    roi : plantcv.plantcv.Objects, optional
        Rectangular region of interest within which to erode. Default is None.

    Returns
    -------
    er_img : numpy.ndarray
         Eroded image.
    """
    k = _format_kernel(ksize, int)
    er_img = _erode(gray_img, k, i, roi=roi)

    _debug(visual=er_img, filename=os.path.join(params.debug_outdir, f"{params.device}_er_image{k}_itr{i}.png"), cmap='gray')

    return er_img
