import cv2
import numpy as np
from plantcv.plantcv.logical_and import logical_and
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv import params


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


def _roi_filter(img, roi, obj, hierarchy, roi_type="partial"):
    """
    Helper function to filter contours using a single ROI

    Find objects partially inside a region of interest or cut objects to the ROI.

    Inputs:
    img            = RGB, binary, or grayscale image data for shape
    roi            = region of interest, an instance of the Object class output from a roi function
    obj            = contours of objects, output from "_cv2_findcontours" function
    hierarchy      = hierarchy of objects, output from "_cv2_findcontours" function
    roi_type       = 'cutto', 'partial' (for partially inside, default), or 'largest' (keep only the largest contour)

    Returns:
    kept_cnt       = kept contours
    kept_hier      = kept hierarchy
    mask           = mask image

    :param img: numpy.ndarray
    :param roi: plantcv.plantcv.classes.Objects
    :param obj: list
    :param hierarchy: np.array
    :param roi_type: str
    :return kept_cnt: list
    :return kept_hier: np.array
    :return mask: numpy.ndarray
    """
    # Store debug
    debug = params.debug
    params.debug = None

    if len(roi.contours) > 1:
        warn("received a multi-ROI but only the first ROI will be used. Consider using a for loop for multi-ROI")

    roi_contour = roi.contours[0]
    object_contour = obj
    obj_hierarchy = hierarchy

    # Create an empty grayscale (black) image the same dimensions as the input image
    mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    cv2.drawContours(mask, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)

    # Create a mask of the filled in ROI
    roi_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
    roi_points = np.vstack(roi_contour[0])
    cv2.fillPoly(roi_mask, [roi_points], (255))

    # Allows user to find all objects that are completely inside or overlapping with ROI
    if roi_type.upper() in ('PARTIAL', 'LARGEST'):
        # Filter contours outside of the region of interest
        for c, _ in enumerate(object_contour):
            filtering_mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.fillPoly(filtering_mask, [np.vstack(object_contour[c])], (255))
            overlap_img = logical_and(filtering_mask, roi_mask)
            # Delete contours that do not overlap at all with the ROI
            if np.sum(overlap_img) == 0:
                cv2.drawContours(mask, object_contour, c, (0), -1, lineType=8, hierarchy=obj_hierarchy)

        # Find the kept contours and area
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

        # Find the largest contour if roi_type is set to 'largest'
        if roi_type.upper() == 'LARGEST' and kept_cnt:
            index = np.argmax([cv2.contourArea(c) for c in kept_cnt])
            mask = np.zeros(np.shape(img)[:2], dtype=np.uint8)
            cv2.drawContours(mask, kept_cnt, contourIdx=index, color=(255), thickness=-1, hierarchy=kept_hierarchy, maxLevel=2)
            kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)

    # Allows user to cut objects to the ROI (all objects completely outside ROI will not be kept)
    elif roi_type.upper() == 'CUTTO':
        background1 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        background2 = np.zeros(np.shape(img)[:2], dtype=np.uint8)
        cv2.drawContours(background1, object_contour, -1, (255), -1, lineType=8, hierarchy=obj_hierarchy)
        roi_points = np.vstack(roi_contour[0])
        cv2.fillPoly(background2, [roi_points], (255))
        mask = cv2.multiply(background1, background2)
        kept_cnt, kept_hierarchy = _cv2_findcontours(bin_img=mask)
    else:
        # Reset debug mode
        params.debug = debug
        fatal_error('ROI Type ' + str(roi_type) + ' is not "cutto", "largest", or "partial"!')

    # Reset debug mode
    params.debug = debug

    return kept_cnt, kept_hierarchy, mask


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
    # Set labels to label
    labels = label
    # If label is a string, make a list of labels
    if isinstance(label, str):
        labels = [label] * n_labels
    # If the length of the labels list is not equal to the number of labels, raise an error
    if len(labels) != n_labels:
        fatal_error(f"Number of labels ({len(labels)}) does not match number of objects ({n_labels})")
    mask_copy = np.copy(labeled_mask)
    if len(np.unique(mask_copy)) == 2 and np.max(mask_copy) == 255:
        mask_copy = np.where(mask_copy == 255, 1, 0).astype(np.uint8)
    for i in range(1, n_labels + 1):
        submask = np.where(mask_copy == i, 255, 0).astype(np.uint8)
        img = function(img=img, mask=submask, label=f"{labels[i - 1]}_{i}", **kwargs)
    return img


def _object_composition(contours, hierarchy):
    """
    Groups objects into a single object, usually done after object filtering.

    Inputs:
    contours  = Contour tuple
    hierarchy = Contour hierarchy NumPy array

    Returns:
    group    = grouped contours list

    :param contours: tuple
    :param hierarchy: numpy.ndarray
    :return group: numpy.ndarray
    """
    stack = np.zeros((len(contours), 1))

    for c, _ in enumerate(contours):
        if hierarchy[0][c][2] == -1 and hierarchy[0][c][3] > -1:
            stack[c] = 0
        else:
            stack[c] = 1

    ids = np.where(stack == 1)[0]
    group = np.array([], dtype=np.int32)
    if len(ids) > 0:
        contour_list = [contours[i] for i in ids]
        group = np.vstack(contour_list)

    return group


def _grayscale_to_rgb(img):
    """
    Convert a grayscale image to an RGB image.

    Inputs:
    img = Grayscale or RGB image data

    Returns:
    img = RGB image data

    :param img: np.ndarray
    :return img: np.ndarray
    """
    if len(np.shape(img)) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img
