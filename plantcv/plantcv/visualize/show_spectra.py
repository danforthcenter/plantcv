# Show spectral or spectra of mouse selected pixel(s) for a given hyperspectral image

from scipy.spatial import distance
import numpy as np


def _find_closest(pt, pts):
    """ Given coordinates of a point and a list of coordinates of a bunch of points, find the point that has the smallest Euclidean to the given point

    :param pt: (tuple) coordinates of a point
    :param pts: (a list of tuples) coordinates of a list of points
    :return: index of the closest point and the coordinates of that point
    """
    if pt in pts:
        return pt
    dists =	distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]


class ShowSpectra(object):
    """
    An interactive visualization tool that shows spectral (spectra) for selected pixel(s).
    """

    def __init__(self, spectral_data, figsize=(12,6)):
        """
        Initialization
        :param spectral_data: hyperspectral image data
        :param figsize: desired figure size, (12,6) by default
        """
        print("Warning: this tool is under development and is expected to have updates frequently, please check the documentation page to make sure you are using the correct version!")
        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        self.axes[0].imshow(array.pseudo_rgb)
        self.axes[0].set_title("Please click on interested pixels\n Right click for removal")

        self.axes[1].set_xlabel("wavelength (nm)")
        self.axes[1].set_ylabel("reflectance")
        self.axes[1].set_title("Spectra")
        self.axes[1].set_ylim([0, 1])

        # Set useblit=True on most backends for enhanced performance.
        # cursor = Cursor(axes[0], horizOn=True, vertOn=True, useblit=True, color='red', linewidth=2)

        self.points  = []
        self.spectra = []
        self.events  = []

        self.array_data = spectral_data.array_data
        self.wvs = [k for k in spectral_data.wavelength_dict.keys()]


        # onclick = functools.partial(_onclick_, fig, axes, array_data, wvs)

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)


    def onclick(self, event):
        self.events.append(event)
        if event.button == 1:

            self.axes[0].plot(event.xdata, event.ydata, 'x', c='red')
            spectral = self.array_data[int(event.ydata), int(event.xdata), :]
            self.spectra.append(spectral)
            self.axes[1].plot(self.wvs, spectral)
            self.points.append((event.xdata, event.ydata))

        else:
            idx_remove, _ = _find_closest((event.xdata, event.ydata), self.points)
            # remove the last added point
            # idx_remove = -1

            # remove the closest point to the user right clicked one
            self.points.pop(idx_remove)
            ax0plots = self.axes[0].lines
            ax1plots = self.axes[1].lines
            self.axes[0].lines.remove(ax0plots[idx_remove])
            self.axes[1].lines.remove(ax1plots[idx_remove])
        self.fig.canvas.draw()