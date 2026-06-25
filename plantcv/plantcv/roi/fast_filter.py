"""PlantCV fast_filter module."""
import os
import cv2
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params


def fast_filter(mask, roi, roi_type="partial"):
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
    roi_type = roi_type.lower()
    binary = (mask > 0).astype(np.uint8) * 255

    roi_mask = np.zeros(binary.shape, dtype=np.uint8)
    for single_roi in roi:
        cv2.drawContours(roi_mask, single_roi.contours[0], -1, 255, -1)

    if roi_type == "cutto":
        filtered_mask = cv2.bitwise_and(binary, roi_mask)
        _debug(visual=filtered_mask,
               filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
               cmap="gray")
        return filtered_mask

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    if num_labels <= 1:
        filtered_mask = np.zeros(binary.shape, dtype=np.uint8)
        _debug(visual=filtered_mask,
               filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
               cmap="gray")
        return filtered_mask

    inside = roi_mask > 0
    label_ids = labels.ravel()
    overlap_counts = np.bincount(
        label_ids,
        weights=inside.ravel().astype(np.uint8),
        minlength=num_labels,
    )
    selected = np.zeros(num_labels, dtype=bool)

    if roi_type == "partial":
        selected = overlap_counts > 0
        selected[0] = False
    elif roi_type == "within":
        outside_counts = np.bincount(
            label_ids,
            weights=(~inside).ravel().astype(np.uint8),
            minlength=num_labels,
        )
        selected = outside_counts == 0
        selected[0] = False
    elif roi_type == "largest":
        candidates = np.flatnonzero(overlap_counts > 0)
        candidates = candidates[candidates != 0]
        if candidates.size:
            best = candidates[np.argmax(stats[candidates, cv2.CC_STAT_AREA])]
            selected[best] = True
    else:
        fatal_error(f'ROI Type {roi_type} is not "cutto", "largest", "within" or "partial"!')

    filtered_mask = np.where(selected[labels], 255, 0).astype(np.uint8)
    _debug(visual=filtered_mask,
           filename=os.path.join(params.debug_outdir, f"{params.device}_roi_filter.png"),
           cmap="gray")
    return filtered_mask
