"""Print image to file."""
import cv2
import numpy
import matplotlib
from xarray.core.dataarray import DataArray
from plantcv.plantcv.classes import PSII_data
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv._show_dataarray import _show_dataarray
from altair.vegalite.v5.api import FacetChart, LayerChart, Chart


def print_image(img, filename, **kwargs):
    """
    Save image to file.

    Inputs:
    img      = image object
    filename = name of file to save image to
    kwargs   = key-value arguments to xarray.plot method

    :param img: numpy.ndarray, matplotlib.figure.Figure, ggplot, xarray.core.dataarray.DataArray
    :param filename: string
    :param kwargs: dict
    :return:
    """
    # Print numpy array type images
    if isinstance(img, numpy.ndarray):
        cv2.imwrite(filename, img)

    # Print matplotlib type images
    elif isinstance(img, matplotlib.figure.Figure):
        img.savefig(filename, dpi=params.dpi)

    # Print altair type images
    elif isinstance(img, (FacetChart, LayerChart, Chart)):
        img.save(filename)

    elif isinstance(img, DataArray):
        fig_handle = _show_dataarray(img, **kwargs)
        # fig_handle comes back as a tuple if xarray makes a histogram
        # fig_handle comes back as a list len 1 containing matplotlib.lines.Line2D if xarray makes a line plot
        # will this ever happen? I think _show_dataarray and xarray will fail first
        fig_handle.fig.savefig(filename, dpi=params.dpi)

    elif isinstance(img, PSII_data):
        fatal_error("You need to provide an underlying DataArray.")

    else:
        fatal_error(f"Error writing file {filename}: input img is {str(type(img))}, not a numpy.ndarray, "
                    "matplotlib.figure, plotnine.ggplot, or xarray.core.dataarray.DataArray and cannot get "
                    "saved out with print_image.")
