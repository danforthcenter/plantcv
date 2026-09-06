"""Define standard color matrices"""
import math
import numpy as np
from plantcv.plantcv.fatal_error import fatal_error


def std_color_matrix(pos=0):
    """Create a standard color matrix.

    Standard color values compatible with the x-rite ColorChecker Classic,
    ColorChecker Mini, and ColorChecker Passport targets.
    Source: https://en.wikipedia.org/wiki/ColorChecker

    Parameters
    ----------
    pos : int
        reference value indicating orientation of the color card. The reference is based on the position of the white chip:
                pos = 0: bottom-left corner (default)
                pos = 1: bottom-right corner
                pos = 2: top-right corner
                pos = 3: top-left corner

    Returns
    -------
    color_matrix
        matrix containing the standard red, green, and blue values for each color chip
    """
    # list of rgb values as indicated in the color card specs. They need to be
    # arranged depending on the orientation of the color card of reference in the
    # image to be corrected.
    values_list = np.array([[115, 82, 68],  # dark skin
                            [194, 150, 130],  # light skin
                            [98, 122, 157],  # blue sky
                            [87, 108, 67],  # foliage
                            [133, 128, 177],  # blue flower
                            [103, 189, 170],  # bluish green
                            [214, 126, 44],  # orange
                            [80, 91, 166],  # purplish blue
                            [193, 90, 99],  # moderate red
                            [94, 60, 108],  # purple
                            [157, 188, 64],  # yellow green
                            [224, 163, 46],  # orange yellow
                            [56, 61, 150],  # blue
                            [70, 148, 73],  # green
                            [175, 54, 60],  # red
                            [231, 199, 31],  # yellow
                            [187, 86, 149],  # magenta
                            [8, 133, 161],  # cyan
                            [243, 243, 242],  # white (.05*)
                            [200, 200, 200],  # neutral 8 (.23*)
                            [160, 160, 160],  # neutral 6.5 (.44*)
                            [122, 122, 121],  # neutral 5 (.7*)
                            [85, 85, 85],  # neutral 3.5 (1.05*)
                            [52, 52, 52]], dtype=np.float64)  # black (1.50*)

    pos = math.floor(pos)
    if (pos < 0) or (pos > 3):
        fatal_error("white chip position reference 'pos' must be a value among {0, 1, 2, 3}")

    N_chips = values_list.shape[0]

    # array of indices from 1 to N chips in order to match the chip numbering
    # in the color card specs. Later when used for indexing, we subtract the 1.
    idx = np.arange(N_chips)+1
    # indices in the shape of the color card
    cc_indices = idx.reshape((4, 6), order='C')
    # rotate the indices depending on the specified orientation
    cc_indices_rot = np.rot90(cc_indices, k=pos, axes=(0, 1))
    # arange color values based on the indices
    color_matrix_wo_chip_nb = values_list[(cc_indices_rot-1).reshape(-1), :]/255.

    # add chip number (mask value) compatible with other PlantCV functions
    chip_nb = np.arange(10, 10*N_chips+1, 10)
    color_matrix = np.concatenate((chip_nb.reshape(N_chips, 1), color_matrix_wo_chip_nb), axis=1)

    return color_matrix


def astro_color_matrix():
    """Create a standard color matrix for astrobotany calibration stickers

    Returns
    -------
    color_matrix
        matrix containing the standard red, green, and blue values for each color chip
    """
    values_list = np.array([[47, 59, 128],      # Blue
                            [87, 158, 63],      # Green
                            [181, 64, 54],      # Red
                            [228, 207, 50],     # Yellow
                            [53, 56, 55],       # Black
                            # Grayscale chips
                            [233, 241, 238],
                            [210, 220, 220],
                            [184, 192, 186],
                            [164, 170, 163],
                            [145, 147, 142],
                            [123, 126, 122],
                            [100, 102,  99],
                            [83, 82, 81],
                            [70, 71, 70],
                            [57, 58, 58]], dtype=np.float64)

    # Convert RGB values to float
    color_matrix_wo_chip_nb = values_list/255.

    # Add chip number (mask value) to be compatible with other PlantCV functions
    N_chips = values_list.shape[0]

    chip_nb = np.arange(10, 10*N_chips+1, 10)
    chip_nb = np.reshape(chip_nb, shape=(-1, 1))

    color_matrix = np.concatenate((chip_nb, color_matrix_wo_chip_nb), axis=1)

    return color_matrix
