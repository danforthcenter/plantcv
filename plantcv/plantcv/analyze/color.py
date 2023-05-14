import os
import cv2
import numpy as np
import pandas as pd
from scipy import stats
from plotnine import ggplot, aes, geom_line, scale_x_continuous, scale_color_manual, labs
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import outputs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def color(rgb_img, labeled_mask, n_labels=1, colorspaces="all", label="default"):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    rgb_img          = RGB image data
    mask             = Binary mask made from selected contours
    hist_plot_type   = None, 'all', 'rgb','lab' or 'hsv' (to be deprecated)
    colorspaces      = 'all', 'rgb', 'lab', or 'hsv'
    label            = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_image   = histogram output

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param colorspaces: str
    :param label: str
    :return analysis_images: list
    """
    img = _iterate_analysis(img=rgb_img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_color,
                            **{"colorspaces": colorspaces})
    return img


def _analyze_color(img, mask, colorspaces="all", label="default"):
    """Analyze the color properties of an image object
    Inputs:
    img              = RGB image data
    mask             = Binary mask made from selected contours
    hist_plot_type   = None, 'all', 'rgb','lab' or 'hsv' (to be deprecated)
    colorspaces      = 'all', 'rgb', 'lab', or 'hsv'
    label            = optional label parameter, modifies the variable name of observations recorded

    Returns:
    analysis_image   = histogram output

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param colorspaces: str
    :param label: str
    :return analysis_images: list
    """
    # Save user debug setting
    debug = params.debug
    if len(np.shape(img)) < 3:
        fatal_error("rgb_img must be an RGB image")

    # Mask the input image
    masked = cv2.bitwise_and(img, img, mask=mask)
    # Extract the blue, green, and red channels
    b, g, r = cv2.split(masked)
    # Convert the BGR image to LAB
    lab = cv2.cvtColor(masked, cv2.COLOR_BGR2LAB)
    # Extract the lightness, green-magenta, and blue-yellow channels
    l, m, y = cv2.split(lab)
    # Convert the BGR image to HSV
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    # Extract the hue, saturation, and value channels
    h, s, v = cv2.split(hsv)

    # Color channel dictionary
    channels = {"b": b, "g": g, "r": r, "l": l, "m": m, "y": y, "h": h, "s": s, "v": v}

    # Histogram plot types
    hist_types = {"all": ("b", "g", "r", "l", "m", "y", "h", "s", "v"),
                  "rgb": ("b", "g", "r"),
                  "lab": ("l", "m", "y"),
                  "hsv": ("h", "s", "v")}

    if colorspaces.lower() not in hist_types:
        fatal_error(f"Colorspace '{colorspaces}' is not supported, must be be one of the following: "
                    f"{', '.join(map(str, hist_types.keys()))}")

    # Calculate histogram
    params.debug = None
    histograms = {
        "b": {"label": "blue", "graph_color": "blue",
              "hist": histogram(channels["b"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "g": {"label": "green", "graph_color": "forestgreen",
              "hist": histogram(channels["g"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "r": {"label": "red", "graph_color": "red",
              "hist": histogram(channels["r"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "l": {"label": "lightness", "graph_color": "dimgray",
              "hist": histogram(channels["l"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "m": {"label": "green-magenta", "graph_color": "magenta",
              "hist": histogram(channels["m"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "y": {"label": "blue-yellow", "graph_color": "yellow",
              "hist": histogram(channels["y"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "h": {"label": "hue", "graph_color": "blueviolet",
              "hist": histogram(channels["h"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "s": {"label": "saturation", "graph_color": "cyan",
              "hist": histogram(channels["s"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()},
        "v": {"label": "value", "graph_color": "orange",
              "hist": histogram(channels["v"], mask, 256, 0, 255,
                                hist_data=True)[1]['proportion of pixels (%)'].tolist()}
    }

    # Restore user debug setting
    params.debug = debug

    # Create list of bin labels for 8-bit data
    binval = np.arange(0, 256)

    # Create a dataframe of bin labels and histogram data
    dataset = pd.DataFrame({'bins': binval, 'blue': histograms["b"]["hist"],
                            'green': histograms["g"]["hist"], 'red': histograms["r"]["hist"],
                            'lightness': histograms["l"]["hist"], 'green-magenta': histograms["m"]["hist"],
                            'blue-yellow': histograms["y"]["hist"], 'hue': histograms["h"]["hist"],
                            'saturation': histograms["s"]["hist"], 'value': histograms["v"]["hist"]})
    # Make the histogram figure using plotnine
    fig_opts = {
        "RGB": {
            "value_vars": ["blue", "green", "red"],
            "plot_colors": ["blue", "green", "red"]
        },
        "LAB": {
            "value_vars": ["lightness", "green-magenta", "blue-yellow"],
            "plot_colors": ["yellow", "magenta", "dimgray"]
        },
        "HSV": {
            "value_vars": ["hue", "saturation", "value"],
            "plot_colors": ["blueviolet", "cyan", "orange"]
        },
        "ALL": {
            "value_vars": ["blue", "green", "red", "lightness", "green-magenta", "blue-yellow", "hue", "saturation", "value"],
            "plot_colors": ["blue", "green", "red", "yellow", "magenta", "dimgray", "blueviolet", "cyan", "orange"]
        }
    }
    df = pd.melt(dataset, id_vars=['bins'], value_vars=fig_opts[colorspaces.upper()]["value_vars"],
                 var_name='color Channel', value_name='proportion of pixels (%)')
    hist_fig = (ggplot(df, aes(x='bins', y='proportion of pixels (%)', color='color Channel')) +
                geom_line() +
                scale_x_continuous(breaks=list(range(0, 256, 25))) +
                scale_color_manual(fig_opts[colorspaces.upper()]["plot_colors"])
                )

    hist_fig = hist_fig + labs(x="Pixel intensity", y="Proportion of pixels (%)")

    # Hue values of zero are red but are also the value for pixels where hue is undefined. The hue value of a pixel will
    # be undef. when the color values are saturated. Therefore, hue values of 0 are excluded from the calculations below
    # Calculate the median hue value (median is rescaled from the encoded 0-179 range to the 0-359 degree range)
    hue_median = np.median(h[np.where(h > 0)]) * 2

    # Calculate the circular mean and standard deviation of the encoded hue values
    # The mean and standard-deviation are rescaled from the encoded 0-179 range to the 0-359 degree range
    hue_circular_mean = stats.circmean(h[np.where(h > 0)], high=179, low=0) * 2
    hue_circular_std = stats.circstd(h[np.where(h > 0)], high=179, low=0) * 2

    # Plot or print the histogram
    analysis_image = hist_fig
    _debug(visual=hist_fig, filename=os.path.join(params.debug_outdir, str(params.device) + '_analyze_color_hist.png'))

    # Store into global measurements
    # RGB signal values are in an unsigned 8-bit scale of 0-255
    rgb_values = list(range(0, 256))
    # Hue values are in a 0-359 degree scale, every 2 degrees at the midpoint of the interval
    hue_values = [i * 2 + 1 for i in range(0, 180)]
    # Percentage values on a 0-100 scale (lightness, saturation, and value)
    percent_values = [round((i / 255) * 100, 2) for i in range(0, 256)]
    # Diverging values on a -128 to 127 scale (green-magenta and blue-yellow)
    diverging_values = list(range(-128, 128))

    if colorspaces.upper() in ('RGB', 'ALL'):
        outputs.add_observation(sample=label, variable='blue_frequencies', trait='blue frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["b"]["hist"], label=rgb_values)
        outputs.add_observation(sample=label, variable='green_frequencies', trait='green frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["g"]["hist"], label=rgb_values)
        outputs.add_observation(sample=label, variable='red_frequencies', trait='red frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["r"]["hist"], label=rgb_values)

    if colorspaces.upper() in ('LAB', 'ALL'):
        outputs.add_observation(sample=label, variable='lightness_frequencies', trait='lightness frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["l"]["hist"], label=percent_values)
        outputs.add_observation(sample=label, variable='green-magenta_frequencies',
                                trait='green-magenta frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["m"]["hist"], label=diverging_values)
        outputs.add_observation(sample=label, variable='blue-yellow_frequencies', trait='blue-yellow frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["y"]["hist"], label=diverging_values)

    if colorspaces.upper() in ('HSV', 'ALL'):
        outputs.add_observation(sample=label, variable='hue_frequencies', trait='hue frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["h"]["hist"][0:180], label=hue_values)
        outputs.add_observation(sample=label, variable='saturation_frequencies', trait='saturation frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["s"]["hist"], label=percent_values)
        outputs.add_observation(sample=label, variable='value_frequencies', trait='value frequencies',
                                method='plantcv.plantcv.analyze_color', scale='frequency', datatype=list,
                                value=histograms["v"]["hist"], label=percent_values)

    # Always save hue stats
    outputs.add_observation(sample=label, variable='hue_circular_mean', trait='hue circular mean',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_circular_mean, label='degrees')
    outputs.add_observation(sample=label, variable='hue_circular_std', trait='hue circular standard deviation',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_circular_std, label='degrees')
    outputs.add_observation(sample=label, variable='hue_median', trait='hue median',
                            method='plantcv.plantcv.analyze_color', scale='degrees', datatype=float,
                            value=hue_median, label='degrees')

    # Store images
    outputs.images.append(analysis_image)

    return img
