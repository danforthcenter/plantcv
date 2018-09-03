# Laplace filtering

import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def laplace_filter(gray_img, k, scale):
    """This is a filtering method used to identify and highlight fine edges based on the 2nd derivative. A very
       sensetive method to highlight edges but will also amplify background noise. ddepth = -1 specifies that the
       dimensions of output image will be the same as the input image.

    Inputs:
    gray_img    = Grayscale image data
    k           = apertures size used to calculate 2nd derivative filter, specifies the size of the kernel
                  (must be an odd integer: 1,3,5...)
    scale       = scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)

    Returns:
    lp_filtered = laplacian filtered image

    :param gray_img: numpy.ndarray
    :param k: int
    :param scale: int
    :return lp_filtered: numpy.ndarray
    """

    lp_filtered = cv2.Laplacian(src=gray_img, ddepth=-1, ksize=k, scale=scale)
    params.device += 1
    if params.debug == 'print':
        print_image(lp_filtered,
                    os.path.join(params.debug_outdir,
                                 str(params.device) + '_lp_out_k' + str(k) + '_scale' + str(scale) + '.png'))
    elif params.debug == 'plot':
        plot_image(lp_filtered, cmap='gray')
    return lp_filtered
