# Print image to file
import sys
import cv2
import numpy
import matplotlib
from plotnine import ggplot
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
        try:
            cv2.imwrite(filename, img)
        except:
            fatal_error("Error writing file " + filename + ": " + str(sys.exc_info()[0]))

    # Print matplotlib type images
    elif image_type == matplotlib.figure.Figure:
        try:
            matplotlib.use('Agg', warn=False)
            from matplotlib import pyplot as plt
            # fig = plt.figure()
            img.savefig(filename)
        except:
            fatal_error("Error writing file " + filename + ": " + str(sys.exc_info()[0]))

    # Print ggplot type images
    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        try:
            img.save(filename)
        except:
            fatal_error("Error writing file " + filename + ": " + str(sys.exc_info()[0]))
