# Interactively click and count objects in a given image

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from scipy.spatial import distance
import json

def _find_closest(pt, pts):
    """ Given coordinates of a point and a list of coordinates of a bunch of points, find the point that has the smallest Euclidean to the given point

    :param pt: (tuple) coordinates of a point
    :param pts: (a list of tuples) coordinates of a list of points
    :return: index of the closest point and the coordinates of that point
    """
    if pt in pts:
        return pts.index(pt), pt
    dists = distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]


class ClickCount(object):
    def __init__(self, img, figsize=(12, 6)):
        print("If you have coordinates to import, the label represent for total count should be 'total'!")
        self.img = img
        self.points = {}
        self.colors = {}
        self.count = {}  # a dictionary that saves the counts of different classes (labels)
        self.figsize = figsize
        self.events = []
        self.label = None  # current label
        self.color = None  # current color
        self.view_all = None  # a flag indicating whether or not view all labels
        self.fig = None
        self.ax = None
        self.p_not_current = None

    def import_coords(self, coords, label="total"):
        """ Import center coordinates of already detected objects
        Inputs:
        coords = list of center coordinates of already detected objects.
        label = class label for imported coordinates, by default label="total".

        Returns:
        :param coords: list
        :param label: string
        :return:
        """
        if label not in self.points:
            self.points[label] = []
            for (y, x) in coords:
                self.points[label].append((x, y))
            self.count[label] = len(self.points[label])

        else:
            print(f"Warning: {label} already included and counted, nothing is imported!")

    def save_coords(self, coord_file):
        """Save collected coordinates to a file.
        Input variables:
        coord_file = Name of the file to save collected coordinate
        :param coord_file: str
        """
        # Open the file for writing
        with open(coord_file, "w") as fp:
            # Save the data in JSON format with indentation
            json.dump(obj=self.points, fp=fp, indent=4)

    # def save_counter(self, counter_file):
    #     """Save a counter object to a file
    #     Input variables:
    #     counter_file = Filename to write counter to
    #     :param counter_file: str
    #     """
    #     # Open the file for writing
    #     with open(counter_file, "w") as fp:
    #         # Save the data in JSON format with indentation
    #         json.dump(obj=vars(self), fp=fp, indent=4)
    #
    # def import_counter(self, counter_file):
    #     """Import a counter object from a file
    #     Input variables:
    #     counter_file = Counter file to import
    #     :param counter_file: str
    #     """
    #     # Open the file for reading
    #     with open(counter_file, "r") as fp:
    #         counter = json.load(fp)
    #         for key, value in counter.items():
    #             setattr(self, key, value)

    def view(self, label="total", color="c", view_all=False):
        """
        View the label for a specific class label
        Inputs:
        label = (optional) class label, by default label="total"
        color = desired color, by default color="c"
        view_all = indicator of whether view all classes, by default view_all=False

        :param label: string
        :param color: string
        :param view_all: boolean
        :return:
        """
        if label not in self.points and color in self.colors.values():
                print("Warning: The color assigned to the new class label is already used, "
                      "if proceeding, items from different classes will not be distinguishable in plots!")

        self.label = label
        self.color = color
        self.view_all = view_all

        if label not in self.points:
            self.points[label] = []
            self.count[label] = 0
        self.colors[label] = color

        print("Warning: this tool is under development and is expected to have updates frequently, "
              "please check the documentation page to make sure you are using the correct version!")
        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)

        self.events = []
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        self.ax.set_title("Please left click on missing pollens\n Right click on those you want to remove")
        self.p_not_current = 0
        # if view_all is True, show all already marked markers
        if view_all:
            for k in self.points.keys():
                for (x, y) in self.points[k]:
                    self.ax.plot(x, y, marker='x', c=self.colors[k])
                    if self.label not in self.points or len(self.points[self.label]) == 0:
                        self.p_not_current += 1
        else:
            for (x, y) in self.points[label]:
                self.ax.plot(x, y, marker='x', c=color)

    def onclick(self, event):
        self.events.append(event)
        if event.button == 1:
            self.ax.plot(event.xdata, event.ydata, marker='x', c=self.color)
            self.points[self.label].append((event.xdata, event.ydata))
            self.count[self.label] += 1
        else:
            idx_remove, _ = _find_closest((event.xdata, event.ydata), self.points[self.label])
            self.points[self.label].pop(idx_remove)
            idx_remove = idx_remove + self.p_not_current
            ax0plots = self.ax.lines
            self.ax.lines.remove(ax0plots[idx_remove])
            self.count[self.label] -= 1
        self.fig.canvas.draw()