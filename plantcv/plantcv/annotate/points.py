# Point/vertice annotation tool(s)

import numpy as np
from scipy.spatial import distance

## INTERACTIVE ROI TOOLS ##


def _find_closest_pt(pt, pts):
    """ Given coordinates of a point and a list of coordinates of a bunch of points, find the point that has the
    smallest Euclidean to the given point

    :param pt: (tuple) coordinates of a point
    :param pts: (a list of tuples) coordinates of a list of points
    :return: index of the closest point and the coordinates of that point
    """
    if pt in pts:
        idx = pts.index(pt)
        return idx, pt

    dists = distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]
