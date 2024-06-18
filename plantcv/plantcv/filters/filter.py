# Filter objects based on calculated properties
import os
import numpy as np
from skimage.measure import label, regionprops
from plantcv.plantcv import params, fatal_error
from plantcv.plantcv._debug import _debug

def filter_property(bin_img, cut_side = "upper", thresh="NA", property="area"):
    """Detect/filter regions in a binary image based on anything calculated by skimage.measure.regionprops.
    Inputs:
    bin_img         = Binary image containing the connected regions to consider
    cut_side        = "upper" or "lower", side to keep when objects are divided by the "thresh" value
    thresh          = Threshold above which a region is kept 
    property        = Which object property to filter on. 
                      Can choose from "float" or "int" type properties calculated by scikitimage.measure.regionprops
    Returns:
    filtered_mask  = Binary image that contains only the detected objects
    :param bin_img: numpy.ndarray
    :param cut_sice: string
    :param thresh: float
    :param property: string
    :return filtered_mask: numpy.ndarray
    """
    params.device += 1
    if cut_side != "upper" and cut_side != "lower":
        fatal_error("Must specify either 'upper' or 'lower' for cut_side")
    # label connected regions
    labeled_img = label(bin_img)
    # measure region properties
    obj_measures = regionprops(labeled_img)
    # check to see if property of interest is the right type
    correct_types = [np.int64, np.float64, int, float]
    if type(getattr(obj_measures[0], property)) in correct_types:  
        # blank mask to draw discs onto
        filtered_mask = np.zeros(labeled_img.shape, dtype=np.uint8)
        # check if there's a thresh value or not:
        if thresh != "NA":
        # Store the list of coordinates (row,col) for the objects that pass
        # also store a list of all values to print the range
            valueslist = []
            for obj in obj_measures:
                valueslist.append(getattr(obj, property))
                if cut_side == "upper":
                    if getattr(obj, property) > thresh:
                        # Convert coord values to int
                        filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
                elif cut_side == "lower":
                    if getattr(obj, property) < thresh:
                        # Convert coord values to int
                        filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
        else:
            valueslist = []
            for obj in obj_measures:
                valueslist.append(getattr(obj, property))
            mean_val = sum(valueslist)/len(valueslist)
            for obj in obj_measures:
                if cut_side == "upper":
                    if getattr(obj, property) > mean_val:
                        # Convert coord values to int
                        filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
                elif cut_side == "lower":
                    if getattr(obj, property) < mean_val:
                        # Convert coord values to int
                        filtered_mask += np.where(labeled_img == obj.label, 255, 0).astype(np.uint8)
        if params.debug == "plot":
            print("Min value = " + str(min(valueslist)))
            print("Max value = " + str(max(valueslist)))
            print("Mean value = " + str(sum(valueslist)/len(valueslist)))
    
        _debug(visual=filtered_mask, filename=os.path.join(params.debug_outdir, f"{params.device}_discs_mask_{property}_{thresh}.png"))
    else:  # Property not the right type
        print(type(getattr(obj_measures[0], property)))
        fatal_error("Property must be of type 'integer' or 'float'")
    return filtered_mask