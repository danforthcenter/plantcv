# Prune barbs off skeleton image

import os
import cv2
import numpy as np
from plantcv.plantcv import params, outputs
from plantcv.plantcv import image_subtract
from plantcv.plantcv.morphology import segment_sort, find_branch_pts, segment_skeleton
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _iterative_prune


def prune(skel_img, size=0, mask=None):
    """Prune the ends of skeletonized segments.
    The pruning algorithm proposed by https://github.com/karnoldbio
    Segments a skeleton into discrete pieces, prunes off all segments less than or
    equal to user specified size. Returns the remaining objects as a list and the
    pruned skeleton.

    Inputs:
    skel_img    = Skeletonized image
    size        = Size to get pruned off each branch
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.

    Returns:
    pruned_img      = Pruned image
    segmented_img   = Segmented debugging image
    segment_objects = List of contours

    :param skel_img: numpy.ndarray
    :param size: int
    :param mask: numpy.ndarray
    :return pruned_img: numpy.ndarray
    :return segmented_img: numpy.ndarray
    :return segment_objects: list
    """
    # Store debug
    debug = params.debug
    params.debug = None

    _, objects = segment_skeleton(skel_img)
    kept_segments = []
    removed_segments = []
    # Initialize pruned_img array
    pruned_img = skel_img.copy()
    if size > 0:
        # Sort through segments since we don't want to remove primary segments
        secondary_objects, _ = segment_sort(skel_img, objects)

        # Keep segments longer than specified size
        for i in range(0, len(secondary_objects)):
            if len(secondary_objects[i]) > size:
                kept_segments.append(secondary_objects[i])
            else:
                removed_segments.append(secondary_objects[i])

        # Draw the contours that got removed
        removed_barbs = np.zeros(skel_img.shape[:2], np.uint8)
        cv2.drawContours(removed_barbs, removed_segments, -1, 255, 1,
                         lineType=8)

        # Subtract all short segments from the skeleton image
        pruned_img = image_subtract(skel_img, removed_barbs)
        pruned_img = _iterative_prune(pruned_img, 1)

    # Make debugging image
    if mask is None:
        pruned_plot = np.zeros(skel_img.shape[:2], np.uint8)
    else:
        pruned_plot = mask.copy()
    pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
    pruned_obj, _ = _cv2_findcontours(bin_img=pruned_img)
    cv2.drawContours(pruned_plot, removed_segments, -1, (0, 0, 255), params.line_thickness, lineType=8)
    cv2.drawContours(pruned_plot, pruned_obj, -1, (150, 150, 150), params.line_thickness, lineType=8)

    # Segment the pruned skeleton
    segmented_img, segment_objects = segment_skeleton(pruned_img, mask)

    # Reset debug mode
    params.debug = debug

    _debug(visual=pruned_img, filename=os.path.join(params.debug_outdir, f"{params.device}_pruned.png"))
    _debug(visual=pruned_plot, filename=os.path.join(params.debug_outdir, f"{params.device}_pruned_debug.png"))

    return pruned_img, segmented_img, segment_objects


def prune_by_height(skel_img, line_position=None, mask=None, label=None):
    """Prune the segments of a skeleton.
    The pruning algorithm proposed by Renee Dale and implemented by Haley Schuhl. 
    Segments a skeleton into discrete pieces, prunes off all below a height threshold.
    Returns the remaining objects as a list and the
    pruned skeleton.

    Inputs:
    skel_img      = Skeletonized image
    line_position = Height below which to prune secondary segments 
    mask          = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = pcv.params.sample_label).

    Returns:
    pruned_img      = Pruned image
    segmented_img   = Segmented debugging image
    segment_objects = List of contours

    :param skel_img: numpy.ndarray
    :param size: int
    :param mask: numpy.ndarray
    :param label: str
    :return pruned_img: numpy.ndarray
    :return segmented_img: numpy.ndarray
    :return segment_objects: list
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Store debug
    debug = params.debug
    params.debug = None

    if line_position is None:
        # Find the line position based on the highest branch point in the skeleton
        _ = find_branch_pts(skel_img=skel_img)
        branch_pts = outputs.observations['default']['branch_pts']['value']
        # Using the min function with a key
        min_y = min(branch_pts, key=lambda coord: coord[1])
        line_position = min_y[1]
    img_dims = np.shape(skel_img)[:2]
    h = img_dims[1] - line_position
    h = line_position + 1 # Adjust by one pixel to shift from directly on the branch point 

    _, objects = segment_skeleton(skel_img)
    kept_segments = []
    removed_segments = []

    if h > 0:
        # If size>0 then check for segments that are smaller than size pixels long

        # Sort through segments since we don't want to remove primary segments
        secondary_objects, _ = segment_sort(skel_img, objects)

        # Keep segments longer than specified size
        for i in range(0, len(secondary_objects)):
            _, y, _, h2 = cv2.boundingRect(secondary_objects[i]) # Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height 
            
            if y + h2 <= h:
                kept_segments.append(secondary_objects[i])
            else:
                removed_segments.append(secondary_objects[i])

        # Draw the contours that got removed
        removed_barbs = np.zeros(skel_img.shape[:2], np.uint8)
        cv2.drawContours(removed_barbs, removed_segments, -1, 255, 1,
                         lineType=8)

        # Subtract all short segments from the skeleton image
        pruned_img = image_subtract(skel_img, removed_barbs)
        pruned_img = _iterative_prune(pruned_img, 1)

    # Make debugging image
    if mask is None:
        pruned_plot = np.zeros(skel_img.shape[:2], np.uint8)
    else:
        pruned_plot = mask.copy()
    pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
    pruned_obj, _ = _cv2_findcontours(bin_img=pruned_img)
    cv2.drawContours(pruned_plot, removed_segments, -1, (0, 0, 255), params.line_thickness, lineType=8)
    cv2.drawContours(pruned_plot, pruned_obj, -1, (150, 150, 150), params.line_thickness, lineType=8)
    start_point = (0,h) 
    end_point = (img_dims[0], h)
    cv2.line(pruned_plot, start_point, end_point, color=(155, 0, 155), thickness=params.line_thickness, lineType=8)


    # Segment the pruned skeleton
    segmented_img, segment_objects = segment_skeleton(pruned_img, mask)
    # Save outputs about number of segments above/below reference
    outputs.add_observation(sample=label, variable='prune_horizontal_reference_position',
                            trait='prune horizontal reference position',
                            method='plantcv.plantcv.morphology.prune_by_height', scale='pixels', datatype=int,
                            value=h, label='none')
    outputs.add_observation(sample=label, variable='segments_above_reference', trait='segments above reference',
                            method='plantcv.plantcv.morphology.prune_by_height', scale='object_number', datatype=int,
                            value=len(kept_segments), label="none")
    outputs.add_observation(sample=label, variable='segments_below_reference', trait='segments below reference',
                            method='plantcv.plantcv.morphology.prune_by_height', scale='object_number', datatype=int,
                            value=len(removed_segments), label="none")

    # Reset debug mode
    params.debug = debug

    _debug(visual=pruned_img, filename=os.path.join(params.debug_outdir, f"{params.device}_pruned.png"))
    _debug(visual=pruned_plot, filename=os.path.join(params.debug_outdir, f"{params.device}_pruned_debug.png"))

    return pruned_img, segmented_img, segment_objects
