# Color a label image

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import color_palette
from plantcv.plantcv._debug import _debug


def colorize_label_img(label_img):
    """ Color a labeled image

    Inputs:
        label_img = 2d image with int values at every pixel, where the values represent for the class the
                    pixel belongs to
    Outputs:
        colored_img = RGB image

    :param label_img: numpy.ndarray
    :return: colored_img: numpy.ndarray
    """

    labels = np.unique(label_img) + 1
    h, w = label_img.shape
    rgb_vals = color_palette(num=len(labels), saved=False)
    colored_img = np.zeros((h, w, 3), dtype=np.uint8)
    for (i, l) in enumerate(labels):
        colored_img[label_img == l] = rgb_vals[i]
    #     for ch in range(3):
    #         colored_img[:, :, ch][label_img == l] = rgb_vals[i][ch]

    _debug(visual=colored_img, filename=os.path.join(params.debug_outdir,
                                                     str(params.device) + "_colorized_label_img.png"))

    return colored_img
