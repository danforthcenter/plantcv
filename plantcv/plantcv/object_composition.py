# Object composition

import numpy as np
import cv2
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params, Objects


def object_composition(img, objects):
    """
    Groups objects into a single object, usually done after object filtering.

    Inputs:
    img       = RGB or grayscale image data for plotting
    objects   = plantcv.Objects class

    Returns:
    group    = grouped contours list
    mask     = image mask

    :param img: numpy.ndarray
    :param Objects: plantcv.Objects
    :return group: list
    :return mask: numpy.ndarray
    """
    ori_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)

    stack = np.zeros((len(objects.contours), 1))
    r, g, b = cv2.split(ori_img)
    mask = np.zeros(g.shape, dtype=np.uint8)

    for c, cnt in enumerate(objects.contours):
        if objects.hierarchy[0][c][2] == -1 and objects.hierarchy[0][c][3] > -1:
            stack[c] = 0
        else:
            stack[c] = 1

    ids = np.where(stack == 1)[0]
    if len(ids) > 0:
        contour_list = [objects.contours[i] for i in ids]
        group = np.vstack(contour_list)
        cv2.drawContours(mask, objects.contours, -1, 255, -1, hierarchy=objects.hierarchy)

        cv2.drawContours(ori_img, group, -1, (255, 0, 0), params.line_thickness)
        for cnt in objects.contours:
            cv2.drawContours(ori_img, cnt, -1, (255, 0, 0), params.line_thickness)

        _debug(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_objcomp.png'))
        _debug(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_objcomp_mask.png'))

        return group, mask
    print("Warning: Invalid contour.")
    return None, None