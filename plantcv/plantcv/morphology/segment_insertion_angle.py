"""Find leaf insertion angles with stem."""
import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import dilate
from plantcv.plantcv import closing
from plantcv.plantcv import outputs
from plantcv.plantcv import logical_and
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology.segment_tangent_angle import _slope_to_intesect_angle
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _find_tips, _iterative_prune 


def segment_insertion_angle(skel_img, segmented_img, leaf_objects, stem_objects, size, label=None):
    """Find leaf insertion angles in degrees of skeleton segments.
    Fit a linear regression line to the stem. Use `size` pixels on  the portion of leaf next to the stem find a linear
    regression line, and calculate angle between the two lines per leaf object.

    Inputs:
    skel_img         = Skeletonized image
    segmented_img    = Segmented image to plot slope lines and intersection angles on
    leaf_objects     = List of leaf segments
    stem_objects     = List of stem segments
    size             = Size of inner leaf used to calculate slope lines
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

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
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    # Store debug
    debug = params.debug
    params.debug = None
    
    # Find and sort segment ends, and create debug image
    inner_segments, _, _, pruned_away = _inner_segments(
        skel_img=skel_img, leaf_objects=leaf_objects, size=size)

    cols = segmented_img.shape[1]
    labeled_img = segmented_img.copy()
    segment_slopes = []
    intersection_angles = []

    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(inner_segments), saved=True)

    for i in range(len(leaf_objects)):
        cv2.drawContours(labeled_img, leaf_objects, i, rand_color[i], params.line_thickness, lineType=8)

    combined_stem = _combine_stem_segments(segmented_img, stem_objects, debug)

    # Find slope of the stem
    [vx, vy, x, y] = cv2.fitLine(combined_stem[0], cv2.DIST_L2, 0, 0.01, 0.01)
    stem_slope = -vy / vx
    stem_slope = stem_slope[0]
    lefty = int(np.array((-x * vy / vx) + y).item())
    righty = int(np.array(((cols - x) * vy / vx) + y).item())
    cv2.line(labeled_img, (cols - 1, righty), (0, lefty), (150, 150, 150), 3)

    i = 0
    for t, segment in enumerate(leaf_objects):
        if not pruned_away[t]:
            # Find line fit to each segment
            [vx, vy, x, y] = cv2.fitLine(inner_segments[i], cv2.DIST_L2, 0, 0.01, 0.01)
            # Increment the index up after plotting a valid segment
            i += 1
            slope = -vy / vx
            left_list = int(np.array((-x * vy / vx) + y).item())
            right_list = int(np.array(((cols - x) * vy / vx) + y).item())
            segment_slopes.append(slope[0])

            # Draw slope lines if possible
            if slope > 1000000 or slope < -1000000:
                print("Slope of contour with ID#", t, "is", slope, "and cannot be plotted.")
            else:
                cv2.line(labeled_img, (cols - 1, right_list), (0, left_list), rand_color[t], 1)

            # Store intersection angles between insertion segment and stem line
            intersection_angle = _slope_to_intesect_angle(slope[0], stem_slope)
            # CV2 measures clockwise, we want the acute angle between stem and inner leaf
            if intersection_angle > 90:
                intersection_angle = 180 - intersection_angle
            intersection_angles.append(intersection_angle)
            # Draw the angle on the debug img
            w = segment[0][0][0]
            h = segment[0][0][1]
            text = f"{intersection_angle:0,.2f}"
            cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        else:
            # If a segment is pruned away then add 'NA' to observations
            intersection_angles.append('NA')
    # Save observations to Outputs class
    outputs.add_observation(sample=label, variable='segment_insertion_angle', trait='segment insertion angle',
                            method='plantcv.plantcv.morphology.segment_insertion_angle', scale='degrees', datatype=list,
                            value=intersection_angles, label=list(range(len(intersection_angles))))

    # Reset debug mode
    params.debug = debug

    _debug(visual=labeled_img,
           filename=os.path.join(params.debug_outdir, f"{params.device}_segment_insertion_angles.png"))

    return labeled_img


def _combine_stem_segments(segmented_img, stem_objects, debug):
    """
    Groups stem objects into a single object.

    Inputs:
    segmented_img  = Contour tuple
    stem_objects   = Contours belonging to the stem

    Returns:
    combined_stem  = grouped contours list

    :param segmented_img: numpy.ndarray
    :param stem_objects: list
    :return combined_stem: numpy.ndarray
    """
    # Plot stem segments
    stem_img = np.zeros(segmented_img.shape[:2], np.uint8)
    cv2.drawContours(stem_img, stem_objects, -1, 255, 2, lineType=8)
    stem_img = closing(stem_img)
    combined_stem, _ = _cv2_findcontours(bin_img=stem_img)
    # Make sure stem objects are a single contour
    loop_count = 0
    while len(combined_stem) > 1 and loop_count < 50:
        loop_count += 1
        stem_img = dilate(stem_img, 2, 1)
        stem_img = closing(stem_img)
        combined_stem, _ = _cv2_findcontours(bin_img=stem_img)
    if len(combined_stem) > 1:
        # Reset debug mode
        params.debug = debug
        fatal_error('Unable to combine stem objects.')
    else:
        return combined_stem
   
def _inner_segments(skel_img, leaf_objects, size):
    """
    Groups stem objects into a single object.

    Inputs:
    skel_img  = Skeletonized image
    leaf_objects   = Contours belonging to leaves most likely
    size = size of segments to collect

    Returns:
    inner_segments  = inner segments from each leaf
    label_coord_x = x coordinate labels for debug image creation
    label_coord_x = y coordinate labels for debug image creation
    pruned_away = list of boolean statements, equal length to the leaf_objects list input

    :param segmented_img: numpy.ndarray
    :param stem_objects: list
    :return inner_segments: list
    :return label_coord_x: list
    :return label_coord_y: list
    :return pruned_away: list
    """   
    # Create a list of tip tuples to use for sorting
    tips, _, _ = _find_tips(skel_img)
    pruned_away = []
    inner_segments = []
    label_coord_x = []
    label_coord_y = []

    for i, _ in enumerate(leaf_objects):
        # Draw leaf objects
        find_segment_tangents = np.zeros(skel_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)

        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, size)

        # Segment ends are the portions pruned off
        segment_ends = find_segment_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=segment_ends)

        if not len(segment_end_obj) == 2:
            print("Size too large, contour with ID#", i, "got pruned away completely.")
            pruned_away.append(True)
        else:
            # The contour can have insertion angle calculated
            pruned_away.append(False)

            # Determine if a segment is leaf end or leaf insertion segment
            for j, obj in enumerate(segment_end_obj):

                segment_plot = np.zeros(skel_img.shape[:2], np.uint8)
                cv2.drawContours(segment_plot, obj, -1, 255, 1, lineType=8)
                segment_plot = dilate(segment_plot, 3, 1)
                overlap_img = logical_and(segment_plot, tips)

                # If none of the tips are within a segment_end then it's an insertion segment
                if np.sum(overlap_img) == 0:
                    inner_segments.append(segment_end_obj[j])

            # Store coordinates for labels
            label_coord_x.append(leaf_objects[i][0][0][0])
            label_coord_y.append(leaf_objects[i][0][0][1])
    return inner_segments, label_coord_x, label_coord_y, pruned_away