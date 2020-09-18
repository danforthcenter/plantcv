# Plot image to screen
import cv2
import numpy
import matplotlib
from plantcv.plantcv import params
from matplotlib import pyplot as plt
from plantcv.plantcv import fatal_error


def plot_image(img, cmap=None):
    """Plot an image to the screen.

    :param img: numpy.ndarray
    :param cmap: str
    :return:
    """

    image_type = type(img)

    dimensions = numpy.shape(img)

    if image_type == numpy.ndarray:
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

    elif image_type == matplotlib.figure.Figure:
        fatal_error("Error, matplotlib Figure not supported. Instead try running without plot_image.")

    # Plot if the image is a plotnine ggplot image
    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        print(img)
