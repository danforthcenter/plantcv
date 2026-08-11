"""Analyze leaf light absorption as alphaL: 1 - (R640nm / R732nm)"""

import numpy as np
import pandas as pd
from plantcv.plantcv.warn import warn
from plantcv.plantcv._helpers import _iterate_analysis
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.analyze.yii import _set_labels


def alphaL(ps, labeled_mask, n_labels=1, measurement_labels=None, label=None, min_bin=-1, max_bin=1):
    """Analyze leaf light absorption

    Parameters
    ----------
    ps                  = plantcv.plantcv.classes.PSII_data
        Photosynthesis data as read by plantcv.plantcv.photosynthesis.read_cropreporter
        Must include the aph frame.
    labeled_mask        = numpy.ndarray,
        Labeled mask of objects (32-bit).
    n_labels            = int,
        Total number expected individual objects (default = 1).
    measurement_labels  = list,
        labels for each measurement, modifies the variable name of observations recorded
    label               = str,
        optional label parameter, modifies the variable name of observations recorded
    min_bin             = int,
        Minimum bin value (default = -1).
    max_bin             = int,
        Maximum bin value (default = 1).

    Returns
    -------
    aph                 = numpy.ndarray,
        alphaL matrix
    """
    # Set labels
    labels = _set_labels(label, n_labels)

    # Validate that the input mask has the same 2D shape as the input DataArray
    ps_shape = (int(ps.metadata["ImageRows"]), int(ps.metadata["ImageCols"]))
    if labeled_mask.shape != ps_shape:
        fatal_error(f"Mask needs to have shape {ps_shape}")
    # standardize binary mask to labeled mask
    if len(np.unique(labeled_mask)) <= 2 and np.max(labeled_mask) == 255:
        labeled_mask = np.where(labeled_mask == 255, 1, 0).astype(np.uint8)
    # Check that the aph frame exists
    if getattr(ps, "aph", None) is None:
        fatal_error("`ps` must be a PSII_Data object with APH data present.")
    # calculate alphaL for each masked object
    aph = _iterate_analysis(img=ps,
                            labeled_mask=labeled_mask, n_labels=n_labels, label=labels,
                            function=_analyze_alphaL, **{"min_bin": min_bin, "max_bin": max_bin})
    return aph


def _analyze_alphaL(img, mask, label, min_bin, max_bin):
    """Analyze Alpha L in _iterate_analysis
    Parameters
    ----------
    ps      = plantcv.plantcv.classes.PSII_data
        Photosynthesis data as read by plantcv.plantcv.photosynthesis.read_cropreporter
        Must include the aph frame.
    mask    = numpy.ndarray,
        Labeled mask of objects (32-bit).
    label   = str,
        optional label parameter, modifies the variable name of observations recorded
    min_bin = int,
        Minimum bin value (default = -1).
    max_bin = int,
        Maximum bin value (default = 1).

    Returns
    -------
    alphaL  = numpy.ndarray,
        alphaL matrix
    """
    ps = img
    red = ps.aph.red
    farred = ps.aph.farred
    # Calculate alphaL
    alphaL = 1 - np.divide(red, farred, out=np.full(np.shape(red), fill_value=np.nan), where=mask.astype(bool))
    # Store mean, median, min, max, and histogram of alphaL
    outputs.add_observation(
        sample=label, variable="alphaL_mean", trait="mean alphaL",
        method="plantcv.plantcv.analyze.alphaL", scale="none", datatype=float,
        value=np.nanmean(alphaL), label="none"
    )
    outputs.add_observation(
        sample=label, variable="alphaL_median", trait="median alphaL",
        method="plantcv.plantcv.analyze.alphaL", scale="none", datatype=float,
        value=np.nanmedian(alphaL), label="none"
    )
    max_alphaL = np.nanmax(alphaL)
    outputs.add_observation(
        sample=label, variable="alphaL_max", trait="max alphaL",
        method="plantcv.plantcv.analyze.alphaL", scale="none", datatype=float,
        value=max_alphaL, label="none"
    )
    min_alphaL = np.nanmin(alphaL)
    outputs.add_observation(
        sample=label, variable="alphaL_min", trait="min alphaL",
        method="plantcv.plantcv.analyze.alphaL", scale="none", datatype=float,
        value=min_alphaL, label="none"
    )
    # Check if bounds are appropriate for the data
    finite_alphaL = alphaL[~np.isnan(alphaL)]
    if (max_alphaL > max_bin) or (min_alphaL < min_bin):
        warn(
            f"alphaL values range from {round(min_alphaL, 3)}... to {round(max_alphaL, 3)}..." +
            ", extending beyond min/max bins. Consider expanding range."
        )
    # Calculate histogram of alphaL
    alphaL_hist, alphaL_bins = np.histogram(finite_alphaL, 100, range=(min_bin, max_bin))
    # Calculate which non-zero bin has the maximum alphaL value
    mode_alphaL = alphaL_bins[np.argmax(alphaL_hist)]
    outputs.add_observation(
        sample=label, variable="alphaL_mode", trait="mode alphaL",
        method="plantcv.plantcv.analyze.alphaL", scale="none", datatype=float,
        value=mode_alphaL, label="none"
    )

    # Convert the histogram pixel counts to proportional frequencies
    alphaL_percent = (alphaL_hist / float(np.sum(alphaL_hist))) * 100

    # Create a dataframe for the histogram
    hist_df = pd.DataFrame({'proportion of pixels (%)': alphaL_percent, 'counts': alphaL_bins[:-1]})
    outputs.add_observation(sample=label, variable="alphaL_hist",
                                trait="alphaL frequencies",
                                method='plantcv.plantcv.analyze.alphaL', scale='none', datatype=list,
                                value=hist_df['proportion of pixels (%)'].values.tolist(),
                                label=np.around(hist_df["counts"].values.tolist(), decimals=2).tolist())

    return alphaL
