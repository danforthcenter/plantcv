# Visualize a scatter plot of pixels

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from plantcv import plantcv as pcv
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params


MAX_MARKER_SIZE = 20
IMG_WIDTH = 128


# functions to get a given channel with parameters compatible
# with rgb2gray_lab and rgb2gray_hsv to use in the dict
def _get_R(rgb_img, _):
    """Get the red channel from a RGB image."""
    return rgb_img[:, :, 2]


def _get_G(rgb_img, _):
    """Get the green channel from a RGB image."""
    return rgb_img[:, :, 1]


def _get_B(rgb_img, _):
    """Get the blue channel from a RGB image."""
    return rgb_img[:, :, 0]


def _get_gray(rgb_img, _):
    """Get the gray scale transformation of a RGB image."""
    return pcv.rgb2gray(rgb_img=rgb_img)


def _get_index(rgb_img, _):
    """Get a vector with linear indices of the pixels in an image."""
    h, w, _ = rgb_img.shape
    return np.arange(h*w)


def _not_valid(*args):
    """Error for a non valid channel."""
    return fatal_error("channel not valid, use R, G, B, l, a, b, h, s, v, gray, or index")


def pixel_scatter_plot(paths_to_imgs, x_channel, y_channel):
    """
    Plot a 2D pixel scatter plot visualization for a dataset of images.
    The horizontal and vertical coordinates are defined by the intensity of the
    pixels in the specified channels.
    The color of each dot is given by the original RGB color of the pixel.

    Inputs:
    paths_to_imgs  = List of paths to the images
    x_channel      = Channel to use for the horizontal coordinate of the scatter plot.
                     Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'gray', and 'index'
    y_channel      = Channel to use for the vertical coordinate of the scatter plot.
                     Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'gray', and 'index'

    Returns:
    fig = matplotlib pyplot Figure object of the visualization
    ax  = matplotlib pyplot Axes object of the visualization

    :param paths_to_imgs: str
    :param x_channel: str
    :param y_channel: str
    :return fig: matplotlib.pyplot Figure object
    :return ax: matplotlib.pyplot Axes object
    """
    # dictionary returns the function that gets the required image channel
    channel_dict = {
        'R': _get_R,
        'G': _get_G,
        'B': _get_B,
        'l': pcv.rgb2gray_lab,
        'a': pcv.rgb2gray_lab,
        'b': pcv.rgb2gray_lab,
        'gray': _get_gray,
        'h': pcv.rgb2gray_hsv,
        's': pcv.rgb2gray_hsv,
        'v': pcv.rgb2gray_hsv,
        'index': _get_index,
    }

    # store debug mode
    debug = params.debug
    params.debug = None

    N = len(paths_to_imgs)

    fig, ax = plt.subplots()
    # load and plot the set of images sequentially
    for p in paths_to_imgs:
        img, _, _ = pcv.readimage(filename=p, mode="native")
        h, _, c = img.shape

        # resizing to predetermined width to reduce the number of pixels
        ratio = h/IMG_WIDTH
        img_height = int(IMG_WIDTH*ratio)
        # nearest interpolation avoids mixing pixel values
        sub_img = cv.resize(img, (IMG_WIDTH, img_height), interpolation=cv.INTER_NEAREST)

        # organize the channels as RGB to use as facecolor for the markers
        sub_img_rgb = cv.cvtColor(sub_img, cv.COLOR_BGR2RGB)
        fcolors = sub_img_rgb.reshape(img_height*IMG_WIDTH, c)/255

        # get channels
        sub_img_x_ch = channel_dict.get(x_channel, _not_valid)(sub_img, x_channel)
        sub_img_y_ch = channel_dict.get(y_channel, _not_valid)(sub_img, y_channel)

        ax.scatter(sub_img_x_ch.reshape(-1),
                   sub_img_y_ch.reshape(-1),
                   alpha=0.05, s=MAX_MARKER_SIZE/N,
                   edgecolors=None, facecolors=fcolors)

    plt.xlabel(x_channel)
    plt.ylabel(y_channel)

    # reset debug
    params.debug = debug

    return fig, ax
