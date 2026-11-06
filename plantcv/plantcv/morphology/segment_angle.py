"""Find angles in degrees of skeleton segments."""
import cv2
import numpy as np
from plantcv.plantcv._globals import outputs


def _segment_angle(morph, label=None):
    """
    Calculate the angle of skeleton segments in degrees by fitting a linear regression line.

    Parameters
    ----------
    morph = plantcv.plantcv.morphology.morph object,
        Morphology object to analyze
    label : str, optional
        Label for the observation variable. If None, uses `params.sample_label`.

    Returns
    -------
    labeled_img : numpy.ndarray
        Segmented image with slope lines and angles labeled.
    """
    objects = morph.leaves

    label_coord_x = []
    label_coord_y = []
    segment_angles = []

    for i, cnt in enumerate(objects):
        # Find bounds for regression lines to get drawn
        rect = cv2.minAreaRect(cnt)
        pts = cv2.boxPoints(rect)

        # Find line fit to each segment
        [vx, vy, _, _] = cv2.fitLine(objects[i], cv2.DIST_L2, 0, 0.01, 0.01)
        slope = -vy / vx

        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

        # Calculate degrees from slopes
        angle_value = (np.arctan(slope[0]) * 180 / np.pi).astype(np.float64)
        segment_angles.append(angle_value)

    segment_ids = list(range(len(objects)))

    outputs.add_observation(sample=label, variable='segment_angle', trait='segment angle',
                            method='plantcv.plantcv.analyze.morphology', scale='degrees',
                            datatype=list, value=segment_angles, label=segment_ids)
