# Gaussian blur device

import cv2
from . import print_image
from . import plot_image


def gaussian_blur(device, img, ksize, sigmax, sigmay=None, debug=None):
    """Applies a Gaussian blur filter.

    Inputs:
    # img     = img object
    # ksize   = kernel size => ksize x ksize box, e.g. (5,5)
    # sigmax = standard deviation in X direction; if 0, calculated from kernel size
    # sigmay = standard deviation in Y direction; if sigmaY is None, sigmaY is taken to equal sigmaX
    # device  = device number. Used to count steps in the pipeline
    # debug   = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device    = device number
    img_gblur = blurred image

    :param img: numpy array
    :param ksize: int
    :param sigmax: int
    :param sigmay: str or int
    :param device: int
    :param debug: str
    :return device: int
    :return img_gblur: numpy array
    """
    img_gblur = cv2.GaussianBlur(img, ksize, sigmax, sigmay)

    device += 1
    if debug == 'print':
        print_image(img_gblur, (str(device) + '_gaussian_blur' + str(ksize) + '.png'))
    elif debug == 'plot':
        plot_image(img_gblur, cmap='gray')

    return device, img_gblur