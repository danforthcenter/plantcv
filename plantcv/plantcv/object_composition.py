# Object composition

import numpy as np
import cv2
import os
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def object_composition(img, contours, hierarchy):
    """Groups objects into a single object, usually done after object filtering.

    Inputs:
    img       = RGB or grayscale image data for plotting
    contours  = Contour list
    hierarchy = Contour hierarchy NumPy array

    Returns:
    group    = grouped contours list
    mask     = image mask

    :param img: numpy.ndarray
    :param contours: list
    :param hierarchy: numpy.ndarray
    :return group: list
    :return mask: numpy.ndarray
    """

    params.device += 1
    ori_img = np.copy(img)
    # If the reference image is grayscale convert it to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)

    stack = np.zeros((len(contours), 1))
    r, g, b = cv2.split(ori_img)
    mask = np.zeros(g.shape, dtype=np.uint8)

    for c, cnt in enumerate(contours):
        # if hierarchy[0][c][3] == -1:
        if hierarchy[0][c][2] == -1 and hierarchy[0][c][3] > -1:
            stack[c] = 0
        else:
            stack[c] = 1

    ids = np.where(stack == 1)[0]
    if len(ids) > 0:
        contour_list = [contours[i] for i in ids]
        group = np.vstack(contour_list)
        cv2.drawContours(mask, contours, -1, 255, -1, hierarchy=hierarchy)

        if params.debug is not None:
            cv2.drawContours(ori_img, group, -1, (255, 0, 0), params.line_thickness)
            for cnt in contours:
                cv2.drawContours(ori_img, cnt, -1, (255, 0, 0), params.line_thickness)
            if params.debug == 'print':
                print_image(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_objcomp.png'))
                print_image(ori_img, os.path.join(params.debug_outdir, str(params.device) + '_objcomp_mask.png'))
            elif params.debug == 'plot':
                plot_image(ori_img)
        return group, mask
    else:
        print("Warning: Invalid contour.")
        return None, None
