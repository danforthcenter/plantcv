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

    with open(headername, "r") as f:
        # Replace characters for easier parsing
        hdata = f.read()
        hdata = hdata.replace("\n,", ",")
        hdata = hdata.replace("{\n", "{")
        hdata = hdata.replace("\n}", "}")
        hdata = hdata.replace(";", "")

    # Loop through and create a dictionary from the header file
    for i, string in enumerate(hdata):
        if '=' in string:
            header_data = hdata[i].split(" = ")
            header_dict.update({header_data[0]: header_data[1].rstrip()})
        elif ':' in string:
            header_data = header_data[i].split(" : ")
            header_dict.update({header_data[0] : header_data[1].rstrip()})

    bands = header_dict["bands"]
    wavelengths = header_dict["wavelength"]

    array_data = raw_data.reshape(header_dict["lines"],
                                  header_dict["bands"],
                                  header_dict["samples"]).transpose((0, 2, 1))

    return array_data, header_dict