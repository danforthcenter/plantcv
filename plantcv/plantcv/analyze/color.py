"""Analyzes the color properties of objects in an image."""
import os
import cv2
import numpy as np
from scipy import stats
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._globals import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import outputs
from plantcv.plantcv._helpers import _iterate_objects

# Histogram plot types
HIST_TYPES = {"all": ("b", "g", "r", "l", "m", "y", "h", "s", "v"),
              "rgb": ("b", "g", "r"),
              "lab": ("l", "m", "y"),
              "hsv": ("h", "s", "v")}


def color(rgb_img, labeled_mask, n_labels=1, colorspaces="hsv", label=None):
    """A function that analyzes the color of objects and outputs data.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data.
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit).
    n_labels : int, optional
        Total number of expected individual objects. The default is 1.
    colorspaces : str, optional
        Color space to analyze. Options are ``'all'``, ``'rgb'``, ``'lab'``,
        or ``'hsv'``. The default is ``'hsv'``.
    label : str, optional
        Label parameter that modifies the variable name of observations
        recorded. The default is ``pcv.params.sample_label``.

    Returns
    -------
    list
        Histogram output.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label

    if colorspaces.lower() not in HIST_TYPES:
        fatal_error(f"Colorspace '{colorspaces}' is not supported, must be be one of the following: "
                    f"{', '.join(map(str, HIST_TYPES.keys()))}")
    if len(np.shape(rgb_img)) < 3:
        fatal_error("rgb_img must be an RGB image")

    # Extract the color channels for the whole image
    channels = _color_channels(rgb_img=rgb_img, colorspaces=colorspaces)

    for sample, slices, obj_mask in _iterate_objects(labeled_mask=labeled_mask, n_labels=n_labels, label=label):
        _analyze_color(channels=channels, slices=slices, obj_mask=obj_mask, colorspaces=colorspaces, label=sample)
    hue_chart = outputs.plot_dists(variable="hue_frequencies")
    _debug(visual=hue_chart, filename=os.path.join(params.debug_outdir, str(params.device) + '_hue_hist.png'))
    return hue_chart


def _color_channels(rgb_img, colorspaces="hsv"):
    """Split an RGB image into the color channels needed for analysis.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data.
    colorspaces : str, optional
        Color spaces to extract. Options are ``'all'``, ``'rgb'``, ``'lab'``,
        or ``'hsv'``. The default is ``'hsv'``.

    Returns
    -------
    dict
        Dictionary of color channel images.
    """
    # Extract the blue, green, and red channels
    b, g, r = cv2.split(rgb_img)
    # Convert the BGR image to HSV (hue is always analyzed)
    hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    # Extract the hue, saturation, and value channels
    h, s, v = cv2.split(hsv)
    channels = {"b": b, "g": g, "r": r, "h": h, "s": s, "v": v}
    if colorspaces.upper() in ('LAB', 'ALL'):
        # Convert the BGR image to LAB
        lab = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2LAB)
        # Extract the lightness, green-magenta, and blue-yellow channels
        channels["l"], channels["m"], channels["y"] = cv2.split(lab)
    return channels


def _analyze_color(channels, slices, obj_mask, colorspaces="hsv", label=None):
    """Analyze the color properties of an image object.

    Parameters
    ----------
    channels : dict
        Dictionary of color channel images.
    slices : tuple
        Bounding box of the object.
    obj_mask : numpy.ndarray
        Boolean mask of the object within the bounding box.
    colorspaces : str, optional
        Color spaces to analyze: ``'all'``, ``'rgb'``, ``'lab'``, or ``'hsv'``.
    label : str, optional
        Label parameter that modifies the variable name of observations recorded.
    """
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
    if np.count_nonzero(obj_mask) != 0:
        # Object pixel values for each color channel
        pixels = {channel: img[slices][obj_mask] for channel, img in channels.items()}
        h, s, v = pixels["h"], pixels["s"], pixels["v"]

        # Calculate histograms as the percent of object pixels in each 8-bit bin
        for channel, values in pixels.items():
            histograms[channel]["hist"] = (np.bincount(values, minlength=256) / float(values.size) * 100).tolist()

        # Hue values of zero are red but are also the value for pixels where hue is undefined. The hue value of a pixel will
        # be undef. when the color values are saturated. Therefore, hue values of 0 are excluded from the calculations below
        hue = h[h > 0]
        # Calculate the median hue value (median is rescaled from the encoded 0-179 range to the 0-359 degree range)
        hue_median = np.median(hue) * 2

        # Calculate the circular mean and standard deviation of the encoded hue values
        # The mean and standard-deviation are rescaled from the encoded 0-179 range to the 0-359 degree range
        hue_circular_mean = stats.circmean(hue, high=179, low=0) * 2
        hue_circular_std = stats.circstd(hue, high=179, low=0) * 2

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
        # Calculate the mean and median saturation and value (lightness) values
        saturation = s[s > 0].astype(np.float64) / 255
        value = v[v > 0].astype(np.float64) / 255
        saturation_mean = np.mean(saturation) * 100
        saturation_median = np.median(saturation) * 100
        value_mean = np.mean(value) * 100
        value_median = np.median(value) * 100

        outputs.add_observation(sample=label, variable='saturation_mean', trait='saturation mean',
                                method='plantcv.plantcv.analyze.color', scale='percent', datatype=float,
                                value=saturation_mean, label='percent')
        outputs.add_observation(sample=label, variable='saturation_median', trait='saturation median',
                                method='plantcv.plantcv.analyze.color', scale='percent', datatype=float,
                                value=saturation_median, label='percent')
        outputs.add_observation(sample=label, variable='value_mean', trait='value mean',
                                method='plantcv.plantcv.analyze.color', scale='percent', datatype=float,
                                value=value_mean, label='percent')
        outputs.add_observation(sample=label, variable='value_median', trait='value median',
                                method='plantcv.plantcv.analyze.color', scale='percent', datatype=float,
                                value=value_median, label='percent')
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
