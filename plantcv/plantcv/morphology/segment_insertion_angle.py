"""Find leaf insertion angles with stem."""
import os
import cv2
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv.morphology.segment_tangent_angle import _slope_to_intersect_angle
from plantcv.plantcv._helpers import _cv2_findcontours, _find_tips, _iterative_prune, _logical_operation, _dilate, _closing


def _segment_insertion_angle(morph, size=20, label=None):
    """
    Find leaf insertion angles in degrees of skeleton segments.

    Fit a linear regression line to the stem. Use `size` pixels on the portion of leaf next to the stem to find a linear
    regression line, and calculate the angle between the two lines per leaf object.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label : str, optional
        Label parameter, modifies the variable name of observations recorded (default = pcv.params.sample_label).
    """
    skel_img = morph.skeleton
    segmented_img = morph.skeleton
    leaf_objects = morph.leaves
    stem_objects = morph.stem

    cols = segmented_img.shape[1]
    segment_slopes = []
    insertion_segments = []
    insertion_hierarchies = []
    intersection_angles = []
    all_intersection_angles = []
    label_coord_x = []
    label_coord_y = []
    valid_segment = []
    pruned_away = []

    # Create a list of tip tuples to use for sorting
    tips, _, _ = _find_tips(skel_img)

    for i, cnt in enumerate(leaf_objects):
        # Draw leaf objects
        find_segment_tangents = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)

        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, size)

        # Segment ends are the portions pruned off
        segment_ends = find_segment_tangents - pruned_segment
        segment_end_obj, segment_end_hierarchy = _cv2_findcontours(bin_img=segment_ends)

        if not len(segment_end_obj) == 2:
            print("Size too large, contour with ID#", i, "got pruned away completely.")
            pruned_away.append(True)
        else:
            # The contour can have insertion angle calculated
            pruned_away.append(False)
            valid_segment.append(cnt)

            # Determine if a segment is leaf end or leaf insertion segment
            for j, obj in enumerate(segment_end_obj):

                segment_plot = np.zeros(segmented_img.shape[:2], np.uint8)
                cv2.drawContours(segment_plot, obj, -1, 255, 1, lineType=8)
                segment_plot = _dilate(segment_plot, 3, 1)
                overlap_img = _logical_operation(segment_plot, tips, "and")

                # If none of the tips are within a segment_end then it's an insertion segment
                if np.sum(overlap_img) == 0:
                    insertion_segments.append(segment_end_obj[j])
                    insertion_hierarchies.append(segment_end_hierarchy[0][j])

            # Store coordinates for labels
            label_coord_x.append(leaf_objects[i][0][0][0])
            label_coord_y.append(leaf_objects[i][0][0][1])

    # Plot stem segments
    combined_stem = _combine_stem(segmented_img, stem_objects)
    # Find slope of the stem
    [vx, vy, x, y] = cv2.fitLine(combined_stem[0], cv2.DIST_L2, 0, 0.01, 0.01)
    stem_slope = -vy / vx
    stem_slope = stem_slope[0]

    for t, segment in enumerate(insertion_segments):
        # Find line fit to each segment
        [vx, vy, x, y] = cv2.fitLine(segment, cv2.DIST_L2, 0, 0.01, 0.01)
        slope = -vy / vx
        left_list = int(np.array((-x * vy / vx) + y).item())
        right_list = int(np.array(((cols - x) * vy / vx) + y).item())
        segment_slopes.append(slope[0])

        # Store intersection angles between insertion segment and stem line
        intersection_angle = _slope_to_intersect_angle(slope[0], stem_slope)
        # Function measures clockwise but we want the acute angle between stem and leaf insertion
        if intersection_angle > 90:
            intersection_angle = 180 - intersection_angle
        intersection_angles.append(intersection_angle)

    intersection_angles_editing = intersection_angles.copy()
    for j in pruned_away:
        if j:
            all_intersection_angles.append('NA')
        else:
            all_intersection_angles.append(intersection_angles_editing.pop(0))

    segment_ids = [i for i in range(len(insertion_segments))]

    outputs.add_observation(sample=label, variable='segment_insertion_angle', trait='segment insertion angle',
                            method='plantcv.plantcv.morphology.segment_insertion_angle', scale='degrees', datatype=list,
                            value=all_intersection_angles, label=segment_ids)



def _combine_stem(segmented_img, stem_objects, maxiter=50):
    """
    Combine multiple stem contours into a single stem contour.

    Parameters
    ----------
    segmented_img : numpy.ndarray
        Segmented image used for plotting and processing.
    stem_objects : list of numpy.ndarray
        List of contours representing stem objects.
    maxiter : int, optional
        Maximum number of iterations to attempt merging stem objects (default is 50).

    combined_stem : list of numpy.ndarray
        List containing the merged stem contour.

    Returns
    -------
    combined_stem : list of numpy.ndarray
        List containing the merged stem contour.

    Raises
    ------
    RuntimeError
        If stem objects cannot be combined into a single contour within `maxiter` iterations.
    """
    stem_img = np.zeros(segmented_img.shape[:2], np.uint8)
    cv2.drawContours(stem_img, stem_objects, -1, 255, 2, lineType=8)
    stem_img = _closing(stem_img)
    combined_stem, _ = _cv2_findcontours(bin_img=stem_img)

    # Make sure stem objects are a single contour
    loop_count = 0
    while len(combined_stem) > 1 and loop_count < maxiter:
        loop_count += 1
        stem_img = _dilate(stem_img, 2, 1)
        stem_img = _closing(stem_img)
        combined_stem, _ = _cv2_findcontours(bin_img=stem_img)
    if len(combined_stem) > 1:
        fatal_error('Unable to combine stem objects.')
    return combined_stem
