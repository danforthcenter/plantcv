# Find tips from skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image


def find_tips(skel_img):
    """
    The endpoints function was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Find tips in skeletonized image.

    Inputs:
    skel_img    = Skeletonized image

    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :return tip_img: numpy.ndarray
    """

    # 1 values line up with 255s, while the -1s line up with 0s (0s correspond to don’t care)
    endpoint1 = np.array([[-1, -1, -1],
                          [-1,  1, -1],
                          [-1,  1, -1]])
    endpoint2 = np.array([[-1, -1, -1],
                          [-1,  1, -1],
                          [-1, -1,  1]])

    endpoint3 = np.rot90(endpoint1)
    endpoint4 = np.rot90(endpoint2)
    endpoint5 = np.rot90(endpoint3)
    endpoint6 = np.rot90(endpoint4)
    endpoint7 = np.rot90(endpoint5)
    endpoint8 = np.rot90(endpoint6)

    endpoints = [endpoint1, endpoint2, endpoint3, endpoint4, endpoint5, endpoint6, endpoint7, endpoint8]
    tip_img = np.zeros(skel_img.shape, dtype=int)
    for endpoint in endpoints:
        tip_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=endpoint,
                                                 borderType=cv2.BORDER_CONSTANT, borderValue=0), tip_img)
    tip_img = tip_img.astype(np.uint8) * 255

    params.device += 1

    if params.debug == 'print':
        print_image(tip_img, os.path.join(params.debug_outdir, str(params.device) + '_skeleton_tips.png'))
    elif params.debug == 'plot':
        plot_image(tip_img, cmap='gray')

    return tip_img
