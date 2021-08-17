# Read in a hyperspectral data cube as an array and parse metadata from the header file

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.transform import rescale
from plantcv.plantcv import fatal_error


def _find_closest(spectral_array, target):
    """Find index of a target wavelength band in a hyperspectral data instance.

    Inputs:
        spectral_array = Hyperspectral data instance
        target         = Target wavelength value

    Returns:
        idx            = Index

    :param spectral_array: __main__.Spectral_data
    :param target: float
    :return spectral_array: __main__.Spectral_data
    """
    # Array must be sorted
    idx = spectral_array.searchsorted(target)
    idx = np.clip(idx, 1, len(spectral_array) - 1)
    left = spectral_array[idx - 1]
    right = spectral_array[idx]
    idx -= target - left < right - target
    return idx


def _make_pseudo_rgb(spectral_array):
    """Create the best pseudo-rgb image possible from a hyperspectral datacube

    Inputs:
        spectral_array = Hyperspectral data instance

    Returns:
        pseudo_rgb     = Pseudo-rgb image

    :param spectral_array: __main__.Spectral_data
    :return pseudo_rgb: numpy.ndarray
    """

    # Make shorter variable names for data from the spectral class instance object
    array_data = spectral_array.array_data
    default_bands = spectral_array.default_bands
    wl_keys = spectral_array.wavelength_dict.keys()

    if default_bands is not None:
        pseudo_rgb = cv2.merge((array_data[:, :, int(default_bands[0])],
                                array_data[:, :, int(default_bands[1])],
                                array_data[:, :, int(default_bands[2])]))

    else:
        max_wavelength = max([float(i) for i in wl_keys])
        min_wavelength = min([float(i) for i in wl_keys])
        # Check range of available wavelength
        if max_wavelength >= 635 and min_wavelength <= 490:
            id_red = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=710)
            id_green = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=540)
            id_blue = _find_closest(spectral_array=np.array([float(i) for i in wl_keys]), target=480)

            pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))
        else:
            # Otherwise take 3 wavelengths, first, middle and last available wavelength
            id_red = int(len(spectral_array.wavelength_dict)) - 1
            id_green = int(id_red / 2)
            pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                    array_data[:, :, [id_green]],
                                    array_data[:, :, [id_red]]))

    # Gamma correct pseudo_rgb image
    pseudo_rgb = pseudo_rgb ** (1 / 2.2)
    # Scale each of the channels up to 255
    debug = params.debug
    params.debug = None
    pseudo_rgb = cv2.merge((rescale(pseudo_rgb[:, :, 0]),
                            rescale(pseudo_rgb[:, :, 1]),
                            rescale(pseudo_rgb[:, :, 2])))

    # Reset debugging mode
    params.debug = debug

    return pseudo_rgb


def read_data(filename):
    """Read hyperspectral image data from file.
    Inputs:
    filename          = Name of image file

    Returns:
    spectral_array    = Hyperspectral data instance

    :param filename: str
    :return spectral_array: __main__.Spectral_data
        """

    # Initialize dictionary
    header_dict = {}

    # Remove any file extension and set .hdr filename
    filename_base = os.path.splitext(filename)[0]
    headername = filename_base + ".hdr"

    with open(headername, "r") as f:
        # Replace characters for easier parsing
        hdata = f.read()
        hdata = hdata.replace(",\n", ",")
        hdata = hdata.replace("\n,", ",")
        hdata = hdata.replace("{\n", "{")
        hdata = hdata.replace("\n}", "}")
        hdata = hdata.replace(" \n ", "")
        hdata = hdata.replace(" \n", "")
        hdata = hdata.replace(";", "")
    hdata = hdata.split("\n")

    # Loop through and create a dictionary from the header file
    for i, string in enumerate(hdata):
        if ' = ' in string:
            header_data = string.split(" = ")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ' : ' in string:
            header_data = string.split(" : ")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})

    # Reformat wavelengths
    header_dict["wavelength"] = header_dict["wavelength"].replace("{", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace("}", "")
    header_dict["wavelength"] = header_dict["wavelength"].replace(" ", "")
    header_dict["wavelength"] = header_dict["wavelength"].split(",")

    # Create dictionary of wavelengths
    wavelength_dict = {}
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({float(wavelength): float(j)})

    # Replace datatype ID number with the numpy datatype
    dtype_dict = {"1": np.uint8, "2": np.int16, "3": np.int32, "4": np.float32, "5": np.float64, "6": np.complex64,
                  "9": np.complex128, "12": np.uint16, "13": np.uint32, "14": np.uint64, "15": np.uint64}
    header_dict["data type"] = dtype_dict[header_dict["data type"]]

    # Read in the data from the file
    raw_data = np.fromfile(filename, header_dict["data type"], -1)

    # Reshape the raw data into a datacube array
    data_format = {
        # Band Interleaved by Line (BIL)
        "BIL": {
            # Divide the raw data by Y (lines), Z (spectral bands), and X (samples)
            # Then reorder into a cube in Y, X, Z order
            "reshape": (int(header_dict["lines"]), int(header_dict["bands"]), int(header_dict["samples"])),
            "transpose": (0, 2, 1)
        },
        # Band Sequential (BSQ)
        "BSQ": {
            # Divide the raw data by Z (spectral bands), Y (lines), and X (samples)
            # Then reorder into a cube in Y, X, Z order
            "reshape": (int(header_dict["bands"]), int(header_dict["lines"]), int(header_dict["samples"])),
            "transpose": (1, 2, 0)
        }
    }
    interleave_type = header_dict.get("interleave").upper()
    if interleave_type not in data_format:
        fatal_error(f"Interleave type {interleave_type} is not supported.")

    # Reshape raw data into a data cube
    array_data = raw_data.reshape(data_format[interleave_type]["reshape"]
                                  ).transpose(data_format[interleave_type]["transpose"])

    # Check for default bands (that get used to make pseudo_rgb image)
    default_bands = None
    if "default bands" in header_dict:
        header_dict["default bands"] = header_dict["default bands"].replace("{", "")
        header_dict["default bands"] = header_dict["default bands"].replace("}", "")
        default_bands = header_dict["default bands"].split(",")

    # Find array min and max values
    max_pixel = float(np.amax(array_data))
    min_pixel = float(np.amin(array_data))

    wavelength_units = header_dict.get("wavelength units")
    if wavelength_units is None:
        wavelength_units = "nm"

        # Create an instance of the spectral_data class
    spectral_array = Spectral_data(array_data=array_data,
                                   max_wavelength=float(str(header_dict["wavelength"][-1]).rstrip()),
                                   min_wavelength=float(str(header_dict["wavelength"][0]).rstrip()),
                                   max_value=max_pixel, min_value=min_pixel,
                                   d_type=header_dict["data type"],
                                   wavelength_dict=wavelength_dict, samples=int(header_dict["samples"]),
                                   lines=int(header_dict["lines"]), interleave=header_dict["interleave"],
                                   wavelength_units=wavelength_units, array_type="datacube",
                                   pseudo_rgb=None, filename=filename, default_bands=default_bands)

    # Make pseudo-rgb image and replace it inside the class instance object
    pseudo_rgb = _make_pseudo_rgb(spectral_array)
    spectral_array.pseudo_rgb = pseudo_rgb

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_pseudo_rgb.png"))

    return spectral_array
