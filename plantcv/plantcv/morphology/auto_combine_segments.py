import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import logical_and
from plantcv.plantcv import find_objects
from plantcv.plantcv.morphology import segment_angle
from plantcv.plantcv.morphology import _iterative_prune


def _get_segment_ends(img, contour, size):
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


def auto_combine_segments(segmented_img, leaf_objects, true_stem_obj, pseudo_stem_obj):
    # automatically combine pseudo-stems to pieces of leaf or other pseudo-stem
    # based on the location of the important branch point, and the slope of the
    # segment near the branch point

    branching_segment = []  # Segments that branch off from the stem
    secondary_segment = []  # Any pseudo-stem segments that aren't branching segments
    end_segment_angles = []
    plotting_img = np.zeros(segmented_img.shape[:2], np.uint8)

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

    for i, cnt in enumerate(branching_segment):
        outer_segment = False
        segment_end_objs = _get_segment_ends(img=segmented_img, contour=cnt, size=10)
        for j, end in enumerate(segment_end_objs):
            segment_end_plot = np.zeros(segmented_img.shape[:2], np.uint8)
            cv2.drawContours(segment_end_plot, end, -1, 255, params.line_thickness, lineType=8)
            overlap_img = logical_and(segment_end_plot, stem_img)
            if np.sum(overlap_img) == 0:
                outer_segment = True
                [vx, vy, x, y] = cv2.fitLine(end, cv2.DIST_L2, 0, 0.01, 0.01)
                slope = -vy / vx
                segment_end_angle = np.arctan(slope[0]) * 180 / np.pi



#    For each pseudo-stem:
#    Determine if the pseudo-stem segment is a branching segment (one that branches off of the stem) or a secondary
#    segment (one between a leaf object and another pseudo-stem object, or even the case where it’s between two pseudo-stem objects)
#    For the branching P-S segments, prune off the ends and determine which end is NOT connect to the stem.
#   Find the slope of this end segment (outer segment) and this is what will be used to help find the corresponding segment
# Identify potential corresponding segments (Find leaf segments or other pseudo-stem segments that share an outer branch point )
# For each potential segment (there will likely be two if I can determine the correct branch point) find the optimal
# pairing by using “tangent” slope of the parts of the segment that coincide with the branch point of interest.
# (Will look something similar to the algorithm for insertion angle since I’m able to determine the correct side of the leaf segment in that function)
# Once I have the ID of the pseudo stem and the optimal pairing, combine segments.

