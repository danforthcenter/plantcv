# Find tangent angles in degrees of skeleton segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology import prune

def _slope_to_intesect_angle(m1, m2):
    """ Calculate intersections angle (in degrees) from the slope of two lines

        Inputs:
        m1    = Slope of line 1
        m2    = Slope of line 2

        Returns:
        angle = Intersection angle (in degrees)

        :param m1: float
        :param m2: float
        :return angle: float
            """
    angle = (np.pi - np.absolute(np.arctan(m1) - np.arctan(m2))) * 180 / np.pi
    return angle


def segment_tangent_angle(skel_img, objects, hierarchies, size, mask=None):
    """ Find 'tangent' angles in degrees of skeleton segments. Use `size` pixels on either end of
        each segment to find a linear regression line, and calculate angle between the two lines
        drawn per segment.

        Inputs:
        skel_img  = Skeletonized image
        objects   = List of contours
        hierarchy = Contour hierarchy NumPy array
        size      = Size of ends used to calculate "tangent" lines
        mask      = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.


        Returns:
        intersection_angles = List of leaf lengths

        :param segmented_img: numpy.ndarray
        :param objects: list
        :param hierarchies: numpy.ndarray
        :param size: int
        :param mask: numpy.ndarray
        :return intersection_angles: list
        """
    # Store debug
    debug = params.debug
    params.debug = None

    intersection_angles = []
    rows, cols = skel_img.shape[:2]
    rand_color = color_palette(len(objects))

    # Plot debugging image on mask if provided.
    if mask is None:
        dilated_skel = dilate(skel_img, 2, 1)
        labeled_img = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)
    else:
        mask_copy = mask.copy()
        labeled_img = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
        skel_obj, skel_hier = find_objects(skel_img, skel_img)
        cv2.drawContours(labeled_img, skel_obj, -1, (150, 150, 150), 2, lineType=8, hierarchy=skel_hier)

    for i, cnt in enumerate(objects):
        find_tangents = np.zeros(skel_img.shape[:2], np.uint8)
        cv2.drawContours(find_tangents, objects, i, 255, 1, lineType=8, hierarchy=hierarchies)
        pruned_segment = prune(find_tangents, size)

        # Remove center of segments and leave both ends
        segment_ends = find_tangents-pruned_segment
        segment_end_objs, segment_end_hierarchy = find_objects(segment_ends, segment_ends)
        slopes = []

        for j, obj in enumerate(segment_end_objs):
            # Find slope of each tip
            [vx, vy, x, y] = cv2.fitLine(obj, cv2.DIST_L2, 0, 0.01, 0.01)
            slope = -vy / vx
            left_list = int((x * slope) + y)
            right_list = int(((x - cols) * slope) + y)
            slopes.append(slope)

            # Check to avoid Overflow error while trying to plot lines with slopes too large
            if slope > 1000000 or slope < -1000000:
                print("Warning: Slope of line tangent with contour with ID #", i, "is", slope, "and cannot be plotted.")
            else:
                # Draw slope lines
                cv2.line(labeled_img, (cols - 1, right_list), (0, left_list), rand_color[i], 1)

        if len(slopes) < 2:
            # If size*2>len(obj) then pruning will remove the segment completely, and
            # makes segment_end_objs contain just one contour.
            print("Warning: Size too large, contour with ID #", i, "got pruned away completely.")
        else:
            slope1 = slopes[0]
            slope2 = slopes[1]
            intersection_angles.append(_slope_to_intesect_angle(slope1, slope2))

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_tangent_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return intersection_angles
