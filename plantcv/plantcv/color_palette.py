# Color palette returns an array of colors (rainbow)

from matplotlib import pyplot as plt
import numpy as np
from plantcv.plantcv import params


def color_palette(num, saved=False):
    """color_palette: Returns a list of colors length num

    Inputs:
    num        = number of colors to return.
    saved      = use the previously stored color scale, if any (default = False).

    Returns:
    colors     = a list of color lists (RGB values)

    :param num: int
    :return colors: list
    """
    # If a previous palette is saved and saved = True, return it
    if params.saved_color_scale is not None and saved is True:
        return params.saved_color_scale
    else:
        # Retrieve the matplotlib colormap
        cmap = plt.get_cmap(params.color_scale)
        # Get num evenly spaced colors
        colors = cmap(np.linspace(0, 1, num), bytes=True)
        colors = colors[:, 0:3].tolist()
        # colors are sequential, if params.color_sequence is random then shuffle the colors
        if params.color_sequence == "random":
            np.random.shuffle(colors)
        # Save the color scale for further use
        params.saved_color_scale = colors

        return colors
