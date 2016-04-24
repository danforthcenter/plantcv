# Median blur device

import cv2
from . import print_image


def median_blur(img, ksize, device, debug=False):
    """Applies a median blur filter (applies median value to central pixel within a kernel size ksize x ksize).

    Inputs:
    # img     = img object
    # ksize   = kernel size => ksize x ksize box
    # device  = device number. Used to count steps in the pipeline
    # debug   = True/False. If True, print image

    Returns:
    device    = device number
    img_mblur = blurred image

    :param img: numpy array
    :param ksize: int
    :param device: int
    :param debug: bool
    :return device: int
    :return img_mblur: numpy array
    """

    img_mblur = cv2.medianBlur(img, ksize)
    device += 1
    if debug:
        print_image(img_mblur, (str(device) + '_median_blur' + str(ksize) + '.png'))
    return device, img_mblur
