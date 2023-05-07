import cv2
import numpy as np


def _cv2_findcontours(bin_img):
    """
    Helper function for OpenCV findContours.

    Reduces duplication of calls to findContours in the event the OpenCV function changes.

    Keyword inputs:
    bin_img = Binary image (np.ndarray)

    :param bin_img: np.ndarray
    :return contours: list
    :return hierarchy: np.array
    """
    contours, hierarchy = cv2.findContours(np.copy(bin_img), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    return contours, hierarchy


def _iterate_analysis(img, labeled_mask, n_labels, label, function, **kwargs):
    """Iterate over labels and apply an analysis function.
    Inputs:
    img      = image to be used for visualization
    mask     = labeled mask
    n_labels = number of expected labels
    label    = label parameter, modifies the variable name of observations recorded
    function = analysis function to apply to each submask
    kwargs   = additional keyword arguments to pass to the analysis function

    :param img: np.ndarray
    :param mask: np.ndarray
    :param n_labels: int
    :param label: str
    :param function: function
    :param kwargs: dict
    """
    mask_copy = np.copy(labeled_mask)
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
    for i in range(1, n_labels + 1):
        submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)
        img = function(img=img, mask=submask, label=label, **kwargs)
    return img
