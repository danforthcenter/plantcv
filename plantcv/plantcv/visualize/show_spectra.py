# Show spectral or spectra of mouse selected pixel(s) for a given hyperspectral image

from scipy.spatial import distance
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Slider
import cv2


def _find_closest(pt, pts):
    """ Given coordinates of a point and a list of coordinates of a bunch of points, find the point that has the smallest Euclidean to the given point

    :param pt: (tuple) coordinates of a point
    :param pts: (a list of tuples) coordinates of a list of points
    :return: index of the closest point and the coordinates of that point
    """
    if pt in pts:
        return pt
    dists = distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]


class ShowSpectra(object):
    """
    An interactive visualization tool that shows spectral (spectra) for selected pixel(s).
    """

    def __init__(self, spectral_data, figsize=(12, 8)):
        """
        Initialization
        :param spectral_data: hyperspectral image data
        :param figsize: desired figure size, (12,8) by default
        """
        print("Warning: this tool is under development and is expected to have updates frequently, please check the documentation page to make sure you are using the correct version!")

        # initialize the pseudocolor rgb data (convert from BGR to RGB)
        self.pseudo_rgb = cv2.cvtColor(spectral_data.pseudo_rgb, cv2.COLOR_BGR2RGB)

        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        self.axes[0].imshow(self.pseudo_rgb)
        self.axes[0].set_title("Please click on interested pixels\n Right click to remove")

        self.axes[1].set_xlabel("wavelength (nm)")
        self.axes[1].set_ylabel("reflectance")
        self.axes[1].set_title("Spectra")
        self.axes[1].set_ylim([0, 1])

        # adjust the main plot to make room for the sliders
        plt.subplots_adjust(left=0.25, bottom=0.25)

        # make a horizontal slider to control the radius
        axradius = self.fig.add_axes([0.15, 0.035, 0.3, 0.035], facecolor='lightgoldenrodyellow')  # [left, bottom, width, height]
        self.radius_slider = Slider(
            ax=axradius,
            label="radius",
            valmin=0,
            valmax=500,
            valinit=1,
            orientation="horizontal"
        )

        # Set useblit=True on most backends for enhanced performance.
        # cursor = Cursor(axes[0], horizOn=True, vertOn=True, useblit=True, color='red', linewidth=2)

        self.points = []
        self.spectra = []
        self.events = []

        self.array_data = spectral_data.array_data
        self.wvs = [k for k in spectral_data.wavelength_dict.keys()]

        self.spectral_std = None
        self.spectral_mean = None

        # initialize radius
        self.r = 0
        self.x = None
        self.y = None
        self.rectangle = None

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.radius_slider.on_changed(self.update)

    def spectra_roi(self):
        """Pull out the spectra inside a square ROI
        """
        r = int(self.r)
        y = int(self.y)
        x = int(self.x)
        kernel_ = np.ones((2 * r + 1, 2 * r + 1)) / (4 * r * r + 4 * r + 1)

        square = self.array_data[(y - r):(y + r + 1), (x - r):(x + r + 1), :]

        num_bands = square.shape[2]

        kernel = np.repeat(kernel_[:, :, np.newaxis], num_bands, axis=2)

        multiplied = np.multiply(square, kernel)
        multiplied_spectra = np.reshape(multiplied, (-1, num_bands))

        self.spectral_mean = multiplied_spectra.sum(axis=0)
        self.spectral_std = multiplied_spectra.std(axis=0)
        # only prepare the patch for plotting if r>1 (not only one pixel, but a square of pixels)
        if r > 0:
            self.rectangle = patches.Rectangle((x - r, y - r), 2 * r, 2 * r, edgecolor="red", fill=False)

    def onclick(self, event):
        self.events.append(event)
        if str(event.inaxes._subplotspec) == 'GridSpec(1, 2)[0:1, 0:1]':
            if event.button == 1:
                self.x, self.y = event.xdata, event.ydata
                self.axes[0].plot(event.xdata, event.ydata, 'x', c='red')
                self.spectra_roi()
                if self.r > 1:
                    self.axes[0].add_patch(self.rectangle)

                self.axes[1].errorbar(self.wvs, self.spectral_mean, xerr=self.spectral_std / 2)
                self.points.append((event.xdata, event.ydata))
            else:
                idx_remove, _ = _find_closest((event.xdata, event.ydata), self.points)
                # remove the last added point
                # idx_remove = -1

                # remove the closest point to the user right clicked one
                self.points.pop(idx_remove)
                if len(self.points) > 0:
                    self.x, self.y = self.points[-1]
                ax0plots = self.axes[0].lines
                ax0patches = self.axes[0].patches
                ax1plots = self.axes[1].lines
                self.axes[0].lines.remove(ax0plots[idx_remove])
                if len(ax0patches) > 0:
                    self.axes[0].patches.remove(ax0patches[idx_remove])
                self.axes[1].lines.remove(ax1plots[idx_remove])
        self.fig.canvas.draw()

    def update(self, val):
        self.r = self.radius_slider.val
        self.spectra_roi()

        # remove old plots
        idx_remove = -1
        ax0patches = self.axes[0].patches
        if len(ax0patches) > 0:
            self.axes[0].patches.remove(ax0patches[idx_remove])
        ax1plots = self.axes[1].lines
        self.axes[1].lines.remove(ax1plots[idx_remove])

        # add new plots
        self.axes[0].add_patch(self.rectangle)
        self.axes[1].errorbar(self.wvs, self.spectral_mean, xerr=self.spectral_std / 2)
        self.fig.canvas.draw_idle()
