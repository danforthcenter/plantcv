# Help visualize histograms for hyperspectral images

import os
import numpy as np
import pandas as pd
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error, params, color_palette
from plotnine import ggplot, aes, geom_line, scale_color_manual, theme_classic, labels
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv.hyperspectral import _find_closest
import math


def _get_color_dict_uv():
    """Create a color dictionary for UV wavelengths."""
    params.color_scale = "cool_r"
    uv_wavelengths = np.arange(290, 444)
    uv_colors_ = color_palette(num=256)
    uv_colors_ = uv_colors_[0:len(uv_wavelengths)]
    uv_colors_ = [tuple([xi / 255 for xi in x]) for x in uv_colors_[::-1]]
    uv_colors = {}
    for i, wv in enumerate(uv_wavelengths):
        uv_colors[wv] = uv_colors_[i]
    return uv_colors


def _get_color_dict_vis():
    """Create a color dictionary for VIS wavelengths."""
    params.color_scale = "turbo"
    vis_wavelengths = np.arange(445, 701)
    vis_colors_ = color_palette(num=256)
    vis_colors_ = [tuple([xi / 255 for xi in x]) for x in vis_colors_]
    vis_colors = {}
    for i, wv in enumerate(vis_wavelengths):
        vis_colors[wv] = vis_colors_[i]
    return vis_colors


def _get_color_dict_nir():
    """Create a color dictionary for infrared wavelengths."""
    params.color_scale = "inferno"
    nir_wavelengths = np.arange(701, 1725)
    # nir_wavelengths = [_round_to_multiple(x, multiple=4, min_wv=701, max_wv=1725) for x in nir_wavelengths_]
    nir_colors_ = color_palette(num=256)
    nir_colors_ = [tuple([xi / 255 for xi in nir_colors_[math.floor(idx / 4)]]) for (idx, _) in
                   enumerate(nir_wavelengths)]
    nir_colors = {}
    for i, wv in enumerate(nir_wavelengths):
        nir_colors[wv] = nir_colors_[i]
    return nir_colors


def _rgb_to_webcode(rgb_values):
    """
    Convert RGB values to webcodes.

    Inputs:
    rgb_value: a tuple of RGB values (0~1, float)

    Returns:
    webcode: a webcode string encoding the RGB values
    """
    webcode = "#"
    for value in rgb_values:
        code_ = hex(int(value*255)).replace('0x', '')
        code = code_.upper() if len(code_) > 1 else '0{}'.format(code_.upper())
        webcode += code
    return webcode


def hyper_histogram(hsi, mask=None, bins=100, lower_bound=None, upper_bound=None,
                    title=None, wvlengths=[480, 550, 650]):
    """
    Plot a histograms of selected wavelengths from a hyperspectral image.
    
    This function calculates the histogram of selected wavelengths hyperspectral images
    The color of the histograms are based on the wavelength if the wavelength is in the range of visible spectrum;
    otherwise, random colors are assigned

    Inputs:
    hsi          = Hyperspectral data instance
    mask         = binary mask, if provided, calculate histogram from masked area only (default=None)
    bins         = divide the data into n evenly spaced bins (default=100)
    lower_bound  = the lower bound of the bins (x-axis min value) (default=None)
    upper_bound  = the upper bound of the bins (x-axis max value) (default=None)
    title        = a custom title for the plot (default=None)
    wvlengths    = (optional) list of wavelengths to show histograms (default = [480,550,670],  i.e. only show
                                                                    histograms for blue, green, and red bands)

    Returns:
    fig_hist      = histogram figure

    :param hsi: plantcv.plantcv.classes.Spectral_data
    :param mask: numpy.ndarray
    :param bins: int
    :param lower_bound: None, int, float
    :param upper_bound: None, int, float
    :param title: None, str
    :param wvlengths: list
    :return fig_hist: plotnine.ggplot.ggplot
    """

    # Always sort desired wavelengths
    wvlengths.sort()

    # Available wavelengths of the spectral data
    wl_keys = hsi.wavelength_dict.keys()
    wls = np.array([float(i) for i in wl_keys])
    wls.sort()

    # Spectral resolution of the spectral data
    diffs = [wls[i] - wls[i - 1] for i in range(1, len(wls))]
    spc_res = sum(diffs) / len(diffs)

    # Check if the distance is greater than 2x the spectral resolution
    # If the distance > 2x resolution, it is considered being out of available ranges
    checks = []
    for i in range(0, len(wvlengths)):
        checks.append(hsi.min_wavelength - wvlengths[i] > 2 * spc_res)
        checks.append(wvlengths[i] - hsi.max_wavelength > 2 * spc_res)
    if np.any(checks):
        fatal_error(f"At least one band is too far from the available wavelength range: "
                    f"({hsi.min_wavelength},{hsi.max_wavelength})!")

    # Find indices of bands whose wavelengths are closest to desired ones
    match_ids = [_find_closest(wls, wv) for wv in wvlengths]
    match_wls = [round(wls[i]) for i in match_ids]

    # prepare color dictionary(ies)
    color_dict = {}
    if any(x < 290 for x in match_wls):
        # under uv
        params.color_scale = "cool_r"
        color_ = color_palette(num=256)[-154]
        under_uv_colors_ = {}
        for i, wv in enumerate([x for x in match_wls if x < 290]):
            under_uv_colors_[wv] = color_
        color_dict = {**color_dict, **under_uv_colors_}
    if any(290 <= x < 445 for x in match_wls):
        uv_colors = _get_color_dict_uv()
        color_dict = {**color_dict, **uv_colors}
    if any(445 <= x < 701 for x in match_wls):
        vis_colors = _get_color_dict_vis()
        color_dict = {**color_dict, **vis_colors}
    if any(701 <= x < 1701 for x in match_wls):
        nir_colors = _get_color_dict_nir()
        color_dict = {**color_dict, **nir_colors}
    if any(x >= 1701 for x in match_wls):
        # above nir
        params.color_scale = "inferno"
        color_ = color_palette(num=256)[-1]
        above_uv_colors_ = {}
        for i, wv in enumerate([x for x in match_wls if x >= 1701]):
            above_uv_colors_[wv] = color_
        color_dict = {**color_dict, **above_uv_colors_}

    colors_rgb = [color_dict[wv] for wv in match_wls]
    colors_hex = [_rgb_to_webcode(x) for x in colors_rgb]

    array_data = hsi.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    histograms = dict()
    hist_dataset = pd.DataFrame(columns=['reflectance'])
    debug = params.debug
    params.debug = None

    # Create a dataframe for all histogram related information
    # (using the "histogram" function in "visualization" subpackage)
    for i_wv, (wv, color) in enumerate(zip(wvlengths, colors_hex)):
        idx = match_ids[i_wv]
        _, hist_data = histogram(array_data[:, :, idx], mask=mask, bins=bins, lower_bound=lower_bound,
                                 upper_bound=upper_bound, title=title, hist_data=True)
        histograms[wv] = {"label": wv, "graph_color": color, "reflectance": hist_data['pixel intensity'].tolist(),
                          "hist": hist_data['proportion of pixels (%)'].tolist()}
        if i_wv == 0:
            hist_dataset['reflectance'] = hist_data['pixel intensity'].tolist()
        hist_dataset[wv] = hist_data['proportion of pixels (%)'].tolist()

    # Make the histogram figure using plotnine
    df_hist = pd.melt(hist_dataset, id_vars=['reflectance'], value_vars=wvlengths,
                      var_name='Wavelength (' + hsi.wavelength_units + ')', value_name='proportion of pixels (%)')

    fig_hist = (ggplot(df_hist, aes(x='reflectance', y='proportion of pixels (%)',
                                    color='Wavelength (' + hsi.wavelength_units + ')'))
                + geom_line()
                + scale_color_manual(colors_hex, expand=(0, 0))
                + theme_classic()
                )
    if title is not None:
        fig_hist = fig_hist + labels.ggtitle(title)

    params.debug = debug
    _debug(fig_hist, filename=os.path.join(params.debug_outdir, str(params.device) + '_histogram.png'))

    return fig_hist
