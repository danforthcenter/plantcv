# Print image to file
import cv2
import numpy
import matplotlib
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error


def print_image(img, filename):
    """Save image to file.

    Inputs:
    img      = image object
    filename = name of file to save image to

    :param img: numpy.ndarray
    :param filename: string
    :return:
    """

    # Print numpy array type images
    image_type = type(img)
    if image_type == numpy.ndarray:
        cv2.imwrite(filename, img)

    # Print matplotlib type images
    elif image_type == matplotlib.figure.Figure:
        img.savefig(filename, dpi=params.dpi)

    # Print ggplot type images
    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        img.save(filename, verbose=False)

    else:
        fatal_error("Error writing file " + filename + ": input img is " + str(type(img)) + ", not a numpy.ndarray, " +
                    "matplotlib.figure, or plotnine.ggplot and cannot get saved out with print_image.")
