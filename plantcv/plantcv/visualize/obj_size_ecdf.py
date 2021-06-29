# Plot Empirical Cumulative Distribution Function for Object Size

import os
import cv2
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from statsmodels.distributions.empirical_distribution import ECDF
from plotnine import ggplot, aes, geom_point, labels, scale_x_log10


def obj_size_ecdf(mask, title=None):
    """
    Plot empirical cumulative distribution for object size based on binary mask.

    Inputs:
    mask  = binary mask
    title = a custom title for the plot (default=None)

    Returns:
    fig_ecdf = empirical cumulative distribution function plot

    :param mask: numpy.ndarray
    :param title: str
    :return fig_ecdf: plotnine.ggplot.ggplot
    """
    objects, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    areas = [cv2.contourArea(cnt) for cnt in objects]
    # Remove objects with areas < 1px
    areas = [i for i in areas if i >= 1.0]

    ecdf = ECDF(areas, side='right')

    ecdf_df = pd.DataFrame({'object area': ecdf.x[1:], 'cumulative probability': ecdf.y[1:]})
    # create ecdf plot and apply log-scale for x-axis (areas)
    fig_ecdf = (ggplot(data=ecdf_df, mapping=aes(x='object area', y='cumulative probability'))
                + geom_point(size=.1)
                + scale_x_log10())
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)

    # Plot or print the ecdf
    _debug(visual=fig_ecdf,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_area_ecdf.png'))
    return fig_ecdf
