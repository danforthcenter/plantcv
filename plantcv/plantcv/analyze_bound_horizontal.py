# User-Input Boundary Line

import os
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def analyze_bound_horizontal(img, obj, mask, line_position, label="default"):
    """
    User-input boundary line tool

    Inputs:
    img             = RGB or grayscale image data for plotting
    obj             = single or grouped contour object
    mask            = Binary mask made from selected contours
    line_position   = position of boundary line (a value of 0 would draw the line through the top of the image)
    label           = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_images = list of output images

    :param img: numpy.ndarray
    :param obj: list
    :param mask: numpy.ndarray
    :param line_position: int
    :param label: str
    :return analysis_images: list
    """
    ori_img = np.copy(img)

    # Draw line horizontal line through bottom of image, that is adjusted to user input height
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    iy, ix, iz = np.shape(ori_img)
    size = (iy, ix)
    size1 = (iy, ix, 3)
    background = np.zeros(size, dtype=np.uint8)
    wback = (np.zeros(size1, dtype=np.uint8)) + 255
    x_coor = int(ix)
    y_coor = line_position
    rec_corner = int(iy - 2)
    rec_point1 = (1, rec_corner)
    rec_point2 = (x_coor - 2, y_coor - 2)
    cv2.rectangle(background, rec_point1, rec_point2, (255), 1)
    below_contour, below_hierarchy = cv2.findContours(background, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    x, y, width, height = cv2.boundingRect(obj)

    if y_coor - y <= 0:
        height_above_bound = 0
        height_below_bound = height
    elif y_coor - y > 0:
        height_1 = y_coor - y
        if height - height_1 <= 0:
            height_above_bound = height
            height_below_bound = 0
        else:
            height_above_bound = y_coor - y
            height_below_bound = height - height_above_bound

    below = []
    above = []
    mask_nonzerox, mask_nonzeroy = np.nonzero(mask)
    obj_points = np.vstack((mask_nonzeroy, mask_nonzerox))
    obj_points1 = np.transpose(obj_points)

    for i, c in enumerate(obj_points1):
        xy = tuple([int(ci) for ci in c])
        pptest = cv2.pointPolygonTest(below_contour[0], xy, measureDist=False)
        if pptest == 1:
            below.append(xy)
            cv2.circle(ori_img, xy, 1, (155, 0, 255))
            cv2.circle(wback, xy, 1, (155, 0, 255))
        else:
            above.append(xy)
            cv2.circle(ori_img, xy, 1, (0, 255, 0))
            cv2.circle(wback, xy, 1, (0, 255, 0))
    above_bound_area = len(above)
    below_bound_area = len(below)
    percent_bound_area_above = ((float(above_bound_area)) / (float(above_bound_area + below_bound_area))) * 100
    percent_bound_area_below = ((float(below_bound_area)) / (float(above_bound_area + below_bound_area))) * 100

    analysis_images = []

    if above_bound_area or below_bound_area:
        point3 = (0, y_coor - 4)
        point4 = (x_coor, y_coor - 4)
        cv2.line(ori_img, point3, point4, (255, 0, 255), params.line_thickness)
        cv2.line(wback, point3, point4, (255, 0, 255), params.line_thickness)
        m = cv2.moments(mask, binaryImage=True)
        cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        if y_coor - y <= 0:
            cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), params.line_thickness)
            cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), params.line_thickness)
        elif y_coor - y > 0:
            height_1 = y_coor - y
            if height - height_1 <= 0:
                cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), params.line_thickness)
                cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), params.line_thickness)
            else:
                cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0),
                         params.line_thickness)
                cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0),
                         params.line_thickness)
                cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0),
                         params.line_thickness)
                cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0),
                         params.line_thickness)
        # Output image with boundary line, above/below bound area
        analysis_images.append(wback)
        analysis_images.append(ori_img)

    if params.debug is not None:
        params.device += 1
        point3 = (0, y_coor - 4)
        point4 = (x_coor, y_coor - 4)
        cv2.line(ori_img, point3, point4, (255, 0, 255), params.line_thickness)
        cv2.line(wback, point3, point4, (255, 0, 255), params.line_thickness)
        m = cv2.moments(mask, binaryImage=True)
        cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
        if y_coor - y <= 0:
            cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), params.line_thickness)
            cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (0, 255, 0), params.line_thickness)
        elif y_coor - y > 0:
            height_1 = y_coor - y
            if height - height_1 <= 0:
                cv2.line(ori_img, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), params.line_thickness)
                cv2.line(wback, (int(cmx), y), (int(cmx), y + height), (255, 0, 0), params.line_thickness)
            else:
                cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0),
                         params.line_thickness)
                cv2.line(ori_img, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0),
                         params.line_thickness)
                cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor - height_above_bound), (255, 0, 0),
                         params.line_thickness)
                cv2.line(wback, (int(cmx), y_coor - 2), (int(cmx), y_coor + height_below_bound), (0, 255, 0),
                         params.line_thickness)
        _debug(visual=wback,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_white.png'))
        _debug(visual=ori_img,
               filename=os.path.join(params.debug_outdir, str(params.device) + '_boundary_on_img.png'))

    outputs.add_observation(sample=label, variable='horizontal_reference_position',
                            trait='horizontal reference position',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='none', datatype=int,
                            value=line_position, label='none')
    outputs.add_observation(sample=label, variable='height_above_reference', trait='height above reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='pixels', datatype=int,
                            value=height_above_bound, label='pixels')
    outputs.add_observation(sample=label, variable='height_below_reference', trait='height_below_reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='pixels', datatype=int,
                            value=height_below_bound, label='pixels')
    outputs.add_observation(sample=label, variable='area_above_reference', trait='area above reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='pixels', datatype=int,
                            value=above_bound_area, label='pixels')
    outputs.add_observation(sample=label, variable='percent_area_above_reference', trait='percent area above reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='none', datatype=float,
                            value=percent_bound_area_above, label='none')
    outputs.add_observation(sample=label, variable='area_below_reference', trait='area below reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='pixels', datatype=int,
                            value=below_bound_area, label='pixels')
    outputs.add_observation(sample=label, variable='percent_area_below_reference', trait='percent area below reference',
                            method='plantcv.plantcv.analyze_bound_horizontal', scale='none', datatype=float,
                            value=percent_bound_area_below, label='none')

    # Store images
    outputs.images.append(analysis_images)

    return ori_img
