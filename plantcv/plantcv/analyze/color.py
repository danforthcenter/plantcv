"""Analyzes the color properties of objects in an image."""
import os
import cv2
import numpy as np
from scipy import stats
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import outputs
from plantcv.plantcv.visualize import histogram
from plantcv.plantcv._helpers import _iterate_analysis


def color(rgb_img, labeled_mask, n_labels=1, colorspaces="hsv", label=None):
    """A function that analyzes the color of objects and outputs data.

    Inputs:
    rgb_img          = RGB image data.
    labeled_mask     = Labeled mask of objects (32-bit).
    n_labels         = Total number expected individual objects (default = 1).
    colorspaces      = 'all', 'rgb', 'lab', or 'hsv' (default = 'hsv').
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image   = histogram output

    :param rgb_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param colorspaces: str
    :param label: str
    :return analysis_images: list
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    _ = _iterate_analysis(img=rgb_img, labeled_mask=labeled_mask, n_labels=n_labels, label=label, function=_analyze_color,
                          **{"colorspaces": colorspaces})
    hue_chart = outputs.plot_dists(variable="hue_frequencies")
    _debug(visual=hue_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_hue_hist.png'))
    return hue_chart


def _analyze_color(img, mask, colorspaces="hsv", label=None):
    """Analyze the color properties of an image object
    Inputs:
    img              = RGB image data
    mask             = Binary mask made from selected contours
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
    # Initialize output data
    # Histogram plot types
    hist_types = {"all": ("b", "g", "r", "l", "m", "y", "h", "s", "v"),
                  "rgb": ("b", "g", "r"),
                  "lab": ("l", "m", "y"),
                  "hsv": ("h", "s", "v")}

    if colorspaces.lower() not in hist_types:
        fatal_error(f"Colorspace '{colorspaces}' is not supported, must be be one of the following: "
                    f"{', '.join(map(str, hist_types.keys()))}")

    # Empty histograms
    histograms = {
        "b": {"label": "blue", "graph_color": "blue",
              "hist": [0] * 256},
        "g": {"label": "green", "graph_color": "forestgreen",
              "hist": [0] * 256},
        "r": {"label": "red", "graph_color": "red",
              "hist": [0] * 256},
        "l": {"label": "lightness", "graph_color": "dimgray",
              "hist": [0] * 256},
        "m": {"label": "green-magenta", "graph_color": "magenta",
              "hist": [0] * 256},
        "y": {"label": "blue-yellow", "graph_color": "yellow",
              "hist": [0] * 256},
        "h": {"label": "hue", "graph_color": "blueviolet",
              "hist": [0] * 256},
        "s": {"label": "saturation", "graph_color": "cyan",
              "hist": [0] * 256},
        "v": {"label": "value", "graph_color": "orange",
              "hist": [0] * 256}
    }

    # Undefined defaults
    hue_median = np.nan
    hue_circular_mean = np.nan
    hue_circular_std = np.nan

    # Skip empty masks
    if np.count_nonzero(mask) != 0:
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

        # Calculate histogram
        params.debug = None
        for channel in hist_types["all"]:
            histograms[channel]["hist"] = histogram(channels[channel], mask, 256, 0, 255,
                                                    hist_data=True)[1]['proportion of pixels (%)'].tolist()

        # Restore user debug setting
        params.debug = debug

        # Hue values of zero are red but are also the value for pixels where hue is undefined. The hue value of a pixel will
        # be undef. when the color values are saturated. Therefore, hue values of 0 are excluded from the calculations below
        # Calculate the median hue value (median is rescaled from the encoded 0-179 range to the 0-359 degree range)
        hue_median = np.median(h[np.where(h > 0)]) * 2

        # Calculate the circular mean and standard deviation of the encoded hue values
        # The mean and standard-deviation are rescaled from the encoded 0-179 range to the 0-359 degree range
        hue_circular_mean = stats.circmean(h[np.where(h > 0)], high=179, low=0) * 2
        hue_circular_std = stats.circstd(h[np.where(h > 0)], high=179, low=0) * 2

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
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["b"]["hist"], label=rgb_values)
        outputs.add_observation(sample=label, variable='green_frequencies', trait='green frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["g"]["hist"], label=rgb_values)
        outputs.add_observation(sample=label, variable='red_frequencies', trait='red frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["r"]["hist"], label=rgb_values)

    if colorspaces.upper() in ('LAB', 'ALL'):
        outputs.add_observation(sample=label, variable='lightness_frequencies', trait='lightness frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["l"]["hist"], label=percent_values)
        outputs.add_observation(sample=label, variable='green-magenta_frequencies',
                                trait='green-magenta frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["m"]["hist"], label=diverging_values)
        outputs.add_observation(sample=label, variable='blue-yellow_frequencies', trait='blue-yellow frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["y"]["hist"], label=diverging_values)

    if colorspaces.upper() in ('HSV', 'ALL'):
        outputs.add_observation(sample=label, variable='hue_frequencies', trait='hue frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["h"]["hist"][0:180], label=hue_values)
        outputs.add_observation(sample=label, variable='saturation_frequencies', trait='saturation frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["s"]["hist"], label=percent_values)
        outputs.add_observation(sample=label, variable='value_frequencies', trait='value frequencies',
                                method='plantcv.plantcv.analyze.color', scale='frequency', datatype=list,
                                value=histograms["v"]["hist"], label=percent_values)

    # Always save hue stats
    outputs.add_observation(sample=label, variable='hue_circular_mean', trait='hue circular mean',
                            method='plantcv.plantcv.analyze.color', scale='degrees', datatype=float,
                            value=hue_circular_mean, label='degrees')
    outputs.add_observation(sample=label, variable='hue_circular_std', trait='hue circular standard deviation',
                            method='plantcv.plantcv.analyze.color', scale='degrees', datatype=float,
                            value=hue_circular_std, label='degrees')
    outputs.add_observation(sample=label, variable='hue_median', trait='hue median',
                            method='plantcv.plantcv.analyze.color', scale='degrees', datatype=float,
                            value=hue_median, label='degrees')

    return img
