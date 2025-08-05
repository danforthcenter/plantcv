# Median blur device

import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from scipy.ndimage import median_filter


def median_blur(gray_img, ksize, roi=None):
    """
    Applies a median blur filter (applies median value to central pixel within a kernel size).

    Inputs:
    gray_img  = Grayscale image data
    ksize = kernel size => integer or tuple, ksize x ksize box if integer, (n, m) size box if tuple
    roi = Optional rectangular ROI to apply median blur in

    Returns:
    img_mblur = blurred image


    :param gray_img: numpy.ndarray
    :param ksize: int or tuple
    :param roi: plantcv.plantcv.Objects
    :return img_mblur: numpy.ndarray
    """
    # Make sure ksize is valid
    if type(ksize) is not int and type(ksize) is not tuple:
        fatal_error("Invalid ksize, must be integer or tuple")

    sub_img_mblur = _rect_filter(gray_img, roi, median_filter,
                                 **{"size": ksize})
    img_mblur = _rect_replace(gray_img, sub_img_mblur, roi)

    _debug(img_mblur,
           filename=os.path.join(params.debug_outdir,
                                 str(params.device) + '_median_blur' + str(ksize) + '.png'),
           cmap='gray')

    return img_mblur
