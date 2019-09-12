# Read in a hyperspectral data cube as an array and parse metadata from the header file

from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Outputs
import numpy as np
import os


def read_data(filename):
    """Read hyperspectral image data from file.

        Inputs:
        filename = name of image file

        Returns:
        raw_data    = image object as numpy array
        bands       = number of bands
        wavelengths = list of wavelengths

        :param filename: str
        :param mode: str
        :return img: numpy.ndarray
        :return bands: ing
        :return wavelengths: list
        """
    # Initialize dictionary
    header_dict = {}

    raw_data = np.fromfile(filename, np.float32, -1)

    headername = filename + ".hdr"
    header = open(headername)

    # Loop through and create a dictonary from the header file
    for i, string in enumerate(header):
        if '=' in string:
            header_data = header[i].split(" = ")
            header_dict.update({header_data[0]: header_data[1].rstrip()})

    bands = header_dict["bands"]

    return raw_data, bands