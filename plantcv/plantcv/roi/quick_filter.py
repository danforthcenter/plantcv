"""PlantCV fast_filter module."""
import os
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv._helpers import _roi_filter
from plantcv.plantcv.deprecation_warning import deprecation_warning


def quick_filter(mask, roi, roi_type="partial"):
    """Filter a binary mask using a region of interest and connected components.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask to filter.
    roi : plantcv.plantcv.classes.Objects
        PlantCV ROI object.
    roi_type : str, optional
        Type of ROI filtering: "partial", "cutto", "within", or "largest".

    Returns
    -------
    numpy.ndarray
        Filtered binary mask.
    """
    deprecation_warning("roi.quick_filter has been merged into roi.filter. " +
                        "The roi.quick_filter function will be removed in the version 5 release.")
    filtered_mask = _roi_filter(mask=mask, roi=roi, roi_type=roi_type)
    _debug(visual=filtered_mask,
           filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
           cmap="gray")
    return filtered_mask
