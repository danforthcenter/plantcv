"""Analyzes the texture of objects and outputs data."""
from skimage.feature import graycomatrix, graycoprops
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _iterate_analysis
from plantcv.plantcv._debug import _debug
import numpy as np
import cv2
import os


def texture(img, labeled_mask, methods=None,
            distances=[1], angles=[0], levels=None,
            symmetric=False, normalize=False,
            n_labels=1, label=None):
    """A function that analyzes the texture of objects and outputs data.

    Parameters
    ----------
    img          = numpy.ndarray, grayscale image data
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
    analysis_image = numpy.ndarray, Diagnostic image showing measurements.
    """
    if label is None:
        label = params.sample_label
    if methods is None:
        methods = ["contrast", "dissimilarity", "homogeneity",
                   "ASM", "energy", "correlation",
                   "mean", "variance", "std", "entropy"]
    # for the debug image I would like to have a mix of matrices, but for non-uint8
    # that could get really large if there is a multi-object mask.
    mat = _iterate_analysis(img=img, labeled_mask=labeled_mask,
                            n_labels=n_labels, label=label,
                            function=_analyze_texture,
                            **{'distances': distances, 'angles': angles,
                               'levels': levels, 'symmetric': symmetric,
                               'methods': methods, 'normalize': normalize}
                            )

    _debug(visual=mat, filename=os.path.join(params.debug_outdir, str(params.device) + "_textures.png"))
    return img


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
    analysis_image = numpy.ndarray, Diagnostic image showing measurements.
    """
    params.device += 1
    # get levels if None
    levels = _default_levels(img, levels)
    # keep only section of image in mask
    subimg = cv2.bitwise_and(img, img, mask=mask)
    # get gray level cooccurence matrix
    glcm = graycomatrix(subimg, distances=distances, angles=angles,
                        levels=levels, symmetric=symmetric, normed=normalize)
    # loop over methods, distances, and angles
    for method in methods:
        props = graycoprops(glcm, method)
        for i in range(len(distances)):
            for j in range(len(angles)):
                outputs.add_observation(
                    sample=label, variable=method, trait=method,
                    method='plantcv.plantcv.analyze.texture',
                    scale="none", datatype=float,
                    value=props[i,j], label="none"
                )
    return glcm


def _default_levels(img, levels):
    """Get default number of levels for an image based on dtype
    For non-8 bit images this will default to the max of the image plus 1,
    but it may be preferable to bin the images in those scenarios.

    Parameters
    ----------
    img = numpy.ndarray, grayscale image data used to make gray-level cooccurence matrix

    Returns
    -------
    n_levels = int, number of levels
    """
    if levels is None:
        if img.dtype == "uint8":
            levels = 256
        else:
            levels = np.max(img) + 1
    return levels
