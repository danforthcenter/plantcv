# Find branch points from skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects


def find_branch_pts(skel_img):
    """
    The branching function was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Inputs:
    skel_img    = Skeletonized image

    Returns:
    branch_img   = Image with just branch points, rest 0

    :param skel_img: numpy.ndarray
    :return branch_pts_img: numpy.ndarray
    """

    # Store debug
    debug = params.debug
    params.debug = None

    # In a kernel: 1 values line up with 255s, -1s line up with 0s, and 0s correspond to don’t care
    # T like branch points
    t1 = np.array([[-1,  1, -1],
                   [ 1,  1,  1],
                   [-1, -1, -1]])
    t2 = np.array([[ 1, -1,  1],
                   [-1,  1, -1],
                   [ 1, -1, -1]])
    t3 = np.rot90(t1)
    t4 = np.rot90(t2)
    t5 = np.rot90(t3)
    t6 = np.rot90(t4)
    t7 = np.rot90(t5)
    t8 = np.rot90(t6)
    t = [t1, t2, t3, t4, t5, t6, t7, t8]

    # Y like branch points
    y1 = np.array([[ 1, -1,  1],
                   [-1,  1, -1],
                   [ 0,  1,  0]])
    y2 = np.array([[-1,  1, -1],
                   [ 1,  1,  0],
                   [-1,  0,  1]])
    y3 = np.rot90(y1)
    y4 = np.rot90(y2)
    y5 = np.rot90(y3)
    y6 = np.rot90(y4)
    y7 = np.rot90(y5)
    y8 = np.rot90(y6)
    y = [y1, y2, y3, y4, y5, y6, y7, y8]

    branch_pts_img = np.zeros(skel_img.shape[:2], dtype=int)

    # Store branch points
    for y_array in y:
        branch_pts_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=y_array,
                                                    borderType=cv2.BORDER_CONSTANT, borderValue=0), branch_pts_img)
    for t_array in t:
        branch_pts_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=t_array,
                                                    borderType=cv2.BORDER_CONSTANT, borderValue=0), branch_pts_img)
    # Switch type to uint8 rather than bool
    branch_pts_img = branch_pts_img.astype(np.uint8) * 255

    # Make debugging image
    branch_objects, _ = find_objects(branch_pts_img, branch_pts_img)
    skel_copy = skel_img.copy()
    dilated_skel = dilate(skel_copy, params.line_thickness, 1)
    branch_plot = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)
    for i in branch_objects:
        x, y = i.ravel()[:2]
        cv2.circle(branch_plot, (x, y), params.line_thickness, (255, 0, 255), -1)

    # Reset debug mode
    params.debug = debug

    params.device += 1

    if params.debug == 'print':
        print_image(branch_plot, os.path.join(params.debug_outdir, str(params.device) + '_skeleton_branches.png'))
    elif params.debug == 'plot':
        plot_image(branch_plot)

    return branch_pts_img
