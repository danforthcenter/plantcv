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
from plantcv.plantcv.morphology import segment_angle
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

    return int(euclidean((target_x, target_y), (candidate_x, candidate_y)))


def _calc_angle(object):
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
    slope = -vy / vx
    # Convert from line slope to degrees
    angle = np.arctan(slope[0]) * 180 / np.pi

    return angle



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


    branching_segment = []  # Segments that branch off from the stem
    secondary_segment = []  # Any pseudo-stem segments that aren't branching segments
    end_segment_angles = []
    new_leaf_obj = []

    plotting_img = np.zeros(segmented_img.shape[:2], np.uint8)
    candidate_segments = np.copy(leaf_objects)
    candidate_segments.append(pseudo_stem_obj)

    # Plot true stem values to help with identifying the axil part of the segment
    cv2.drawContours(plotting_img, true_stem_obj, -1, 255, params.line_thickness, lineType=8)
    # Dilate stem
    stem_img = dilate(gray_img=plotting_img, ksize=4, i=1)

    # Loop through segment contours
    for i, cnt in enumerate(pseudo_stem_obj):
        segment_end_objs = _get_segment_ends(img=segmented_img, contour=cnt, size=10)

        # If one of the segment ends overlaps with the stem then it's a branching segment
        segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(segment_end_plot, segment_end_objs, -1, 255, params.line_thickness, lineType=8)
        overlap_img = logical_and(segment_end_plot, stem_img)
        if np.sum(overlap_img) == 0:
            branching_segment.append(cnt)
        else:
            secondary_segment.append(cnt)

    # For each of the pseudo-stem segments, find the most compatible segment for combining
    for i, cnt in enumerate(branching_segment):
        target_segment = cnt
        candidate_compatibility = []
        for j, candidate in enumerate(candidate_segments):


#    For each pseudo-stem:
#    Determine if the pseudo-stem segment is a branching segment (one that branches off of the stem) or a secondary
#    segment (one between a leaf object and another pseudo-stem object, or even the case where it’s between two pseudo-stem objects)
#    For the branching P-S segments, prune off the ends and determine which end is NOT connect to the stem.
#    Find the slope of this end segment (outer segment) and this is what will be used to help find the corresponding segment
#    Identify potential corresponding segments (Find leaf segments or other pseudo-stem segments that share an outer branch point )
#    For each potential segment (there will likely be two if I can determine the correct branch point) find the optimal
#    pairing by using “tangent” slope of the parts of the segment that coincide with the branch point of interest.
#    (Will look something similar to the algorithm for insertion angle since I’m able to determine the correct side of
#    the leaf segment in that function)
#    Once I have the ID of the pseudo stem and the optimal pairing, combine segments.


# Matching candidate segments to pseudo-stem end segment of interest can come from a compatibility score that is calculated from
# proximity and slope.

