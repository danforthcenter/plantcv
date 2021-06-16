# Help visualize histograms for hyperspectral images

import os
import numpy as np
import pandas as pd
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error, params, color_palette
from plotnine import ggplot, aes, geom_line, scale_color_manual, theme_classic
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv.hyperspectral import _find_closest
from scipy.spatial import distance
import colour


def _rgb_to_webcode(rgb_values):
    """
    RGB_value: a tuple of RGB values (0~255, uint8)
    """
    webcode = "#"
    for value in rgb_values:
        code_ = hex(value).replace('0x', '')
        code = code_.upper() if len(code_) > 1 else '0{}'.format(code_.upper())
        webcode += code
    return webcode


def hyper_histogram(array, mask=None, bins=100, lower_bound=None, upper_bound=None,
                    title=None, wvlengths=[480, 550, 670]):
    """This function calculates the histogram of selected wavelengths hyperspectral images
    The color of the histogram is based on the wavelength: if the wavelength is in the range of visible spectrum
    Inputs:
    array        = Hyperspectral data instance
    mask         = Binary mask made from selected contours
    wvlengths    = (optional) list of wavelengths to show histograms. default = [480,550,670]

    Returns:
    fig_hist = histogram figure

    :param array: plantcv.plantcv.classes.Spectral_data
    :param mask: numpy.ndarray
    :param bins: int
    :param lower_bound: None, int, float
    :param upper_bound: None, int, float
    :param title: None, str
    :param wvlengths: list
    :return fig_hist: plotnine.ggplot.ggplot
    """

    # always sort desired wavelengths
    wvlengths.sort()

    wl_keys = array.wavelength_dict.keys()
    wls = np.array([float(i) for i in wl_keys])

    # spectral resolution of the spectral data
    diffs = [wls[i] - wls[i - 1] for i in range(1, len(wls))]
    spc_res = sum(diffs) / len(diffs)

    # check if the distance is greater than 2x the spectral resolution
    checks = []
    for i in range(0, len(wvlengths)):
        checks.append(array.min_wavelength - wvlengths[i] > 2 * spc_res)
        checks.append(wvlengths[i] - array.max_wavelength > 2 * spc_res)

    if np.any(checks):
        fatal_error(f"At least one band is too far from the available wavelength range: "
                    f"({array.min_wavelength},{array.max_wavelength})!")

    # find indices of bands whose wavelengths are closest to desired ones
    match_ids = [_find_closest(wls, wv) for wv in wvlengths]

    # check if in the visible wavelengths range
    ids_vis = [idx for (idx, wv) in enumerate(wvlengths) if 390 <= wv <= 830]
    # invisible wavelengths
    ids_inv = [idx for (idx, wv) in enumerate(wvlengths) if wv < 390 or wv > 830]

    colors = [tuple(x) for x in color_palette(len(wvlengths))]
    if len(ids_vis) < len(wvlengths):
        print("Warning: at least one of the desired wavelengths is not in the visible spectrum range!")
        # if len(ids_inv) == len(wvlengths): # All wavelengths in invisible range
        #     colors = [tuple(x) for x in color_palette(len(wvlengths))]
    if len(ids_inv) < len(wvlengths):
        colors_vis = []
        colors_inv = colors

        # Color matching function
        cmfs = colour.MSDS_CMFS["CIE 2012 10 Degree Standard Observer"]
        matrix = np.array([[3.24062548, -1.53720797, -0.49862860],
                           [-0.96893071, 1.87575606, 0.04151752],
                           [0.05571012, -0.20402105, 1.05699594]]
                          )
        for i in ids_vis:
            # colors_vis.append(_wavelength_to_rgb(wvlengths[i], gamma=0.8))
            # color_vis = _wavelength_to_rgb(wvlengths[i], gamma=0.8)
            # Convert wavelength to RGB
            rgb = colour.XYZ_to_RGB(colour.wavelength_to_XYZ(wvlengths[i], cmfs),
                                    illuminant_XYZ=np.array([0.9, 0.9]),
                                    illuminant_RGB=np.array([0.9, 0.9]),
                                    chromatic_adaptation_transform="Bradford",
                                    matrix_XYZ_to_RGB=matrix)
            # Set negative values to zero before scaling
            rgb[np.where(rgb < 0)] = 0
            # Convert float RGB to 8-bit unsigned integer
            color_vis = colour.io.convert_bit_depth(rgb, "uint8")
            colors_vis.append(color_vis)
        # calculate the distances between every pair of (R,G,B) colors
        dists = distance.cdist(colors_vis, colors_inv, 'euclidean')
        # exclude those colors "too close" to visible colors
        exclude = np.argmin(dists, axis=1)
        colors_inv = [c for (i, c) in enumerate(colors_inv) if i not in exclude]
        j_vis, j_inv = 0, 0
        colors = []
        for i in range(0, len(wvlengths)):
            if i in ids_vis:
                colors.append(colors_vis[j_vis])
                j_vis += 1
            else:
                colors.append(colors_inv[j_inv])
                j_inv += 1

    array_data = array.array_data

    # List of wavelengths recorded created from parsing the header file will be string, make list of floats
    histograms = dict()
    hist_dataset = pd.DataFrame(columns=['reflectance'])
    debug = params.debug
    params.debug = None
    color_codes = []

    for i_wv, (wv, color) in enumerate(zip(wvlengths, colors)):
        idx = match_ids[i_wv]
        code_c = _rgb_to_webcode(color)
        color_codes.append(code_c)
        _, hist_data = histogram(array_data[:, :, idx], mask=mask, bins=bins, lower_bound=lower_bound,
                                 upper_bound=upper_bound, title=title, hist_data=True)
        histograms[wv] = {"label": wv, "graph_color": code_c, "reflectance": hist_data['pixel intensity'].tolist(),
                          "hist": hist_data['proportion of pixels (%)'].tolist()}
        if i_wv == 0:
            hist_dataset['reflectance'] = hist_data['pixel intensity'].tolist()
        hist_dataset[wv] = hist_data['proportion of pixels (%)'].tolist()

    # Make the histogram figure using plotnine
    df_hist = pd.melt(hist_dataset, id_vars=['reflectance'], value_vars=wvlengths,
                      var_name='Wavelength (' + array.wavelength_units + ')', value_name='proportion of pixels (%)')

    fig_hist = (ggplot(df_hist, aes(x='reflectance', y='proportion of pixels (%)',
                                    color='Wavelength (' + array.wavelength_units + ')'))
                + geom_line()
                + scale_color_manual(color_codes, expand=(0, 0))
                + theme_classic()
                )
    params.debug = debug
    _debug(fig_hist, filename=os.path.join(params.debug_outdir, str(params.device) + '_histogram.png'))

    return fig_hist
