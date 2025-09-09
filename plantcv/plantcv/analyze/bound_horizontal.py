"""Analyze the vertical distribution of the plant relative to a horizontal reference line."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis, _grayscale_to_rgb, _scale_size
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def _get_boundary_values(bound_mask, total_area, axis=0):
    """Calculate area, percent area and distance (height or width) in a boundary.
    Parameters
    ----------
    bound_mask = numpy.ndarray, a binary mask of one side of a horizontal or vertical boundary
    total_area = int, total area of the unbounded mask
    axis       = int (0 or 1), which axis to use in calculated distance. 0 is height, 1 is width.

    Returns
    -------
    bound_area         = int, area within boundary
    distance_bound     = int, height/width of mask within boundary
    percent_area_bound = float, percent of total area in this boundary
    """
    bound_area = int(np.sum(bound_mask))
    distance_bound = 0
    percent_area_bound = 0
    if bound_area:
        distance_bound = int(np.max(np.where(bound_mask)[axis]) +
                             1 - np.min(np.where(bound_mask)[axis]))
        percent_area_bound = int((bound_area / total_area) * 100)
    return bound_area, distance_bound, percent_area_bound


def bound_horizontal(img, labeled_mask, line_position, n_labels=1, label=None):
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
                            label=label, function=_analyze_bound_horizontal,
                            **{"line_position": line_position})
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img


def _analyze_bound_horizontal(img, mask, line_position, label):
    """
    User-input boundary line analysis for individual objects

    Inputs:
    img             = RGB or grayscale image data for plotting
    mask            = Binary image data
    line_position   = Position of boundary line in pixels from top to bottom
    label           = Label of object

    Returns:
    analysis_images = list of output images

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param line_position: int
    :param label: str
    :return analysis_images: list
    """
    # Initialize output measurements
    height_above_bound = 0
    height_below_bound = 0
    above_bound_area = 0
    percent_bound_area_above = 0
    below_bound_area = 0
    percent_bound_area_below = 0
    ori_img = np.copy(img)
    # Skip empty masks
    if np.count_nonzero(mask) != 0 and line_position >= 0:
        ori_img = _grayscale_to_rgb(ori_img)
        # make copy of mask for above and below threshold
        top_mask = np.copy(mask).astype(bool)
        bottom_mask = np.copy(mask).astype(bool)
        # fill in area on opposite side of threshold with 0s
        top_mask[line_position:np.shape(top_mask)[0] + 1] = np.zeros(
            np.shape(top_mask[line_position:np.shape(top_mask)[0] + 1]))
        bottom_mask[0:line_position - 1] = np.zeros(
            np.shape(top_mask[0:line_position - 1]))
        tot_area = np.sum(mask.astype(bool))
        # calculate values above and below boundary
        above_bound_area, height_above_bound, percent_bound_area_above = _get_boundary_values(top_mask, tot_area, 0)
        below_bound_area, height_below_bound, percent_bound_area_below = _get_boundary_values(bottom_mask, tot_area, 0)

    outputs.add_observation(sample=label, variable='horizontal_reference_position',
                            trait='horizontal reference position',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale='none', datatype=int,
                            value=line_position, label='none')
    outputs.add_observation(sample=label, variable='height_above_reference', trait='height above reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale=params.unit, datatype=int,
                            value=_scale_size(height_above_bound), label=params.unit)
    outputs.add_observation(sample=label, variable='height_below_reference', trait='height_below_reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale=params.unit, datatype=int,
                            value=_scale_size(height_below_bound), label=params.unit)
    outputs.add_observation(sample=label, variable='area_above_reference', trait='area above reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale=params.unit, datatype=int,
                            value=_scale_size(above_bound_area, "area"), label=params.unit)
    outputs.add_observation(sample=label, variable='percent_area_above_reference', trait='percent area above reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale='none', datatype=float,
                            value=percent_bound_area_above, label='none')
    outputs.add_observation(sample=label, variable='area_below_reference', trait='area below reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale=params.unit, datatype=int,
                            value=_scale_size(below_bound_area, "area"), label=params.unit)
    outputs.add_observation(sample=label, variable='percent_area_below_reference', trait='percent area below reference',
                            method='plantcv.plantcv.analyze.bound_horizontal', scale='none', datatype=float,
                            value=percent_bound_area_below, label='none')

    return ori_img
