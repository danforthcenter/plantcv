# Plot histogram

import cv2
import os
import numpy as np
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import params
import pandas as pd
from plotnine import ggplot, aes, geom_line, scale_x_continuous, labels



def histogram(gray_img, mask=None, bins=256, color='red', title=None):
    """Plot a histogram using ggplot.

    Inputs:
    gray_img = grayscale image to analyze
    mask     = binary mask made from selected contours
    bins     = number of classes to divide spectrum into
    color    = color of the line drawn
    title    = custom title for the plot gets drawn if title is not None

    :param gray_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param color: str
    :param title: str
    :return fig_hist: ggplot
    """

    params.device += 1
    debug = params.debug
    # Apply mask if one is supplied
    if mask is not None:
        # apply plant shaped mask to image
        params.debug=None
        mask1 = binary_threshold(mask, 0, 255, 'light')
        mask1 = (mask1 / 255)
        masked = np.multiply(gray_img, mask1)
    else:
        masked = gray_img

    if gray_img.dtype == 'uint16':
        maxval = 65536
    else:
        maxval = 256

    # Store histogram data
    hist_gray_data, hist_bins = np.histogram(masked, bins, (1, maxval))
    hist_bins1 = hist_bins[:-1]
    hist_bins2 = [l for l in hist_bins1]
    hist_gray = [l for l in hist_gray_data]
    # make hist percentage for plotting
    pixels = cv2.countNonZero(masked)
    hist_percent = (hist_gray_data / float(pixels)) * 100

    hist_x = hist_percent
    bin_labels = np.arange(0, bins)
    dataset = pd.DataFrame({'Grayscale pixel intensity': bin_labels,
                            'Proportion of pixels (%)': hist_x})
    if title is None:
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Grayscale pixel intensity',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color=color)
                    + scale_x_continuous(breaks=list(range(0, bins, 25))))
    elif title is not None:
        fig_hist = (ggplot(data=dataset,
                           mapping=aes(x='Grayscale pixel intensity',
                                       y='Proportion of pixels (%)'))
                    + geom_line(color=color)
                    + scale_x_continuous(breaks=list(range(0, bins, 25)))
                    + labels.ggtitle(title))
    params.debug=debug
    if params.debug is not None:
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_hist.png'))
        if params.debug == "plot":
            print(fig_hist)

    return fig_hist
