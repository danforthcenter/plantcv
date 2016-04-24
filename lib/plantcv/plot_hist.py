# Plot histogram

import cv2
from matplotlib import pyplot as plt


def plot_hist(img, name):
    """Plot a histogram using the pyplot library.

    Inputs:
    img  = image to analyze
    name = name for plot output

    :param img: numpy array
    :param name: str
    :return:
    """

    # get histogram
    hist = cv2.calcHist([img], [0], None, [256], [0, 255])
    # open pyplot plotting window using hist data
    plt.plot(hist)
    # set range of x-axis
    xaxis = plt.xlim([0, (255)])
    fig_name = name + '.png'
    # write the figure to current directory
    plt.savefig(fig_name)
    # close pyplot plotting window
    plt.clf()
