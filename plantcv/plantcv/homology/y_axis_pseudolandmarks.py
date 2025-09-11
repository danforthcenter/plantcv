"""Function to scan for pseudolandmarks along the y-axis."""
import cv2
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition
from plantcv.plantcv.homology.x_axis_pseudolandmark import _small_img_pseudolandmarks, _pseudolandmarks
from plantcv.plantcv import params, outputs


def y_axis_pseudolandmarks(img, mask, label=None):
    """
    Divide up object contour into 19 equidistant segments and generate landmarks for each

    Inputs:
    img      = This is a copy of the original plant image generated using np.copy if debug is true it will be drawn on
    mask     = this is a binary image. The object should be white and the background should be black
    label    = Optional label parameter, modifies the variable name of
               observations recorded (default = pcv.params.sample_label).

    Returns:
    left      = List of landmarks within the left side
    right     = List of landmarks within the right side
    center_h  = List of landmarks within the center

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    :return left: list
    :return right: list
    :return center_h: list
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # Find contours
    cnt, cnt_str = _cv2_findcontours(bin_img=mask)
    # Consolidate contours
    obj = _object_composition(contours=cnt, hierarchy=cnt_str)
    # Empty pot type scenario
    if not np.any(obj):
        return ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA')
    # Bounding rectangle
    _, _, _, height = cv2.boundingRect(obj)
    extent = height
    # If height is greater than 21 pixels make 20 increments (5% intervals)
    if extent >= 21:
        left, right, center_h = _pseudolandmarks(img, obj, mask, label, 1)
        # If the width of the object is less than 20 pixels just make the object a 20 pixel rectangle
    elif extent < 21:
        left, right, center_h = _small_img_pseudolandmarks(img, obj, mask, label, 1)

    return left, right, center_h
