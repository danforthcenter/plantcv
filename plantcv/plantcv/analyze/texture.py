"""Analyzes the texture of objects and outputs data."""
from skimage.feature import graycomatrix, graycoprops
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv._globals import params, outputs
import cv2


def texture(img, methods=None,
            distances=[1], angles=[0], levels=None,
            symmetric=False, normalize=False,
            labeled_mask, n_labels=1, label=None):
    """A function that analyzes the shape and size of objects and outputs data.

    Inputs:
    img          = RGB or grayscale image data for plotting
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
    labeled_mask = Labeled mask of objects (32-bit).
    n_labels     = Total number expected individual objects (default = 1).
    label        = Optional label parameter, modifies the variable name of
                   observations recorded (default = pcv.params.sample_label).

    Returns:
    analysis_image = Diagnostic image showing measurements.
    """
    if label is None:
        label = params.sample_label

    img = _iterate_analysis(img=img, labeled_mask=labeled_mask, n_labels=n_labels, label=label,
                            function=_analyze_texture,
                            distances=distances, angles=angles, levels=levels,
                            symmetric=symmetric, normalize=normalize,
                            )

    _debug(visual=img, filename=os.path.join(params.debug_outdir, str(params.device) + "_textures.png"))
    return img


def _analyze_texture(img, mask, label, distances, angles, levels, symmetric, normalize):
    """Analyze the size of individual objects.

    Inputs:
    img   = RGB or grayscale image data for plotting
    mask  = Binary image data
    label = Label of object

    Returns:
    analysis_image = Diagnostic image showing measurements

    :param mask: numpy.ndarray
    :param label: int
    :return analysis_image: numpy.ndarray
    """
    params.device += 1
    
