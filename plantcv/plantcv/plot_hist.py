# Plot histogram

import cv2
import numpy as np


def plot_hist(img, name=False):
    """Plot a histogram using the pyplot library.

    Inputs:
    img  = image to analyze
    name = name for plot output

    :param img: numpy.ndarray
    :param name: str
    :return bins: list
    :return hist: list
    """

    import matplotlib
    matplotlib.use('Agg', warn=False)
    from matplotlib import pyplot as plt

    # get histogram
    if img.dtype == 'uint8':
        hist = cv2.calcHist([img], [0], None, [256], [0, 255])
        bins = range(0, 256, 1)

        if name is not False:
            # open pyplot plotting window using hist data
            plt.plot(hist)
            # set range of x-axis
            xaxis = plt.xlim([0, 255])
            fig_name = name + '.png'
            # write the figure to current directory
            plt.savefig(fig_name)
            # close pyplot plotting window
            plt.clf()

    else:
        hist, bins = np.histogram(img, bins='auto')

        if name is not False:
            # open pyplot plotting window using hist data
            plt.plot(bins[:-1], hist)
            plt.xticks(bins[:-1], rotation='vertical', fontsize=4)
            # set range of x-axis
            # xaxis = plt.xlim([0, bins.max()])
            fig_name = name + '.png'
            # write the figure to current directory
            plt.savefig(fig_name)
            # close pyplot plotting window
            plt.clf()

    return bins, hist
