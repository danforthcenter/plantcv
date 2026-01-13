from plantcv.plantcv.roi.roi_methods import circle
from plantcv.plantcv.roi.roi2mask import roi2mask
from plantcv.plantcv.warn import warn
import numpy as np
import random
import cv2


def _make_random_circle(img, mask, radius=5):
    """
    Make a circular ROI at a random point in a mask

    Parameters
    ----------
    img    = numpy.ndarray, input image
    mask   = numpy.ndarray, binary mask of an object
    radius = int, radius of circular mask to make. Defaults to 5.

    Returns
    -------
    spot = PlantCV.Objects class, Circular ROI in random part of mask.
    """
    # Find coordinates in mask where mask is non-zero
    coords = np.column_stack(np.where(mask > 0))
    # Randomly select a center point from these coordinates
    center = coords[random.randint(0, len(coords) - 1)]
    x, y = center[1], center[0]
    # Create an ROI from the random center point
    spot = circle(img=img, x=x, y=y, r=radius)
    return spot


def _is_mask_within(full_mask, sub_mask):
    """
    Check if a mask is wholly within another mask

    Parameters
    ----------
    full_mask  = numpy.ndarray, complete binary mask of an object
    sub_mask   = numpy.ndarray, binary mask of a smaller part of the full mask

    Returns
    -------
    within = Boolean, comparison of full_mask against full_mask and sub_mask.
    """
    combined = cv2.bitwise_and(sub_mask, full_mask)
    within = np.array_equal(combined, sub_mask)
    return within


def sub_mask(img, mask, num_masks=1, radius=5):
    """
    Make circular sub-masks inside the mask of an object

    Parameters
    ----------
    img       = numpy.ndarray, input image
    mask      = numpy.ndarray, binary mask of object
    num_masks = int, number of circular sub-masks to make
    radius    = int, radius of circular mask to make. Defaults to 5.

    Returns
    -------
    labeled_mask = numpy.ndarray, labelled mask of circular masks each within complete mask.
    """
    # Create an empty mask
    labeled_mask = np.zeros_like(mask)
    tries = 0
    sample_num = 0
    while len(np.unique(labeled_mask)) - 1 < num_masks:
        tries += 1
        spot = _make_random_circle(img=img, mask=mask, radius=radius)
        spot_mask = roi2mask(img=img, roi=spot)
        within = _is_mask_within(full_mask=mask, sub_mask=spot_mask)
        if within:
            sample_num += 1
            # Label spots with unique integers
            labeled_mask[np.where(spot_mask > 0)] = sample_num
        if tries > num_masks * 100:  # Prevent infinite loop
            # warn if stuck, break loop
            warn("Too many iterations. Placed " + str(sample_num) +
                 " circular masks instead of " + str(num_masks))
            break
    return labeled_mask
