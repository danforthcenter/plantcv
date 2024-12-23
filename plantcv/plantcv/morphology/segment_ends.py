# Find both segment end coordinates
import os
import cv2
import numpy as np
from plantcv.plantcv import dilate, logical_and
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.morphology import _iterative_prune, _find_tips
from plantcv.plantcv._helpers import _cv2_findcontours


def segment_ends(skel_img, leaf_objects, mask=None, label=None):
    """Find tips and segment branch points .

    Inputs:
    skel_img         = Skeletonized image
    leaf_objects     = List of leaf segments
    mask             = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    :param segmented_img: numpy.ndarray
    :param objects: list
    :param label: str
    """
    # Store debug
    debug = params.debug
    params.debug = None
    
    
    if mask is None:
        labeled_img = skel_img.copy()
    else:
        labeled_img = mask.copy()
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)
    tips, _, _ = _find_tips(skel_img)
    # Initialize list of tip data points
    tip_list = []
    labels = []
    inner_list = []

    # Find segment end coordinates
    for i in range(len(leaf_objects)):
        labels.append(i)
        # Draw leaf objects
        find_segment_tangents = np.zeros(labeled_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)
        cv2.drawContours(labeled_img, leaf_objects, i, (150, 150, 150), params.line_thickness, lineType=8)  # segments debug
        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, 1)
        # Segment ends are the portions pruned off
        ends = find_segment_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=ends)
        # Determine if a segment is segment tip or branch point
        for j, obj in enumerate(segment_end_obj):
            segment_plot = np.zeros(skel_img.shape[:2], np.uint8)
            cv2.drawContours(segment_plot, obj, -1, 255, 1, lineType=8)
            segment_plot = dilate(segment_plot, 3, 1)
            overlap_img = logical_and(segment_plot, tips)
            x, y = segment_end_obj[j].ravel()[:2]
            coord = (int(x), int(y))

            # If none of the tips are within a segment_end then it's an insertion segment
            if np.sum(overlap_img) == 0:
                inner_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (50, 0, 255), -1)  # Red auricles
            else:
                tip_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (0, 255, 0), -1)  # green tips
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Save coordinates to Outputs
    outputs.add_observation(sample=label, variable='segment_tips',
                            trait='list of tip coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=tip_list, label=labels)
    outputs.add_observation(sample=label, variable='segment_branch_points',
                            trait='list of branch point coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=inner_list, label=labels)
    # Reset debug mode
    params.debug = debug
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_ends.png"))
