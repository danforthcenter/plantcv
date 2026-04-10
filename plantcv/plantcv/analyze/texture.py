"""Analyzes the texture of objects and outputs data."""
from skimage.feature import graycomatrix, graycoprops
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _iterate_analysis, _rgb2gray
from plantcv.plantcv._debug import _debug
import altair as alt
import pandas as pd
import numpy as np
import cv2
import os


def texture(img, labeled_mask, methods=None,
            distances=None, angles=None, levels=None,
            symmetric=False, normalize=False,
            n_labels=1, label=None):
    """A function that analyzes the texture of objects and outputs data.

    Parameters
    ----------
    img          = numpy.ndarray, grayscale image data. If data is not grayscale then
                   it will be coerced to grayscale using pcv._helpers._rgb2gray.
    labeled_mask = numpy.ndarray, Labeled mask of objects (32-bit).
    methods      = list, List of str specifying phenotypes to return. Options
                   come from skimage.feature.graycoprops and include "contrast",
                   "dissimilarity", "homogeneity", "ASM", "energy", "correlation",
                   "mean", "variance", "std", "entropy". The default, None, will
                   use all methods.
    distances    = list of Int. Pixel pair distances, defaults to 1 which compares
                   adjacent pixels.
    angles       = list of float, angles or direction to check travel for each
                   distance.
    levels       = Int, optional. If None (the default) then it will be inferred from the
                   dtype of the image. Represents the number of different options for a
                   value in each channel, IE an 8bit image would have levels=256.
    symmetric    = bool, optional
                   If True, the output is symmetric because the order of value pairs
                   is ignored so that (i, j) and (j, i) the same. The default is False.
    normalize    = bool, optional
                   If True then the matrix is rescaled to sum to 1. Default is False.
    n_labels     = Int, Total number expected individual objects (default = 1).
    label        = str, Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns
    -------
    plot = altair.vegalite.v5.api.FacetChart, Diagnostic image showing measurements.
    """
    if distances is None:
        distances = [1]
    if angles is None:
        angles = [0]
    if len(np.shape(img)) > 2:
        img = _rgb2gray(img)
    if label is None:
        label = params.sample_label
    if methods is None:
        methods = ["contrast", "dissimilarity", "homogeneity",
                   "ASM", "energy", "correlation",
                   "mean", "variance", "std", "entropy"]
    # for the debug image I would like to have a mix of matrices, but for non-uint8
    # that could get really large if there is a multi-object mask.
    _ = _iterate_analysis(img=img, labeled_mask=labeled_mask,
                          n_labels=n_labels, label=label,
                          function=_analyze_texture,
                          **{'distances': distances, 'angles': angles,
                             'levels': levels, 'symmetric': symmetric,
                             'methods': methods, 'normalize': normalize}
                          )
    plot = _make_texture_debug_plot()
    _debug(visual=plot, cmap="turbo",
           filename=os.path.join(params.debug_outdir, str(params.device) + "_textures.png"))
    return plot


def _analyze_texture(img, mask, label, methods, distances, angles, levels, symmetric, normalize):
    """Analyze the texture of individual objects.

    Parameters
    ----------
    img          = numpy.ndarray, grayscale image data
    mask         = Binary image data
    label        = str, Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).
    methods      = list, List of str specifying phenotypes to return. Options
                   come from skimage.feature.graycoprops and include "contrast",
                   "dissimilarity", "homogeneity", "ASM", "energy", "correlation",
                   "mean", "variance", "std", "entropy"
    distances    = list of Int. Pixel pair distances, defaults to 1 which compares
                   adjacent pixels.
    angles       = list of float, angles or direction to check travel for each
                   distance.
    levels       = Int, optional. If None (the default) then it will be inferred from the
                   dtype of the image. Represents the number of different options for a
                   value in each channel, IE an 8bit image would have levels=256.
    symmetric    = bool, optional
                   If True, the output is symmetric because the order of value pairs
                   is ignored so that (i, j) and (j, i) the same. The default is False.
    normalize    = bool, optional
                   If True then the matrix is rescaled to sum to 1. Default is False.

    Returns
    -------
    glcm         = numpy.ndarray, currently not used.
    """
    params.device += 1
    # keep only section of image in mask
    subimg = cv2.bitwise_and(img, img, mask=mask).astype(np.uint8)
    # get gray level cooccurence matrix
    glcm = graycomatrix(subimg, distances=distances, angles=angles,
                        levels=256, symmetric=symmetric, normed=normalize)
    # loop over methods, distances, and angles
    for method in methods:
        props = graycoprops(glcm, method)
        for i in range(len(distances)):
            for j in range(len(angles)):
                outputs.add_observation(
                    sample=label,
                    variable=method + "_" + str(distances[i]) + "_" + str(angles[j]),
                    trait=method,
                    method='plantcv.plantcv.analyze.texture',
                    scale="none", datatype=float,
                    value=props[i, j], label="none"
                )
    return glcm


def _make_texture_debug_plot():
    """Makes a plot using the outputs from analyze.texture to use as a debug image"""
    rows = []
    for key, value in outputs.observations.items():
        for k, v in value.items():
            if v["method"] == 'plantcv.plantcv.analyze.texture':
                row = [key, k, v["value"]]
                rows.append(row)
    df = pd.DataFrame(rows)
    df.columns = ["label", "variable", "value"]
    df["facet"] = np.where(
        df['variable'].isin(
            ["ASM", "correlation", "dissimilarity",
             "energy", "entropy", "homogeneity",
             "mean"]),
        'Bounded', 'Unbounded')
    plot = alt.Chart(df).mark_point().encode(
        x='variable:N',
        y='value:Q'
    ).facet("facet:N").resolve_scale(
        y='independent',
        x='independent'
    )
    return plot
