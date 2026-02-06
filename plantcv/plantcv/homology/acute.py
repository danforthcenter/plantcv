# Identify landmark positions within a contour for morphometric analysis

import numpy as np
import math
import cv2
from plantcv.plantcv import params, outputs
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours, _object_composition


def acute(img, mask, win, threshold, label=None):
    """
    Identify landmark positions within a contour for morphometric analysis.

    Parameters
    ----------
    img : numpy.ndarray
        Original image used for plotting purposes
    mask : numpy.ndarray
        Binary mask used to generate contour array (necessary for ptvals)
    win : int
        Maximum cumulative pixel distance window for calculating angle score; 1 cm in pixels often works well
    threshold : int
        Angle score threshold to be applied for mapping out landmark coordinate clusters within each contour
    label : str or None, optional
        Optional label parameter, modifies the variable name of
        observations recorded, (default = pcv.params.sample_label)

    Returns
    -------
    homolog_pts : list
        List of pseudo-landmark coordinates (x,y) for each landmark cluster
    start_pts : list
        List of pseudo-landmark island starting coordinates (x,y)
    stop_pts : list
        List of pseudo-landmark island ending coordinates (x,y)
    ptvals : list
        List of mean pixel values underlying each landmark cluster
    chain : list
        List of angle scores for each contour point
    max_dist : list
        List of maximum distances for each contour point
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    # initialize returns
    homolog_pts = []
    start_pts = []
    stop_pts = []
    ptvals = []
    max_dist = []
    num_acute_pts = 0
    # Find contours
    contours, hierarchy = _cv2_findcontours(bin_img=mask)
    obj = _object_composition(contours=contours, hierarchy=hierarchy)
    # make list of angles in obj limited by window
    chain = _angle_chain(obj, win)
    index = []
    for c, link in enumerate(chain):
        if float(link) <= threshold:
            index.append(c)

    if len(index) != 0:
        # find islands from acute angles
        isle = _find_islands(obj, index, chain, win)
        # get relevant points from acute islands
        homolog_pts, start_pts, stop_pts, ptvals = _process_islands(obj, isle, chain, mask)
        num_acute_pts = len(homolog_pts)
        ori_img = np.copy(img)
        # Convert grayscale images to color
        if len(np.shape(ori_img)) == 2:
            ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
        # Draw acute points on the original image
        cv2.drawContours(ori_img, homolog_pts, -1, (255, 255, 255), params.line_thickness)
        # print/plot debug image
        _debug(visual=ori_img, filename=f"{params.device}_acute_plms.png")
    # add to outputs and return values for troubleshooting or downstream steps
    outputs.add_observation(sample=label, variable='num_acute_pts', trait='number of acute points',
                            method='plantcv.plantcv.homology.acute', scale='none', datatype=int,
                            value=num_acute_pts, label='none')
    return homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist


def _angle_chain(obj, win):
    """
    Creates a list of angles to be used in detecting acute angles.

    Parameters
    ----------
    obj : plantcv.Objects
        Contours and hierarchy of objects
    win : int
        Maximum cumulative pixel distance window for calculating angle score

    Returns
    -------
    chain : list
        List of angles for each contour point
    """
    # initialize chain list
    chain = []
    # assign 3 points, coordinate by coordinate
    for k in list(range(len(obj))):
        # first point, vert
        vert = obj[k]
        # initial distance is 0, there is only 1 point
        dist_1 = 0
        # loop over points to use with vert, starting by looking backwards for second point (A)
        for r in range(len(obj)):
            rev = k - r
            # get next point of the 3
            pos = obj[rev]
            dist_2 = np.sqrt(np.square(pos[0][0] - vert[0][0]) + np.square(pos[0][1] - vert[0][1]))
            if r >= 2:
                if (dist_2 > dist_1) & (dist_2 <= win):  # Further from vertex than current pt A while within window
                    dist_1 = dist_2
                    pt_a = pos
                elif dist_2 > win:
                    break
            else:
                pt_a = pos
        dist_1 = 0
        # find third point (B), looking forward
        for f in range(len(obj)):
            fwd = k + f
            if fwd >= len(obj):
                fwd -= len(obj)
            pos = obj[fwd]
            dist_2 = np.sqrt(np.square(pos[0][0] - vert[0][0]) + np.square(pos[0][1] - vert[0][1]))
            if f >= 2:
                if (dist_2 > dist_1) & (dist_2 <= win):
                    dist_1 = dist_2
                    pt_b = pos
                elif dist_2 > win:
                    break
            else:
                pt_b = pos

        # Angle in radians derived from Law of Cosines, converted to degrees
        p12 = np.sqrt((vert[0][0]-pt_a[0][0])*(vert[0][0]-pt_a[0][0])+(vert[0][1]-pt_a[0][1])*(vert[0][1]-pt_a[0][1]))
        p13 = np.sqrt((vert[0][0]-pt_b[0][0])*(vert[0][0]-pt_b[0][0])+(vert[0][1]-pt_b[0][1])*(vert[0][1]-pt_b[0][1]))
        p23 = np.sqrt((pt_a[0][0]-pt_b[0][0])*(pt_a[0][0]-pt_b[0][0])+(pt_a[0][1]-pt_b[0][1])*(pt_a[0][1]-pt_b[0][1]))
        dot = (p12*p12 + p13*p13 - p23*p23)/(2*p12*p13)

        ang = math.degrees(math.acos(dot))
        chain.append(ang)
    return chain


def _find_islands(obj, index, chain, win):
    """
    Find islands of acute angles from list of angles.

    Parameters
    ----------
    obj : plantcv.Objects
        Contours and hierarchy of binary mask.
    index : list
        Angles found from contours of mask.
    chain : list
        Angle scores for each contour.
    win : int
        Maximum cumulative pixel distance window for calculating angle score.

    Returns
    -------
    isle : list
        List of islands around acute angles.
    """
    isle = []
    island = []
    # for every acute angle
    for ind in index:
        if not island:
            island.append(ind)
        # if (last element of island) + 1 is this entry, append the entry as is
        elif island[-1] + 1 == ind:
            island.append(ind)
        else:
            pt_a = obj[ind]
            pt_b = obj[island[-1] + 1]
            dist = np.sqrt(np.square(pt_a[0][0] - pt_b[0][0]) + np.square(pt_a[0][1] - pt_b[0][1]))
            if win / 2 > dist:
                island.append(ind)
            else:
                isle.append(island)
                island = [ind]

    isle.append(island)

    if (len(isle) > 1) & (isle[0][0] == 0) & (isle[-1][-1] == (len(chain)-1)):
        island = isle[-1] + isle[0]  # Fuse overlapping ends of contour
        # Delete islands to be spliced if start-end fusion required
        del isle[0]
        del isle[-1]
        isle.insert(0, island)

    return isle


def _process_islands(obj, isle, chain, mask):
    """
    Process list of islands into start/landmark/termination sites.

    Parameters
    ----------
    obj : plantcv.Objects
        Contours and hierarchy of binary mask.
    isle : list
        List of islands around acute angles.
    chain : list
        Angle scores for each contour.
    mask : numpy.ndarray
        Binary mask used to generate contour array.

    Returns
    -------
    homolog_pts : list
        Pseudo-landmarks from each landmark cluster.
    start_pts : list
        Pseudo-landmark island starting position.
    stop_pts : list
        Pseudo-landmark island end position.
    pt_vals  : list
        Point values
    """
    # Initialize empty lists for homologous point max distance method
    maxpts = []
    ss_pts = []
    ts_pts = []
    ptvals = []
    max_dist = [['cont_pos', 'max_dist', 'angle']]
    vals = []
    for island in isle:
        # Identify if contour is concavity/convexity using image mask
        pix_x, pix_y, w, h = cv2.boundingRect(obj[island])  # Obtain local window around island
        for c in range(w):
            for r in range(h):
                # Identify pixels in local window internal to the island hull
                pos = cv2.pointPolygonTest(obj[island], (pix_x + c, pix_y + r), 0)
                if pos > 0:
                    vals.append(mask[pix_y + r][pix_x + c])  # Store pixel value if internal
        if len(vals) > 0:
            ptvals.append(sum(vals) / len(vals))
            vals = []
        else:
            ptvals.append('NaN')
            vals = []
        if len(island) >= 3:               # If landmark is multiple points (distance scan for position)
            ss = obj[island[0]]            # Store isle "x" start site
            ts = obj[island[-1]]           # Store isle "x" termination site
            dist_1 = 0
            for d in island:   # Scan from ss to ts within isle "x"
                site = obj[[d]]
                ss_d = np.sqrt(np.square(ss[0][0] - site[0][0][0]) + np.square(ss[0][1] - site[0][0][1]))
                ts_d = np.sqrt(np.square(ts[0][0] - site[0][0][0]) + np.square(ts[0][1] - site[0][0][1]))
                # Current mean distance of 'd' to 'ss' & 'ts'
                dist_2 = np.mean([np.abs(ss_d), np.abs(ts_d)])
                max_dist.append([d, dist_2, chain[d]])
                if dist_2 > dist_1:                          # Current mean distance better fit that previous best?
                    pt = d
                    dist_1 = dist_2                          # Current mean becomes new best mean
            # print pt
            if params.verbose:
                print(f"Landmark site: {pt}, Start site: {island[0]}, Term. site: {island[-1]}")

            maxpts.append(pt)           # Empty 'pts' prior to next mean distance scan
            ss_pts.append(island[0])
            ts_pts.append(island[-1])

        if params.verbose:
            print(f'Landmark point indices: {maxpts}')
            print(f'Starting site indices: {ss_pts}')
            print(f'Termination site indices: {ts_pts}')
    homolog_pts = obj[maxpts]
    start_pts = obj[ss_pts]
    stop_pts = obj[ts_pts]

    return homolog_pts, start_pts, stop_pts, ptvals
