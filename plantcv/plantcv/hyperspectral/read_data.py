# Read in a hyperspectral data cube as an array and parse metadata from the header file

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import Spectral_data


def _find_closest(A, target):
    # A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A) - 1)
    left = A[idx - 1]
    right = A[idx]
    idx -= target - left < right - target
    return idx


def read_data(filename):
    """Read hyperspectral image data from file.

        Inputs:
        filename = name of image file

        Returns:
        array_data    = image object as numpy array
        header_dict   = dictionary with metadata from the header file

        :param filename: str
        :return array_data: numpy.ndarray
        """
    # Initialize dictionary
    header_dict = {}

    raw_data = np.fromfile(filename, np.float32, -1)

    headername = filename + ".hdr"

    with open(headername, "r") as f:
        # Replace characters for easier parsing
        hdata = f.read()
        hdata = hdata.replace(",\n", ",")
        hdata = hdata.replace("\n,", ",")
        hdata = hdata.replace("{\n", "{")
        hdata = hdata.replace("\n}", "}")
        hdata = hdata.replace(" \n ", "")
        hdata = hdata.replace(";", "")
    hdata = hdata.split("\n")

    # Loop through and create a dictionary from the header file
    for i, string in enumerate(hdata):
        if ' = ' in string:
            header_data = string.split(" = ")
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ' : ' in string:
            header_data = string.split(" : ")
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Reshape the raw data into a datacube array
    array_data = raw_data.reshape(int(header_dict["lines"]),
                                  int(header_dict["bands"]),
                                  int(header_dict["samples"])).transpose((0, 2, 1))

    # Reformat wavelengths
    header_dict["wavelength"] = header_dict["wavelength"].replace("{", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace("}", "")
    header_dict["wavelength"] = header_dict["wavelength"].split(",")

    # Create dictionary of wavelengths
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({wavelength: j})

    # Replace datatype ID number with the numpy datatype
    dtype_dict = {"1": np.uint8, "2": np.int16, "3": np.int32, "4": np.float32, "5": np.float64, "6": np.complex64,
                  "9": np.complex128, "12": np.uint16, "13": np.uint32, "14": np.uint64, "15": np.uint64}
    header_dict["data type"] = dtype_dict[header_dict["data type"]]

    if "default bands" in header_dict:
        header_dict["default bands"] = header_dict["default bands"].replace("{", "")
        header_dict["default bands"] = header_dict["default bands"].replace("}", "")
        default_bands = header_dict["default bands"].split(",")

        pseudo_rgb = cv2.merge((array_data[:, :, int(default_bands[0])],
                                array_data[:, :, int(default_bands[1])],
                                array_data[:, :, int(default_bands[2])]))
    else:
        try:
            max_wavelength = max([float(i.rstrip()) for i in wavelength_dict.keys()])
            min_wavelength = min([float(i.rstrip()) for i in wavelength_dict.keys()])
        except ValueError:
            max_wavelength = 1
            min_wavelength = 0
        # Check range of available wavelength
        if max_wavelength >= 635 and min_wavelength <= 490:
            id_red = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 710)
            id_green = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 540)
            id_blue = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 480)

            pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))
        else:
            # Otherwise take 3 wavelengths, first, middle and last available wavelength
            id_red = len(header_dict["wavelength"])
            id_green = int(id_red / 2)
            pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))

    # Gamma correct pseudo_rgb image
    pseudo_rgb = pseudo_rgb ** (1 / 2.2)

    # Create an instance of the spectral_data class
    spectral_array = Spectral_data(array_data=array_data, max_wavelength=float(header_dict["wavelength"][-1]),
                                   min_wavelength=float(header_dict["wavelength"][0]), d_type=header_dict["data type"],
                                   wavelength_dict=wavelength_dict, samples=int(header_dict["samples"]),
                                   lines=int(header_dict["lines"]), interleave=header_dict["interleave"],
                                   wavelength_units=header_dict["wavelength units"], array_type="datacube",
                                   filename=filename)

    if params.debug == "plot":
        # Gamma correct pseudo_rgb image
        plot_image(pseudo_rgb)
    elif params.debug == "print":
        print_image(pseudo_rgb, os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array
