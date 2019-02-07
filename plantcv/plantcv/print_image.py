# Print image to file
import sys
import cv2
import numpy
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
    import matplotlib
    from plotnine import ggplot

    # Print numpy array type images
    image_type = type(img)
    if image_type == numpy.ndarray:
        cv2.imwrite(filename, img)

    # Print matplotlib type images
    elif image_type == matplotlib.figure.Figure:
        matplotlib.use('Agg', warn=False)
        from matplotlib import pyplot as plt
        # fig = plt.figure()
        img.savefig(filename)

    # Print ggplot type images
    elif str(image_type) == "<class 'plotnine.ggplot.ggplot'>":
        img.save(filename)

    else:
        fatal_error("Error writing file " + filename + ": " + str(sys.exc_info()[0]))
