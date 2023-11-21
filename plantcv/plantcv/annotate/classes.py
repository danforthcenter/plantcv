"""Annotation classes."""
import cv2
import json
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from scipy.spatial import distance
from plantcv.plantcv import warn, floodfill, _debug, params, visualize.colorize_label_img 



# Class helpers
def _find_closest_pt(pt, pts):
    """Find the closest (Euclidean) point to a given point from a list of points.

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

def _recover_circ(bin_img, c):
    """function to recover circular objects"""
    # Generates a binary image of a disc based on the coordinates c
    # and the surrounding white pixels in bin_img
    # make bin_img 1-0
    bin_img = 1*(bin_img != 0)
    h, w = bin_img.shape
    # coordinates of pixels in the shape of the bin_image
    X, Y = np.meshgrid(np.linspace(0, w-1, w), np.linspace(0, h-1, h))

    # Alternate two steps:
    # 1 - growing the disc centered in c until it overlaps with black pixels in bin_img.
    # 2 - move c a step of at least one pixel towards the center of mass (mean of coordinate values)
    # of the white pixels of bin_img that overlap with the disc.
    # It terminates when the direction of the step in both axis has changed once.
    # radius
    r = 0
    # sum of previous directions
    dir_x_hist = 0
    dir_y_hist = 0
    # flags indicate if there has been a change in direction in each axis
    chg_dir_x = False
    chg_dir_y = False

    while (chg_dir_x and chg_dir_y) is False:
        # image of concentric circles centered in c
        circ = np.sqrt((X-c[1])**2+(Y-c[0])**2)
        # growing radius until it reaches black pixels
        inside = True
        while inside is True:
            circ_mask = 1*(circ < r)
            circ_mask_area = np.sum(circ_mask)
            masked_circ = bin_img*circ_mask
            # if masked_circ has a smaller count it means the circle is
            # overlapping black pixels -> no longer inside the white part
            if np.abs(np.sum(masked_circ) - circ_mask_area) > 100:
                inside = False
            else:
                r += 1
        # moving center towards the center of mass
        Cx = np.mean(X[masked_circ == 1])
        Cy = np.mean(Y[masked_circ == 1])

        dir_x = np.sign(Cx - c[1])
        dir_y = np.sign(Cy - c[0])

        stepx = dir_x*np.ceil(np.abs(Cx - c[1]))
        stepy = dir_y*np.ceil(np.abs(Cy - c[0]))

        dir_x_hist += dir_x
        dir_y_hist += dir_y
        # register that a change in direction has occurred to terminate when
        # is has happened in both directions
        if np.sign(dir_x_hist) != dir_x or dir_x == 0:
            chg_dir_x = True

        if np.sign(dir_y_hist) != dir_y or dir_y == 0:
            chg_dir_y = True

        c[1] += stepx.astype(np.int32)
        c[0] += stepy.astype(np.int32)

    circ_mask = 1*(circ < r)
    masked_circ = (bin_img*circ_mask).astype(np.uint8)
    masked_circ[c[0], c[1]] = 1  # center of mass always part of the mask

    return masked_circ, c

def _clickcount_labels(self):
    """Function to get label names"""
    labels = list(self.count)

    return labels

def _remove_points(autolist, confirmedlist):
    """Function to remove points if interactively removed by user"""
    # internal function to remove to remove points specified by a user
    removecoor = []

    for element in autolist:
        if element not in confirmedlist:
            removecoor.append(element)

    return removecoor


class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point
    """

    def __init__(self, img, figsize=(12, 6)):
        """Initialization
        :param img: image data
        :param figsize: desired figure size, (12,6) by default
        :attribute points: list of points as (x,y) coordinates tuples
        """
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        self.points = []
        self.events = []

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        """Handle mouse click events."""
        self.events.append(event)
        if event.button == 1:

            self.ax.plot(event.xdata, event.ydata, 'x', c='red')
            self.points.append((floor(event.xdata), floor(event.ydata)))

        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.points)
            # remove the closest point to the user right clicked one
            self.points.pop(idx_remove)
            self.ax.lines[idx_remove].remove()
        self.fig.canvas.draw()


class ClickCount:
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
        """Import center coordinates of already detected objects
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
            warn(f"{label} already included and counted, nothing is imported!")

    def file_import(self, filename):
        """
        Method to import ClickCount coordinate file to ClickCount object
        
        Inputs:
        filename = filename of stored coordinates and classes

        :param filename: ndarray
        :return: 
        """
        # img - img file to initialize ClickCount class
        # coor_file - file of coordinates and classes
        coords = open(filename, "r")
        coords = json.load(coords)

        keys = list(coords.keys())

        for key in keys:
            keycoor = coords[key]
            keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
            self.import_coords(keycoor, label=key)

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
            warn("The color assigned to the new class label is already used, if proceeding, "
                 "items from different classes will not be distinguishable in plots!")

        self.label = label
        self.color = color
        self.view_all = view_all

        if label not in self.points:
            self.points[label] = []
            self.count[label] = 0
        self.colors[label] = color

        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)

        self.events = []
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        self.ax.set_title("Please left click on missing objects\n Right click on those you want to remove")
        self.p_not_current = 0
        # if view_all is True, show all already marked markers
        if view_all:
            for k in self.points:
                for (x, y) in self.points[k]:
                    self.ax.plot(x, y, marker='x', c=self.colors[k])
                    if self.label not in self.points or len(self.points[self.label]) == 0:
                        self.p_not_current += 1
        else:
            for (x, y) in self.points[label]:
                self.ax.plot(x, y, marker='x', c=color)

    def onclick(self, event):
        """Handle mouse click events."""
        self.events.append(event)
        if event.button == 1:
            self.ax.plot(event.xdata, event.ydata, marker='x', c=self.color)
            self.points[self.label].append((floor(event.xdata), floor(event.ydata)))
            self.count[self.label] += 1
        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.points[self.label])
            self.points[self.label].pop(idx_remove)
            idx_remove = idx_remove + self.p_not_current
            self.ax.lines[idx_remove].remove()
            self.count[self.label] -= 1
        self.fig.canvas.draw()

    def correct(self, bin_img, bin_img_recover, coords):
        """
        Method to correct ClickCount object instance by removing or recovering points
        
        Inputs:
        bin_img = binary image, image with selected objects
        bin_img_recover = binary image, image with all potential objects
        coords = coordinates of 'auto' detected points (coordinate output of detect_discs)

        :param bin_img: ndarray
        :param bin_img_recover = ndarray
        :param coords = list
        :return completed_mask: ndarray
        :return self: plantcv.plantcv.classes.ClickCount
        """

        debug = params.debug
        params.debug = None

        labelnames = _clickcount_labels(self)

        completed_mask = np.copy(bin_img)

        totalcoor = []

        for names in labelnames:
            for i, (x, y) in enumerate(self.points[names]):
                x = int(x)
                y = int(y)
                totalcoor.append((y, x))

        removecoor = _remove_points(coords, totalcoor)
        removecoor = list(map(lambda sub: (sub[1], sub[0]), removecoor))
        completed_mask = floodfill(completed_mask, removecoor, 0)

        # points in class used for recovering and labeling
        for names in labelnames:
            for i, (x, y) in enumerate(self.points[names]):
                x = int(x)
                y = int(y)
                # corrected coordinates
                self.points[names][i] = (x, y)
                # if the coordinates point to 0 in the binary image, recover the grain and coordinates of center
                if completed_mask[y, x] == 1 or completed_mask[y, x] == 0:
                    print(f"Recovering grain at coordinates: x = {x}, y = {y}")
                    masked_circ, [a, b] = _recover_circ(bin_img_recover, [y, x])
                    completed_mask = completed_mask + masked_circ
                    self.points[names][i] = (b, a)

        completed_mask1 = 1*((completed_mask + 1*(completed_mask == 255)) != 0).astype(np.uint8)

        params.debug = debug

        _debug(visual=completed_mask1, filename=os.path.join(params.debug_outdir, f"{params.device}_clickcount-corrected.png"))

        return completed_mask, self

    def label(self, gray_img, label='default'):
        """
        Saves out ClickCount labeled category count to Outputs 
        
        Inputs:
        gray_img = gray image with objects labeled (e.g.watershed output)
        label = label parameter, modifies the variable name of
        observations recorded (defaults to label="default") 

        Outputs:
        corrected_label = labeled object image
        corrected_class = labeled class image
        corrected_name = ordered list of names
        num = number of objects 

        :param gray_img: ndarray
        :label = str, list
        :return corrected_label = ndarray
        :return corrected_class = ndarray
        :return corrected_name = list
        :return num: int
        """

        debug = params.debug
        params.debug = None

        labelnames = _clickcount_labels(self)

        dict_class_labels = {}

        for i, x in enumerate(labelnames):
            dict_class_labels[x] = i+1

        shape = np.shape(gray_img)
        class_label = np.zeros((shape[0], shape[1]), dtype=np.uint8)

        class_number = []
        class_name = []

        # Only keep watersed results that overlap with a clickpoint and do not ==0
        for cl in list(dict_class_labels.keys()):
            for (y, x) in self.points[cl]:
                x = int(x)
                y = int(y)
                seg_label = gray_img[x, y]
                if seg_label != 0:
                    class_number.append(seg_label)
                    class_name.append(cl)
                    class_label[gray_img == seg_label] = seg_label

        # Get corrected name
        corrected_number = []
        corrected_name = []

        for i, x in enumerate(class_number):
            if x in corrected_number:
                ind = (corrected_number.index(x))
                y = corrected_name[ind]+"_"+str(class_name[i])
                corrected_name[ind] = y
            else:
                corrected_number.append(x)
                y = str(class_name[i])
                corrected_name.append(y)

        classes = np.unique(corrected_name)
        class_dict = {}
        count_class_dict = {}

        for i, x in enumerate(classes):
            class_dict[x] = i+1
            count_class_dict[x] = corrected_name.count(x)

        corrected_label = np.zeros((shape[0], shape[1]))
        corrected_class = np.zeros((shape[0], shape[1]))

        for i, value in enumerate(corrected_number):
            if value != 0:
                corrected_label[gray_img == value] = i+1
                corrected_class[gray_img == value] = class_dict[corrected_name[i]]
                corrected_name[i] = str(i+1)+"_"+corrected_name[i]

        num = len(corrected_name)

        vis_labeled = colorize_label_img(corrected_label)
        vis_class = colorize_label_img(corrected_class)

        params.debug = debug
        _debug(visual=vis_labeled,
            filename=os.path.join(params.debug_outdir, str(params.device) + '_corrected__labels_img.png'))
        _debug(visual=vis_class,
            filename=os.path.join(params.debug_outdir, str(params.device) + '_corrected_class.png'))

        for i, x in enumerate(count_class_dict.keys()):
            variable = x
            value = count_class_dict[x]
            outputs.add_observation(sample=label, variable=variable,
                                    trait='count of category',
                                    method='count', scale='count', datatype=int,
                                    value=value, label=variable)

        return corrected_label, corrected_class, corrected_name, num

