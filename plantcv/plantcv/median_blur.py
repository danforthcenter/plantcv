# Median blur device

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def median_blur(gray_img, ksize):
    """Applies a median blur filter (applies median value to central pixel within a kernel size ksize x ksize).

    Inputs:
    gray_img  = Grayscale image data
    ksize     = kernel size => ksize x ksize box

    Returns:
    img_mblur = blurred image

    :param gray_img: numpy.ndarray
    :param ksize: int
    :return img_mblur: numpy.ndarray
    """

    img_mblur = cv2.medianBlur(gray_img, ksize)
    params.device += 1
    if params.debug == 'print':
        print_image(img_mblur, os.path.join(params.debug_outdir,
                                            str(params.device) + '_median_blur' + str(ksize) + '.png'))
    elif params.debug == 'plot':
        plot_image(img_mblur, cmap='gray')
    return img_mblur
