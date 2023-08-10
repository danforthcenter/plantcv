"""Plot Empirical Cumulative Distribution Function for Object Size."""
import os
import cv2
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _cv2_findcontours
from statsmodels.distributions.empirical_distribution import ECDF
import altair as alt


def obj_size_ecdf(mask):
    """
    Plot empirical cumulative distribution for object size based on binary mask.

    Inputs:
    mask  = binary mask

    Returns:
    chart = empirical cumulative distribution function plot

    :param mask: numpy.ndarray
    :return chart: altair.vegalite.v5.api.Chart
    """
    objects, _ = _cv2_findcontours(bin_img=mask)
    areas = [cv2.contourArea(cnt) for cnt in objects]
    # Remove objects with areas < 1px
    areas = [i for i in areas if i >= 1.0]

    ecdf = ECDF(areas, side='right')

    ecdf_df = pd.DataFrame({'object area': ecdf.x[1:], 'cumulative probability': ecdf.y[1:]})
    # create ecdf plot and apply log-scale for x-axis (areas)
    chart = alt.Chart(ecdf_df).mark_circle(size=10).encode(
        x=alt.X("object area:Q").scale(type='log'),
        y="cumulative probability:Q",
        tooltip=['object area', 'cumulative probability']
    ).interactive()

    # Plot or print the ecdf
    _debug(visual=chart,
           filename=os.path.join(params.debug_outdir, str(params.device) + '_area_ecdf.png'))
    return chart
