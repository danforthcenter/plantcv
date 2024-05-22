# Filter regions based on object area
import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def obj_area(bin_img, upper_thresh, lower_thresh=0):
    """Detect/filter regions in a binary image based on object area.

    Inputs:
    bin_img         = Binary image containing the connected regions to consider
    upper_thresh    = Upper threshold size, above which an object is removed from the bin_img
    lower_thresh    = (Optional) Lower threshold size, below which an object is removed (default = 0)


    Returns:
    filtered_mask  = Binary image that contains only the filtered regions

    :param bin_img: numpy.ndarray
    :param upper_thresh: float
    :param lower_thresh: float
    :return filtered_mask: numpy.ndarray
    """
    params.device += 1
    # label connected regions
    labeled_img = label(bin_img)
    # measure region properties
    obj_measures = regionprops(labeled_img)
    # blank masks to draw discs onto
    large = np.zeros(labeled_img.shape, dtype=np.uint8)
    medium_large = np.zeros(labeled_img.shape, dtype=np.uint8)
    # Store the list of coordinates (row,col) for the objects that pass
    for obj in obj_measures:
        if obj.area > upper_thresh:
            # Where region area is too large, draw the region 
            large += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
        if obj.area > lower_thresh:
            # Where region area is large enough to keep, draw the region 
            medium_large += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
    # Keep middle sized objects
    keep = medium_large - large
    _debug(visual=keep, filename=os.path.join(params.debug_outdir, f"{params.device}_filters_area.png"))

    return keep
