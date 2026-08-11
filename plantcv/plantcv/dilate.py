# Dilation filter

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _dilate
from plantcv.plantcv._globals import params
from plantcv.plantcv.get_kernel import _format_kernel


def dilate(gray_img, ksize, i, roi=None):
    """
    Performs morphological 'dilation' filtering. Adds pixel to center of kernel if conditions set in kernel are true.

    Parameters:
    -----------
    gray_img = numpy.ndarray,
        Grayscale (usually binary) image data
    ksize    = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
    i        = int,
        iterations, i.e. number of consecutive filtering passes
    roi      = plantcv.plantcv.Objects,
        rectangular ROI to dilate within

    Returns:
    --------
    dil_img = numpy.ndarray,
        dilated image
    """
    k = _format_kernel(ksize, int)
    dil_img = _dilate(gray_img, k, i, roi=roi)

    _debug(visual=dil_img,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_dil_image' + str(k) + '_itr' + str(i) + '.png'),
           cmap='gray')

    return dil_img
