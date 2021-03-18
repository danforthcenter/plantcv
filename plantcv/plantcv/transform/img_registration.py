# Image Registration Based On User Selected Landmark Points

from plantcv import plantcv as pcv
from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl


def _find_closest(pt, pts):
    """ Given coordinates of a point and a list of coordinates of a bunch of points, find the point that has the smallest Euclidean to the given point

    :param pt: (tuple) coordinates of a point
    :param pts: (a list of tuples) coordinates of a list of points
    :return: index of the closest point and the coordinates of that point
    """
    dists = distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]


class ImageRegistrator:
    """
    An interactive tool that takes user selected landmark points to register two images
    """
    def __init__(self, img_ref, img_tar, figsize=(12, 6)):
        self.img_ref = img_ref
        self.img_tar = img_tar

        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        self.axes[0].text(0, -100,
                          'Collect points matching features between images. Select location on reference image then target image. \nPlease first click on the reference image, then on the same point on the target image.\nPlease select at least 4 pairs of points')
        self.axes[0].imshow(img_ref, cmap='jet')
        self.axes[0].set_title('Reference Image')

        self.axes[1].imshow(img_tar)
        self.axes[1].set_title('Target Image')

        # Set useblit=True on most backends for enhanced performance.
        # cursor = Cursor(axes[0], horizOn=True, vertOn=True, useblit=True, color='red', linewidth=2)

        self.points = [[], []]
        self.events = []

        # onclick = functools.partial(_onclick_, fig, axes, array_data, wvs)

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.model = None
        self.img_registered = None

    def left_click(self, idx_ax, x, y):
        self.axes[idx_ax].plot(x, y, 'x', c='red')
        self.points[idx_ax].append((x, y))

    def right_click(self, idx_ax, x, y):
        idx_remove, _ = _find_closest((x, y), self.points[idx_ax])
        # remove the last added point
        # idx_remove = -1
        self.points[idx_ax].pop(idx_remove)
        axplots = self.axes[idx_ax].lines
        self.axes[idx_ax].lines.remove(axplots[idx_remove])

    def onclick(self, event):
        self.events.append(event)

        # collect points on reference image
        if str(event.inaxes._subplotspec) == 'GridSpec(1, 2)[0:1, 0:1]':
            # left click
            if event.button == 1:
                self.left_click(0, event.xdata, event.ydata)
            # right click
            else:
                self.right_click(0, event.xdata, event.ydata)

        # collect points on target image
        elif str(event.inaxes._subplotspec) == 'GridSpec(1, 2)[0:1, 1:2]':
            # left click
            if event.button == 1:
                self.left_click(1, event.xdata, event.ydata)

            # right click
            else:
                self.right_click(1, event.xdata, event.ydata)
        self.fig.canvas.draw()

    def save_model(self, model_file="model"):
        pkl.dump(self.model, open("{}.pkl".format(model_file), "wb"))

    def display_coords(self):
        print("\nCoordinates for selected reference points: ")
        for point_ref in self.points[0]:
            print("\n{}".format(point_ref))
        print("\nCoordinates for selected target points: ")
        for point_tar in self.points[1]:
            print("\n{}".format(point_tar))

    def regist(self):
        # use warp function in plantcv
        self.model, self.img_registered = pcv.transform.warp_align(self.img_tar, self.img_ref, self.points[1], self.points[0], method='ransac')

