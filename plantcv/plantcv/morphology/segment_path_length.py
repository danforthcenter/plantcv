"""Find geodesic lengths of skeleton segments."""
import os
import cv2
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _scale_size


def _segment_path_length(morph, label=None):
    """Use segments to calculate geodesic distance per segment.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label = str,
        Optional label parameter, modifies the variable name of
        observations recorded (default = pcv.params.sample_label).
    """
    objects = morph.leaves

    label_coord_x = []
    label_coord_y = []
    segment_lengths = []

    for obj in objects:
        # Calculate geodesic distance, divide by two since cv2 seems to be taking the perimeter of the contour
        segment_lengths.append(float(cv2.arcLength(obj, False) / 2))
        # Store coordinates for labels
        label_coord_x.append(obj[0][0][0])
        label_coord_y.append(obj[0][0][1])

    segment_ids = [i for i in range(len(segment_lengths))]

    outputs.add_observation(sample=label, variable='segment_path_length', trait='segment path length',
                            method='plantcv.plantcv.analysis.morphology', scale=params.unit,
                            datatype=list, value=_scale_size(segment_lengths), label=segment_ids)
