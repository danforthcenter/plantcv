"""Find tangent angles in degrees of skeleton segments."""
import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import color_palette
from plantcv.plantcv.morphology import _iterative_prune
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours


def _slope_to_intesect_angle(m1, m2):
    """Calculate intersections angle (in degrees) from the slope of two lines

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


def segment_tangent_angle(segmented_img, objects, size, label=None):
    """Find 'tangent' angles in degrees of skeleton segments.
    Use `size` pixels on either end of each segment to find a linear regression line, and calculate angle between the two
    lines drawn per segment.

    Inputs:
    segmented_img  = Segmented image to plot slope lines and intersection angles on
    objects        = List of contours
    size           = Size of ends used to calculate "tangent" lines
    label          = Optional label parameter, modifies the variable name of
                     observations recorded (default = pcv.params.sample_label).

    Returns:
    labeled_img    = Segmented debugging image with angles labeled

    :param segmented_img: numpy.ndarray
    :param objects: list
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

    labeled_img = segmented_img.copy()
    intersection_angles = []
    label_coord_x = []
    label_coord_y = []

    # Create a color scale, use a previously stored scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    for i, cnt in enumerate(objects):
        find_tangents = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(find_tangents, objects, i, 255, 1, lineType=8)
        cv2.drawContours(labeled_img, objects, i, rand_color[i], params.line_thickness, lineType=8)
        pruned_segment = _iterative_prune(find_tangents, size)
        segment_ends = find_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=segment_ends)
        slopes = []
        for obj in segment_end_obj:
            # Find bounds for regression lines to get drawn
            rect = cv2.minAreaRect(cnt)
            pts = cv2.boxPoints(rect)
            df = pd.DataFrame(pts, columns=('x', 'y'))
            x_max = int(df['x'].max())
            x_min = int(df['x'].min())

            # Find line fit to each segment
            vx, vy, x, y = cv2.fitLine(obj, cv2.DIST_L2, 0, 0.01, 0.01)
            slope = -vy / vx
            left_list = int(np.array(((x - x_min) * slope) + y).item())
            right_list = int(np.array(((x - x_max) * slope) + y).item())
            slopes.append(slope)

            if slope > 1000000 or slope < -1000000:
                print("Slope of contour with ID#", i, "is", slope, "and cannot be plotted.")
            else:
                # Draw slope lines
                cv2.line(labeled_img, (x_max - 1, right_list), (x_min, left_list), rand_color[i], 1)

        if len(slopes) < 2:
            # If size*2>len(obj) then pruning will remove the segment completely, and
            # makes segment_end_objs contain just one contour.
            print("Size too large, contour with ID#", i, "got pruned away completely.")
            intersection_angles.append("NA")
        else:
            # Calculate intersection angles
            slope1 = slopes[0][0]
            slope2 = slopes[1][0]
            intersection_angle = _slope_to_intesect_angle(slope1, slope2)
            intersection_angles.append(intersection_angle)

        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

    segment_ids = []
    # Reset debug mode
    params.debug = debug

    for i, cnt in enumerate(objects):
        # Label slope lines
        w = label_coord_x[i]
        h = label_coord_y[i]
        if type(intersection_angles[i]) is str:
            text = f"{intersection_angles[i]}"
        else:
            text = f"{intersection_angles[i]:0,.2f}"
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        segment_ids.append(i)

    outputs.add_observation(sample=label, variable='segment_tangent_angle', trait='segment tangent angle',
                            method='plantcv.plantcv.morphology.segment_tangent_angle', scale='degrees', datatype=list,
                            value=intersection_angles, label=segment_ids)

    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_segment_tangent_angles.png"))

    return labeled_img
