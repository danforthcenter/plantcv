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
    objects, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    areas = [cv2.contourArea(cnt) for cnt in objects]

    ecdf = ECDF(areas, side='right')

    ecdf_df = pd.DataFrame({'object area': ecdf.x, 'cumulative probability': ecdf.y})
    fig_ecdf = (ggplot(data=ecdf_df,
                       mapping=aes(x='object area', y='cumulative probability'))
                + geom_point(size=.1)
                + scale_x_log10())
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)

    # Plot or print the histogram
    _debug(visual=fig_ecdf, filename=os.path.join(params.debug_outdir, str(params.device) + '_area_ecdf.png'))
    return fig_ecdf


def pix_intensity(img, mask=None, title=None):
    if len(img.shape) < 2:
        fatal_error("Input image should be at least a 2d array!")

    if mask is not None:
        masked = img[np.where(mask > 0)]
    else:
        masked = img

    if len(img.shape) > 2 and img.shape[2] == 3:
        b_names = ['blue', 'green', 'red']

    if len(img.shape) == 2:
        ecdf = ECDF(masked.reshape(-1, ), side='right')
        ecdf_df = pd.DataFrame({'pixel intensity': ecdf.x, 'cumulative probability': ecdf.y,
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
        # Create dataframe
        ecdf_df = pd.DataFrame(
            {'pixel intensity': px_int, 'cumulative probability': cdfs,
             'color channel': channel})

    fig_ecdf = (ggplot(data=ecdf_df,
                       mapping=aes(x='pixel intensity', y='cumulative probability', color='color channel'))
                + geom_point(size=0.01)
                + scale_x_log10())
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)
    if len(img.shape) > 2 and img.shape[2] == 3:
        fig_ecdf = fig_ecdf + scale_color_manual(['blue', 'green', 'red'])

    # Plot or print the histogram
    _debug(visual=fig_ecdf, filename=os.path.join(params.debug_outdir, str(params.device) + '_pix_intensity_ecdf.png'))
    return fig_ecdf
