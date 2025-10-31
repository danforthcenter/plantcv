# PlantCV classes
import cv2
import numpy as np
from plantcv.plantcv.annotate.points import _find_closest_pt
import matplotlib.pyplot as plt
from math import floor


class Spectral_data:
    """PlantCV Hyperspectral data class"""

    def __init__(self, array_data, max_wavelength, min_wavelength, max_value, min_value, d_type, wavelength_dict,
                 samples, lines, interleave, wavelength_units, array_type, pseudo_rgb, filename, default_bands,
                 metadata=None):
        # The actual array/datacube
        self.array_data = array_data
        # Min/max available wavelengths (for spectral datacube)
        self.max_wavelength = max_wavelength
        self.min_wavelength = min_wavelength
        #  Min/max pixel value for single wavelength or index
        self.max_value = max_value
        self.min_value = min_value
        # Numpy data type
        self.d_type = d_type
        # Contains all available wavelengths where keys are wavelength and value are indices
        self.wavelength_dict = wavelength_dict
        # Resolution of a single band of spectral data is (samples, lines) rather than (x,y) with other arrays
        self.samples = samples
        self.lines = lines
        # Interleave type
        self.interleave = interleave
        self.wavelength_units = wavelength_units
        # The type of array data (entire datacube, specific index, first derivative, etc)
        self.array_type = array_type
        # Pseudo-RGB image if the array_type is a datacube
        self.pseudo_rgb = pseudo_rgb
        # The filename where the data originated from
        self.filename = filename
        # The default band indices needed to make an pseudo_rgb image, if not available then store None
        self.default_bands = default_bands
        # Metadata, flexible components in a dictionary
        self.metadata = metadata
        if not metadata:
            self.metadata = {}


class PSII_data:
    """PSII data class"""

    def __init__(self):
        self.ojip_dark = None
        self.ojip_light = None
        self.pam_dark = None
        self.pam_light = None
        self.spectral = None
        self.chlorophyll = None
        self.datapath = None
        self.filename = None

    def __repr__(self):
        mvars = []
        for k, v in self.__dict__.items():
            if v is not None:
                mvars.append(k)
        return "PSII variables defined:\n" + '\n'.join(mvars)

    def add_data(self, protocol):
        """Input:
        protocol: xr.DataArray with name equivalent to initialized attributes
        """
        self.__dict__[protocol.name] = protocol


class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point
    """

    def __init__(self, img, figsize=(12, 6)):
        """
        Initialization
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
        """Handle mouse click events"""
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


class Objects:
    """Class for managing image contours/objects and their hierarchical relationships."""

    def __init__(self, contours: list = None, hierarchy: list = None):
        self.contours = contours
        self.hierarchy = hierarchy
        self._n = 0
        if contours is None:
            self.contours = []
            self.hierarchy = []

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self.contours):
            self._n += 1
            return Objects(contours=[self.contours[self._n-1]], hierarchy=[self.hierarchy[self._n-1]])
        raise StopIteration

    def append(self, contour, h):
        """Append a contour and its hierarchy to the object"""
        self.contours.append(contour)
        self.hierarchy.append(h)

    def save(self, filename):
        """Save the object to a file"""
        np.savez(filename, contours=self.contours, hierarchy=self.hierarchy)

    @staticmethod
    def load(filename):
        """Load a saved object file"""
        file = np.load(filename)
        obj = Objects(file['contours'].tolist(), file['hierarchy'])
        return obj
