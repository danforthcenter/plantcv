"""Help visualize histograms for hyperspectral images."""
import os
import numpy as np
import pandas as pd
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error, params, color_palette
from plantcv.plantcv.hyperspectral import _find_closest
from plantcv.plantcv.visualize import histogram
import altair as alt
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
        code = code_.upper() if len(code_) > 1 else f'0{code_.upper()}'
        webcode += code
    return webcode


def assign_color(wavelength):
    """
    Assigns a color to a given wavelength based on predefined wavelength ranges.
    Inputs:
    - wavelength (int): The wavelength for which to assign a color.

    Returns:
    - color (str or None): The color assigned to the wavelength.
                           Returns None if the wavelength is not within any predefined range.
    """
    if wavelength < 290:
        # under uv
        return color_palette(num=256)[-154]
    if 290 <= wavelength < 445:
        # uv
        uv_colors = _get_color_dict_uv()
        return uv_colors.get(wavelength)
    if 445 <= wavelength < 701:
        # visible
        vis_colors = _get_color_dict_vis()
        return vis_colors.get(wavelength)
    if 701 <= wavelength < 1701:
        # nir
        nir_colors = _get_color_dict_nir()
        return nir_colors.get(wavelength)
    # above nir
    return color_palette(num=256)[-1]


def hyper_histogram(hsi, mask=None, bins=100, lower_bound=None, upper_bound=None,
                    title=None, wvlengths=None):
    """Plot a histograms of selected wavelengths from a hyperspectral image.

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
    :return fig_hist: altair.vegalite.v5.api.Chart
    """
    # Use default wavelengths if none given
    if wvlengths is None:
        wvlengths = [480, 550, 650]
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
    color_dict = {wavelength: assign_color(wavelength) for wavelength in match_wls}
    colors_rgb = [color_dict[wv] for wv in match_wls]
    colors_hex = [_rgb_to_webcode(x) for x in colors_rgb]

    array_data = hsi.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    histograms = {}
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

    # Make the histogram figure using pandas and altair
    df_hist = pd.melt(hist_dataset, id_vars=['reflectance'], value_vars=wvlengths,
                      var_name='Wavelength (' + hsi.wavelength_units + ')', value_name='proportion of pixels (%)')

    fig_hist = alt.Chart(df_hist).mark_line().encode(
        x="reflectance",
        y="proportion of pixels (%)",
        color=alt.Color('Wavelength (' + hsi.wavelength_units + ')').scale(scheme='turbo'),
        tooltip=['Wavelength (' + hsi.wavelength_units + ')']
        ).interactive()

    if title is not None:
        fig_hist.properties(title=title)

    params.debug = debug
    _debug(fig_hist, filename=os.path.join(params.debug_outdir, str(params.device) + '_histogram.png'))

    return fig_hist
