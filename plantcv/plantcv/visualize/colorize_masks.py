# Color mask(s) in any color

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error


def colorize_masks(masks, colors):
    """Plot masks with different colors
    Inputs:
        masks    = list of masks to colorize
        colors   = list of colors (either keys from the color_dict or a list of custom tuples)

        :param masks: list
        :param colors: list
        :return colored_img: ndarray
        """

    # Users must enter the exact same number of colors as classes they'd like to color
    num_classes = len(masks)
    num_colors = len(colors)
    if not num_classes == num_colors:
        fatal_error("The number of colors provided doesn't match the number of class masks provided.")

    # Check to make sure user provided at least one mask and color
    if len(colors) == 0 or len(masks) == 0:
        fatal_error("At least one class mask and color must be provided.")

    # Dictionary of colors and the BGR values, based on some of the colors listed here:
    # https://en.wikipedia.org/wiki/X11_color_names
    color_dict = {'white': (255, 255, 255), 'black': (0, 0, 0), 'aqua': (0, 255, 255), 'blue': (255, 0, 0),
                  'blue violet': (228, 44, 138), 'brown': (41, 41, 168), 'chartreuse': (0, 255, 128),
                  'dark blue': (140, 0, 0), 'gray': (169, 169, 169), 'yellow': (0, 255, 255),
                  'turquoise': (210, 210, 64), 'red': (0, 0, 255), 'purple': (241, 33, 161), 'orange red': (0, 69, 255),
                  'orange': (0, 166, 255), 'lime': (0, 255, 0), 'lime green': (52, 205, 52), 'fuchsia': (255, 0, 255),
                  'crimson': (61, 20, 220), 'beige': (197, 220, 246), 'chocolate': (31, 105, 210),
                  'coral': (79, 128, 255), 'dark green': (0, 100, 0), 'dark orange': (0, 140, 255),
                  'green yellow': (46, 255, 174), 'light blue': (230, 218, 174), 'tomato': (72, 100, 255),
                  'slate gray': (143, 128, 113), 'gold': (0, 215, 255), 'goldenrod': (33, 166, 218),
                  'light green': (143, 238, 143), 'sea green': (77, 141, 46), 'dark red': (0, 0, 141),
                  'pink': (204, 192, 255), 'dark yellow': (0, 205, 255), 'green': (0, 255, 0)}

    ix, iy = np.shape(masks[0])
    colored_img = np.zeros((ix, iy, 3), dtype=np.uint8)
    # Assign pixels to the selected color

    for i in range(0, len(masks)):
        mask = np.copy(masks[i])
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        if isinstance(colors[i], tuple):
            mask[masks[i] > 0] = colors[i]
        elif isinstance(colors[i], str):
            mask[masks[i] > 0] = color_dict[colors[i]]
        else:
            fatal_error("All elements of the 'colors' list must be either str or tuple")
        colored_img = colored_img + mask

    _debug(visual=colored_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_classes_plot.png'))

    return colored_img
