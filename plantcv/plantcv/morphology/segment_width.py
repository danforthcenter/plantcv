"""A function that analyzes the width of an object using a distance transformation."""

import os
import cv2
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._helpers import _scale_size, _dilate, _cv2_findcontours
from plantcv.plantcv._debug import _debug


def segment_width(segmented_img, skel_img, labeled_mask, n_labels=1, label=None):
    """
    A function that analyzes the width of an object using a distance transformation.

    Parameters
    ----------
    segmented_img : numpy.ndarray
        Segmented image to plot slope lines and angles on.
    skel_img : numpy.ndarray
        Skeletonized image, ideally pruned/clean
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    n_labels : int
        Total number expected individual objects (default = 1).
    label : str, optional
        Label for the observation variable. If None, uses `params.sample_label`.

    Returns
    -------
    labeled_img : numpy.ndarray
        Segmented image with average width per segment.
    """
    widths = []
    dilated_midline =  _dilate(skel_img, 2, 1)
    labeled_img = segmented_img.copy()

    for i in range(1, n_labels + 1):
        submask = np.where(labeled_mask == i, 255, 0).astype(np.uint8)
        cnt, _ = _cv2_findcontours(submask)

        if np.count_nonzero(submask) > 0:
            mask_copy = submask.copy().astype(np.uint8)
            k = cv2.distanceTransform(mask_copy, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
                        
            # Select central non-zero values from weighted distance transform
            nonzero_mask = (k * dilated_midline) != 0
            weighted_values = k[nonzero_mask]
            
            if len(weighted_values) > 0:
                stroke_width = 2 * np.mean(weighted_values)
                widths.append(stroke_width.astype(np.float64))
                print(f"Stroke Width = {stroke_width}")
                text = str(int(stroke_width))
                cv2.putText(img=labeled_img, text=text, org=(cnt[0][0][0][0], cnt[0][0][0][1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
                        
            else:
                widths.append(0)
                print("No stroke width detected")
     
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    outputs.add_observation(sample=label, variable='segment_width', trait='segment width',
                                method='plantcv.plantcv.morphology.analyze_width',
                                scale=params.unit, datatype=list,
                                value=_scale_size(value=widths, trait_type="segment_width"),
                                label=range(1, n_labels + 1))   
    all_mask = np.where(labeled_mask > 0, 255, 0).astype(np.uint8)
    dist = cv2.distanceTransform(all_mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    # Debugging
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_segment_width.png'))
    
    return dist