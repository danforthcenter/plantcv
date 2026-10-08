# Visualize a scatter plot of pixels
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from plantcv.plantcv import fatal_error, params
from plantcv.plantcv.readimage import readimage
from plantcv.plantcv._helpers import _rgb2lab, _rgb2hsv, _rgb2cmyk, _rgb2gray


MAX_MARKER_SIZE = 20
IMG_WIDTH = 128


# functions to get a given channel with parameters compatible
# with rgb2gray_lab, rgb2gray_hsv, and rgb2gray_cmyk to use in the dict
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
    return _rgb2gray(rgb_img=rgb_img)


def _get_index(rgb_img, _):
    """Get a vector with linear indices of the pixels in an image."""
    h, w, _ = rgb_img.shape
    return np.arange(h*w)


def _not_valid(*args):
    """Error for a non valid channel."""
    return fatal_error("channel not valid, use R, G, B, l, a, b, h, s, v, c, m, y, k, gray, or index")


def pixel_scatter_plot(source, x_channel, y_channel, n=20, ext="png"):
    """
    Plot a 2D pixel scatter plot visualization for a dataset of images.
    The horizontal and vertical coordinates are defined by the intensity of the
    pixels in the specified channels.
    The color of each dot is given by the original RGB color of the pixel.

    Parameters
    ----------
    source : list, numpy.ndarray, or str,
        List of paths to the images, an image as a numpy array, or a path to a starting directory to find images in
    x_channel : str,
        Channel to use for the horizontal coordinate of the scatter plot.
        Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'c', 'm', 'y', 'k', 'gray', and 'index'
    y_channel : str,
        Channel to use for the vertical coordinate of the scatter plot.
        Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'c', 'm', 'y', 'k', 'gray', and 'index'
    n : int,
        max number of images to use if source is a string
    ext : str,
        image file extension to search for if source is a string

    Returns
    -------
    fig : matplotlib pyplot Figure object of the visualization
    ax : matplotlib pyplot Axes object of the visualization
    """
    # dictionary returns the function that gets the required image channel
    channel_dict = {
        'R': _get_R,
        'G': _get_G,
        'B': _get_B,
        'l': _rgb2lab,
        'a': _rgb2lab,
        'b': _rgb2lab,
        'gray': _get_gray,
        'h': _rgb2hsv,
        's': _rgb2hsv,
        'v': _rgb2hsv,
        'index': _get_index,
        'c': _rgb2cmyk,
        'm': _rgb2cmyk,
        'y': _rgb2cmyk,
        'k': _rgb2cmyk
    }
    if isinstance(source, np.ndarray):
        fig, ax = _px_scatter_from_img(source, x_channel, y_channel, channel_dict)
        return fig, ax
    # if not an image then keep going
    paths_to_imgs = source
    N = len(paths_to_imgs)
    if isinstance(source, str):
        N = n
        paths_to_imgs = []
        for root, _, files in os.walk(source):
            for file in files:
                if file.lower().endswith(ext) and len(paths_to_imgs) < n:
                    paths_to_imgs.append(os.path.join(root, file))

    # store debug mode
    debug = params.debug
    params.debug = None

    fig, ax = plt.subplots()
    # load and plot the set of images sequentially
    for p in paths_to_imgs:
        img, _, _ = readimage(filename=p)
        h, _, c = img.shape

        # resizing to predetermined width to reduce the number of pixels
        ratio = h/IMG_WIDTH
        img_height = int(IMG_WIDTH*ratio)
        # nearest interpolation avoids mixing pixel values
        sub_img = cv2.resize(img, (IMG_WIDTH, img_height), interpolation=cv2.INTER_NEAREST)

        # organize the channels as RGB to use as facecolor for the markers
        sub_img_rgb = cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB)
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


def _px_scatter_from_img(source, x_channel, y_channel, channel_dict):
    """Make pixel scatter plot from an image

    Parameters
    ----------
    source : numpy.ndarray
        List of paths to the images, an image as a numpy array, or a path to a starting directory to find images in
    x_channel : str,
        Channel to use for the horizontal coordinate of the scatter plot.
        Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'c', 'm', 'y', 'k', 'gray', and 'index'
    y_channel : str,
        Channel to use for the vertical coordinate of the scatter plot.
        Options:  'R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'c', 'm', 'y', 'k', 'gray', and 'index'
    channel_dict : dict,
        dictionary of functions to pull channels. Defined internally in user facing function.

    Returns
    -------
    fig : matplotlib pyplot Figure object of the visualization
    ax : matplotlib pyplot Axes object of the visualization
    """
    fig, ax = plt.subplots()
    h, _, c = source.shape
    # resizing to predetermined width to reduce the number of pixels
    ratio = h/IMG_WIDTH
    img_height = int(IMG_WIDTH*ratio)
    # nearest interpolation avoids mixing pixel values
    sub_img = cv2.resize(source, (IMG_WIDTH, img_height), interpolation=cv2.INTER_NEAREST)

    # organize the channels as RGB to use as facecolor for the markers
    sub_img_rgb = cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB)
    fcolors = sub_img_rgb.reshape(img_height*IMG_WIDTH, c)/255

    # get channels
    sub_img_x_ch = channel_dict.get(x_channel, _not_valid)(sub_img, x_channel)
    sub_img_y_ch = channel_dict.get(y_channel, _not_valid)(sub_img, y_channel)

    ax.scatter(sub_img_x_ch.reshape(-1),
               sub_img_y_ch.reshape(-1),
               alpha=0.05, s=MAX_MARKER_SIZE,
               edgecolors=None, facecolors=fcolors)

    plt.xlabel(x_channel)
    plt.ylabel(y_channel)

    return fig, ax
