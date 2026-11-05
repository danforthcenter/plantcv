"""Find tangent angles in degrees of skeleton segments."""
import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv._helpers import _cv2_findcontours, _iterative_prune


def _slope_to_intersect_angle(m1, m2):
    """
    Calculate the intersection angle (in degrees) between two lines given their slopes.

    Parameters
    ----------
    m1 : float
        Slope of the first line.
    m2 : float
        Slope of the second line.

    Returns
    -------
    angle : float
        Intersection angle between the two lines, in degrees.
    """
    angle = ((np.pi - np.absolute(np.arctan(m1) - np.arctan(m2))) * 180 / np.pi).astype(np.float64)
    return angle


def _segment_tangent_angle(morph, size=20, label=None):
    """
    Find 'tangent' angles in degrees of skeleton segments.

    Uses `size` pixels on either end of each segment to find a linear regression line, and calculates the
    angle between the two lines drawn per segment.

    Parameters
    ----------
    morph : plantcv.plantcv.morphology.morph,
        morphology object to analyze
    size : int
        Size of ends used to calculate "tangent" lines.
    label : str, optional
        Label parameter, modifies the variable name of observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    labeled_img : numpy.ndarray
        Segmented debugging image with angles labeled.
    """
    segmented_img = morph.skeleton
    objects = morph.leaves

    intersection_angles = []

    for i, cnt in enumerate(objects):
        find_tangents = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(find_tangents, objects, i, 255, 1, lineType=8)
        pruned_segment = _iterative_prune(find_tangents, size)
        segment_ends = find_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=segment_ends)
        slopes = []
        for obj in segment_end_obj:
            # Find line fit to each segment
            vx, vy, _, _ = cv2.fitLine(obj, cv2.DIST_L2, 0, 0.01, 0.01)
            slope = -vy / vx
            slopes.append(slope)

        if len(slopes) < 2:
            # If size*2>len(obj) then pruning will remove the segment completely, and
            # makes segment_end_objs contain just one contour.
            print("Size too large, contour with ID#", i, "got pruned away completely.")
            intersection_angles.append("NA")
        else:
            # Calculate intersection angles
            slope1 = slopes[0][0]
            slope2 = slopes[1][0]
            intersection_angle = _slope_to_intersect_angle(slope1, slope2)
            intersection_angles.append(intersection_angle)

    segment_ids = [i for i in range(len(objects))]

    outputs.add_observation(sample=label, variable='segment_tangent_angle', trait='segment tangent angle',
                            method='plantcv.plantcv.analyze.morphology', scale='degrees', datatype=list,
                            value=intersection_angles, label=segment_ids)
