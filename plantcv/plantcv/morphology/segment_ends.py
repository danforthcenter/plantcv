# Find both segment end coordinates 
import os
import cv2
import numpy as np
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.morphology import _iterative_prune
from plantcv.plantcv._helpers import _cv2_findcontours


def segment_ends(segmented_img, objects, label=None):
    """Find tips in skeletonized image.
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699

    Inputs:
    objects     = List of contours to analyze
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label       = Optional label parameter, modifies the variable name of
                  observations recorded (default = pcv.params.sample_label).

    :param segmented_img: numpy.ndarray
    :param objects: list
    :param label: str
    """
    
    labeled_img = segmented_img.copy()
    leaf_objects = objects
    segment_end_objs1 = [] 
    segment_end_objs2 = [] 

    # Find segment end coordinates
    for i in range(len(leaf_objects)):
        # Draw leaf objects
        find_segment_tangents = np.zeros(labeled_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)
        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, 1)
        # Segment ends are the portions pruned off
        segment_ends = find_segment_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=segment_ends)
        segment_end_objs1.append(segment_end_obj[0])
        segment_end_objs2.append(segment_end_obj[1])
        
    # Initialize list of tip data points
    tip_list = []
    labels = []
    inner_list = [] 
    for i, coor in enumerate(segment_end_objs1):
        x, y = coor.ravel()[:2]
        coord = (int(x), int(y))
        inner_list.append(coord)
        print(coord)
        labels.append(i)
        cv2.drawContours(labeled_img, leaf_objects, i, (150, 150, 150), params.line_thickness, lineType=8)  # segments
        cv2.circle(labeled_img, (x, y), params.line_thickness, (50, 0, 255), -1)  # Red auricles
        tip = segment_end_objs2[i]
        x, y = tip.ravel()[:2]
        coord = (int(x), int(y))
        tip_list.append(coord)
        cv2.circle(labeled_img, (x, y), params.line_thickness, (0, 255, 0), -1)  # green tips

    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Save coordinates to Outputs 
    outputs.add_observation(sample=label, variable='segment_tips', trait='list of tip coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=tip_list, label=labels)
    outputs.add_observation(sample=label, variable='segment_branch_points', trait='list of branch point coordinates identified from segments',
                            method='plantcv.plantcv.morphology.segment_ends', scale='None', datatype=list,
                            value=inner_list, label=labels)
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_ends.png"))
