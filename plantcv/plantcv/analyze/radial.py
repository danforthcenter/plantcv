"""Analyzes the average pixel values within a percentile of the distance from each object's center."""
import os
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv._helpers import _iterate_objects


def radial_percentile(img, labeled_mask, n_labels=1, percentile=50, label=None):
    """Analyzes the average pixel values within a percentile of the maximum distance from each object's center.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data.
    labeled_mask : numpy.ndarray
        Labeled mask of objects (32-bit), or a binary mask of a single object.
    n_labels : int, default=1
        Total number of expected individual objects.
    percentile : int or float, default=50
        Cutoff for inclusion of pixels, as a percent of the maximum distance from an object's center.
    label : str or list, optional
        Label that modifies the variable name of recorded observations. Defaults
        to ``pcv.params.sample_label``.

    Returns
    -------
    avgs : list
        Average pixel values within the distance percentile for each object. Each entry is a float
        (grayscale) or a list of [red, green, blue] floats (RGB). Empty objects are NaN.
    """
    # Set label to params.sample_label if None
    if label is None:
        label = params.sample_label

    avgs = []
    # Debug image showing the pixels that were averaged for every object
    debug_img = np.zeros_like(img)
    for sample, slices, obj_mask in _iterate_objects(labeled_mask=labeled_mask, n_labels=n_labels, label=label):
        avg, keep = _analyze_radial(img=img, slices=slices, obj_mask=obj_mask, percentile=percentile, label=sample)
        avgs.append(avg)
        if keep is not None:
            debug_img[slices][keep] = img[slices][keep]

    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, str(params.device) + "_radial_average.png"))
    return avgs


def _analyze_radial(img, slices, obj_mask, percentile=50, label=None):
    """Analyzes the average pixel values within a percentile of the maximum distance from an object's center.

    Parameters
    ----------
    img : numpy.ndarray
        RGB or grayscale image data.
    slices : tuple
        Bounding box of the object.
    obj_mask : numpy.ndarray
        Boolean mask of the object within the bounding box.
    percentile : int or float, default=50
        Cutoff for inclusion of pixels, as a percent of the maximum distance from the object's center.
    label : str, optional
        Label that modifies the variable name of recorded observations.

    Returns
    -------
    avg : float or list
        Average pixel value (grayscale) or [red, green, blue] averages (RGB). NaN if the object is empty
        or no object pixels fall within the cutoff.
    keep : numpy.ndarray or None
        Boolean mask (within the bounding box) of the pixels that were averaged, or None if none were.
    """
    is_rgb = img.ndim == 3
    empty = [np.nan, np.nan, np.nan] if is_rgb else np.nan

    # Skip empty masks
    if np.count_nonzero(obj_mask) == 0:
        return empty, None

    # Object pixel coordinates within the bounding box and the object's center of mass
    ys, xs = np.nonzero(obj_mask)
    distances = np.sqrt((xs - np.mean(xs)) ** 2 + (ys - np.mean(ys)) ** 2)
    # Cutoff distance as a percentile of the maximum distance of an object pixel from the center
    cutoff = np.max(distances) * (percentile / 100.0)
    inside = (distances <= cutoff) & (percentile > 0)

    # No object pixels within the cutoff (e.g., very small percentile or single-pixel object)
    if not np.any(inside):
        return empty, None

    # Only object pixels within the cutoff are averaged (background pixels are never included)
    keep = np.zeros_like(obj_mask, dtype=bool)
    keep[ys[inside], xs[inside]] = True
    values = img[slices][keep]

    method = 'plantcv.plantcv.analyze.radial'
    if is_rgb:
        # OpenCV is BGR; outputs are ordered R, G, B
        avg = [float(np.mean(values[:, 2])), float(np.mean(values[:, 1])), float(np.mean(values[:, 0]))]
        for channel, value in zip(["red", "green", "blue"], avg):
            outputs.add_observation(sample=label, variable=f'{channel}_{percentile}%_avg',
                                    trait=f'{channel}_{percentile}%_radial_average', method=method,
                                    scale='none', datatype=float, value=value, label='none')
    else:
        avg = float(np.mean(values))
        outputs.add_observation(sample=label, variable=f'gray_{percentile}%_avg',
                                trait=f'gray_{percentile}%_radial_average', method=method,
                                scale='none', datatype=float, value=avg, label='none')
    return avg, keep
