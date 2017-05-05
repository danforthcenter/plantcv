# Object composition

import numpy as np
import cv2
from . import print_image
from . import plot_image


def object_composition(img, contours, hierarchy, device, debug=None):
    """Groups objects into a single object, usually done after object filtering.

    Inputs:
    contours = object list
    device   = device number. Used to count steps in the pipeline
    debug    = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device   = device number
    group    = grouped contours list
    mask     = image mask

    :param img: numpy array
    :param contours: list
    :param hierarchy: list
    :param device: int
    :param debug: str
    :return device: int
    :return group: list
    :return mask: numpy array
    """

    device += 1
    ori_img = np.copy(img)

    stack = np.zeros((len(contours), 1))
    r, g, b = cv2.split(ori_img)
    mask = np.zeros(g.shape, dtype=np.uint8)

    for c, cnt in enumerate(contours):
        # if hierarchy[0][c][3] == -1:
        if hierarchy[0][c][2] == -1 and hierarchy[0][c][3] > -1:
            stack[c] = 0
            # stack[c] = 1
            # cv2.drawContours(img, cnt, -1, color_palette(1)[0], 3)
            # np.append(group, np.vstack(cnt))
        else:
            stack[c] = 1
            # cv2.drawContours(img, contours, -1, color_palette(1)[0], -1, hierarchy=hierarchy)
            # stack[c] = 0
    ids = np.where(stack == 1)[0]
    if len(ids) > 0:
        group = np.vstack(contours[i] for i in ids)
        cv2.drawContours(mask, contours, -1, (255), -1, hierarchy=hierarchy)

        if debug is not None:
            cv2.drawContours(ori_img, group, -1, (255, 0, 0), 4)
            for cnt in contours:
                cv2.drawContours(ori_img, cnt, -1, (255, 0, 0), 4)
            if debug == 'print':
                print_image(ori_img, (str(device) + '_objcomp.png'))
                print_image(ori_img, (str(device) + '_objcomp_mask.png'))
            elif debug == 'plot':
                plot_image(ori_img)
        return device, group, mask
    else:
        print("Warning: Invalid contour.")
        return device, None, None
