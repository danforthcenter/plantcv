# Plot Empirical Cumulative Distribution Function for Object Size or Pixel Intensity

import os
import cv2
import pandas as pd
import numpy as np
from plantcv.plantcv import params, fatal_error
from plantcv.plantcv._debug import _debug
from statsmodels.distributions.empirical_distribution import ECDF
from plotnine import ggplot, aes, geom_point, labels, scale_color_manual, scale_x_log10


def obj_size(mask, title=None):
    """ Plot empirical cumulative distribution for object size based on binary mask

    Inputs:
    mask  = binary mask
    title = a custom title for the plot (default=None)

    Returns:
    fig_ecdf = empirical cumulative distribution function plot

    :param mask: numpy.ndarray
    :param title: str
    :return fig_ecdf: plotnine.ggplot.ggplot
    """

    objects, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    areas = [cv2.contourArea(cnt) for cnt in objects]

    ecdf = ECDF(areas, side='right')

    ecdf_df = pd.DataFrame({'object area': ecdf.x, 'cumulative probability': ecdf.y})
    # create ecdf plot and apply log-scale for x-axis (areas)
    fig_ecdf = (ggplot(data=ecdf_df,
                       mapping=aes(x='object area', y='cumulative probability'))
                + geom_point(size=.1)
                + scale_x_log10())
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)

    # Plot or print the ecdf
    _debug(visual=fig_ecdf, filename=os.path.join(params.debug_outdir, str(params.device) + '_area_ecdf.png'))
    return fig_ecdf


def pix_intensity(img, mask=None, title=None):
    """ Plot empirical cumulative distribution for pixel intensity of each input image channel

    Inputs:
    img   = an RGB or grayscale image to analyze
    mask  = binary mask, if given, calculate ecdf from masked area only (default=None)
    title = a custom title for the plot (default=None)

    Returns:
    fig_ecdf = empirical cumulative distribution function plot

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param title: str
    :return fig_ecdf: plotnine.ggplot.ggplot
    """

    if len(img.shape) < 2:
        fatal_error("Input image should be at least a 2d array!")

    # if a binary mask is provided, only the masked area is of interest
    if mask is not None:
        masked = img[np.where(mask > 0)]
    else:
        masked = img

    # assumption: if there are 3 color channels, the names are 'blue', 'green', and 'red', respectively
    if len(img.shape) > 2 and img.shape[2] == 3:
        b_names = ['blue', 'green', 'red']

    # prepare dataframe to plot for either garyscale or RGB imagery
    if len(img.shape) == 2:
        ecdf = ECDF(masked.reshape(-1, ), side='right')
        # create dataframe for ecdf
        ecdf_df = pd.DataFrame({'pixel intensity': ecdf.x,
                                'cumulative probability': ecdf.y,
                                'color channel': ['0' for _ in range(len(ecdf.x))]})
    else:
        px_int = []
        cdfs = []
        channel = []
        for (b, b_name) in enumerate(b_names):
            ecdf = ECDF(masked[:, b].reshape(-1, ), side='right')
            px_int = np.append(px_int, ecdf.x)
            cdfs = np.append(cdfs, ecdf.y)
            channel = channel + [b_name for _ in range(len(ecdf.x))]
        # create dataframe for ecdf
        ecdf_df = pd.DataFrame(
            {'pixel intensity': px_int,
             'cumulative probability': cdfs,
             'color channel': channel})

    # create ecdf plot and apply log-scale for x-axis (pixel intensity)
    fig_ecdf = (ggplot(data=ecdf_df,
                       mapping=aes(x='pixel intensity', y='cumulative probability', color='color channel'))
                + geom_point(size=0.01)
                # + scale_x_log10()
                )
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)

    # if input an RGB image, set legend for color channels to be 'blue', 'green', and 'red', respectively
    if len(img.shape) > 2 and img.shape[2] == 3:
        fig_ecdf = fig_ecdf + scale_color_manual(b_names)

    # Plot or print the ecdf plot
    _debug(visual=fig_ecdf, filename=os.path.join(params.debug_outdir, str(params.device) + '_pix_intensity_ecdf.png'))
    return fig_ecdf
