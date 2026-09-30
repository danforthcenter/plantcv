from plantcv.plantcv.visualize.colorize_label_img import colorize_label_img
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.roi.roi_methods import circle
from plantcv.plantcv.roi.roi2mask import roi2mask
from plantcv.plantcv.warn import warn
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
import numpy as np
import random
import cv2
import os


def sub_mask(img, mask, num_masks=1, radius=5):
    """
    Make circular sub-masks inside the mask of an object

    Parameters
    ----------
    img       : numpy.ndarray,
        input image
    mask      : numpy.ndarray,
        binary mask of object
    num_masks : int,
        number of circular sub-masks to make
    radius    : int,
        radius of circular mask to make. Defaults to 5.

    Returns
    -------
    labeled_mask : numpy.ndarray,
        labelled mask of circular masks each within complete mask.
    """
    # Create an empty labeled mask with sufficient integer range for labels
    labeled_mask = np.zeros(mask.shape[:2], dtype=np.int32)
    tries = 0
    sample_num = 0
    debug_state = params.debug
    while sample_num < num_masks:
        tries += 1
        params.debug = None
        spot = _make_random_circle(img=img, mask=mask, radius=radius)
        spot_mask = roi2mask(img=img, roi=spot)
        params.debug = debug_state
        within = _is_mask_within(full_mask=mask, submask=spot_mask)
        overlapping = _check_overlapping_masks(labeled_mask, spot_mask)
        if within and overlapping:
            sample_num += 1
            # Label spots with unique integers
            labeled_mask[np.where(spot_mask > 0)] = sample_num
        if tries > num_masks * 100:  # Prevent infinite loop
            # warn if stuck, break loop
            warn("Too many iterations. Placed " + str(sample_num) +
                 " circular masks instead of " + str(num_masks))
            break

    if sample_num == 1:
        labeled_mask = (labeled_mask*255).astype(np.uint8)

    if debug_state:
        params.debug = None
        col_mask = colorize_label_img(labeled_mask)
        params.debug = debug_state
        _debug(visual=col_mask,
               filename=os.path.join(params.debug_outdir,
                                     f"{params.device}_sub_mask.png"))

    return labeled_mask


def _check_overlapping_masks(labeled_mask, new_mask):
    """
    Check for any overlapping masks

    Parameters
    ----------
    labeled_mask : numpy.ndarray,
        the labeled_mask that the new_mask may be added to
    new_mask     : numpy.ndarray,
        the new proposed region to mask

    Returns
    -------
    Boolean, True if new_mask does not overlap the labeled mask
    """
    # set all labeled mask values to 1 for bin_mask
    bin_mask = np.copy(labeled_mask)
    bin_mask[np.where(bin_mask > 0)] = 1
    new_bin = np.copy(new_mask)
    new_bin[np.where(new_bin > 0)] = 1
    # check max of sum of binary mask and new_mask
    return np.max(np.add(bin_mask, new_bin)) == 1


def _make_random_circle(img, mask, radius=5):
    """
    Make a circular ROI at a random point in a mask

    Parameters
    ----------
    img    : numpy.ndarray,
        input image
    mask   : numpy.ndarray,
        binary mask of an object
    radius : int,
        radius of circular mask to make. Defaults to 5.

    Returns
    -------
    spot : PlantCV.Objects class,
        Circular ROI in random part of mask.
    """
    # Find coordinates in mask where mask is non-zero
    coords = np.column_stack(np.where(mask > 0))
    # Filter for only coords that are at least radius away from image edge
    y_filt = (coords[:, 0] >= 0 + radius) & (coords[:, 0] <= mask.shape[0] - radius)
    x_filt = (coords[:, 1] >= 0 + radius) & (coords[:, 1] <= mask.shape[1] - radius)
    coords_filt = coords[y_filt & x_filt]
    if not coords_filt.any():
        fatal_error("Mask is empty, no subset circles can be placed.")
    # Randomly select a center point from these coordinates
    center = coords_filt[random.randint(0, len(coords_filt) - 1)]
    x, y = center[1], center[0]
    # Create an ROI from the random center point
    spot = circle(img=img, x=x, y=y, r=radius)
    return spot


def _is_mask_within(full_mask, submask):
    """
    Check if a mask is wholly within another mask

    Parameters
    ----------
    full_mask  : numpy.ndarray,
        complete binary mask of an object
    sub_mask   : numpy.ndarray,
        binary mask of a smaller part of the full mask

    Returns
    -------
    within :Boolean,
        comparison of full_mask against full_mask and sub_mask.
    """
    combined = cv2.bitwise_and(submask, full_mask)
    within = np.array_equal(combined.astype(bool), submask.astype(bool))
    return within
