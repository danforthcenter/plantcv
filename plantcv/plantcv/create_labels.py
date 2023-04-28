from plantcv.plantcv import params, roi_objects, Objects
from plantcv.plantcv._helpers import _cv2_findcontours
from skimage.color import label2rgb
import cv2
import numpy as np 


def create_labels(mask, rois, roi_type="partial"):
    """Create a labeled mask for color card chips
    Inputs:
    mask            = Input RGB image data containing a color card.
    rois            = list of multiple ROIs (from roi.multi or roi.auto_grid)

    Returns:
    mask           = Labeled mask of chips
    number_labels  = Number of labeled objects 

    :param mask: numpy.ndarray
    :param rois: plantcv.plantcv.classes.Objects
    :return mask: numpy.ndarray
    """
    # Initialize chip list
    masks = []
    bin_img = np.zeros((np.shape(mask)[0], np.shape(mask)[1]), dtype=np.uint8)
    mask_copy = np.copy(mask)
    contours, hierarchy = _cv2_findcontours(mask) 
    
    if rois is not None:
        num_rois = len(rois.contours)
    else:
        # Dealing with a single entity/plant, or the edge case of seed scatter (have to assume 1:1 ratio of contours and entities)
        for i, cnt in enumerate(contours):
            labeled_masks = cv2.drawContours(mask_copy, cnt, -1, (i+1), -1)
    
    # Intermediate. Will change when implementing _roi_filter
    plant_obj = Objects(contours=[contours], hierarchy=[hierarchy])

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Loop over each color card row
    for i, roi in enumerate(rois):
        # Intermediate
        objects, intermediate_mask, obj_area = roi_objects(img=mask_copy, roi=roi, 
                                                               obj=plant_obj, roi_type=roi_type)
        # Pixel intensity of (i+1) such that the first object has value 
        labeled_masks = cv2.drawContours(mask_copy, objects.contours[0], -1, (i+1), -1)
        masks.append(intermediate_mask)
        
    # Restore debug parameter
    params.debug = debug
    
    return labeled_masks, num_rois

