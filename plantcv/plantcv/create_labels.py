# Create labels base on clean mask and optionally, multiple ROIs 

from plantcv.plantcv import params, roi_objects, Objects, _debug
from plantcv.plantcv._helpers import _cv2_findcontours
from skimage.color import label2rgb
import numpy as np
import cv2, os


def create_labels(mask, rois, roi_type="partial"):
    """Create a labeled mask for color card chips
    Inputs:
    mask            = Input RGB image data containing a color card.
    rois            = list of multiple ROIs (from roi.multi or roi.auto_grid)
    roi_type        = 'cutto', 'partial' (for partially inside, default), 'largest' (keep only the largest contour), or 'auto' (use the mask alone withtout roi filtering)

    Returns:
    mask            = Labeled mask of chips
    num_labels      = Number of labeled objects 

    :param mask: numpy.ndarray
    :param rois: plantcv.plantcv.classes.Objects
    :return mask: numpy.ndarray
    :return num_labels: int 
    """
    # Initialize chip list
    bin_img = np.zeros((np.shape(mask)[0], np.shape(mask)[1]), dtype=np.uint8)
    mask_copy = np.copy(mask)
    contours, hierarchy = _cv2_findcontours(mask) 
    
    if rois is not None:
        num_labels = len(rois.contours)
    else:
        if roi_type.upper() == "AUTO":
            for i, cnt in enumerate(contours): # assume 1:1 ratio of contours and entities (seed scatter edge case)
                labeled_masks = cv2.drawContours(mask_copy, cnt, -1, (i+1), -1)
                
        else: # assume single entity even if there are multiple contours (single plant)
            labeled_masks = cv2.drawContours(mask_copy, contours, -1, (255), -1)
            num_labels = len(contours)
    # Intermediate. Will change when implementing _roi_filter
    plant_obj = Objects(contours=[contours], hierarchy=[hierarchy])

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Loop over each color card row
    for i, roi in enumerate(rois):
        # Intermediate
        objects, intermediate_mask, obj_area = pcv.roi_objects(img=mask_copy, roi=roi, 
                                                               obj=plant_obj, roi_type=roi_type)
        # Pixel intensity of (i+1) such that the first object has value 
        labeled_masks = cv2.drawContours(mask_copy, objects.contours[0], -1, (i+1), -1)
        
    # Restore debug parameter
    params.debug = debug
    colorful = label2rgb(labeled_masks)

    _debug(colorful, filename=os.path.join(params.debug_outdir, str(params.device) + '_label_colored_mask.png'))

    
    return labeled_masks, num_labels
