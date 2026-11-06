"""Find euclidean lengths of skeleton segments."""
import cv2
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._helpers import _cv2_findcontours, _find_tips, _scale_size
from scipy.spatial.distance import euclidean


def _segment_euclidean_length(morph, label=None):
    """Use segmented skeleton image to gather euclidean length measurements per segment.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).
    """
    segmented_img = morph.skeleton
    objects = morph.leaves

    x_list = []
    y_list = []
    segment_lengths = []

    for i, obj in enumerate(objects):
        # Store coordinates for labels
        x_list.append(obj[0][0][0])
        y_list.append(obj[0][0][1])

        # Draw segments one by one to group segment tips together
        finding_tips_img = np.zeros(segmented_img.shape[:2], np.uint8)
        cv2.drawContours(finding_tips_img, objects, i, (255, 255, 255), 1, lineType=8)
        segment_tips, _, _ = _find_tips(finding_tips_img)
        tip_objects, _ = _cv2_findcontours(bin_img=segment_tips)
        points = []
        if not len(tip_objects) == 2:
            fatal_error("Too many tips found per segment, try pruning again")
        for t in tip_objects:
            # Gather pairs of coordinates
            x, y = t.ravel()
            coord = (x, y)
            points.append(coord)

        # Calculate euclidean distance between tips of each contour
        segment_lengths.append(float(euclidean(points[0], points[1])))

    segment_ids = list(range(len(segment_lengths)))

    outputs.add_observation(sample=label, variable='segment_eu_length', trait='segment euclidean length',
                            method='plantcv.plantcv.analyze.morphology', scale=params.unit, datatype=list,
                            value=_scale_size(segment_lengths), label=segment_ids)
