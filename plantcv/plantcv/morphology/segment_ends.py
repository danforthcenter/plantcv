# Find both segment end coordinates 
import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv.morphology import _iterative_prune
from plantcv.plantcv._helpers import _cv2_findcontours


def segment_ends(objects, mask=None, label=None):
    """Find tips in skeletonized image.
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699

    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label       = Optional label parameter, modifies the variable name of
                  observations recorded (default = pcv.params.sample_label).
    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    :return tip_img: numpy.ndarray
    """
    
    mask_copy = mask.copy()
    leaf_objects = objects
    tip_plot = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
    segment_end_objs1 = [] 
    segment_end_objs2 = [] 

    # Find segment end coordinates
    for i, cnt in enumerate(leaf_objects):
        # Draw leaf objects
        find_segment_tangents = np.zeros(mask.shape[:2], np.uint8)
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
        cv2.drawContours(tip_plot, leaf_objects, i, (150, 150, 150), params.line_thickness, lineType=8)  # segments
        cv2.circle(tip_plot, (x, y), params.line_thickness, (50, 0, 255), -1)  # Red auricles
        tip = segment_end_objs2[i]
        x, y = tip.ravel()[:2]
        coord = (int(x), int(y))
        tip_list.append(coord)
        cv2.circle(tip_plot, (x, y), params.line_thickness, (0, 255, 0), -1)  # green tips
    _debug(visual=tip_plot, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_ends.png"))
