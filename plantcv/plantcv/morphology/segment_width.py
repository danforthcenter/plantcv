"""A function that analyzes the width of an object using a distance transformation."""

import os
import cv2
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._helpers import _scale_size
from plantcv.plantcv._debug import _debug


def _iterate_distance_transform(bin_img, threshold=0.4):
    result = bin_img.copy()
    for _ in range(5):
        dt = cv2.distanceTransform(result.astype(np.uint8), cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
        dt_normalized = cv2.normalize(dt, None, 0, 1, cv2.NORM_MINMAX)
        result = (dt_normalized > threshold).astype(np.uint8) * 255
    return result


def segment_width(img, labeled_mask, n_labels=1, label=None):
    """A function that analyzes the width of an object using a distance transformation.

    Inputs:
    img          = RGB or grayscale image data for plotting
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    widths = []
    for i in range(1, n_labels + 1):
        submask = np.where(labeled_mask == i, 255, 0).astype(np.uint8)
        # Set lable to params.sample_label if None
        if label is None:
            label = params.sample_label

        if np.count_nonzero(submask) > 0:
            mask_copy = submask.copy().astype(np.uint8)
            k = cv2.distanceTransform(mask_copy, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
            k_normalized = cv2.normalize(k, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            weights = _iterate_distance_transform((mask_copy > 127).astype(np.uint8) * 255)
            
            # Calculate stroke width
            k_flat = k.flatten()
            weights_flat = weights.flatten() / 255.0
            
            # Select non-zero values from weighted distance transform
            nonzero_mask = (k_flat * weights_flat) != 0
            weighted_values = k_flat[nonzero_mask]
            
            if len(weighted_values) > 0:
                stroke_width = 2 * np.mean(weighted_values)
                widths.append(stroke_width.astype(np.float64))
                print(f"Stroke Width = {stroke_width}")
                
            else:
                widths.append(0)
                print("No stroke width detected")
        
     
    outputs.add_observation(sample=label, variable='segment_width', trait='segment width',
                                method='plantcv.plantcv.morphology.analyze_width',
                                scale=params.unit, datatype=list,
                                value=_scale_size(value=widths, trait_type="segment_width"),
                                label=range(1, n_labels + 1))   
    all_mask = np.where(labeled_mask > 0, 255, 0).astype(np.uint8)
    dist = cv2.distanceTransform(all_mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    # Debugging
    _debug(visual=dist, filename=os.path.join(params.debug_outdir, str(params.device) + '_segment_width.png'))
    
    return dist
