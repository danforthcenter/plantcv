# Find Objects

import cv2
import numpy as np
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours
from plantcv.plantcv import params, Objects


def find_objects(img, mask):
    """
    Find all objects and color them blue.

    Inputs:
    img       = RGB or grayscale image data for plotting
    mask      = Binary mask used for contour detection


    Returns:
    objects   = a dataclass with roi objects and hierarchies

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :return objects: plantcv.plantcv.classes.Objects
    """
    ori_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    cnts, hierarchy = _cv2_findcontours(bin_img=mask)
    # Cast tuple objects as a list
    objects = [cnts]
    for i, cnt in enumerate(objects):
        cv2.drawContours(ori_img, objects, i, (255, 102, 255), -1, lineType=8, hierarchy=hierarchy)

    objects = Objects(contours=objects, hierarchy=hierarchy) # contours already in list format

    _debug(visual=ori_img,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_id_objects.png'))

    return objects
