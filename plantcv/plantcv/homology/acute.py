# Identify landmark positions within a contour for morphometric analysis

import numpy as np
import math
import cv2
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition


def _get_distance(point1, point2):
    """Helper function for distance between two points"""
    return np.sqrt((point1[0][0]-point2[0][0]) ** 2 + (point1[0][1]-point2[0][1]) ** 2)


def _get_point(obj, k, direction, win):
    """Helper function for getting a point in a contour"""
    vert = obj[k]
    dist_1 = 0
    for i in range(len(obj)):
        idx = k - i if direction == 'reverse' else k + i
        if idx < 0:
            idx += len(obj)
        elif idx >= len(obj):
            idx -= len(obj)
        pos = obj[idx]
        dist_2 = np.sqrt(np.square(pos[0][0] - vert[0][0]) + np.square(pos[0][1] - vert[0][1]))
        if i >= 2:
            if dist_1 < dist_2 <= win:
                dist_1 = dist_2
                point = pos
            elif dist_2 > win:
                break
        else:
            point = pos
    return point


def _calculate_angle(pt_a, vert, pt_b):
    """Calculate angle in degrees using the Law of Cosines"""
    p12 = _get_distance(vert, pt_a)
    p13 = _get_distance(vert, pt_b)
    p23 = _get_distance(pt_a, pt_b)
    dot = (p12 ** 2 + p13 ** 2 - p23 ** 2) / (2 * p12 * p13)
    ang = math.degrees(math.acos(dot))
    return ang


def _get_isle(index, obj, win):
    """
    Find clusters of points with angles below the threshold

    Inputs:
    index       = list of positions of acute links
    obj         = object composition of the contour
    win         = maximum cumulative pixel distance window for calculating angle

    Returns:
    isle        = list of clusters of points with angles below the threshold

    :param index: list
    :param obj: numpy.ndarray
    :param win: int
    :return isle: list
    """
    isle = []
    island = []

    for ind in index:           # Scan for iterative links within index
        if not island:
            island.append(ind)       # Initiate new link island
        elif island[-1]+1 == ind:
            island.append(ind)       # Append successful iteration to island
        elif island[-1]+1 != ind:
            pt_a = obj[ind]
            pt_b = obj[island[-1]+1]
            dist = np.sqrt(np.square(pt_a[0][0]-pt_b[0][0])+np.square(pt_a[0][1]-pt_b[0][1]))
            if win/2 > dist:
                island.append(ind)
            else:
                isle.append(island)
                island = [ind]

    isle.append(island)
    return isle


def _get_internal_pixels(mask, obj, island):
    """
    Get pixel values from the mask that are internal to the island

    Inputs:
    mask        = binary mask used to generate contour array (necessary for ptvals)
    obj         = object composition of the contour
    island      = list of clusters of points with angles below the threshold

    Returns:
    vals        = list of pixel values within the island

    :param mask: numpy.ndarray
    :param obj: numpy.ndarray
    :param island: list
    :return vals: list
    """
    vals = []
    pix_x, pix_y, w, h = cv2.boundingRect(obj[island])  # Obtain local window around island
    for c in range(w):
        for r in range(h):
            # Identify pixels in local window internal to the island hull
            pos = cv2.pointPolygonTest(obj[island], (pix_x+c, pix_y+r), 0)
            if pos > 0:
                vals.append(mask[pix_y+r][pix_x+c])  # Store pixel value if internal
    return vals


def _find_farthest_point(obj, island):
    """Helper function to find the farthest point in the island from the start and end points of the island

    Inputs:
    obj         = object composition of the contour
    island      = list of clusters of points with angles below the threshold

    Returns:
    pt          = farthest point from the start and end points of the island
    max_dist    = list of maximum distances from the start and end points of the island

    :param obj: numpy.ndarray
    :param island: list
    :return pt: int
    :return max_dist: list
    """
    ss = obj[island[0]]            # Store isle "x" start site
    ts = obj[island[-1]]           # Store isle "x" termination site
    dist_1 = 0
    pt = island[0]
    max_dist = []

    for d in island:
        site = obj[[d]]
        ss_d = np.sqrt(np.square(ss[0][0] - site[0][0][0]) + np.square(ss[0][1] - site[0][0][1]))
        ts_d = np.sqrt(np.square(ts[0][0] - site[0][0][0]) + np.square(ts[0][1] - site[0][0][1]))
        dist_2 = np.mean([np.abs(ss_d), np.abs(ts_d)])

        if dist_2 > dist_1:
            pt = d
            dist_1 = dist_2

    return pt, max_dist


def _process_islands_for_landmarks(isle, mask, obj, params_obj):
    """
    Helper function to process islands to find landmark points and average pixel values within the island

    Inputs:
    isle        = list of clusters of points with angles below the threshold
    mask        = binary mask used to generate contour array (necessary for ptvals)
    obj         = object composition of the contour
    params_obj      = plantcv.params object

    Returns:
    maxpts      = list of landmark points
    ss_pts      = list of starting points
    ts_pts      = list of termination points
    ptvals      = list of average pixel values within the island
    max_dist    = list of maximum distances from the start and end points of the island

    :param isle: list
    :param mask: numpy.ndarray
    :param obj: numpy.ndarray
    :param params_obj: plantcv.params
    :return maxpts: list
    :return ss_pts: list
    :return ts_pts: list
    :return ptvals: list
    :return max_dist: list
    """
    maxpts = []
    ss_pts = []
    ts_pts = []
    ptvals = []
    max_dist = [['cont_pos', 'max_dist', 'angle']]
    for island in isle:
        vals = _get_internal_pixels(mask, obj, island)
        if len(vals) > 0:
            ptvals.append(sum(vals)/len(vals))
            vals = []
        else:
            ptvals.append('NaN')        # If no values can be retrieved (small/collapsed contours)
            vals = []
        if len(island) >= 3:               # If landmark is multiple points (distance scan for position)
            if params_obj.debug is not None:
                print('route C')

            pt, max_dist = _find_farthest_point(obj, island)
            if params_obj.debug is not None:
                print(f"Landmark site: {pt}, Start site: {island[0]}, Term. site: {island[-1]}")

            maxpts.append(pt)           # Empty 'pts' prior to next mean distance scan
            ss_pts.append(island[0])
            ts_pts.append(island[-1])

        if params_obj.debug is not None:
            print(f'Landmark point indices: {maxpts}')
            print(f'Starting site indices: {ss_pts}')
            print(f'Termination site indices: {ts_pts}')

    return maxpts, ss_pts, ts_pts, ptvals, max_dist


def acute(img, mask, win, threshold):
    """
    Identify landmark positions within a contour for morphometric analysis

    Inputs:
    img         = Original image used for plotting purposes
    mask        = binary mask used to generate contour array (necessary for ptvals)
    win         = maximum cumulative pixel distance window for calculating angle
                  score; 1 cm in pixels often works well
    threshold   = angle score threshold to be applied for mapping out landmark
                  coordinate clusters within each contour

    Returns:
    homolog_pts = pseudo-landmarks selected from each landmark cluster
    start_pts   = pseudo-landmark island starting position; useful in parsing homolog_pts in downstream analyses
    stop_pts    = pseudo-landmark island end position ; useful in parsing homolog_pts in downstream analyses
    ptvals      = average values of pixel intensity from the mask used to generate cont;
                  useful in parsing homolog_pts in downstream analyses
    chain       = raw angle scores for entire contour, used to visualize landmark
                  clusters
    verbose_out = supplemental file which stores coordinates, distance from
                  landmark cluster edges, and angle score for entire contour.  Used
                  in troubleshooting.

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param win: int
    :param threshold: int
    :return homolog_pts: numpy.ndarray
    :return start_pts: numpy.ndarray
    :return stop_pts: numpy.ndarray
    :return ptvals: list
    :return chain: lsit
    :return verbose_out: list
    """
    # Find contours
    contours, hierarchy = _cv2_findcontours(bin_img=mask)
    obj = _object_composition(contours=contours, hierarchy=hierarchy)

    chain = [_calculate_angle(_get_point(obj, k, 'reverse', win), obj[k], _get_point(obj, k, 'forward', win))
             for k in range(len(obj))]

    index = []                      # Index chain to find clusters below angle threshold

    for c, link in enumerate(chain):     # Identify links in chain with acute angles
        if float(link) <= threshold:
            index.append(c)         # Append positions of acute links to index

    if len(index) == 0:
        return [], [], [], [], [], []

    isle = _get_isle(index, obj, win)  # Find clusters of points with angles below the threshold

    if len(isle) > 1:
        if (isle[0][0] == 0) & (isle[-1][-1] == (len(chain)-1)):
            if params.debug is not None:
                print('Fusing contour edges')
            island = isle[-1]+isle[0]  # Fuse overlapping ends of contour
            # Delete islands to be spliced if start-end fusion required
            del isle[0]
            del isle[-1]
            isle.insert(0, island)      # Prepend island to isle
    else:
        if params.debug is not None:
            print('Microcontour...')

    maxpts, ss_pts, ts_pts, ptvals, max_dist = _process_islands_for_landmarks(isle, mask, obj, params)

    homolog_pts = obj[maxpts]
    start_pts = obj[ss_pts]
    stop_pts = obj[ts_pts]

    ori_img = np.copy(img)
    # Convert grayscale images to color
    if len(np.shape(ori_img)) == 2:
        ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    # Draw acute points on the original image
    cv2.drawContours(ori_img, homolog_pts, -1, (255, 255, 255), params.line_thickness)
    # print/plot debug image
    _debug(visual=ori_img, filename=f"{params.device}_acute_plms.png")

    return homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist
