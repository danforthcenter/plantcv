import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from plantcv import plantcv as pcv

from plantcv.plantcv import fatal_error


MAX_MARKER_SIZE = 20
IMG_WIDTH = 256


# functions to get a given channel with parameters compatible
# with rgb2gray_lab and rgb2gray_hsv to use in the dict
def _get_R(rgb_img, _):
    return rgb_img[:,:,2]


def _get_G(rgb_img, _):
    return rgb_img[:,:,1]


def _get_B(rgb_img, _):
    return rgb_img[:,:,0]


def _get_gray(rgb_img, _):
    return pcv.rgb2gray(rgb_img=rgb_img)


def _not_valid(*args):
    return fatal_error("channel not valid, use R, G, B, l, a, b, h, s, v or gray")


def pixel_scatter_vis(paths_to_imgs, channel):

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
    }

    N = len(paths_to_imgs)
    _ = plt.figure()
    # load and plot the set of images sequentially
    for p in paths_to_imgs:
        img, _, _ = pcv.readimage(filename=p, mode="native")
        h, w, c = img.shape

        # resizing to predetermined width to reduce the number of pixels
        ratio = h/IMG_WIDTH
        img_height = int(IMG_WIDTH*ratio)
        # nearest interpolation avoids mixing pixel values
        sub_img = cv.resize(img, (IMG_WIDTH, img_height), interpolation=cv.INTER_NEAREST)

        # organize the channels as RGB to use as facecolor for the markers
        sub_img_rgb = cv.cvtColor(sub_img, cv.COLOR_BGR2RGB)
        fcolors = sub_img_rgb.reshape(img_height*IMG_WIDTH,c)/255

        # get the channel
        sub_img_ch = channel_dict.get(channel, _not_valid)(sub_img, channel)
        sub_img_ch_lin = sub_img_ch.reshape(-1)

        plt.scatter(np.arange(img_height*IMG_WIDTH), sub_img_ch_lin,
                            alpha=0.05, s=MAX_MARKER_SIZE/N,
                            edgecolors=None, facecolors=fcolors)

    plt.xlabel('Pixel linear index')
    plt.ylabel(channel + ' channel')
