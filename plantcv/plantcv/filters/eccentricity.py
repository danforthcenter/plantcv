# Detect dics based on object eccentricity
import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def eccentricity(bin_img, ecc_thresh=0):
    """Detect/filter disc-shaped regions in a binary image based on eccentricity.

    A value of eccentricity between 0 and 1 corresponds to an ellipse.
    The closer the value to 0 the closer the shape is to a circle.

    Inputs:
    bin_img       = Binary image containing the connected regions to consider
    ecc_thresh    = Eccentricity threshold below which a region is kept


    Returns:
    discs_mask  = Binary image that contains only the detected discs

    :param bin_img: numpy.ndarray
    :param ecc_thresh: float
    :return discs_mask: numpy.ndarray
    """
    params.device += 1
    # label connected regions
    labeled_img = label(bin_img)
    # measure region properties
    obj_measures = regionprops(labeled_img)
    # blank mask to draw discs onto
    discs_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
    # Store the list of coordinates (row,col) for the objects that pass
    for obj in obj_measures:
        if obj.eccentricity < ecc_thresh:
            # Convert coord values to int
            discs_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)

    _debug(visual=discs_mask, filename=os.path.join(params.debug_outdir, f"{params.device}_discs_mask_{ecc_thresh*10}.png"))

    return discs_mask
