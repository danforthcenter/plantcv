# Function to scan for pseudolandmarks along the x-axis

import cv2
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import fatal_error


def x_axis_pseudolandmarks(img, obj, mask, label="default"):
    """
    Divide up object contour into 20 equidistance segments and generate landmarks for each

    Inputs:
    img      = This is a copy of the original plant image generated using np.copy if debug is true it will be drawn on
    obj      = a contour of the plant object (this should be output from the object_composition.py fxn)
    mask     = this is a binary image. The object should be white and the background should be black
    label    = optional label parameter, modifies the variable name of observations recorded

    Returns:
    top      = List of landmark points within 'top' portion
    bottom   = List of landmark points within the 'bottom' portion
    center_v = List of landmark points within the middle portion

    :param img: numpy.ndarray
    :param obj: list
    :param mask: numpy.ndarray
    :param label: str
    :return top: list
    :return bottom: list
    :return center_v: list
    """

    # Lets get some landmarks scanning along the x-axis
    if not np.any(obj):
        return ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA')
    x, y, width, height = cv2.boundingRect(obj)
    extent = width

    # Outputs
    top = []
    bottom = []
    center_v = []
    top_list = []
    bottom_list = []
    center_v_list = []

    # If width is greater than 21 pixels make 20 increments (5% intervals)
    if extent >= 21:
        inc = int(extent / 21)
        # Define variable for max points and min points
        pts_max = []
        pts_min = []
        # Get max and min points for each of the intervals
        for i in range(1, 21):
            if i == 1:
                pt_max = x + (inc * i)
                pt_min = x
            else:
                pt_max = x + (inc * i)
                pt_min = x + (inc * (i - 1))
            # Put these in an array
            pts_max.append(pt_max)
            pts_min.append(pt_min)
        # Combine max and min into a set of tuples
        point_range = list(zip(pts_min, pts_max))
        # define some list variables to fill
        col_median = []
        col_ave = []
        max_height = []
        top_points = []
        bottom_points = []
        x_vals = []
        x_centroids = []
        y_centroids = []
        # For each of the 20 intervals
        for pt in point_range:
            # Get the left and right bounds
            left_point, right_point = pt
            # Get all cols within these two points
            cols = []
            ups = []
            bps = []
            # Get a continuous list of the values between the left and the right of the interval save as vals
            vals = list(range(left_point, right_point))
            # For each col... get all coordinates from object contour that match col
            for v in vals:
                # Value is all entries that match the col
                value = obj[v == obj[:, 0, 0]]
                if len(value) > 0:
                    # Could potentially be more than two points in all contour in each pixel row
                    # Grab largest y coordinate (row)
                    largest = value[:, 0, 1].max()
                    # Grab smallest y coordinate (row)
                    smallest = value[:, 0, 1].min()
                    # Take the difference between the two (this is how far across the object is on this plane)
                    col_width = largest - smallest
                    # Append this value to a list
                    cols.append(col_width)
                    ups.append(smallest)
                    bps.append(largest)
                if len(value) == 0:
                    col_width = 1
                    cols.append(col_width)
                    ups.append(1)
                    bps.append(1)
            # For each of the points find the median and average width
            col_median.append(np.median(np.array(cols)))
            col_ave.append(np.mean(np.array(cols)))
            max_height.append(np.max(np.array(cols)))
            top_points.append(np.mean(smallest))
            bottom_points.append(np.mean(largest))
            xval = int((left_point + right_point) / 2)
            x_vals.append(xval)
            # Make a copy of the mask; we want to get landmark points from this
            window = np.copy(mask)
            window[:, :left_point] = 0
            window[:, right_point:] = 0
            s = cv2.moments(window)
            # Centroid (center of mass x, center of mass y)
            if largest - smallest > 3:
                if s['m00'] > 0.001:
                    smx, smy = (s['m10'] / s['m00'], s['m01'] / s['m00'])
                    x_centroids.append(int(smx))
                    y_centroids.append(int(smy))
                if s['m00'] < 0.001:
                    smx, smy = (s['m10'] / 0.001, s['m01'] / 0.001)
                    x_centroids.append(int(smx))
                    y_centroids.append(int(smy))
            else:
                smx = (largest + smallest) / 2
                smy = xval
                x_centroids.append(int(smx))
                y_centroids.append(int(smy))
        # Get the indicie of the largest median/average y-axis value (if there is a tie it takes largest index)
        # indice_median = col_median.index(max(col_median))
        # indice_ave = col_ave.index(max(col_ave))
        # median_value = col_median[indice_median]
        # ave_value = col_ave[indice_ave]
        # max_value = max_width[indice_ave]
        top = list(zip(x_vals, top_points))
        top = np.array(top)
        top.shape = (20, 1, 2)
        bottom = list(zip(x_vals, bottom_points))
        bottom = np.array(bottom)
        bottom.shape = (20, 1, 2)
        center_v = list(zip(x_centroids, y_centroids))
        center_v = np.array(center_v)
        center_v.shape = (20, 1, 2)

        img2 = np.copy(img)
        for i in top:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 0), -1)
        for i in bottom:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 255), -1)
        for i in center_v:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (0, 79, 255), -1)

        _debug(visual=img2,
               filename=os.path.join(params.debug_outdir, (str(params.device) + '_x_axis_pseudolandmarks.png')))

    elif extent < 21:
        # If the width of the object is less than 20 pixels just make the object a 20 pixel rectangle
        x, y, width, height = cv2.boundingRect(obj)
        x_coords = list(range(x, x + 20))
        u_points = [y] * 20
        top = list(zip(x_coords, u_points))
        top = np.array(top)
        top.shape = (20, 1, 2)
        b_points = [y + width] * 20
        bottom = list(zip(x_coords, b_points))
        bottom = np.array(bottom)
        bottom.shape = (20, 1, 2)
        m = cv2.moments(mask, binaryImage=True)
        if m['m00'] == 0:
            fatal_error('Check input parameters, first moment=0')
        else:
            # Centroid (center of mass x, center of mass y)
            cmx, cmy = (m['m10'] / m['m00'], m['m01'] / m['m00'])
            c_points = [cmy] * 20
            center_v = list(zip(x_coords, c_points))
            center_v = np.array(center_v)
            center_v.shape = (20, 1, 2)

        img2 = np.copy(img)
        for i in top:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 0), -1)
        for i in bottom:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 255), -1)
        for i in center_v:
            x = i[0, 0]
            y = i[0, 1]
            cv2.circle(img2, (int(x), int(y)), params.line_thickness, (0, 79, 255), -1)

        _debug(visual=img2,
               filename=os.path.join(params.debug_outdir, (str(params.device) + '_x_axis_pseudolandmarks.png')))

    # Store into global measurements
    for pt in top:
        top_list.append(pt[0].tolist())
    for pt in bottom:
        bottom_list.append(pt[0].tolist())
    for pt in center_v:
        center_v_list.append(pt[0].tolist())

    outputs.add_observation(sample=label, variable='top_lmk', trait='top landmark coordinates',
                            method='plantcv.plantcv.x_axis_pseudolandmarks', scale='none', datatype=tuple,
                            value=tuple(top_list), label='none')
    outputs.add_observation(sample=label, variable='bottom_lmk', trait='bottom landmark coordinates',
                            method='plantcv.plantcv.x_axis_pseudolandmarks', scale='none', datatype=tuple,
                            value=tuple(bottom_list), label='none')
    outputs.add_observation(sample=label, variable='center_v_lmk', trait='center vertical landmark coordinates',
                            method='plantcv.plantcv.x_axis_pseudolandmarks', scale='none', datatype=tuple,
                            value=tuple(center_v_list), label='none')

    return top, bottom, center_v
