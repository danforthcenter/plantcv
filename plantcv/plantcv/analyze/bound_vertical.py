"""Analyze the horizontal distribution of the plant relative to a vertical reference line."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis, _grayscale_to_rgb, _scale_size
from plantcv.plantcv.analyze.bound_horizontal import _get_boundary_values, _boundary_img_annotation
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def bound_vertical(img, labeled_mask, line_position, n_labels=1, label=None):
    """
    Analyze the horizontal distribution of the plant relative to a vertical reference line for individual objects.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    line_position : int
        Position of boundary line in pixels from left to right (a value of 0 draws the line through the left of the image).
    n_labels : int, optional
        Total number of expected individual objects (default = 1).
    label : str, optional
        Optional label parameter, modifies the variable name of observations recorded (default = params.sample_label).

    Returns
    -------
    analysis_image : numpy.ndarray
        Diagnostic image showing measurements.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels,
                            label=label, function=_analyze_bound_vertical,
                            **{"line_position": line_position})
    img = _boundary_img_annotation(img, labeled_mask, line_position, 1)
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img


def _analyze_bound_vertical(img, mask, line_position, label):
    """
    Analyze the mask relative to a user-input vertical boundary line.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    mask : numpy.ndarray
        Binary mask made from selected contours.
    line_position : int
        Position of boundary line in pixels from left to right (a value of 0 draws the line through the left of the image).
    label : str
        Optional label parameter, modifies the variable name of observations recorded.

    Returns
    -------
    ori_img : numpy.ndarray
        Output image.
    """
    # Initialize output measurements
    width_left_bound = 0
    width_right_bound = 0
    left_bound_area = 0
    percent_bound_area_left = 0
    right_bound_area = 0
    percent_bound_area_right = 0

    ori_img = np.copy(img)
    # Skip empty masks
    if np.count_nonzero(mask) != 0 and line_position >= 0:
        # Draw line horizontal line through bottom of image, that is adjusted to user input height
        ori_img = _grayscale_to_rgb(img)
        left_mask = np.copy(mask).astype(bool)
        right_mask = np.copy(mask).astype(bool)
        left_mask[:, line_position:np.shape(left_mask)[1] + 1] = np.zeros(
            np.shape(left_mask[:, line_position:np.shape(left_mask)[1] + 1]))
        right_mask[:, 0:line_position - 1] = np.zeros(
            np.shape(right_mask[:, 0:line_position - 1]))
        tot_area = np.sum(mask.astype(bool))
        left_bound_area, width_left_bound, percent_bound_area_left = _get_boundary_values(left_mask, tot_area, 1)
        right_bound_area, width_right_bound, percent_bound_area_right = _get_boundary_values(right_mask, tot_area, 1)

    outputs.add_observation(sample=label, variable='vertical_reference_position', trait='vertical reference position',
                            method='plantcv.plantcv.analyze.bound_vertical', scale='none', datatype=int,
                            value=line_position, label='none')
    outputs.add_observation(sample=label, variable='width_left_reference', trait='width left of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale=params.unit, datatype=int,
                            value=_scale_size(width_left_bound), label=params.unit)
    outputs.add_observation(sample=label, variable='width_right_reference', trait='width right of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale=params.unit, datatype=int,
                            value=_scale_size(width_right_bound), label=params.unit)
    outputs.add_observation(sample=label, variable='area_left_reference', trait='area left of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale=params.unit, datatype=int,
                            value=_scale_size(left_bound_area, "area"), label=params.unit)
    outputs.add_observation(sample=label, variable='percent_area_left_reference',
                            trait='percent area left of reference', method='plantcv.plantcv.analyze.bound_vertical',
                            scale='none', datatype=float,
                            value=percent_bound_area_left, label='none')
    outputs.add_observation(sample=label, variable='area_right_reference', trait='area right of reference',
                            method='plantcv.plantcv.analyze.bound_vertical', scale=params.unit, datatype=int,
                            value=_scale_size(right_bound_area, "area"), label=params.unit)
    outputs.add_observation(sample=label, variable='percent_area_right_reference',
                            trait='percent area right of reference', method='plantcv.plantcv.analyze.bound_vertical',
                            scale='none', datatype=float, value=percent_bound_area_right, label='none')

    return ori_img
