# Filter objects based on calculated properties
import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params, fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rect_filter, _rect_replace


def obj_props(bin_img, cut_side="upper", thresh=0, regprop="area", roi=None):
    """Detect/filter regions in a binary image based on calculated properties.

    Parameters:
    ----------
    bin_img : numpy.ndarray
        Binary image containing the objects to consider.
    cut_side : str, default: "upper"
        Side to keep when objects are divided by the "thresh" value,
        options are 'upper', 'lower', 'in' (within tuple of thresh range),
        and 'out' (outside of tuple of thresh range)
    thresh : int | float | tuple of int/float, default: 0
        Region property threshold value. 'in' and 'out' cut_side require a tuple.
    regprop : str, default: "area"
        Region property to filter on. Can choose from "area" or other int and float properties calculated by
        skimage.measure.regionprops.
    roi : plantcv.plantcv.Objects, default None
        Optional region of interest to apply the object property filter within

    Returns:
    -------
    filtered_mask : numpy.ndarray
        Binary image that contains only the filtered objects.
    """
    # Increment step counter
    params.device += 1
    # Make cut_side all lowercase
    cut_side = cut_side.lower()
    # Check if cut_side is valid
    if cut_side.lower() not in ("upper", "lower", "in", "out"):
        fatal_error("Must specify either 'upper', 'lower', 'in', or 'out' for cut_side")
    if cut_side.lower() in ("in", "out") and not isinstance(thresh, tuple):
        fatal_error("If cut_side is 'in' or 'out' then thresh must be a tuple")
    # subset binary image for ROI
    sub_bin_img = _rect_filter(bin_img, roi=roi)
    # Skip empty masks
    if np.count_nonzero(sub_bin_img) != 0:
        # label connected regions in ROI
        labeled_img = label(sub_bin_img)
        # measure region properties
        obj_measures = regionprops(labeled_img)
        # list of correct data types
        correct_types = [np.int64, np.float64, int, float]
        # check to see if property of interest is the right type
        if type(getattr(obj_measures[0], regprop)) not in correct_types:
            fatal_error(f"Property {regprop} is not an integer or float type.")

        # blank mask to draw discs onto
        sub_filtered_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
        # Pull all values and calculate the mean
        valueslist = []
        # Store the list of coordinates (row,col) for the objects that pass
        for obj in obj_measures:
            # Object color
            gray_val = 255
            # Store the value of the property for each object
            val = getattr(obj, regprop)
            valueslist.append(val)
            # apply filter
            gray_val = _apply_cut_side(cut_side, thresh, val)
            # Add the object to the filtered mask (255 if it passes, 0 if it does not)
            sub_filtered_mask += np.where(labeled_img == obj.label, gray_val, 0).astype(np.uint8)

        if params.debug == "plot":
            print(f"Min value = {min(valueslist)}")
            print(f"Max value = {max(valueslist)}")
            print(f"Mean value = {sum(valueslist)/len(valueslist)}")

    else:
        sub_filtered_mask = np.copy(sub_bin_img)
    # slice subset back into full size binary image
    filtered_mask = _rect_replace(bin_img, sub_filtered_mask, roi)

    _debug(visual=filtered_mask, filename=os.path.join(params.debug_outdir,
                                                       f"{params.device}_filter_mask_{regprop}_{thresh}.png"))
    return filtered_mask


def _apply_cut_side(cut_side, thresh, val):
    """Helper function to apply a filter based on the cut_side

    Parameters
    ----------
    cut_side = str,
        direction of filter, one of 'upper', 'lower', 'in', or 'out'
    thresh   = int, float, or tuple of int/float
        value above/below/between/within which to keep an object based on cut_side
    val      = int or float
        The numeric property of an object

    Returns
    -------
    gray_val = int,
        255 or 0 depending on the logical evaluation of the cut side
    """
    # If it is an upper threshold, keep the objects that are above the threshold
    if cut_side == "upper":
        gray_val = 255 if val > max(thresh) else 0
    # If it is a lower threshold, keep the objects that are below the threshold
    elif cut_side == "lower":
        gray_val = 255 if val < min(thresh) else 0
    # If it is 'in' threshold, keep the objects that are within the thresholds
    elif cut_side == "in":
        gray_val = 255 if val > min(thresh) or val < max(thresh) else 0
    # If it is 'out' threshold, keep the objects that are outside of the thresholds
    elif cut_side == "out":
        gray_val = 255 if val < min(thresh) or val > max(thresh) else 0
    return gray_val
