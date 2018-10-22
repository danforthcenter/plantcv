# Median blur device

import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from scipy.ndimage.filters import median_filter


def median_blur(gray_img, ksize):
    """Applies a median blur filter (applies median value to central pixel within a kernel size).

    Inputs:
    gray_img  = Grayscale image data
    ksize = kernel size => integer or tuple, ksize x ksize box if integer, (n, m) size box if tuple

    Returns:
    img_mblur = blurred image


    :param gray_img: numpy.ndarray
    :param ksize: int or tuple
    :return img_mblur: numpy.ndarray
    """

    # Make sure ksize is valid
    if type(ksize) is not int and type(ksize) is not tuple:
        fatal_error("Invalid ksize, must be integer or tuple")

    img_mblur = median_filter(gray_img, size=ksize)
    params.device += 1
    if params.debug == 'print':
        print_image(img_mblur, os.path.join(params.debug_outdir,
                                            str(params.device) + '_median_blur' + str(ksize) + '.png'))
    elif params.debug == 'plot':
        plot_image(img_mblur, cmap='gray')
    return img_mblur
