# Prune barbs off skeleton image

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import image_subtract
from plantcv.plantcv.morphology import find_tips


def prune(skel_img, size):
    """
    The pruning function was written by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    Iteratively remove endpoints (tips) from a skeletonized image. "Prunes" barbs off a skeleton.

    Inputs:
    skel_img    = Skeletonized image
    size        = Size to get pruned off each branch

    Returns:
    pruned_img  = Pruned image

    :param skel_img: numpy.ndarray
    :param size: int
    :return pruned_img: numpy.ndarray

    """
    # Store debug
    debug = params.debug
    params.debug = None

    pruned_img = skel_img.copy()

    # Check to see if the skeleton has multiple objects
    mask_skel = pruned_img.astype(np.uint8) * 255
    objects, _ = find_objects(mask_skel, mask_skel)
    if not len(objects) == 1:
        print("Warning: Multiple objects detected and pruning will further separate the difference pieces.")

    for i in range(0, size):
        endpoints = find_tips(pruned_img)
        pruned_img = image_subtract(pruned_img, endpoints)

    # Reset debug mode
    params.debug = debug

    params.device += 1

    if params.debug == 'print':
        print_image(pruned_img, os.path.join(params.debug_outdir, str(params.device) + '_pruned.png'))
    elif params.debug == 'plot':
        plot_image(pruned_img, cmap='gray')

    return pruned_img
