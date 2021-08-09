# Plot image to screen
import cv2
import numpy
import matplotlib
from xarray.core.dataarray import DataArray
from plotnine.ggplot import ggplot
from plantcv.plantcv import params
from plantcv.plantcv.classes import PSII_data
from matplotlib import pyplot as plt
from plantcv.plantcv import fatal_error
from plantcv.plantcv._show_dataarray import _show_dataarray


def plot_image(img, cmap=None, **kwargs):
    """
    Plot an image to the screen.

    :param img: numpy.ndarray, ggplot, xarray.core.dataarray.DataArray
    :param cmap: str
    :param kwargs: key-value arguments to xarray.plot method
    :return:
    """

    dimensions = numpy.shape(img)

    if isinstance(img, numpy.ndarray):
        matplotlib.rcParams['figure.dpi'] = params.dpi
        # If the image is color then OpenCV stores it as BGR, we plot it as RGB
        if len(dimensions) == 3:
            plt.figure()
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.show()

        elif cmap is None and len(dimensions) == 2:
            plt.figure()
            plt.imshow(img, cmap="gray")
            plt.show()

        elif cmap is not None and len(dimensions) == 2:
            plt.figure()
            plt.imshow(img, cmap=cmap)
            plt.show()

    elif isinstance(img, matplotlib.figure.Figure):
        fatal_error(
            "Error, matplotlib Figure not supported. Instead try running without plot_image.")

    # Plot if the image is a plotnine ggplot image
    elif isinstance(img, ggplot):
        print(img)

    elif isinstance(img, DataArray):
        _show_dataarray(img, **kwargs)

    elif isinstance(img, PSII_data):
        fatal_error("You need to plot an underlying DataArray.")

    else:
        fatal_error(f"Plotting {type(img)} is not supported.")
