import cv2
import numpy as np
from plantcv.plantcv.dilate import dilate
from plantcv.plantcv.logical_and import logical_and
from plantcv.plantcv.image_subtract import image_subtract
from plantcv.plantcv import fatal_error, warn
from plantcv.plantcv import params
import pandas as pd


def _find_segment_ends(skel_img, leaf_objects, plotting_img, size):
    """Find both segment ends and sort into tips or inner branchpoints.
    Inputs:
    skel_img         = Skeletonized image
    leaf_objects     = List of leaf segments
    plotting_img     = Mask for debugging, might be a copy of the Skeletonized image
    size             = Size of inner segment ends (in pixels)
    :param skel_img: numpy.ndarray
    :param leaf_objects: list
    :param plotting_img: numpy.ndarray
    """
    labeled_img = cv2.cvtColor(plotting_img, cv2.COLOR_GRAY2RGB)
    tips, _, _ = _find_tips(skel_img)
    # Initialize list of tip data points
    labels = []
    tip_list = []
    inner_list = []
    remove = []
    sortabled_objs = leaf_objects.copy()

    # Find segment end coordinates
    for i in range(len(leaf_objects)):
        labels.append(i)
        # Draw leaf objects
        find_segment_tangents = np.zeros(labeled_img.shape[:2], np.uint8)
        cv2.drawContours(find_segment_tangents, leaf_objects, i, 255, 1, lineType=8)
        cv2.drawContours(labeled_img, leaf_objects, i, (150, 150, 150), params.line_thickness, lineType=8)  # segments debug
        # Prune back ends of leaves
        pruned_segment = _iterative_prune(find_segment_tangents, size)
        # Segment ends are the portions pruned off
        ends = find_segment_tangents - pruned_segment
        segment_end_obj, _ = _cv2_findcontours(bin_img=ends)
        branch_pt_found = False
        coords = []
        # Determine if a segment is segment tip or branch point
        for j, obj in enumerate(segment_end_obj):
            segment_plot = np.zeros(skel_img.shape[:2], np.uint8)
            cv2.drawContours(segment_plot, obj, -1, 255, 1, lineType=8)
            segment_plot = dilate(segment_plot, 3, 1)
            overlap_img = logical_and(segment_plot, tips)
            x, y = segment_end_obj[j].ravel()[:2]
            coord = (int(x), int(y))
            coords.append(coord)
            # If none of the tips are within a segment_end then it's an insertion segment
            if np.sum(overlap_img) == 0:
                inner_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (50, 0, 255), -1)  # Red auricles/branch points
                branch_pt_found = True
            else:
                tip_list.append(coord)
                cv2.circle(labeled_img, coord, params.line_thickness, (0, 255, 0), -1)  # green tips
        if not branch_pt_found:  # there is no branch point associated with a given segment and therefore it cannot be sorted
            remove.append(i)

    # Remove the segments that cannot be resorted, since they do not have a branch point
    for k in remove:
        sortabled_objs.pop(k)

    return labeled_img, tip_list, inner_list, labels, sortabled_objs


def _iterative_prune(skel_img, size):
    """Iteratively remove endpoints (tips) from a skeletonized image.
    The pruning algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699
    "Prunes" barbs off a skeleton.
    Inputs:
    skel_img    = Skeletonized image
    size        = Size to get pruned off each branch
    Returns:
    pruned_img  = Pruned image
    :param skel_img: numpy.ndarray
    :param size: int
    :return pruned_img: numpy.ndarray
    """
    pruned_img = skel_img.copy()
    # Store debug
    debug = params.debug
    params.debug = None

    # Iteratively remove endpoints (tips) from a skeleton
    for _ in range(0, size):
        endpoints, _, _ = _find_tips(pruned_img)
        pruned_img = image_subtract(pruned_img, endpoints)

    # Make debugging image
    pruned_plot = np.zeros(skel_img.shape[:2], np.uint8)
    pruned_plot = cv2.cvtColor(pruned_plot, cv2.COLOR_GRAY2RGB)
    skel_obj, skel_hierarchy = _cv2_findcontours(bin_img=pruned_img)
    pruned_obj, pruned_hierarchy = _cv2_findcontours(bin_img=pruned_img)

    # Reset debug mode
    params.debug = debug

    cv2.drawContours(pruned_plot, skel_obj, -1, (0, 0, 255), params.line_thickness,
                     lineType=8, hierarchy=skel_hierarchy)
    cv2.drawContours(pruned_plot, pruned_obj, -1, (255, 255, 255), params.line_thickness,
                     lineType=8, hierarchy=pruned_hierarchy)

    return pruned_img


def _find_tips(skel_img, mask=None):
    """Helper function to find tips in skeletonized image.
    The endpoints algorithm was inspired by Jean-Patrick Pommier: https://gist.github.com/jeanpat/5712699

    Inputs:
    skel_img    = Skeletonized image
    mask        = (Optional) binary mask for debugging. If provided, debug image will be overlaid on the mask.
    label       = Optional label parameter, modifies the variable name of
                  observations recorded (default = pcv.params.sample_label).
    Returns:
    tip_img   = Image with just tips, rest 0

    :param skel_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param label: str
    :return tip_img: numpy.ndarray
    """
    # In a kernel: 1 values line up with 255s, -1s line up with 0s, and 0s correspond to dont care
    endpoint1 = np.array([[-1, -1, -1],
                          [-1, 1, -1],
                          [0, 1,  0]])
    endpoint2 = np.array([[-1, -1, -1],
                          [-1, 1, 0],
                          [-1, 0, 1]])

    endpoint3 = np.rot90(endpoint1)
    endpoint4 = np.rot90(endpoint2)
    endpoint5 = np.rot90(endpoint3)
    endpoint6 = np.rot90(endpoint4)
    endpoint7 = np.rot90(endpoint5)
    endpoint8 = np.rot90(endpoint6)

    endpoints = [endpoint1, endpoint2, endpoint3, endpoint4, endpoint5, endpoint6, endpoint7, endpoint8]
    tip_img = np.zeros(skel_img.shape[:2], dtype=int)
    for endpoint in endpoints:
        tip_img = np.logical_or(cv2.morphologyEx(skel_img, op=cv2.MORPH_HITMISS, kernel=endpoint,
                                                 borderType=cv2.BORDER_CONSTANT, borderValue=0), tip_img)
    tip_img = tip_img.astype(np.uint8) * 255
    # Store debug
    debug = params.debug
    params.debug = None
    tip_objects, _ = _cv2_findcontours(bin_img=tip_img)

    if mask is None:
        # Make debugging image
        dilated_skel = dilate(skel_img, params.line_thickness, 1)
        tip_plot = cv2.cvtColor(dilated_skel, cv2.COLOR_GRAY2RGB)

    else:
        # Make debugging image on mask
        mask_copy = mask.copy()
        tip_plot = cv2.cvtColor(mask_copy, cv2.COLOR_GRAY2RGB)
        skel_obj, skel_hier = _cv2_findcontours(bin_img=skel_img)
        cv2.drawContours(tip_plot, skel_obj, -1, (150, 150, 150), params.line_thickness,
                         lineType=8, hierarchy=skel_hier)

    # Initialize list of tip data points
    tip_list = []
    tip_labels = []
    for i, tip in enumerate(tip_objects):
        x, y = tip.ravel()[:2]
        coord = (int(x), int(y))
        tip_list.append(coord)
        tip_labels.append(i)
        cv2.circle(tip_plot, (x, y), params.line_thickness, (0, 255, 0), -1)

    # Reset debug mode
    params.debug = debug

    return tip_img, tip_list, tip_labels


def _hough_circle(gray_img, mindist, candec, accthresh, minradius, maxradius, maxfound=None):
    """
    Hough Circle Detection

    Keyword inputs:
    gray_img = gray image (np.ndarray)
    mindist = minimum distance between detected circles
    candec = higher threshold of canny edge detector
    accthresh = accumulator threshold for the circl centers
    minradius = minimum circle radius
    maxradius = maximum circle radius
    maxfound = maximum number of circles to find

    :param gray_img: np.ndarray
    :param mindist: int
    :param candec: int
    :param accthresh: int
    :param minradius: int
    :param maxradius: int
    :param maxfound: None or int
    :return dataframe: pandas dataframe
    :return img: np.ndarray
    """
    # Store debug
    debug = params.debug
    params.debug = None

    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT,
                               dp=1, minDist=mindist,
                               param1=candec, param2=accthresh,
                               minRadius=minradius, maxRadius=maxradius)

    cimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    x = []
    y = []
    radius = []
    if circles is None:
        fatal_error('number of circles found is None with these parameters')
    circles = np.uint16(np.around(circles))
    if maxfound is not None:
        if maxfound >= len(circles[0, :]):
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                           params.line_thickness)
                # draw the center of the circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                           params.line_thickness)
                x.append(i[0])
                y.append(i[1])
                radius.append(i[2])
        else:
            for n, i in enumerate(circles[0, :]):
                if n <= (maxfound-1):
                    # draw the outer circle
                    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                               params.line_thickness)
                    # draw the center of the circle
                    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                               params.line_thickness)
                    x.append(i[0])
                    y.append(i[1])
                    radius.append(i[2])
            warn('Number of found circles is ' +
                 str(len(circles[0, :])) +
                 ' Change Parameters. Only drawing first '+str(maxfound))
    else:
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0),
                       params.line_thickness)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255),
                       params.line_thickness)
            x.append(i[0])
            y.append(i[1])
            radius.append(i[2])

    data = {'x': x, 'y': y, 'radius': radius}
    df = pd.DataFrame(data)

    # Reset debug mode
    params.debug = debug

    return df, cimg


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


def _rgb2lab(rgb_img, channel):
    """Convert image from RGB colorspace to LAB colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (l = lightness, a = green-magenta, b = blue-yellow)

    Returns
    -------
    numpy.ndarray
        grayscale image from one LAB color channel
    """
    # The allowable channel inputs are l, a or b
    channel = channel.lower()
    if channel not in ["l", "a", "b"]:
        fatal_error("Channel " + str(channel) + " is not l, a or b!")

    # Convert the input BGR image to LAB colorspace
    lab = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2LAB)
    # Split LAB channels
    l, a, b = cv2.split(lab)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"l": l, "a": a, "b": b}
    return channels[channel]


def _rgb2hsv(rgb_img, channel):
    """Convert image from RGB colorspace to HSV colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (h = hue, s = saturation, v = value/intensity/brightness)

    Returns
    -------
    numpy.ndarray
        grayscale image from one HSV color channel
    """
    # The allowable channel inputs are h, s or v
    channel = channel.lower()
    if channel not in ["h", "s", "v"]:
        fatal_error("Channel " + str(channel) + " is not h, s or v!")

    # Convert the input BGR image to HSV colorspace
    hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    # Split HSV channels
    h, s, v = cv2.split(hsv)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"h": h, "s": s, "v": v}

    return channels[channel]


def _rgb2cmyk(rgb_img, channel):
    """Convert image from RGB colorspace to CMYK colorspace. Returns the specified subchannel as a gray image.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data
    channel : str
        color subchannel (c = cyan, m = magenta, y = yellow, k=black)

    Returns
    -------
    numpy.ndarray
        grayscale image from one CMYK color channel
    """
    # Set NumPy to ignore divide by zero errors
    _ = np.seterr(divide='ignore', invalid='ignore')
    # The allowable channel inputs are c, m , y or k
    channel = channel.lower()
    if channel not in ["c", "m", "y", "k"]:
        fatal_error("Channel " + str(channel) + " is not c, m, y or k!")

    # Create float
    bgr = rgb_img.astype(float)/255.

    # K channel
    k = 1 - np.max(bgr, axis=2)

    # C Channel
    c = (1 - bgr[..., 2] - k) / (1 - k)

    # M Channel
    m = (1 - bgr[..., 1] - k) / (1 - k)

    # Y Channel
    y = (1 - bgr[..., 0] - k) / (1 - k)

    # Convert the input BGR image to LAB colorspace
    cmyk = (np.dstack((c, m, y, k)) * 255).astype(np.uint8)
    # Split CMYK channels
    y, m, c, k = cv2.split(cmyk)
    # Create a channel dictionaries for lookups by a channel name index
    channels = {"c": c, "m": m, "y": y, "k": k}

    return channels[channel]


def _rgb2gray(rgb_img):
    """Convert image from RGB colorspace to Gray.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        RGB image data

    Returns
    -------
    numpy.ndarray
        grayscale image
    """
    gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)

    return gray
