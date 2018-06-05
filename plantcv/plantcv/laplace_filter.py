# Laplace filtering

import cv2
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def laplace_filter(img, k, scale, device, debug=None):
    """This is a filtering method used to identify and highlight fine edges based on the 2nd derivative. A very
       sensetive method to highlight edges but will also amplify background noise. ddepth = -1 specifies that the
       dimensions of output image will be the same as the input image.

    Inputs:
    img         = input image
    k           = apertures size used to calculate 2nd derivative filter, specifies the size of the kernel
                  (must be an odd integer: 1,3,5...)
    scale       = scaling factor applied (multiplied) to computed Laplacian values (scale = 1 is unscaled)
    device      = device number. Used to count steps in the pipeline
    debug       = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device      = device number
    lp_filtered = laplacian filtered image

    :param img: numpy array
    :param k: int
    :param scale: int
    :param device: int
    :param debug: str
    :return device: int
    :return lp_filtered: numpy array
    """

    lp_filtered = cv2.Laplacian(src=img, ddepth=-1, ksize=k, scale=scale)
    device += 1
    if debug == 'print':
        print_image(lp_filtered, str(device) + '_lp_out_k' + str(k) + '_scale' + str(scale) + '.png')
    elif debug == 'plot':
        plot_image(lp_filtered, cmap='gray')
    return device, lp_filtered
