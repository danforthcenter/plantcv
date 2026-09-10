"""A function that analyzes the width of an object using a distance transformation."""

import os
import cv2
import numpy as np
from plantcv.plantcv import outputs, params
from plantcv.plantcv._helpers import _scale_size, _dilate
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
    stdevs = []
    max_width = []
    dilated_midline = _dilate(skel_img, 2, 1)
    labeled_img = segmented_img.copy()

    for i in range(1, n_labels + 1):
        submask = np.where(labeled_mask == i, 255, 0).astype(np.uint8)
        if np.count_nonzero(submask) > 0:
            mask_copy = submask.copy().astype(np.uint8)
            # Find contours from the submask
            id_objects = cv2.findContours(mask_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]
            # ID and store area values and centers of mass for labeling them
            m = cv2.moments(id_objects[0])
            # Skip iteration if contour area is zero
            # This is needed because cv2.contourArea can be > 0 while moments area is 0.
            if m['m00'] != 0:
                label_coord_x = int(m["m10"] / m["m00"])
                label_coord_y = int(m["m01"] / m["m00"])
            k = cv2.distanceTransform(mask_copy, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

            # Select central non-zero values from weighted distance transform
            nonzero_mask = (k * dilated_midline) != 0
            weighted_values = k[nonzero_mask]

            if len(weighted_values) > 0:
                stroke_width = 2 * np.mean(weighted_values)
                stroke_width_max = 2 * np.max(weighted_values)
                width_std = np.std(weighted_values)
                widths.append(stroke_width.astype(np.float64))
                stdevs.append(width_std.astype(np.float64))
                max_width.append(stroke_width_max.astype(np.float64))
                text = str(int(stroke_width))
                if params.verbose:
                    cv2.putText(img=labeled_img, text=text,
                                org=(label_coord_x, label_coord_y),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=params.text_size, color=(150, 150, 150),
                                thickness=params.text_thickness)
            else:
                widths.append(0)
                stdevs.append("NA")
                max_width.append(0)

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    outputs.add_observation(sample=label, variable='mean_segment_width', trait='mean segment widths',
                            method='plantcv.plantcv.morphology.segment_width',
                            scale=params.unit, datatype=list,
                            value=_scale_size(value=widths, trait_type="linear"),
                            label=list(range(1, n_labels + 1)))
    outputs.add_observation(sample=label, variable='segment_width_std', trait='segment width standard deviation',
                            method='plantcv.plantcv.morphology.segment_width',
                            scale="pixels", datatype=list,
                            value=stdevs,
                            label=list(range(1, n_labels + 1)))
    outputs.add_observation(sample=label, variable='segment_width_max', trait='maximum segment widths',
                            method='plantcv.plantcv.morphology.segment_width',
                            scale=params.unit, datatype=list,
                            value=_scale_size(value=max_width, trait_type="linear"),
                            label=list(range(1, n_labels + 1)))
    # Debugging
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_segment_width.png'))

    return labeled_img
