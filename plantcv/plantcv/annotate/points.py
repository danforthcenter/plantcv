# Point/vertice annotation tool(s)

import cv2
import numpy as np
from math import floor
from scipy.spatial import distance
import matplotlib.pyplot as plt

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
    dists =	distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]


class Points(object):
    """
    Draw polygon
    """

    def __init__(self, img, figsize=(12, 6)):
        """
        Initialization
        :param img: image data
        :param figsize: desired figure size, (12,6) by default
        """

        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        self.points = []
        self.events = []

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        self.events.append(event)
        if event.button == 1:

            self.ax.plot(event.xdata, event.ydata, 'x', c='red')
            self.points.append((floor(event.xdata), floor(event.ydata)))

        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.points)
            # remove the closest point to the user right clicked one
            self.points.pop(idx_remove)
            ax0plots = self.ax.lines
            self.ax.lines.remove(ax0plots[idx_remove])
        self.fig.canvas.draw()


