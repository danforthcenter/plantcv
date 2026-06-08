# Variance texture filter


import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv.get_kernel import _format_kernel
from plantcv.plantcv._globals import params
from scipy.ndimage import generic_filter


def stdev_filter(img, ksize, borders='nearest', roi=None):
    """
    Creates a binary image from a grayscale image using skimage texture calculation for thresholding.
    This function is quite slow.

    Parameters:
    -----------
    gray_img       = numpy.ndarray,
        Grayscale image data
    ksize        = int, numpy.ndarray, or tuple
        Kernel specified as a binary numpy.ndarray for arbitrary shapes,
        shape tuple for a rectangular kernel, or integer for a square kernel.
        Here values are coerced to int.
    borders        = str,
        How the array borders are handled, either 'reflect',
        'constant', 'nearest', 'mirror', or 'wrap'
    roi            = plantcv.plantcv.Objects,
        optional rectangular ROI to apply filter within

    Returns:
    --------
    output         = numpy.ndarray,
        Standard deviation values image
    """
    # Make an array the same size as the original image
    output = np.zeros(img.shape, dtype=img.dtype)
    # Take the pieces of the empty mask and image in the ROI
    sub_zeros = _rect_filter(output, roi)
    sub_img = _rect_filter(img, roi)
    k = _format_kernel(ksize, int)
    # Apply the texture function over the subset image
    generic_filter(sub_img, np.std, size=k, output=sub_zeros, mode=borders)
    # re-insert the subset into the full size mask
    replaced = _rect_replace(img, sub_zeros, roi)

    _debug(visual=replaced,
           filename=os.path.join(params.debug_outdir, str(params.device) + "_variance.png"))

    return replaced
