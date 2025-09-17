"""Function to scan for pseudolandmarks along the y-axis."""
import cv2
import numpy as np
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition
from plantcv.plantcv.homology.x_axis_pseudolandmark import _small_img_pseudolandmarks, _pseudolandmarks
from plantcv.plantcv import params


def y_axis_pseudolandmarks(img, mask, label=None):
    """Divide up object contour into 19 equidistant segments and generate landmarks for each.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting
    mask : numpy.ndarray
        Binary mask of the object of interest
    label : str or None, optional
        Optional label parameter, modifies the variable name of
        observations recorded, (default = pcv.params.sample_label)

    Returns
    -------
    left : list
        Left landmark points (depending on axis)
    right : list
        Right landmark points (depending on axis)
    center_h : list
        Horizontal landmark points in middle portion (depending on axis)
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
