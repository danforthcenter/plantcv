import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import logical_and
from plantcv.plantcv import find_objects
from scipy.spatial.distance import euclidean
from plantcv.plantcv.morphology import segment_id
from plantcv.plantcv.morphology import _iterative_prune


def _get_segment_ends(img, contour, size):
    """ Get end segments through pruning and subtracting off the original segment. Returns two end segment objects
        that are cv2 format contours.

            Inputs:
            img                 = Image for plotting size
            contour             = Original segment
            size                = Number of pixels to get pruned off each end of the original segment

            Returns:
            segment_end_objects = Two end objects

            :param img: numpy.ndarray
            :param contour: list
            :param size: int
            :return segment_end_objects: list
            """
    # Store debug mode
    debug = params.debug
    params.debug = None

    # Draw the segment
    segment_plot = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(segment_plot, contour, -1, 255, params.line_thickness, lineType=8)

    # Prune back ends of segments
    pruned_segment = _iterative_prune(segment_plot, size)

    # Segment ends are the portions pruned off
    segment_ends = segment_plot - pruned_segment
    segment_end_objects, _ = find_objects(segment_ends, segment_ends)

    return segment_end_objects


def _calc_proximity(target_obj, candidate_obj):
    """ Calculate the proximity of two segments by calculating euclidean distance between their centroids.

                Inputs:
                target_obj    = Original segment
                candidate_obj = Candidate segment

                Returns:
                proximity     = Distance between two segments

                :param target_obj: list
                :param candidate_obj: list
                :return proximity: int
                """
    # Compute the center of each contour
    target_moments = cv2.moments(target_obj)
    target_x = int(target_moments["m10"] / target_moments["m00"])
    target_y = int(target_moments["m01"] / target_moments["m00"])
    candidate_moments = cv2.moments(candidate_obj)
    candidate_x = int(candidate_moments["m10"] / candidate_moments["m00"])
    candidate_y = int(candidate_moments["m01"] / candidate_moments["m00"])

    # Compute distance between centroids
    proximity = int(euclidean((target_x, target_y), (candidate_x, candidate_y)))

    return proximity


def _calc_angle(img, object):
    """ Calculate the angle of a contour object

                Inputs:
                object    = Contour list

                Returns:
                angle     = Angle of the linear regression curve fit to the object

                :param object: list
                :return angle: int
                """
    # Fit a regression line to the object
    [vx, vy, x, y] = cv2.fitLine(object, cv2.DIST_L2, 0, 0.01, 0.01)
    # If the object is too small cv2 won't find a slope
    if vy == 0:
        obj_img = cv2.drawContours(img, object, -1, 255, params.line_thickness, lineType=8)
        dilated_img = dilate(gray_img=obj_img, ksize=10, i=1)
        dilated_objects, _ = find_objects(img=dilated_img, mask=dilated_img)
        [vx, vy, x, y] = cv2.fitLine(dilated_objects[0], cv2.DIST_L2, 0, 0.01, 0.01)
    slope = -vy / vx

    # Convert from line slope to degrees
    angle = np.arctan(slope[0]) * 180 / np.pi

    return angle


def _calc_compatibility(target_obj, candidate_obj):
    """ Calculate the compatibility of two segments using proximity and angle. If two segments have similar angle,
        and are close to one another they are more compatible.

                Inputs:
                target_obj    = Original segment
                candidate_obj = Candidate segment

                Returns:
                compatibility     = Distance between two segments

                :param target_obj: list
                :param candidate_obj: list
                :return compatibility: float
                """
    # Calculate distance between objects
    prox = _calc_proximity(target_obj=target_obj, candidate_obj=candidate_obj)

    # Calculate difference between the angle of each object
    target_angle = _calc_angle(object=target_obj)
    candidate_segment_angle = _calc_angle(candidate_obj)
    angle_difference = abs(candidate_segment_angle - target_angle)

    # Calculate compatibility score based proximity and angle similarity (lower compatibility scores are better)
    compatibility = (prox + (2 * angle_difference))

    return compatibility


def auto_combine_segments(segmented_img, leaf_objects, true_stem_obj, pseudo_stem_obj):
    """ Automatically combine pseudo-stems to pieces of leaf or other pseudo-stem based on the location of the
        important branch point, and the slope of the segment near the branch point

               Inputs:
               segmented_img       = Image for debugging
               leaf_objects        = Leaf object contours
               true_stem_obj       = Segments sorted to be true stem by the id_pseudo_stem function
               pseudo_stem_obj     = Segments sorted to be pseudo-stem by the id_pseudo_stem function

               Returns:
               segmented_img       = Debugging image
               new_leaf_obj        = Leaf objects after automatically combining segments together

               :param segmented_img: numpy.ndarray
               :param leaf_objects: list
               :param true_stem_obj: list
               :param pseudo_stem_obj: list
               :return segmented_img: numpy.ndarray
               :return new_leaf_obj: list
               """
    # Store debug mode
    debug = params.debug
    params.debug = None

    new_leaf_obj = [] # Leaf objects after automatically combining segments together
    branching_segments = []  # Segments that branch off from the stem
    secondary_segments = []  # Any pseudo-stem segments that aren't branching segments
    candidate_segments = leaf_objects.copy()
    plotting_img = np.zeros(segmented_img.shape[:2], np.uint8)

    # Plot true stem values to help with identifying the axil part of the segment
    cv2.drawContours(plotting_img, true_stem_obj, -1, 255, params.line_thickness, lineType=8)
    # Dilate stem
    stem_img = dilate(gray_img=plotting_img, ksize=4, i=1)

    # Identify "true leaf" segments i.e. single segments that accurately represent a biological leaf
    for i, cnt in enumerate(leaf_objects):
        segment_end_objs = _get_segment_ends(img=segmented_img, contour=cnt, size=10)
        # If one of the segment ends overlaps with the stem then it's a full leaf segment
        segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(segment_end_plot, segment_end_objs, -1, 255, params.line_thickness, lineType=8)
        overlap_img = logical_and(segment_end_plot, stem_img)
        # Add them to the list of new leaf objects
        if np.sum(overlap_img) > 0:
            new_leaf_obj.append(cnt)
            # Remove "true leaf" segments from candidate segments, they shouldn't get combined with any pseudo-stems
            candidate_segments.remove(cnt)

    # Loop through pseudo-stem segment contours to sort into ones next to stem and not
    for i, cnt in enumerate(pseudo_stem_obj):
        segment_end_objs = _get_segment_ends(img=segmented_img, contour=cnt, size=10)
        # If one of the segment ends overlaps with the stem then it's a branching segment
        segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(segment_end_plot, segment_end_objs, -1, 255, params.line_thickness, lineType=8)
        overlap_img = logical_and(segment_end_plot, stem_img)
        if np.sum(overlap_img) > 0:
            branching_segments.append(cnt)
        # Otherwise a segment is located between pseudo-stems or between a pseudo-stem and leaf object
        else:
            candidate_segments.append(cnt)

    # For each of the pseudo-stem segments, find the most compatible segment for combining
    for i, cnt in enumerate(branching_segments):
        candidate_compatibility = [] # Initialize list of compatibility scores
        # Determine which end of the branching segment is NOT the axil of the plant
        segment_end_objs = _get_segment_ends(img=segmented_img, contour=cnt, size=10)
        for j, end in enumerate(segment_end_objs):
            segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
            cv2.drawContours(segment_end_plot, end, -1, 255, params.line_thickness, lineType=8)
            overlap_img = logical_and(segment_end_plot, stem_img)
            if np.sum(overlap_img) == 0:
                target_segment = end
        # Calculate compatibility scores for each candidate segment
        for j, candidate in enumerate(candidate_segments):
            # Find which end of the candidate segment to compare to the target segment
            candidate_end_objs = _get_segment_ends(img=segmented_img,
                                                   contour=candidate, size=10)
            # Determine which end segment is closer to the target segment, and calculate compatibility
            # with the target of the closer of the end segment for each candidate
            prox0 = _calc_proximity(target_segment, candidate_end_objs[0])
            prox1 = _calc_proximity(target_segment, candidate_end_objs[1])
            if prox0 < prox1:
                compatibility_score = _calc_compatibility(target_obj=target_segment,
                                                          candidate_obj=candidate_end_objs[0])

            else:
                compatibility_score = _calc_compatibility(target_obj=target_segment,
                                                          candidate_obj=candidate_end_objs[1])

            # Append compatibility score to the list
            candidate_compatibility.append(compatibility_score)

        # Get the index of the most compatible (lowest score) end segment
        optimal_seg_i = np.where(candidate_compatibility == np.amin(candidate_compatibility))[0][0]

        # Join the target segment and most compatible segment
        optimal_candidate = candidate_segments[optimal_seg_i]
        combined_segment = np.append(cnt, optimal_candidate, 0)

        # Remove the segment that got combined from the list of candidates
        candidate_segments.remove(optimal_candidate)

        # Combine segments until the combined segment traverses from stem to leaf tip
        if optimal_candidate in leaf_objects:
            new_leaf_obj.append(combined_segment)
        else:
            while not optimal_candidate in leaf_objects:
                candidate_compatibility = []  # Initialize list of compatibility scores
                # Determine which end of the combined segment is NOT the axil end
                segment_end_objs = _get_segment_ends(img=segmented_img, contour=combined_segment, size=10)
                for j, end in enumerate(segment_end_objs):
                    segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
                    cv2.drawContours(segment_end_plot, end, -1, 255, params.line_thickness, lineType=8)
                    overlap_img = logical_and(segment_end_plot, stem_img)
                    if np.sum(overlap_img) == 0:
                        target_segment = end
                # Calculate compatibility scores for each candidate segment
                for j, candidate in enumerate(candidate_segments):
                    # Find which end of the candidate segment to compare to the target segment
                    candidate_end_objs = _get_segment_ends(img=segmented_img,
                                                           contour=candidate, size=10)
                    # Determine which end segment is closer to the target segment, and calculate compatibility
                    # with the target of the closer of the end segment for each candidate
                    prox0 = _calc_proximity(target_segment, candidate_end_objs[0])
                    prox1 = _calc_proximity(target_segment, candidate_end_objs[1])
                    if prox0 < prox1:
                        candidate_compatibility.append(_calc_compatibility(target_obj=target_segment,
                                                                           candidate_obj=candidate_end_objs[0]))
                    else:
                        candidate_compatibility.append(_calc_compatibility(target_obj=target_segment,
                                                                           candidate_obj=candidate_end_objs[1]))

                # Get the index of the most compatible (lowest score) end segment
                optimal_seg_i = np.where(candidate_compatibility == np.amin(candidate_compatibility))[0][0]

                # Join the target segment and most compatible segment
                optimal_candidate = candidate_segments[optimal_seg_i]
                combined_segment = np.append(combined_segment, optimal_candidate, 0)

                # Remove the segment that got combined from the list of candidates
                candidate_segments.remove(optimal_candidate)

            # Once a segment is complete (traverses from stem to leaf tip), add to new leaf objects list
            new_leaf_obj.append(combined_segment)

    # Create a plot reflecting new leaf objects to show how they got combined
    _, labeled_img = segment_id(skel_img=plotting_img, objects=new_leaf_obj, mask=None)

    # Reset debug mode
    params.debug = debug

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img,
                    os.path.join(params.debug_outdir, str(params.device) + '_auto_combined_segments.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, new_leaf_obj
