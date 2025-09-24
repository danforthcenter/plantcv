"""Analyze the vertical distribution of the plant relative to a horizontal reference line."""
import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _iterate_analysis, _grayscale_to_rgb, _scale_size
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def _get_boundary_values(bound_mask, total_area, axis=0):
    """
    Calculate area, percent area, and distance (height or width) in a boundary.

    Parameters
    ----------
    bound_mask : numpy.ndarray
        A binary mask of one side of a horizontal or vertical boundary.
    total_area : int
        Total area of the unbounded mask.
    axis : int, optional
        Which axis to use in calculated distance. 0 is height, 1 is width.

    Returns
    -------
    bound_area : int
        Area within boundary.
    distance_bound : int
        Height/width of mask within boundary.
    percent_area_bound : float
        Percent of total area in this boundary.
    """
    bound_area = int(np.sum(bound_mask))
    distance_bound = 0
    percent_area_bound = 0
    if bound_area:
        distance_bound = int(np.max(np.where(bound_mask)[axis]) +
                             1 - np.min(np.where(bound_mask)[axis]))
        percent_area_bound = int((bound_area / total_area) * 100)
    return bound_area, distance_bound, percent_area_bound


def _boundary_img_annotation(img, mask, line_position, axis=0):
    """Annotate a debug image used in horizontal/vertical boundary analysis
    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    mask : numpy.ndarray
        Binary mask of objects (32-bit).
    line_position : int
        Position of boundary line in pixels from top to bottom (a value of 0 draws the line through the top of the image).
    axis : int
        Which axis to use in drawing division

    Returns
    -------
    out_image : numpy.ndarray
        Diagnostic image showing measurements.
    """
    out_img = np.copy(img)
    # split mask by boundary
    mask1 = np.copy(mask).astype(bool)
    mask2 = np.copy(mask).astype(bool)
    # split mask by line_position on axis
    if not bool(axis):
        # fill in area on opposite side of threshold with 0s
        mask1[line_position:np.shape(mask1)[0] + 1] = np.zeros(
            np.shape(mask1[line_position:np.shape(mask1)[0] + 1]))
        mask2[0:line_position - 1] = np.zeros(
            np.shape(mask2[0:line_position - 1]))
    else:
        # fill in area on opposite side of threshold
        mask1[:, line_position:np.shape(mask1)[1] + 1] = np.zeros(
            np.shape(mask1[:, line_position:np.shape(mask1)[1] + 1]))
        mask2[:, 0:line_position - 1] = np.zeros(
            np.shape(mask2[:, 0:line_position - 1]))

    # replace mask with colors
    out_img[np.where(mask1)] = (255, 0, 255)
    out_img[np.where(mask2)] = (0, 255, 0)
    # draw boundary line
    line_start = [(0, line_position), (line_position, 0)][axis]
    line_end = [(np.shape(out_img)[1], line_position), (line_position, np.shape(img)[0])][axis]
    cv2.line(out_img, line_start, line_end, (255, 0, 0), thickness=params.line_thickness)
    return out_img


def bound_horizontal(img, labeled_mask, line_position, n_labels=1, label=None):
    """
    Analyze the vertical distribution of the plant relative to a horizontal reference line.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    n_labels : int, optional
        Total number of expected individual objects (default = 1).
    line_position : int
        Position of boundary line in pixels from top to bottom (a value of 0 draws the line through the top of the image).
    label : str, optional
        Optional label parameter, modifies the variable name of observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    analysis_image : numpy.ndarray
        Diagnostic image showing measurements.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels,
                            label=label, function=_analyze_bound_horizontal,
                            **{"line_position": line_position})
    img = _boundary_img_annotation(img, labeled_mask, line_position, 0)
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))
    return img


def _analyze_bound_horizontal(img, mask, line_position, label):
    """
    User-input boundary line analysis for individual objects.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting.
    mask : numpy.ndarray
        Binary image data.
    line_position : int
        Position of boundary line in pixels from top to bottom.
    label : str
        Label of object.

    Returns
    -------
    ori_img : numpy.ndarray
        Output image.
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
