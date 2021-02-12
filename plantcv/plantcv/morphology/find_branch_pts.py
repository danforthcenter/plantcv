# Find branch points from skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects


def find_branch_pts(skel_img, mask=None, label="default"):
    """
    The branching algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label        = optional label parameter, modifies the variable name of observations recorded

    Returns:
    branch_pts_img = Image with just branch points, rest 0

    :param skel_img: numpy.ndarray
    :param mask: np.ndarray
    :param label: str
    :return branch_pts_img: numpy.ndarray
    """

    # In a kernel: 1 values line up with 255s, -1s line up with 0s, and 0s correspond to don't care
    # T like branch points
    t1 = np.array([[-1, 1, -1],
                   [1, 1, 1],
                   [-1, -1, -1]])
    t2 = np.array([[1, -1, 1],
                   [-1, 1, -1],
                   [1, -1, -1]])
    t3 = np.rot90(t1)
    t4 = np.rot90(t2)
    t5 = np.rot90(t3)
    t6 = np.rot90(t4)
    t7 = np.rot90(t5)
    t8 = np.rot90(t6)

    # Y like branch points
    y1 = np.array([[1, -1, 1],
                   [0, 1, 0],
                   [0, 1, 0]])
    y2 = np.array([[-1, 1, -1],
                   [1, 1, 0],
                   [-1, 0, 1]])
    y3 = np.rot90(y1)
    y4 = np.rot90(y2)
    y5 = np.rot90(y3)
    y6 = np.rot90(y4)
    y7 = np.rot90(y5)
    y8 = np.rot90(y6)
    kernels = [t1, t2, t3, t4, t5, t6, t7, t8, y1, y2, y3, y4, y5, y6, y7, y8]

    branch_pts_img = np.zeros(skel_img.shape[:2], dtype=int)

    # Store branch points
    for kernel in kernels:
        branch_pts_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=kernel,
                                                        borderType=cv2.BORDER_CONSTANT, borderValue=0), branch_pts_img)

    # Switch type to uint8 rather than bool
    branch_pts_img = branch_pts_img.astype(np.uint8) * 255

    # Store debug
    debug = params.debug
    params.debug = None

    # Make debugging image
    if mask is None:
        dilated_skel = dilate(skel_img, params.line_thickness, 1)
        branch_plot = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)
    else:
        # Make debugging image on mask
        mask_copy = mask.copy()
        branch_plot = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
        skel_obj, skel_hier = find_objects(skel_img, skel_img)
        cv2.drawContours(branch_plot, skel_obj, -1, (150, 150, 150), params.line_thickness, lineType=8,
                         hierarchy=skel_hier)

    branch_objects, _ = find_objects(branch_pts_img, branch_pts_img)

    # Initialize list of tip data points
    branch_list = []
    branch_labels = []
    for i, branch in enumerate(branch_objects):
        x, y = branch.ravel()[:2]
        coord = (int(x), int(y))
        branch_list.append(coord)
        branch_labels.append(i)
        cv2.circle(branch_plot, (x, y), params.line_thickness, (255, 0, 255), -1)

    outputs.add_observation(sample=label, variable='branch_pts',
                            trait='list of branch-point coordinates identified from a skeleton',
                            method='plantcv.plantcv.morphology.find_branch_pts', scale='pixels', datatype=list,
                            value=branch_list, label=branch_labels)

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(branch_plot, os.path.join(params.debug_outdir, str(params.device) + '_branch_pts.png'))
    elif params.debug == 'plot':
        plot_image(branch_plot)

    return branch_pts_img
