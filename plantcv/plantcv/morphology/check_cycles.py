# Check for cycles in a skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import find_objects


def check_cycles(skel_img):
    """
    The branching function was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Inputs:
    skel_img    = Skeletonized image

    Returns:
    num_cycles  = Number of cycles found

    :param skel_img: numpy.ndarray
    :return num_cycles: int
    """
    # Create the mask needed for cv2.floodFill, must be larger than the image
    h, w = skel_img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Copy the skeleton since cv2.floodFill will draw on it
    skel_copy = skel_img.copy()
    cv2.floodFill(skel_copy, mask=mask, seedPoint=(0, 0), newVal=255)

    # Invert so the holes are white and background black
    just_holes = cv2.bitwise_not(skel_copy)

    # Use pcv.find_objects to turn plots of holes into countable contours
    cycle_objects, _ = find_objects(just_holes, just_holes)

    # Count the number of holes
    num_cycles = len(cycle_objects)
    params.device += 1
    # if params.debug == 'print':
    #     print_image(branch_img, os.path.join(params.debug_outdir, str(params.device) + '_skeleton_branches.png'))
    # elif params.debug == 'plot':
    #     plot_image(branch_img, cmap='gray')

    return num_cycles
