"""Analyze stem characteristics."""
import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _scale_size


def analyze_stem(rgb_img, stem_objects, label=None):
    """
    Analyze stem characteristics by fitting a linear regression line to stem segments.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image to plot debug image.
    stem_objects : list
        List of stem segments (output from segment_sort function).
    label : str, optional
        Label parameter, modifies the variable name of observations recorded.

    Returns
    -------
    labeled_img : numpy.ndarray
        Stem analysis debugging image.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    labeled_img = np.copy(rgb_img)
    img_x = np.shape(labeled_img)[0]
    grouped_stem = np.vstack(stem_objects)

    # Find vertical height of the stem by measuring bounding box
    stem_x, stem_y, _, height = cv2.boundingRect(grouped_stem)

    # Calculate stem angle
    [vx, vy, x, y] = cv2.fitLine(grouped_stem, cv2.DIST_L2, 0, 0.01, 0.01)
    slope = -vy / vx

    # Calculate stem path length
    stem_length = cv2.arcLength(grouped_stem, False) / 2

    outputs.add_observation(sample=label, variable='stem_height', trait='vertical length of stem segments',
                            method='plantcv.plantcv.morphology.analyze_stem', scale=params.unit, datatype=float,
                            value=_scale_size(height), label=params.unit)
    outputs.add_observation(sample=label, variable='stem_angle', trait='angle of combined stem object',
                            method='plantcv.plantcv.morphology.analyze_stem', scale='degrees', datatype=float,
                            value=float(slope.item()), label='degrees')
    outputs.add_observation(sample=label, variable='stem_length', trait='path length of combined stem object',
                            method='plantcv.plantcv.morphology.analyze_stem', scale=params.unit, datatype=float,
                            value=_scale_size(stem_length), label=params.unit)

    # Draw culm_height
    cv2.line(labeled_img, (int(stem_x), stem_y), (int(stem_x), stem_y + height), (0, 255, 0), params.line_thickness)
    # Draw combined stem angle
    x_min = 0  # Set bounds for regression lines to get drawn
    x_max = img_x
    intercept1 = int(np.array(((x - x_min) * slope) + y).item())
    intercept2 = int(np.array(((x - x_max) * slope) + y).item())
    if abs(slope) > 1000000:
        print("Slope  is ", slope, " and cannot be plotted.")
    else:
        cv2.line(labeled_img, (x_max - 1, intercept2), (x_min, intercept1), (0, 0, 255), 1)
    _debug(visual=labeled_img, filename=os.path.join(params.debug_outdir, f"{params.device}_stem_analze.png"))

    return labeled_img
