# Filter objects based on calculated properties
import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params, fatal_error
from plantcv.plantcv._debug import _debug


def filter_objs(bin_img, cut_side="upper", thresh="NA", regprop="area"):
    """Detect/filter regions in a binary image based on anything calculated by skimage.measure.regionprops.
    Inputs:
    bin_img         = Binary image containing the connected regions to consider
    cut_side        = "upper" or "lower", side to keep when objects are divided by the "thresh" value
    thresh          = Threshold above which a region is kept
    regprop         = Which object property to filter on
                      Can choose from "float" or "int" type properties calculated by scikitimage.measure.regionprops
    Returns:
    filtered_mask  = Binary image that contains only the detected objects
    :param bin_img: numpy.ndarray
    :param cut_sice: string
    :param thresh: float
    :param regprop: string
    :return filtered_mask: numpy.ndarray
    """
    params.device += 1
    if cut_side not in ("upper", "lower"):
        fatal_error("Must specify either 'upper' or 'lower' for cut_side")
    # label connected regions
    labeled_img = label(bin_img)
    # measure region properties
    obj_measures = regionprops(labeled_img)
    # check to see if property of interest is the right type
    correct_types = [np.int64, np.float64, int, float]
    if type(getattr(obj_measures[0], regprop)) in correct_types: 
        # blank mask to draw discs onto
        filtered_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
        # Pull all values and calculate the mean
        valueslist = []
        for obj in obj_measures:
            valueslist.append(getattr(obj, regprop))
        if thresh == "NA":
            thresh = sum(valueslist)/len(valueslist)   # mean
        # Store the list of coordinates (row,col) for the objects that pass
        if cut_side == "upper":
            for obj in obj_measures:
                if getattr(obj, regprop) > thresh:
                    # Convert coord values to int
                    filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
        elif cut_side == "lower":
            for obj in obj_measures:
                if getattr(obj, regprop) < thresh:
                    # Convert coord values to int
                    filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
        if params.debug == "plot":
            print("Min value = " + str(min(valueslist)))
            print("Max value = " + str(max(valueslist)))
            print("Mean value = " + str(sum(valueslist)/len(valueslist)))

        _debug(visual=filtered_mask, filename=os.path.join(params.debug_outdir, 
                                                           f"{params.device}_discs_mask_{regprop}_{thresh}.png"))
    else:  # Property not the right type
        print(type(getattr(obj_measures[0], regprop)))
        fatal_error("regprop must be of type 'integer' or 'float'")
    return filtered_mask
