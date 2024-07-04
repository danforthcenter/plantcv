"""Analyzes the shape and size of objects and outputs data."""
import os
import cv2
import numpy as np
from plantcv.plantcv._helpers import _iterate_analysis, _cv2_findcontours, _object_composition, _grayscale_to_rgb
from plantcv.plantcv import outputs, within_frame
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def size(img, labeled_mask, n_labels=1, label=None):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    img          = RGB or grayscale image data for plotting
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Diagnostic image showing measurements.

    :param img: numpy.ndarray
    :param labeled_mask: numpy.ndarray
    :param n_labels: int
    :param label: str
    :return analysis_image: numpy.ndarray
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_size)
    # Debugging
    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + '_shapes.png'))
    return img


def _analyze_size(img, mask, label):
    """Analyze the size of individual objects.

    Inputs:
    img   = RGB or grayscale image data for plotting
    mask  = Binary image data
    label = Label of object

    Returns:
    analysis_image = Diagnostic image showing measurements

    :param mask: numpy.ndarray
    :param label: int
    :return analysis_image: numpy.ndarray
    """
    params.device += 1
    # Initialize analysis output values
    area = 0
    hull_area = 0
    solidity = 0
    perimeter = 0
    width = 0
    height = 0
    caliper_length = 0
    cmx = 0
    cmy = 0
    hull_vertices = 0
    ellipse_center = 0, 0
    ellipse_major_axis = 0
    ellipse_minor_axis = 0
    ellipse_angle = 0
    ellipse_eccentricity = 0
    # Check is object is touching image boundaries (QC)
    in_bounds = within_frame(mask=mask, label=label)

    # Convert grayscale images to color
    img = _grayscale_to_rgb(img)
    # Plot image
    plt_img = np.copy(img)

    # Find contours
    cnt, cnt_str = _cv2_findcontours(bin_img=mask)

    # Consolidate contours
    obj = _object_composition(contours=cnt, hierarchy=cnt_str)

    # Analyze shape properties if the object is large enough
    if len(obj) > 5:
        # Convex Hull
        hull = cv2.convexHull(obj)
        # Number of convex hull vertices
        hull_vertices = len(hull)
        # Convex Hull area
        hull_area = cv2.contourArea(hull)
        # Moments
        m = cv2.moments(mask, binaryImage=True)
        # Area
        area = m['m00']
        # Solidity
        solidity = area / hull_area if hull_area != 0 else 1
        # Perimeter
        perimeter = cv2.arcLength(obj, closed=True)
        # Bounding rectangle
        x, y, width, height = cv2.boundingRect(obj)
        # Centroid/Center of Mass
        cmx = m['m10'] / m['m00']
        cmy = m['m01'] / m['m00']
        # Bounding ellipse
        ellipse_center, axes, ellipse_angle = cv2.fitEllipse(obj)
        major_axis_idx = np.argmax(axes)
        minor_axis_idx = 1 - major_axis_idx
        ellipse_major_axis = float(axes[major_axis_idx])
        ellipse_minor_axis = float(axes[minor_axis_idx])
        ellipse_eccentricity = float(np.sqrt(1 - (axes[minor_axis_idx] / axes[major_axis_idx]) ** 2))
        # Caliper length
        caliper_length, caliper_transpose = _longest_axis(height=img.shape[0], width=img.shape[1],
                                                          hull=hull, cmx=cmx, cmy=cmy)
        # Debugging output
        cv2.drawContours(plt_img, obj, -1, (255, 0, 0), params.line_thickness)
        cv2.drawContours(plt_img, [hull], -1, (255, 0, 255), params.line_thickness)
        cv2.line(plt_img, (x, y), (x + width, y), (255, 0, 255), params.line_thickness)
        cv2.line(plt_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 255), params.line_thickness)
        cv2.circle(plt_img, (int(cmx), int(cmy)), 10, (255, 0, 255), params.line_thickness)
        cv2.line(plt_img, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])),
                 (255, 0, 255), params.line_thickness)

    # Store outputs
    outputs.add_observation(sample=label, variable='area', trait='area',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=area, label='pixels')
    outputs.add_observation(sample=label, variable='convex_hull_area', trait='convex hull area',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=hull_area, label='pixels')
    outputs.add_observation(sample=label, variable='solidity', trait='solidity',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=float,
                            value=solidity, label='none')
    outputs.add_observation(sample=label, variable='perimeter', trait='perimeter',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=perimeter, label='pixels')
    outputs.add_observation(sample=label, variable='width', trait='width',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=width, label='pixels')
    outputs.add_observation(sample=label, variable='height', trait='height',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=height, label='pixels')
    outputs.add_observation(sample=label, variable='longest_path', trait='longest path',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=caliper_length, label='pixels')
    outputs.add_observation(sample=label, variable='center_of_mass', trait='center of mass',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=tuple,
                            value=(cmx, cmy), label=("x", "y"))
    outputs.add_observation(sample=label, variable='convex_hull_vertices', trait='convex hull vertices',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=int,
                            value=hull_vertices, label='none')
    outputs.add_observation(sample=label, variable='object_in_frame', trait='object in frame',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=bool,
                            value=in_bounds, label='none')
    outputs.add_observation(sample=label, variable='ellipse_center', trait='ellipse center',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=tuple,
                            value=(ellipse_center[0], ellipse_center[1]), label=("x", "y"))
    outputs.add_observation(sample=label, variable='ellipse_major_axis', trait='ellipse major axis length',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=ellipse_major_axis, label='pixels')
    outputs.add_observation(sample=label, variable='ellipse_minor_axis', trait='ellipse minor axis length',
                            method='plantcv.plantcv.analyze.size', scale='pixels', datatype=int,
                            value=ellipse_minor_axis, label='pixels')
    outputs.add_observation(sample=label, variable='ellipse_angle', trait='ellipse major axis angle',
                            method='plantcv.plantcv.analyze.size', scale='degrees', datatype=float,
                            value=float(ellipse_angle), label='degrees')
    outputs.add_observation(sample=label, variable='ellipse_eccentricity', trait='ellipse eccentricity',
                            method='plantcv.plantcv.analyze.size', scale='none', datatype=float,
                            value=float(ellipse_eccentricity), label='none')
    return plt_img


def _longest_axis(height, width, hull, cmx, cmy):
    """
    Calculate the line through center of mass and point on the convex hull that is furthest away

    :param height: int
    :param width: int
    :param hull: numpy.ndarray
    :param cmx: int
    :param cmy: int
    :return caliper_length: int
    """
    background = np.zeros((height, width, 3), np.uint8)
    background1 = np.zeros((height, width), np.uint8)
    background2 = np.zeros((height, width), np.uint8)
    # Longest Axis: line through center of mass and point on the convex hull that is furthest away
    cv2.circle(background, (int(cmx), int(cmy)), 4, (255, 255, 255), -1)
    center_p = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    _, centerp_binary = cv2.threshold(center_p, 0, 255, cv2.THRESH_BINARY)
    centerpoint, _ = _cv2_findcontours(bin_img=centerp_binary)

    dist = []
    vhull = np.vstack(hull)

    for i, c in enumerate(vhull):
        xy = tuple(int(ci) for ci in c)
        pptest = cv2.pointPolygonTest(centerpoint[0], xy, measureDist=True)
        dist.append(pptest)

    abs_dist = np.absolute(dist)
    max_i = np.argmax(abs_dist)

    caliper_max_x, caliper_max_y = list(tuple(vhull[max_i]))
    caliper_mid_x, caliper_mid_y = [int(cmx), int(cmy)]

    xdiff = float(caliper_max_x - caliper_mid_x)
    ydiff = float(caliper_max_y - caliper_mid_y)

    # Set default values
    slope = 1

    if xdiff != 0:
        slope = float(ydiff / xdiff)
    b_line = caliper_mid_y - (slope * caliper_mid_x)

    if slope != 0:
        xintercept = int(-b_line / slope)
        xintercept1 = int((height - b_line) / slope)
        if 0 <= xintercept <= width and 0 <= xintercept1 <= width:
            cv2.line(background1, (xintercept1, height), (xintercept, 0), (255), params.line_thickness)
        elif xintercept < 0 or xintercept > width or xintercept1 < 0 or xintercept1 > width:
            yintercept = int(b_line)
            yintercept1 = int((slope * width) + b_line)
            cv2.line(background1, (0, yintercept), (width, yintercept1), (255), 5)
    else:
        cv2.line(background1, (width, caliper_mid_y), (0, caliper_mid_y), (255), params.line_thickness)

    _, line_binary = cv2.threshold(background1, 0, 255, cv2.THRESH_BINARY)

    cv2.drawContours(background2, [hull], -1, (255), -1)
    _, hullp_binary = cv2.threshold(background2, 0, 255, cv2.THRESH_BINARY)

    caliper = cv2.multiply(line_binary, hullp_binary)

    caliper_y, caliper_x = np.array(caliper.nonzero())
    caliper_matrix = np.vstack((caliper_x, caliper_y))
    caliper_transpose = np.transpose(caliper_matrix)
    caliper_length = len(caliper_transpose)

    caliper_transpose1 = np.lexsort((caliper_y, caliper_x))
    caliper_transpose2 = [(caliper_x[i], caliper_y[i]) for i in caliper_transpose1]
    caliper_transpose = np.array(caliper_transpose2)

    return caliper_length, caliper_transpose
