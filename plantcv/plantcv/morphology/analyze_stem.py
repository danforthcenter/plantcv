"""Analyze stem characteristics."""
import cv2
import numpy as np
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _scale_size


def _analyze_stem(morph, label=None):
    """
    Analyze stem characteristics by fitting a linear regression line to stem segments.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label : str, optional
        Label parameter, modifies the variable name of observations recorded.

    Returns
    -------
    labeled_img : numpy.ndarray
        Stem analysis debugging image.
    """
    stem_objects = morph.stem
    grouped_stem = np.vstack(stem_objects)

    # Find vertical height of the stem by measuring bounding box
    _, _, _, height = cv2.boundingRect(grouped_stem)

    # Calculate stem angle
    [vx, vy, _, _] = cv2.fitLine(grouped_stem, cv2.DIST_L2, 0, 0.01, 0.01)
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
