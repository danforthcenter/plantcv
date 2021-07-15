# Print image to file
import cv2
import numpy
import matplotlib
from plotnine.ggplot import ggplot
from xarray.core.dataarray import DataArray
from plantcv.plantcv.classes import PSII_data
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error


def print_image(img, filename, **kwargs):
    """
    Save image to file.

    Inputs:
    img      = image object
    filename = name of file to save image to
    kwargs   = key-value arguments to xarray.plot method

    :param img: numpy.ndarray, matplotlib.figure.Figure, ggplot, xarray.plot.facetgrid.FacetGrid
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

    # Print ggplot type images
    elif isinstance(img, ggplot):
        img.save(filename, verbose=False)

    elif isinstance(img, DataArray):
        img.plot(**kwargs).fig.savefig(filename, dpi=params.dpi)

    elif isinstance(img, tuple) and len(img) == 3:
        fatal_error('Looks like you are trying to save a histogram. If so, you have 2 options: 1. Use '
                    'pcv.visualize.histogram() on each numpy.ndarray 2. Create a matplotlib figure by running '
                    'myfig=plt.gcf() in the same execution as generating the histogram and then use pcv.print_image('
                    'myplot, filename=...). ')

    elif isinstance(img, PSII_data):
        fatal_error("You need to plot an underlying DataArray.")

    else:
        fatal_error(f"Error writing file {filename}: input img is {str(type(img))}, not a numpy.ndarray, "
                    "matplotlib.figure, plotnine.ggplot, or xarray.plot.facetgrid.FacetGrid and cannot get "
                    "saved out with print_image.")
