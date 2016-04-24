# Find Objects

import cv2
import numpy as np
from . import print_image


def find_objects(img, mask, device, debug=False):
    """Find all objects and color them blue.

    Inputs:
    img       = image that the objects will be overlayed
    mask      = what is used for object detection
    device    = device number.  Used to count steps in the pipeline
    debug     = True/False. If True, print image

    Returns:
    device    = device number
    objects   = list of contours
    hierarchy = contour hierarchy list

    :param img: numpy array
    :param mask: numpy array
    :param device: int
    :param debug: bool
    :return device: int
    :return objects: list
    :return hierarchy: list
    """

    device += 1
    mask1 = np.copy(mask)
    ori_img = np.copy(img)
    objects, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i, cnt in enumerate(objects):
        cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)
    if debug:
        print_image(ori_img, (str(device) + '_id_objects.png'))

    return device, objects, hierarchy
