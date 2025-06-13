# Read image

import os
import cv2
import re
import nd2
import numpy as np
import pandas as pd
from plantcv.plantcv import Spectral_data
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def _find_hdr(filename):
    """Find a header file paired with an hyperspectral data file.

    Keyword arguments:
    filename = File path/name of a hyperspectral data file.

    Returns:
    hdrfile = File path/name of hyperspectral header file.

    :param filename: str
    :return hdrfile: str
    """
    # Split the filename into the path and name
    dat_path, dat_filename = os.path.split(filename)
    # Extract the base of the data file name and the extension, if any
    dat_basename, dat_ext = os.path.splitext(dat_filename)
    # Create a regular expression for the header file
    # The data file extension is included optionally
    hdr_regex = re.compile(f"{dat_basename}({dat_ext})?.hdr")
    # List all the files in the data file directory
    for fname in os.listdir(dat_path):
        # If the filename matches, return the header file path
        if hdr_regex.match(fname):
            return os.path.join(dat_path, fname)
    return None


def _parse_envi(headername):
    """Parse a header file and create dictionary of relevant metadata

    Keyword arguments:
    headername      = File path/name of a hyperspectral data file.

    Returns:
    header_dict     = Dictionary of hdr metadata
    wavelength_dict = Dictionary of wavelength metadata

    :param headername: str
    :return header_dict: dict
    :return wavelength_dict: dict

    """
    # Initialize dictionary
    header_dict = {}
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
    # Try to reformat strings by replacing all " = " with '=' and " : "
    for string in hdata:
        # Remove white space for consistency across header file formats
        string = string.replace(' ', '')
        if '=' in string:
            header_data = string.split("=")
            header_data[0] = header_data[0].lower()
            header_dict.update({header_data[0].rstrip(): header_data[1].rstrip()})
        elif ':' in string:
            header_data = string.split(":")
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
                  "9": np.complex128, "12": np.uint16, "13": np.uint32, "14": np.int64, "15": np.uint64}
    header_dict["datatype"] = dtype_dict[header_dict["datatype"]]

    return header_dict, wavelength_dict


def _parse_arcgis(headername):
    """Parse a header file and create dictionary of relevant metadata

    Keyword arguments:
    headername      = File path/name of a hyperspectral data file.

    Returns:
    header_dict     = Dictionary of hdr metadata
    wavelength_dict = Dictionary of wavelength metadata

    :param headername: str
    :return header_dict: dict
    :return wavelength_dict: dict

    """
    # Initialize dictionary/lists
    header_dict = {"wavelength": []}
    wavelength_dict = {}
    keyword_dict = {"LAYOUT": "interleave", "NROWS": "lines", "NCOLS": "samples", "NBANDS": "bands",
                    "NBITS": "datatype", "WAVELENGTHS": "wavelength"}

    # Read in metadata
    with open(headername, "r") as f:
        hdata = f.read()
    hdata = hdata.split("\n")  # split on line returns

    # Loop through and create a dictionary from the header file
    for string in hdata:
        header_data = string.upper().split(" ")  # split string on white space
        # If there are two elements then it is a keyword and value pair
        if len(header_data) == 2:
            # Only keep the pair if the keyword is in the keyword dictionary
            if header_data[0] in keyword_dict:
                header_dict[keyword_dict[header_data[0]]] = header_data[1]
        # Otherwise if the line has one element it is either the WAVELENGTH or WAVELENGTH_END keyword
        # or a wavelength value
        elif header_data[0] not in ["WAVELENGTHS", "WAVELENGTHS_END", ""]:
            # Append the wavelength value to the wavelength list
            header_dict["wavelength"].append(header_data[0])
    # Build the wavelength dictionary from the list and index values of wavelengths
    for j, wavelength in enumerate(header_dict["wavelength"]):
        wavelength_dict.update({float(wavelength): float(j)})

    dtype_dict = {"8": np.uint8, "16": np.int16, "32": np.int32, "64": np.float32}
    header_dict["datatype"] = dtype_dict[header_dict["datatype"]]

    return header_dict, wavelength_dict


def _read_hyper(filename, mode="ENVI"):
    """Read hyperspectral image data from file.
    Inputs:
    filename          = Name of image file
    mode              = Format of img data (ENVI or ARCGIS, case insensitive)

    Returns:
    spectral_array    = Hyperspectral data instance

    :param filename: str
    :param mode: str
    :return spectral_array: __main__.Spectral_data
    """
    # Remove any file extension and set .hdr filename
    headername = _find_hdr(filename=filename)

    if headername is None:
        fatal_error(f"Unable to find the header file corresponding to {filename}")

    if mode.upper() == "ENVI":
        header_dict, wavelength_dict = _parse_envi(headername=headername)
    elif mode.upper() == "ARCGIS":
        header_dict, wavelength_dict = _parse_arcgis(headername=headername)

    # Read in the data from the file
    raw_data = np.fromfile(filename, header_dict["datatype"], -1)

    # Reshape the raw data into a datacube array
    data_format = {
        # Band Interleaved by Line (BIL)
        "BIL": {
            # Divide the raw data by Y (lines), Z (spectral bands), and X (samples)
            # Then reorder into a cube in Y, X, Z order
            "reshape": (int(header_dict["lines"]), int(header_dict["bands"]), int(header_dict["samples"])),
            "transpose": (0, 2, 1)
        },
        # Band Interleaved by Pixel (BIP)
        "BIP": {
            # Divide the raw data by Y (lines), and X (samples), Z (spectral bands)
            # Then reorder into a cube in Y, X, Z order
            "reshape": (int(header_dict["lines"]), int(header_dict["samples"]), int(header_dict["bands"])),
            "transpose": (0, 1, 2)
        },
        # Band Sequential (BSQ)
        "BSQ": {
            # Divide the raw data by Z (spectral bands), Y (lines), and X (samples)
            # Then reorder into a cube in Y, X, Z order
            "reshape": (int(header_dict["bands"]), int(header_dict["lines"]), int(header_dict["samples"])),
            "transpose": (1, 2, 0)
        }
    }
    interleave_type = header_dict.get("interleave")
    if interleave_type is not None:
        interleave_type = interleave_type.upper()
    if interleave_type not in data_format:
        fatal_error(f"Interleave type {interleave_type} is not supported.")

    # Reshape raw data into a data cube
    array_data = raw_data.reshape(data_format[interleave_type]["reshape"]
                                  ).transpose(data_format[interleave_type]["transpose"])

    # Check for default bands (that get used to make pseudo_rgb image)
    default_bands = None
    if "defaultbands" in header_dict:
        header_dict["defaultbands"] = header_dict["defaultbands"].replace("{", "")
        header_dict["defaultbands"] = header_dict["defaultbands"].replace("}", "")
        default_bands = header_dict["defaultbands"].split(",")

    # Find array min and max values
    max_pixel = float(np.amax(array_data))
    min_pixel = float(np.amin(array_data))

    wavelength_units = header_dict.get("wavelengthunits")
    if wavelength_units is None:
        wavelength_units = "nm"

        # Create an instance of the spectral_data class
    spectral_array = Spectral_data(array_data=array_data,
                                   max_wavelength=float(str(header_dict["wavelength"][-1]).rstrip()),
                                   min_wavelength=float(str(header_dict["wavelength"][0]).rstrip()),
                                   max_value=max_pixel, min_value=min_pixel,
                                   d_type=header_dict["datatype"],
                                   wavelength_dict=wavelength_dict, samples=int(header_dict["samples"]),
                                   lines=int(header_dict["lines"]), interleave=header_dict["interleave"],
                                   wavelength_units=wavelength_units, array_type="datacube",
                                   pseudo_rgb=None, filename=filename, default_bands=default_bands)

    # Make pseudo-rgb image and replace it inside the class instance object
    pseudo_rgb = _make_pseudo_rgb(spectral_array)
    spectral_array.pseudo_rgb = pseudo_rgb

    return spectral_array


def read_image(filename, mode="native"):
    """Read image from file.

    Inputs:
    filename = name of image file
    mode     = mode of imread ("native", "rgb", "rgba", "gray", "csv", "envi", "arcgis", "nd2")

    Returns:
    img      = image object as numpy array
    path     = path to image file
    img_name = name of image file

    :param filename: str
    :param mode: str
    :return img: numpy.ndarray
    :return path: str
    :return img_name: str
    """
    if mode.upper() in ("GRAY", "GREY"):
        img = cv2.imread(filename, 0)
    elif mode.upper() == "RGB":
        img = cv2.imread(filename)
    elif mode.upper() == "RGBA":
        img = cv2.imread(filename, -1)
    elif mode.upper() == "CSV":
        inputarray = pd.read_csv(filename, sep=',', header=None)
        img = inputarray.values
    elif mode.upper() in ["ENVI", "ARCGIS"]:
        array_data = _read_hyper(filename, mode=mode)
        return array_data
    elif mode.upper() == "ND2":
        img = nd2.imread(filename)
    else:
        img = cv2.imread(filename, -1)

    # Default to drop alpha channel if user doesn't specify 'rgba'
    if len(np.shape(img)) == 3 and np.shape(img)[2] == 4 and mode.upper() == "NATIVE":
        img = cv2.imread(filename)

    if img is None:
        fatal_error("Failed to open " + filename)

    # Split path from filename
    path, img_name = os.path.split(filename)

    # Debugging visualization
    _debug(visual=img, filename=os.path.join(params.debug_outdir, "input_image.png"))

    return img, path, img_name
