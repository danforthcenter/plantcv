# Identify stem segments that are likely to be pieces of leaf

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv.morphology import segment_angle
from plantcv.plantcv.morphology import segment_curvature


def id_pseudo_stem(segmented_img, stem_objects, threshold):
    """
        The identification of pseudo-stem segments (segments that are identified as primary objects by the
        plantcv.morphology.segment_sort algorithm, but truly belong to a leaf but get classified as stem
        due to leaves obscuring each other or leaves that have sharp angles that get picked up as branch points).
        The algorithm for identifying pseudo-stem segments assumes that true pieces of stem should be close to
        vertical in angle, should be closely stacked (relatively low x-value spread), and have low measures of
        curvature.

        Inputs:
        segmented_img = Segmented debugging image
        stem_objects  = List of stem segments
        threshold     = Threshold of penalty values to classify stem objects as pseudo-stem objects

        Returns:
        labeled_img     = Segmented debugging image

        :param segmented_img: numpy.ndarray
        :param stem_objects: list
        :param threshold: int
        :return labeled_img: numpy.ndarray

        """

    labeled_img = np.copy(segmented_img)
    if len(np.shape(labeled_img)) == 2:
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_GRAY2RGB)

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Initialize lists
    segment_rank = np.zeros(len(stem_objects))
    segment_angle_penalty = np.zeros(len(stem_objects))
    x_val_penalty = np.zeros(len(stem_objects))
    true_stem = []
    pseudo_stem = []

    # Calculate average angle of segments
    _ = segment_angle(segmented_img=segmented_img, objects=stem_objects)
    segment_angle_vals = outputs.observations['segment_angle']['value']
    # Segments close to vertical will have angles close to 90 or -90
    segment_angle_penalty = (90 * np.ones(len(segment_angle_vals))) - np.absolute(segment_angle_vals)
    # Find the segment with the steepest slope
    most_vertical_i = np.where(segment_angle_penalty == np.amin(segment_angle_penalty))[0][0]
    # Find range of x-values
    x, y, w, h = cv2.boundingRect(stem_objects[most_vertical_i])
    x_range = list(range(x - w, x + (2 * w)))

    # Calculate x-value penalty for each segment depending on x-val location compared to the most vertical segment
    for i, cnt in enumerate(stem_objects):
        if not i == most_vertical_i:
            # Find range of x-values
            x, y, w, h = cv2.boundingRect(cnt)
            x_vals = list(range(x, x + w))
            if not x_vals in x_range:
                x_offset = abs(x_range[0] - x_vals[-1])
                x_val_penalty[i] =+ x_offset

    # Calculate curvature of each segment
    _ = segment_curvature(segmented_img=segmented_img, objects=stem_objects)
    segment_curvature_vals = outputs.observations['segment_curvature']['value']
    # Curvature value = 1.0 is perfectly straight, larger is more curved.
    segment_curve_penalty = abs(segment_curvature_vals - np.ones(len(segment_curvature_vals))) * 200

    # Combine penalty values into a total penalty value for each segment
    segment_penalty = segment_curve_penalty + x_val_penalty + segment_angle_penalty

    # Draw debugging image and append to list of segment types
    for i, cnt in enumerate(stem_objects):
        # Draw true stem segments as fuschia
        if segment_penalty[i] < threshold:
            cv2.drawContours(labeled_img, stem_objects, i, (255, 0, 255), params.line_thickness, lineType=8)
            true_stem.append(stem_objects[i])
        # Draw pseudo-stem segments are yellow
        else:
            cv2.drawContours(labeled_img, stem_objects, i, (0, 255, 255), params.line_thickness, lineType=8)
            pseudo_stem.append(stem_objects[i])

    # Reset debug mode
    params.debug = debug
    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_pseudo_stem.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, true_stem, pseudo_stem
