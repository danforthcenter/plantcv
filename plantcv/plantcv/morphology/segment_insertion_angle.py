# Find leaf insertion angles with stem

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import closing
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import logical_and
from plantcv.plantcv import fatal_error
from plantcv.plantcv import print_image
from plantcv.plantcv import find_objects
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology import _iterative_prune
from plantcv.plantcv.morphology import find_tips
from plantcv.plantcv.morphology import find_branch_pts
from plantcv.plantcv.morphology.segment_tangent_angle import _slope_to_intesect_angle


def segment_insertion_angle(skel_img, segmented_img, leaf_objects, stem_objects, size, label="default"):
    """ Find leaf insertion angles in degrees of skeleton segments. Fit a linear regression line to the stem.
        Use `size` pixels on  the portion of leaf next to the stem find a linear regression line,
        and calculate angle between the two lines per leaf object.
        Inputs:
        skel_img         = Skeletonized image
        segmented_img    = Segmented image to plot slope lines and intersection angles on
        leaf_objects     = List of leaf segments
        stem_objects     = List of stem segments
        size             = Size of inner leaf used to calculate slope lines
        label        = optional label parameter, modifies the variable name of observations recorded

        Returns:
        labeled_img      = Debugging image with angles labeled

        :param skel_img: numpy.ndarray
        :param segmented_img: numpy.ndarray
        :param leaf_objects: list
        :param stem_objects: list
        :param size: int
        :param label: str
        :return labeled_img: numpy.ndarray
        """

    # Store debug
    debug = params.debug
    params.debug = None

    rows, cols = segmented_img.shape[:2]
    labeled_img = segmented_img.copy()
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
    tips = find_tips(skel_img)
    tips = dilate(tips, 3, 1)
    tip_objects, tip_hierarchies = find_objects(tips, tips)
    tip_tuples = []
    for i, cnt in enumerate(tip_objects):
        tip_tuples.append((cnt[0][0][0], cnt[0][0][1]))

    # rand_color = color_palette(len(leaf_objects))

    for i, cnt in enumerate(leaf_objects):
        # Draw leaf objects
        find_segment_tangents = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)

        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, size)

        # Segment ends are the portions pruned off
        segment_ends = find_segment_tangents - pruned_segment
        segment_end_obj, segment_end_hierarchy = find_objects(segment_ends, segment_ends)
        # is_insertion_segment = []

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
                segment_plot = dilate(segment_plot, 3, 1)
                # tips = dilate(tips, 3, 1)
                overlap_img = logical_and(segment_plot, tips)

                # If none of the tips are within a segment_end then it's an insertion segment
                if np.sum(overlap_img) == 0:
                    insertion_segments.append(segment_end_obj[j])
                    insertion_hierarchies.append(segment_end_hierarchy[0][j])

            # Store coordinates for labels
            label_coord_x.append(leaf_objects[i][0][0][0])
            label_coord_y.append(leaf_objects[i][0][0][1])

    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(valid_segment), saved=True)

    for i, cnt in enumerate(valid_segment):
        cv2.drawContours(labeled_img, valid_segment, i, rand_color[i], params.line_thickness, lineType=8)

    # Plot stem segments
    stem_img = np.zeros(segmented_img.shape[:2], np.uint8)
    cv2.drawContours(stem_img, stem_objects, -1, 255, 2, lineType=8)
    branch_pts = find_branch_pts(skel_img)
    # stem_img = stem_img + branch_pts ## there can be branch points not along the stem, and they're not needed
    stem_img = closing(stem_img)
    combined_stem, combined_stem_hier = find_objects(stem_img, stem_img)

    # Make sure stem objects are a single contour
    loop_count = 0
    while len(combined_stem) > 1 and loop_count < 50:
        loop_count += 1
        stem_img = dilate(stem_img, 2, 1)
        stem_img = closing(stem_img)
        combined_stem, combined_stem_hier = find_objects(stem_img, stem_img)
    if len(combined_stem) > 1:
        # Reset debug mode
        params.debug = debug
        fatal_error('Unable to combine stem objects.')

    # Find slope of the stem
    [vx, vy, x, y] = cv2.fitLine(combined_stem[0], cv2.DIST_L2, 0, 0.01, 0.01)
    stem_slope = -vy / vx
    stem_slope = stem_slope[0]
    lefty = int((-x * vy / vx) + y)
    righty = int(((cols - x) * vy / vx) + y)
    cv2.line(labeled_img, (cols - 1, righty), (0, lefty), (150, 150, 150), 3)

    for t, segment in enumerate(insertion_segments):
        # Find line fit to each segment
        [vx, vy, x, y] = cv2.fitLine(segment, cv2.DIST_L2, 0, 0.01, 0.01)
        slope = -vy / vx
        left_list = int((-x * vy / vx) + y)
        right_list = int(((cols - x) * vy / vx) + y)
        segment_slopes.append(slope[0])

        # Draw slope lines if possible
        if slope > 1000000 or slope < -1000000:
            print("Slope of contour with ID#", t, "is", slope, "and cannot be plotted.")
        else:
            cv2.line(labeled_img, (cols - 1, right_list), (0, left_list), rand_color[t], 1)

        # Store intersection angles between insertion segment and stem line
        intersection_angle = _slope_to_intesect_angle(slope[0], stem_slope)
        # Function measures clockwise but we want the acute angle between stem and leaf insertion
        if intersection_angle > 90:
            intersection_angle = 180 - intersection_angle
        intersection_angles.append(intersection_angle)

    # Compile list of measurements where there is a 'NA' where pruned away segments would go.
    intersection_angles_editing = intersection_angles.copy()
    for j in pruned_away:
        if j:
            all_intersection_angles.append('NA')
        else:
            all_intersection_angles.append(intersection_angles_editing[0])
            intersection_angles_editing.remove(intersection_angles_editing[0])

    segment_ids = []

    for i, cnt in enumerate(insertion_segments):
        # Label slope lines
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = "{:.2f}".format(intersection_angles[i])
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        # segment_label = "ID" + str(i)
        segment_ids.append(i)

    outputs.add_observation(sample=label, variable='segment_insertion_angle', trait='segment insertion angle',
                            method='plantcv.plantcv.morphology.segment_insertion_angle', scale='degrees', datatype=list,
                            value=all_intersection_angles, label=segment_ids)

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img,
                    os.path.join(params.debug_outdir, str(params.device) + '_segment_insertion_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
