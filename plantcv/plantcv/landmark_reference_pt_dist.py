# Script to generate an image with metrics displayed on image

import numpy as np
import math
import numbers
from plantcv.plantcv import params
from plantcv.plantcv import outputs


def landmark_reference_pt_dist(points_r, centroid_r, bline_r, label="default"):
    """landmark_reference_pt_dist

    For each point in contour, get a point before (pre) and after (post) the point of interest.
    The win argument specifies the pre and post point distances.

    Inputs:
    points_r   = a set of rescaled points (basically the output of the acute_vertex fxn after the scale_features fxn)
    centroid_r = a tuple that contains the rescaled centroid coordinates
    bline_r    = a tuple that contains the rescaled boundary line - centroid coordinates
    label      = optional label parameter, modifies the variable name of observations recorded

    :param points_r: ndarray
    :param centroid_r: tuple
    :param bline_r: tuple
    :param label: str
    """

    params.device += 1
    vert_dist_c = []
    hori_dist_c = []
    euc_dist_c = []
    angles_c = []
    cx, cy = centroid_r
    # Check to see if points are numerical or NA
    if not isinstance(cy, numbers.Number):
        return ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA'), ('NA', 'NA'), \
               ('NA', 'NA'), ('NA', 'NA')
    # Do this for centroid
    for pt in points_r:
        # Get coordinates from point
        x, y = pt
        # Get vertical distance and append to list
        v = y - cy
        vert_dist_c.append(v)

        # Get horizontal distance and append to list
        h = abs(x - cx)
        hori_dist_c.append(h)
        e = np.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))
        # print "Here is the centroid euclidian distance: " + str(h)
        euc_dist_c.append(e)

        a = (h * h + e * e - v * v) / (2 * h * e)

        ang = abs(math.degrees(math.acos(a)))
        if v < 0:
            ang = ang * -1
        # print "Here is the centroid angle: " + str(ang)
        angles_c.append(ang)

    vert_ave_c = np.mean(vert_dist_c)
    hori_ave_c = np.mean(hori_dist_c)
    euc_ave_c = np.mean(euc_dist_c)
    ang_ave_c = np.mean(angles_c)

    vert_dist_b = []
    hori_dist_b = []
    euc_dist_b = []
    angles_b = []
    bx, by = bline_r
    # Do this for baseline
    for pt in points_r:
        # Get coordinates from point
        x, y = pt
        # Get vertical distance and append to list
        v = y - by
        # print "Here is the baseline vertical distance: " + str(v)
        vert_dist_b.append(v)
        # Get horizontal distance and append to list
        h = abs(x - bx)
        hori_dist_b.append(h)
        e = np.sqrt((bx - x) * (bx - x) + (by - y) * (by - y))
        euc_dist_b.append(e)

        a = (h * h + e * e - v * v) / (2 * h * e)

        ang = abs(math.degrees(math.acos(a)))
        if v < 0:
            ang = ang * -1
        angles_b.append(ang)

    vert_ave_b = np.mean(vert_dist_b)
    hori_ave_b = np.mean(hori_dist_b)
    euc_ave_b = np.mean(euc_dist_b)
    ang_ave_b = np.mean(angles_b)

    outputs.add_observation(sample=label, variable='vert_ave_c', trait='average vertical distance from centroid',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=vert_ave_c, label='pixels')
    outputs.add_observation(sample=label, variable='hori_ave_c', trait='average horizontal distance from centeroid',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=hori_ave_c, label='pixels')
    outputs.add_observation(sample=label, variable='euc_ave_c', trait='average euclidean distance from centroid',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=euc_ave_c, label='pixels')
    outputs.add_observation(sample=label, variable='ang_ave_c',
                            trait='average angle between landmark point and centroid',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='degrees', datatype=float,
                            value=ang_ave_c, label='degrees')
    outputs.add_observation(sample=label, variable='vert_ave_b', trait='average vertical distance from baseline',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=vert_ave_b, label='pixels')
    outputs.add_observation(sample=label, variable='hori_ave_b', trait='average horizontal distance from baseline',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=hori_ave_b, label='pixels')
    outputs.add_observation(sample=label, variable='euc_ave_b', trait='average euclidean distance from baseline',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='pixels', datatype=float,
                            value=euc_ave_b, label='pixels')
    outputs.add_observation(sample=label, variable='ang_ave_b',
                            trait='average angle between landmark point and baseline',
                            method='plantcv.plantcv.landmark_reference_pt_dist', scale='degrees', datatype=float,
                            value=ang_ave_b, label='degrees')
