"""Function to scan for pseudolandmarks along the x-axis."""
import cv2
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition
from plantcv.plantcv import params, outputs


def x_axis_pseudolandmarks(img, mask, label=None):
    """Divide up object contour into 20 equidistance segments and generate landmarks for each.

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
    top : list
        Top landmark points (depending on axis)
    bottom : list
        Bottom landmark points (depending on axis)
    center_v : list
        Vertical landmark points in middle portion (depending on axis)
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
    _, _, width, _ = cv2.boundingRect(obj)
    extent = width
    # If width is greater than 21 pixels make 20 increments (5% intervals)
    if extent >= 21:
        top, bottom, center_v = _pseudolandmarks(img, obj, mask, label, 0)
        # If the width of the object is less than 20 pixels just make the object a 20 pixel rectangle
    elif extent < 21:
        top, bottom, center_v = _small_img_pseudolandmarks(img, obj, mask, label, 0)

    return top, bottom, center_v


def _small_img_pseudolandmarks(img, obj, mask, label, axis=0):
    """Divide object contour into equidistance segments for small (<=20px tall) images.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting
    obj : list
        Contours of the object of interest
    mask : numpy.ndarray
        Binary mask of the object of interest
    label : str
        Label parameter, modifies the variable name of
        observations recorded
    axis : int, optional
        Axis along which to generate landmarks, 0 for x axis, 1 for y axis, by default 0

    Returns
    -------
    left_or_top : list
        Left or top landmark points (depending on axis)
    right_or_bottom : list
        Right or bottom landmark points (depending on axis)
    center_h_or_v : list
        Horizontal or vertical landmark points in middle portion (depending on axis)
    """
    # Lists to return
    left_or_top = []
    right_or_bottom = []
    center_h_or_v = []
    # Lists for outputs class
    left_or_top_list = []
    right_or_bottom_list = []
    center_h_or_v_list = []
    # helper lists for x/y directions
    axes_names = ["x", "y"]
    axis_name = axes_names.pop(axis)
    direction_names = [["top", "bottom", "vertical"], ["left", "right", "horizontal"]][axis]
    lt = direction_names[0]
    rb = direction_names[1]
    hv = direction_names[2]
    # If the length of the object is less than 20 pixels make 20 pixel rectangle
    x, y, width, _ = cv2.boundingRect(obj)
    xy = [x, y]
    main_ax = xy.pop(axis)
    other_ax = xy[0]
    coords = list(range(main_ax, main_ax + 20))
    points = [other_ax] * 20
    points2 = [other_ax + width] * 20
    left_or_top = list(zip(points, coords))
    right_or_bottom = list(zip(points2, coords))
    # if using x axis then flip order of points and coords
    if axis:
        left_or_top = list(zip(coords, points))
        right_or_bottom = list(zip(coords, points2))
    left_or_top = np.array(left_or_top)
    left_or_top.shape = (20, 1, 2)
    right_or_bottom = np.array(right_or_bottom)
    right_or_bottom.shape = (20, 1, 2)
    # get moments from mask
    m = cv2.moments(mask, binaryImage=True)
    # Centroid (center of mass)
    cms = (m['m10'] / m['m00'], m['m01'] / m['m00'])
    cm = cms[axis]
    c_points = [cm] * 20
    center_h_or_v = list(zip(c_points, coords))
    center_h_or_v = np.array(center_h_or_v)
    center_h_or_v.shape = (20, 1, 2)
    img2 = np.copy(img)
    for i in left_or_top:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 0), -1)
    for i in right_or_bottom:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 255), -1)
    for i in center_h_or_v:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (0, 79, 255), -1)
    _debug(visual=img2,
           filename=os.path.join(params.debug_outdir, (str(params.device) + f'_{axis_name}_axis_pseudolandmarks.png')))
    # add points to lists for saving output
    for pt in left_or_top:
        left_or_top_list.append(pt[0].tolist())
    for pt in right_or_bottom:
        right_or_bottom_list.append(pt[0].tolist())
    for pt in center_h_or_v:
        center_h_or_v_list.append(pt[0].tolist())
    # save outputs
    outputs.add_observation(sample=label, variable=f'{lt}_lmk', trait=f'{lt} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(left_or_top_list), label='none')
    outputs.add_observation(sample=label, variable=f'{rb}_lmk', trait=f'{rb} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(right_or_bottom_list), label='none')
    outputs.add_observation(sample=label, variable=f'center_{hv[0]}_lmk',
                            trait=f'center {hv} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(center_h_or_v_list), label='none')

    return left_or_top, right_or_bottom, center_h_or_v


def _pseudolandmarks(img, obj, mask, label, axis=0):
    """Divide object contour into equidistance segments for >20px tall images.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data for plotting
    obj : list
        Contours of the object of interest
    mask : numpy.ndarray
        Binary mask of the object of interest
    label : str
        Label parameter, modifies the variable name of
        observations recorded
    axis : int, optional
        Axis along which to generate landmarks, 0 for x axis, 1 for y axis, by default 0

    Returns
    -------
    left_or_top : list
        Left or top landmark points (depending on axis)
    right_or_bottom : list
        Right or bottom landmark points (depending on axis)
    center_h_or_v : list
        Horizontal or vertical landmark points in middle portion (depending on axis)
    """
    x, y, width, height = cv2.boundingRect(obj)
    xy = [x, y]
    main_ax = xy.pop(axis)
    directions = [width, height]
    main_direction = directions.pop(axis)
    channels = [0, 1]
    main_c = channels.pop(axis)
    other_c = channels[0]
    extent = main_direction
    # Lists to return
    left_or_top = []
    right_or_bottom = []
    center_h_or_v = []
    # Lists for outputs class
    left_or_top_list = []
    right_or_bottom_list = []
    center_h_or_v_list = []
    # helper lists for x/y directions
    axes_names = ["x", "y"]
    axis_name = axes_names.pop(axis)
    direction_names = [["top", "bottom", "vertical"], ["left", "right", "horizontal"]][axis]
    lt = direction_names[0]
    rb = direction_names[1]
    hv = direction_names[2]
    # define increment
    inc = int(extent / 21)
    # Define variable for max points and min points
    pts_max = [main_ax]
    pts_min = [main_ax + inc]
    # Get max and min points for each of the intervals
    for i in range(2, 21):
        pt_max = main_ax + (inc * (i - 1))
        pt_min = main_ax + (inc * i)
        # Put these in an array
        pts_max.append(pt_max)
        pts_min.append(pt_min)
    # Combine max and min into a set of tuples
    point_range = list(zip(pts_max, pts_min))
    # define some list variables to fill
    row_median = []
    row_ave = []
    max_width = []
    left_or_top_points = []
    right_or_bottom_points = []
    y_vals = []
    x_centroids = []
    y_centroids = []
    # For each of the 20 intervals
    for pt in point_range:
        # Get the lower and upper bounds
        low_point, high_point = pt
        # Get all rows within these two points
        rows = []
        lps = []
        rps = []
        # Get a continuous list of the values between the top and the bottom of the interval save as vals
        vals = list(range(low_point, high_point))
        # For each row... get all coordinates from object contour that match row
        for v in vals:
            # Value is all entries that match the row
            value = obj[v == obj[:, 0, main_c]]
            if len(value) > 0:
                # Could potentially be more than two points in all contour in each pixel row
                # Grab largest x coordinate (column)
                largest = value[:, 0, other_c].max()
                # Grab smallest x coordinate (column)
                smallest = value[:, 0, other_c].min()
                # Take the difference between the two (this is how far across the object is on this plane)
                row_width = largest - smallest
                # Append this value to a list
                rows.append(row_width)
                lps.append(smallest)
                rps.append(largest)
            if len(value) == 0:
                row_width = 1
                rows.append(row_width)
                lps.append(1)
                rps.append(1)
        # For each of the points find the median and average width
        row_median.append(np.median(np.array(rows)))
        row_ave.append(np.mean(np.array(rows)))
        max_width.append(np.max(np.array(rows)))
        left_or_top_points.append(np.mean(smallest))
        right_or_bottom_points.append(np.mean(largest))
        yval = int((high_point + low_point) / 2)
        y_vals.append(yval)
        # Make a copy of the mask; we want to get landmark points from this
        window = np.copy(mask)
        window[:low_point] = 0
        window[high_point:] = 0
        s = cv2.moments(window)
        # Centroid (center of mass x, center of mass y)
        smx = (largest + smallest) / 2
        smy = yval
        # if difference is very small then recalculate centroids
        if largest - smallest > 3:
            smx, smy = (s['m10'] / max(s['m00'], 0.001),
                        s['m01'] / max(s['m00'], 0.001))
        # append results to centroids
        x_centroids.append(int(smx))
        y_centroids.append(int(smy))
    left_or_top = list(zip(left_or_top_points, y_vals))
    right_or_bottom = list(zip(right_or_bottom_points, y_vals))
    if not axis:
        left_or_top = list(zip(y_vals, left_or_top_points))
        right_or_bottom = list(zip(y_vals, right_or_bottom_points))
    left_or_top = np.array(left_or_top)
    left_or_top.shape = (20, 1, 2)
    right_or_bottom = np.array(right_or_bottom)
    right_or_bottom.shape = (20, 1, 2)
    center_h_or_v = list(zip(x_centroids, y_centroids))
    center_h_or_v = np.array(center_h_or_v)
    center_h_or_v.shape = (20, 1, 2)

    img2 = np.copy(img)
    for i in left_or_top:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 0), -1)
    for i in right_or_bottom:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (255, 0, 255), -1)
    for i in center_h_or_v:
        x = i[0, 0]
        y = i[0, 1]
        cv2.circle(img2, (int(x), int(y)), params.line_thickness, (0, 79, 255), -1)

    _debug(visual=img2,
           filename=os.path.join(params.debug_outdir, (str(params.device) + f'_{axis_name}_axis_pseudolandmarks.png')))

    # Store into global measurements
    for pt in left_or_top:
        left_or_top_list.append(pt[0].tolist())
    for pt in right_or_bottom:
        right_or_bottom_list.append(pt[0].tolist())
    for pt in center_h_or_v:
        center_h_or_v_list.append(pt[0].tolist())

    # save outputs
    outputs.add_observation(sample=label, variable=f'{lt}_lmk', trait=f'{lt} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(left_or_top_list), label='none')
    outputs.add_observation(sample=label, variable=f'{rb}_lmk', trait=f'{rb} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(right_or_bottom_list), label='none')
    outputs.add_observation(sample=label, variable=f'center_{hv[0]}_lmk',
                            trait=f'center {hv} landmark coordinates',
                            method=f'plantcv.plantcv.homology.{axis_name}_axis_pseudolandmarks',
                            scale='none', datatype=tuple,
                            value=tuple(center_h_or_v_list), label='none')

    return left_or_top, right_or_bottom, center_h_or_v
