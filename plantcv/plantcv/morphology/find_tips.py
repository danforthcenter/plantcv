# Find tips from skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects


def find_tips(skel_img, mask=None):
    """
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Find tips in skeletonized image.

    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :return tip_img: numpy.ndarray
    """
    # Store debug
    debug = params.debug
    params.debug = None

    # In a kernel: 1 values line up with 255s, -1s line up with 0s, and 0s correspond to dont care
    endpoint1 = np.array([[-1, -1, -1],
                          [-1,  1, -1],
                          [ 0,  1,  0]])
    endpoint2 = np.array([[-1, -1, -1],
                          [-1,  1,  0],
                          [-1,  0,  1]])

    endpoint3 = np.rot90(endpoint1)
    endpoint4 = np.rot90(endpoint2)
    endpoint5 = np.rot90(endpoint3)
    endpoint6 = np.rot90(endpoint4)
    endpoint7 = np.rot90(endpoint5)
    endpoint8 = np.rot90(endpoint6)

    endpoints = [endpoint1, endpoint2, endpoint3, endpoint4, endpoint5, endpoint6, endpoint7, endpoint8]
    tip_img = np.zeros(skel_img.shape[:2], dtype=int)
    for endpoint in endpoints:
        tip_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=endpoint,
                                                 borderType=cv2.BORDER_CONSTANT, borderValue=0), tip_img)
    tip_img = tip_img.astype(np.uint8) * 255
    tip_objects, _ = find_objects(tip_img, tip_img)

    if mask is None:
        # Make debugging image
        dilated_skel = dilate(skel_img, params.line_thickness, 1)
        tip_plot = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)

    else:
        # Make debugging image on mask
        mask_copy = mask.copy()
        tip_plot = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
        skel_obj, skel_hier = find_objects(skel_img, skel_img)
        cv2.drawContours(tip_plot, skel_obj, -1, (150, 150, 150), params.line_thickness,
                         lineType=8, hierarchy=skel_hier)

    for i in tip_objects:
        x, y = i.ravel()[:2]
        cv2.circle(tip_plot, (x, y), params.line_thickness, (0, 255, 0), -1)

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(tip_plot, os.path.join(params.debug_outdir, str(params.device) + '_skeleton_tips.png'))
    elif params.debug == 'plot':
        plot_image(tip_plot)

    return tip_img
