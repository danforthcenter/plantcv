"""Analyze the horizontal distribution of the plant relative to a vertical reference line."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis, _grayscale_to_rgb, _scale_size
from plantcv.plantcv.analyze.bound_horizontal import _get_boundary_values
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def bound_vertical(img, labeled_mask, line_position, n_labels=1, label=None):
    """User-input boundary line analysis for individual objects.

    Inputs:
    img           = RGB or grayscale image data for plotting
    labeled_mask  = Labeled mask of objects (32-bit).
    n_labels      = Total number expected individual objects (default = 1).
    line_position = position of boundary line in pixels from top to bottom
                    (a value of 0 would draw the line through the top of the image)
    label         = Optional label parameter, modifies the variable name of
                    observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param line_position: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels,
                            label=label, function=_analyze_bound_vertical,
                            **{"line_position": line_position})
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img


def _analyze_bound_vertical(img, mask, line_position, label):
    """
    User-input boundary line tool

    Inputs:
    img             = RGB or grayscale image data for plotting
    mask            = Binary mask made from selected contours
    line_position   = position of boundary line (a value of 0 would draw the line through the left side of the image)
    label           = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = output images

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param line_position: int
    :param label: str
    :return analysis_images: list
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
