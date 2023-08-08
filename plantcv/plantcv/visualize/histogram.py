"""Visualize histograms from image data."""
import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
import pandas as pd
import altair as alt


def _hist_gray(gray_img, bins, lower_bound, upper_bound, mask=None):
    """Prepare the ready to plot histogram data.

    Inputs:
    gray_img       = grayscale image to analyze
    bins           = divide the data into n evenly spaced bins
    lower_bound    = the lower bound of the bins (x-axis min value)
    upper_bound    = the upper bound of the bins (x-axis max value)
    mask           = binary mask, calculate histogram from masked area only (default=None)

    Returns:
    bin_labels     = an array of histogram bin labels
    hist_percent   = an array of histogram represented by percent values
    hist_gray_data = an array of histogram (original values)

    :param gray_img: numpy.ndarray
    :param bins: int
    :param lower_bound: int
    :param upper_bound: int
    :param mask: numpy.ndarray
    :return bin_labels: numpy.ndarray
    :return hist_percent: numpy.ndarray
    :return hist_gray_data: numpy.ndarray
    """
    params.device += 1
    # Create a dummy mask if none was supplied
    if mask is None:
        mask = np.ones(gray_img.shape, dtype=np.uint8)

    # Apply mask
    pixels = len(np.where(mask > 0)[0])
    masked = gray_img[np.where(mask > 0)]

    # Store histogram data
    hist_gray_data, hist_bins = np.histogram(masked, bins, (lower_bound, upper_bound))

    # make hist percentage for plotting
    hist_percent = (hist_gray_data / float(pixels)) * 100
    # use middle value of every bin as bin label
    bin_labels = np.array([np.average([hist_bins[i], hist_bins[i+1]]) for i in range(0, len(hist_bins) - 1)])

    return bin_labels, hist_percent, hist_gray_data
    # hist_data = pd.DataFrame({'pixel intensity': bin_labels, 'proportion of pixels (%)': hist_percent})
    # return hist_data


def histogram(img, mask=None, bins=100, lower_bound=None, upper_bound=None, title=None, hist_data=False):
    """Plot histograms of each input image channel.

    Inputs:
    img            = an RGB or grayscale image to analyze
    mask           = binary mask, calculate histogram from masked area only (default=None)
    bins           = divide the data into n evenly spaced bins (default=100)
    lower_bound    = the lower bound of the bins (x-axis min value) (default=None)
    upper_bound    = the upper bound of the bins (x-axis max value) (default=None)
    title          = a custom title for the plot (default=None)
    hist_data      = return the frequency distribution data if True (default=False)

    Returns:
    chart          = histogram figure
    hist_df        = dataframe with histogram data, with columns "pixel intensity" and "proportion of pixels (%)"

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param lower_bound: int
    :param upper_bound: int
    :param title: str
    :param hist_data: bool
    :return chart: altair.vegalite.v5.api.Chart
    :return hist_df: pandas.core.frame.DataFrame
    """
    if not isinstance(img, np.ndarray):
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

    if len(img.shape) > 2:
        if img.shape[2] == 3:
            b_names = ['blue', 'green', 'red']
        else:
            b_names = [str(i) for i in range(img.shape[2])]

    if len(img.shape) == 2:
        bin_labels, hist_percent, hist_ = _hist_gray(img, bins=bins, lower_bound=lower_bound, upper_bound=upper_bound,
                                                     mask=mask)
        hist_df = pd.DataFrame(
            {'pixel intensity': bin_labels, 'proportion of pixels (%)': hist_percent, 'hist_count': hist_,
             'color channel': ['0' for _ in range(len(hist_percent))]})
    else:
        # Assumption: RGB image
        # Initialize dataframe column arrays
        px_int = np.array([])
        prop = np.array([])
        hist_count = np.array([])
        channel = []
        for (b, b_name) in enumerate(b_names):
            bin_labels, hist_percent, hist_ = _hist_gray(img[:, :, b], bins=bins, lower_bound=lower_bound,
                                                         upper_bound=upper_bound, mask=mask)
            # Append histogram data for each channel
            px_int = np.append(px_int, bin_labels)
            prop = np.append(prop, hist_percent)
            hist_count = np.append(hist_count, hist_)
            channel = channel + [b_name for _ in range(len(hist_percent))]
        # Create dataframe
        hist_df = pd.DataFrame(
            {'pixel intensity': px_int, 'proportion of pixels (%)': prop, 'hist_count': hist_count,
             'color channel': channel})

    # Create an altair chart
    chart = alt.Chart(hist_df).mark_line(point=True).encode(
        x="pixel intensity",
        y="proportion of pixels (%)",
        color="color channel",
        tooltip=['pixel intensity', 'proportion of pixels (%)']
        ).interactive()

    if title is not None:
        chart = chart.properties(title=title)

    if len(img.shape) > 2 and img.shape[2] == 3:
        # Add a blue, green, red color scale if the image is RGB
        chart = chart.configure_range(category=['blue', 'green', 'red'])

    # Plot or print the histogram
    _debug(visual=chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_hist.png'))

    if hist_data is True:
        return chart, hist_df
    return chart
