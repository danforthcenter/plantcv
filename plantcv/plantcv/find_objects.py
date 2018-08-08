# Find Objects

import cv2
import numpy as np
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def find_objects(img, mask):
    """Find all objects and color them blue.

    Inputs:
    img       = image that the objects will be overlayed
    mask      = what is used for object detection


    Returns:
    objects   = list of contours
    hierarchy = contour hierarchy list

    :param img: numpy array
    :param mask: numpy array
    :return objects: list
    :return hierarchy: list
    """

    params.device += 1
    mask1 = np.copy(mask)
    ori_img = np.copy(img)
    objects, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    for i, cnt in enumerate(objects):
        cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)
    if params.debug == 'print':
        print_image(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_id_objects.png'))
    elif params.debug == 'plot':
        plot_image(ori_img)

    return objects, hierarchy
