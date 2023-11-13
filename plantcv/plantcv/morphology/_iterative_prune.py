import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import image_subtract
from plantcv.plantcv.morphology import find_tips
from plantcv.plantcv._helpers import _cv2_findcontours


def _iterative_prune(skel_img, size):
    """Iteratively remove endpoints (tips) from a skeletonized image.
    The pruning algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    "Prunes" barbs off a skeleton.
    Inputs:
    skel_img    = Skeletonized image
    size        = Size to get pruned off each branch
    Returns:
    pruned_img  = Pruned image
    :param skel_img: numpy.ndarray
    :param size: int
    :return pruned_img: numpy.ndarray
    """
    pruned_img = skel_img.copy()
    # Store debug
    debug = params.debug
    params.debug = None

    # Iteratively remove endpoints (tips) from a skeleton
    for _ in range(0, size):
        endpoints = find_tips(pruned_img)
        pruned_img = image_subtract(pruned_img, endpoints)

    # Make debugging image
    pruned_plot = np.zeros(skel_img.shape[:2], np.uint8)
    pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
    skel_obj, skel_hierarchy = _cv2_findcontours(bin_img=pruned_img)
    pruned_obj, pruned_hierarchy = _cv2_findcontours(bin_img=pruned_img)

    # Reset debug mode
    params.debug = debug

    cv2.drawContours(pruned_plot, skel_obj, -1, (0, 0, 255), params.line_thickness,
                     lineType=8, hierarchy=skel_hierarchy)
    cv2.drawContours(pruned_plot, pruned_obj, -1, (255, 255, 255), params.line_thickness,
                     lineType=8, hierarchy=pruned_hierarchy)

    return pruned_img
