# Plot histogram

import os
import numpy as np
from plantcv.plantcv.threshold import binary as binary_threshold
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
import pandas as pd
from plotnine import ggplot, aes, geom_line, scale_x_continuous, labels, scale_color_manual


def _hist_gray(gray_img, bins, lower_bound, upper_bound, mask=None):
    """ Prepare the ready to plot histogram data
    :param gray_img: (numpy.ndarray) = grayscale image to analyze
    :param bins: (int) number of classes to divide spectrum into
    :param lower_bound: (int) the lower bound of the bins
    :param upper_bound: (int) the upper bound of the bins
    :param mask: (numpy.ndarray) = (optional) binary mask made from selected contours, by default mask = None

    :return:
    bin_labels (numpy.ndarray): an array of histogram bin labels
    hist_percent (numpy.ndarray): an array of histogram represented by percent values
    hist_gray_data (numpy.ndarray): an array of histogram (original values)
    """

    params.device += 1
    debug = params.debug

    # Apply mask if one is supplied
    if mask is not None:
        min_val = np.min(gray_img)
        pixels = len(np.where(mask > 0)[0])
        # apply plant shaped mask to image
        params.debug = None
        mask1 = binary_threshold(mask, 0, 255, 'light')
        mask1 = (mask1 / 255)
        masked = np.where(mask1 != 0, gray_img, min_val - 5000)

    else:
        pixels = gray_img.shape[0] * gray_img.shape[1]
        masked = gray_img

    params.debug = debug

    # Store histogram data
    hist_gray_data, hist_bins = np.histogram(masked, bins, (lower_bound, upper_bound))

    # make hist percentage for plotting
    hist_percent = (hist_gray_data / float(pixels)) * 100
    # use middle value of every bin as bin label
    bin_labels   = np.array([np.average([hist_bins[i],hist_bins[i+1]]) for i in range(0,len(hist_bins)-1)])

    return bin_labels, hist_percent, hist_gray_data
    # hist_data = pd.DataFrame({'pixel intensity': bin_labels, 'proportion of pixels (%)': hist_percent})
    # return hist_data


def histogram(img, mask=None, bins=100, lower_bound=None, upper_bound=None, title=None):
    """Plot a histogram using ggplot
    :param img: (numpy.ndarray) = image to analyze
    :param mask: (numpy.ndarray) = (optional) binary mask made from selected contours, by default mask = None
    :param bins: (int) number of classes to divide spectrum into, by default bins = 256
    :param lower_bound: (int) the lower range of the bins, by default lower_bound = None
    :param upper_bound: (int) the upper range of the bins, by default upper_bound = None
    :param title: (str) custom title for the plot gets drawn if title is not None, by default title = None
    :return:
    fig_hist: ggplot
    hist_data: dataframe with histogram data, with columns "pixel intensity" and "proportion of pixels (%)", Ready to be used for ggplot
    """
    if type(img) is not np.ndarray:
        fatal_error("Only image of type numpy.ndarray is supported input!")
    if len(img.shape) < 2:
        fatal_error("Input image should be at least a 2d array!")

    if mask is not None:
        masked = img[np.where(mask > 0)]
        img_min, img_max = np.nanmin(masked), np.nanmax(masked)
    else:
        img_min, img_max = np.nanmin(img), np.nanmax(img)

    # for lower / upper bound, if given, use the given value, otherwise, use the min / max of the image
    lower_bound = lower_bound if lower_bound is not None else img_min
    upper_bound = upper_bound if upper_bound is not None else img_max

    params.device += 1

    if len(img.shape) > 2:
        if img.shape[2] == 3:
            b_names = ['blue', 'green', 'red']
        else:
            b_names = [str(i) for i in range(img.shape[2])]

    if len(img.shape) == 2:
        bin_labels, hist_percent, hist_ = _hist_gray(img, bins=bins, lower_bound=lower_bound, upper_bound=upper_bound,
                                                     mask=mask)
        hist_data = pd.DataFrame(
            {'pixel intensity': bin_labels, 'proportion of pixels (%)': hist_percent, 'hist_count': hist_,
             'color channel': ['0' for i in range(len(hist_percent))]})
    else:
        # Assumption: RGB image
        for (b, b_name) in enumerate(b_names):
            bin_labels, hist_percent, hist_ = _hist_gray(img[:, :, b], bins=bins, lower_bound=lower_bound,
                                                         upper_bound=upper_bound, mask=mask)
            hist_temp = pd.DataFrame(
                {'pixel intensity': bin_labels, 'proportion of pixels (%)': hist_percent, 'hist_count': hist_,
                 'color channel': [b_name for i in range(len(hist_percent))]})
            if b == 0:
                hist_data = hist_temp
            else:
                hist_data = hist_data.append(hist_temp)

    fig_hist = (ggplot(data=hist_data,
                       mapping=aes(x='pixel intensity', y='proportion of pixels (%)', color='color channel'))
                + geom_line())

    if title is not None:
        fig_hist = fig_hist + labels.ggtitle(title)
    if len(img.shape) > 2 and img.shape[2] == 3:
        fig_hist = fig_hist + scale_color_manual(['blue', 'green', 'red'])
    if params.debug is not None:
        if params.debug == "print":
            fig_hist.save(os.path.join(params.debug_outdir, str(params.device) + '_hist.png'), verbose=False)
        if params.debug == "plot":
            print(fig_hist)

    return fig_hist, hist_data