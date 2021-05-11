# Analyzes an object and outputs numeric properties

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import within_frame
from plantcv.plantcv._debug import _debug


def analyze_object(img, obj, mask, label="default"):
    """Outputs numeric properties for an input object (contour or grouped contours).

    Inputs:
    img             = RGB or grayscale image data for plotting
    obj             = single or grouped contour object
    mask            = Binary image to use as mask
    label           = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = list of output images

    :param img: numpy.ndarray
    :param obj: list
    :param mask: numpy.ndarray
    :param label: str
    :return analysis_images: list
    """
    # Valid objects can only be analyzed if they have >= 5 vertices
    if len(obj) < 5:
        return None

    ori_img = np.copy(img)
    # Convert grayscale images to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)

    if len(np.shape(img)) == 3:
        ix, iy, iz = np.shape(img)
    else:
        ix, iy = np.shape(img)
    size = ix, iy, 3
    size1 = ix, iy
    background = np.zeros(size, dtype=np.uint8)
    background1 = np.zeros(size1, dtype=np.uint8)
    background2 = np.zeros(size1, dtype=np.uint8)

    # Check is object is touching image boundaries (QC)
    in_bounds = within_frame(mask=mask, label=label)

    # Convex Hull
    hull = cv2.convexHull(obj)
    hull_vertices = len(hull)
    # Moments
    #  m = cv2.moments(obj)
    m = cv2.moments(mask, binaryImage=True)
    # Properties
    # Area
    area = m['m00']

    if area:
        # Convex Hull area
        hull_area = cv2.contourArea(hull)
        # Solidity
        solidity = 1
        if int(hull_area) != 0:
            solidity = area / hull_area
        # Perimeter
        perimeter = cv2.arcLength(obj, closed=True)
        # x and y position (bottom left?) and extent x (width) and extent y (height)
        x, y, width, height = cv2.boundingRect(obj)
        # Centroid (center of mass x, center of mass y)
        cmx, cmy = (float(m['m10'] / m['m00']), float(m['m01'] / m['m00']))
        # Ellipse
        center, axes, angle = cv2.fitEllipse(obj)
        major_axis = np.argmax(axes)
        minor_axis = 1 - major_axis
        major_axis_length = float(axes[major_axis])
        minor_axis_length = float(axes[minor_axis])
        eccentricity = float(np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2))

        # Longest Axis: line through center of mass and point on the convex hull that is furthest away
        cv2.circle(background, (int(cmx), int(cmy)), 4, (255, 255, 255), -1)
        center_p = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        ret, centerp_binary = cv2.threshold(center_p, 0, 255, cv2.THRESH_BINARY)
        centerpoint, cpoint_h = cv2.findContours(centerp_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

        dist = []
        vhull = np.vstack(hull)

        for i, c in enumerate(vhull):
            xy = tuple([int(ci) for ci in c])
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
            slope = (float(ydiff / xdiff))
        b_line = caliper_mid_y - (slope * caliper_mid_x)

        if slope != 0:
            xintercept = int(-b_line / slope)
            xintercept1 = int((ix - b_line) / slope)
            if 0 <= xintercept <= iy and 0 <= xintercept1 <= iy:
                cv2.line(background1, (xintercept1, ix), (xintercept, 0), (255), params.line_thickness)
            elif xintercept < 0 or xintercept > iy or xintercept1 < 0 or xintercept1 > iy:
                yintercept = int(b_line)
                yintercept1 = int((slope * iy) + b_line)
                cv2.line(background1, (0, yintercept), (iy, yintercept1), (255), 5)
        else:
            cv2.line(background1, (iy, caliper_mid_y), (0, caliper_mid_y), (255), params.line_thickness)

        ret1, line_binary = cv2.threshold(background1, 0, 255, cv2.THRESH_BINARY)

        cv2.drawContours(background2, [hull], -1, (255), -1)
        ret2, hullp_binary = cv2.threshold(background2, 0, 255, cv2.THRESH_BINARY)

        caliper = cv2.multiply(line_binary, hullp_binary)

        caliper_y, caliper_x = np.array(caliper.nonzero())
        caliper_matrix = np.vstack((caliper_x, caliper_y))
        caliper_transpose = np.transpose(caliper_matrix)
        caliper_length = len(caliper_transpose)

        caliper_transpose1 = np.lexsort((caliper_y, caliper_x))
        caliper_transpose2 = [(caliper_x[i], caliper_y[i]) for i in caliper_transpose1]
        caliper_transpose = np.array(caliper_transpose2)

    analysis_images = []

    # Draw properties
    if area:
        cv2.drawContours(ori_img, obj, -1, (255, 0, 0), params.line_thickness)
        cv2.drawContours(ori_img, [hull], -1, (255, 0, 255), params.line_thickness)
        cv2.line(ori_img, (x, y), (x + width, y), (255, 0, 255), params.line_thickness)
        cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 255), params.line_thickness)
        cv2.line(ori_img, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])), (255, 0, 255),
                 params.line_thickness)
        cv2.circle(ori_img, (int(cmx), int(cmy)), 10, (255, 0, 255), params.line_thickness)

        analysis_images.append(ori_img)

        analysis_images.append(mask)

    else:
        pass

    outputs.add_observation(sample=label, variable='area', trait='area',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=area, label='pixels')
    outputs.add_observation(sample=label, variable='convex_hull_area', trait='convex hull area',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=hull_area, label='pixels')
    outputs.add_observation(sample=label, variable='solidity', trait='solidity',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=float,
                            value=solidity, label='none')
    outputs.add_observation(sample=label, variable='perimeter', trait='perimeter',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=perimeter, label='pixels')
    outputs.add_observation(sample=label, variable='width', trait='width',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=width, label='pixels')
    outputs.add_observation(sample=label, variable='height', trait='height',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=height, label='pixels')
    outputs.add_observation(sample=label, variable='longest_path', trait='longest path',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=caliper_length, label='pixels')
    outputs.add_observation(sample=label, variable='center_of_mass', trait='center of mass',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=tuple,
                            value=(cmx, cmy), label=("x", "y"))
    outputs.add_observation(sample=label, variable='convex_hull_vertices', trait='convex hull vertices',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=int,
                            value=hull_vertices, label='none')
    outputs.add_observation(sample=label, variable='object_in_frame', trait='object in frame',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=bool,
                            value=in_bounds, label='none')
    outputs.add_observation(sample=label, variable='ellipse_center', trait='ellipse center',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=tuple,
                            value=(center[0], center[1]), label=("x", "y"))
    outputs.add_observation(sample=label, variable='ellipse_major_axis', trait='ellipse major axis length',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=major_axis_length, label='pixels')
    outputs.add_observation(sample=label, variable='ellipse_minor_axis', trait='ellipse minor axis length',
                            method='plantcv.plantcv.analyze_object', scale='pixels', datatype=int,
                            value=minor_axis_length, label='pixels')
    outputs.add_observation(sample=label, variable='ellipse_angle', trait='ellipse major axis angle',
                            method='plantcv.plantcv.analyze_object', scale='degrees', datatype=float,
                            value=float(angle), label='degrees')
    outputs.add_observation(sample=label, variable='ellipse_eccentricity', trait='ellipse eccentricity',
                            method='plantcv.plantcv.analyze_object', scale='none', datatype=float,
                            value=float(eccentricity), label='none')

    # Debugging output
    params.device += 1
    cv2.drawContours(ori_img, obj, -1, (255, 0, 0), params.line_thickness)
    cv2.drawContours(ori_img, [hull], -1, (255, 0, 255), params.line_thickness)
    cv2.line(ori_img, (x, y), (x + width, y), (255, 0, 255), params.line_thickness)
    cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 255), params.line_thickness)
    cv2.circle(ori_img, (int(cmx), int(cmy)), 10, (255, 0, 255), params.line_thickness)
    cv2.line(ori_img, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])), (255, 0, 255),
             params.line_thickness)
    _debug(visual=ori_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_shapes.png'))

    # Store images
    outputs.images.append(analysis_images)
    return ori_img
