# Plot Empirical Cumulative Distribution Function for Object Size

import os
import cv2
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from statsmodels.distributions.empirical_distribution import ECDF
from plotnine import ggplot, aes, geom_point, labels, scale_color_manual

def obj_size(mask, title=None):
# def obj_size(img, mask, title=None):
    # mask1 = np.copy(mask)
    # ori_img = np.copy(img)
    # if len(np.shape(ori_img)) == 2:
    #     ori_img = cv2.cvtColor(ori_img, cv2.COLOR_GRAY2BGR)
    #
    # objects, hierarchy = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    objects, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    areas = [cv2.contourArea(cnt) for cnt in objects]

    ecdf = ECDF(areas, side='right')

    ecdf_df = pd.DataFrame({'object area': ecdf.x, 'cumulative probability': ecdf.y})
    fig_ecdf = (ggplot(data=ecdf_df,
                       mapping=aes(x='object area', y='cumulative probability'))
                + geom_point(size=.1))
    if title is not None:
        fig_ecdf = fig_ecdf + labels.ggtitle(title)

    # Plot or print the histogram
    _debug(visual=fig_ecdf, filename=os.path.join(params.debug_outdir, str(params.device) + '_area_ecdf.png'))
    return fig_ecdf

