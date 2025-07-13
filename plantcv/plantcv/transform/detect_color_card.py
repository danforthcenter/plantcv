"""Automatically detect color cards.

Algorithm written by mtwatso2-eng (github). Updated and implemented into PlantCV by Haley Schuhl.
"""
import os
import cv2
import math
import numpy as np
from plantcv.plantcv import params, outputs, fatal_error, deprecation_warning, warn
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray, _cv2_findcontours, _object_composition


def _is_square(contour, min_size):
    """Determine if a contour is square or not.

    Parameters
    ----------
    contour : list
        OpenCV contour.

    Returns
    -------
    bool
        True if the contour is square, False otherwise.
    """
    return (cv2.contourArea(contour) > min_size and
            max(cv2.minAreaRect(contour)[1]) / min(cv2.minAreaRect(contour)[1]) < 1.27 and
            (cv2.contourArea(contour) / np.prod(cv2.minAreaRect(contour)[1])) > 0.8)


def _get_contour_sizes(contours):
    """Get the shape and size of all contours.

    Parameters
    ----------
    contours : list
        List of OpenCV contours.

    Returns
    -------
    list
        Contour areas, widths, and heights.
    """
    # Initialize chip shape lists
    marea, mwidth, mheight = [], [], []
    # Loop over our contours and size data about them
    for cnt in contours:
        marea.append(cv2.contourArea(cnt))
        _, wh, _ = cv2.minAreaRect(cnt)  # Rotated rectangle
        mwidth.append(wh[0])
        mheight.append(wh[1])
    return marea, mwidth, mheight


def _draw_color_chips(rgb_img, centers, radius):
    """Create labeled mask and debug image of color chips.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    new_centers : numpy.array
        Chip centers after transformation.
    radius : int or list
        Radius of circles to draw on the color chips.

    Returns
    -------
    list
        Labeled mask and debug image.
    """
    # Create blank img for drawing the labeled color card mask
    labeled_mask = np.zeros(rgb_img.shape[0:2])
    debug_img = np.copy(rgb_img)

    # Calculate the offset for centering text positions
    text_size, _ = cv2.getTextSize(str(id), cv2.FONT_HERSHEY_SIMPLEX, params.text_size, params.text_thickness)
    offset_dir = np.array([-1, 1])

    # Loop over the new chip centers and draw them on the RGB image and labeled mask
    if type(radius) is int:
        for i, pt in enumerate(centers):
            cv2.circle(labeled_mask, centers[i], radius, [(i + 1) * 10], -1)
            cv2.circle(debug_img, centers[i], radius, (255, 255, 0), -1)

            text_pos = (pt + text_size*offset_dir/2).astype(int)
            cv2.putText(debug_img, text=str(i), org=text_pos, fontScale=params.text_size, color=(0, 0, 0),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)
    elif len(radius) == len(centers):
        for i, pt in enumerate(centers):
            cv2.circle(labeled_mask,  centers[i], radius[i], [(i + 1) * 10], -1)
            cv2.circle(debug_img, centers[i], radius[i], (255, 255, 0), -1)

            text_pos = (pt + text_size*offset_dir/2).astype(int)
            cv2.putText(debug_img, text=str(i), org=text_pos, fontScale=params.text_size, color=(0, 0, 0),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)
    else:
        fatal_error(f"Radius must be int or list with same length as centers, not: {radius}")

    return labeled_mask, debug_img


def _calibrite_card_detection(rgb_img, **kwargs):
    """Algorithm to automatically detect a color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------
    list
        Labeled mask of chips, debug img, detected chip areas, chip heights, chip widths, bounding box mask
    """
    # Get keyword arguments and set defaults if not set
    min_size = kwargs.get("min_size", 1000)  # Minimum size for _is_square chip filtering
    radius = kwargs.get("radius", 20)  # Radius of circles to draw on the color chips
    adaptive_method = kwargs.get("adaptive_method", 1)  # cv2.adaptiveThreshold method
    block_size = kwargs.get("block_size", 51)  # cv2.adaptiveThreshold block size

    # Throw a fatal error if block_size is not odd or greater than 1
    if not (block_size % 2 == 1 and block_size > 1):
        fatal_error('block_size parameter must be an odd int greater than 1.')

    nrows = 6
    ncols = 4

    # Convert to grayscale, threshold, and findContours
    imgray = _rgb2gray(rgb_img=rgb_img)
    gaussian = cv2.GaussianBlur(imgray, (11, 11), 0)
    thresh = cv2.adaptiveThreshold(gaussian, 255, adaptive_method, cv2.THRESH_BINARY_INV, block_size, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours, keep only square-shaped ones
    filtered_contours = [contour for contour in contours if _is_square(contour, min_size)]
    # Calculate median area of square contours
    target_square_area = np.median([cv2.contourArea(cnt) for cnt in filtered_contours])
    # Filter contours again, keep only those within 20% of median area
    filtered_contours = [contour for contour in filtered_contours if
                         (0.8 < (cv2.contourArea(contour) / target_square_area) < 1.2)]

    # Throw a fatal error if no color card found
    if len(filtered_contours) == 0:
        fatal_error('No color card found')

    # Draw filtered contours on debug img
    debug_img = np.copy(rgb_img)
    cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
    # Find the bounding box of the detected chips
    x, y, w, h = cv2.boundingRect(np.vstack(filtered_contours))

    # Draw the bound box rectangle
    bounding_mask = cv2.rectangle(np.zeros(rgb_img.shape[0:2]), (x, y), (x + w, y + h), (255), -1).astype(np.uint8)

    # Initialize chip shape lists
    marea, mwidth, mheight = _get_contour_sizes(filtered_contours)

    # Concatenate all contours into one array and find the minimum area rectangle
    rect = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
    rect = cv2.minAreaRect(rect)
    # Get the corners of the rectangle
    corners = np.array(np.intp(cv2.boxPoints(rect)))
    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rgb_img[corner[1], corner[0], :], (255, 255, 255))) for corner in corners])
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[0, 1, 3, 2]]]
    # Increment amount is arbitrary, cell distances rescaled during perspective transform
    increment = 100
    centers = [[int(0 + i * increment), int(0 + j * increment)] for j in range(nrows) for i in range(ncols)]

    # Find the minimum area rectangle of the chip centers
    new_rect = cv2.minAreaRect(np.array(centers))
    # Get the corners of the rectangle
    box_points = cv2.boxPoints(new_rect).astype("float32")
    # Calculate the perspective transform matrix from the minimum area rectangle
    m_transform = cv2.getPerspectiveTransform(box_points, corners.astype("float32"))
    # Transform the chip centers using the perspective transform matrix
    new_centers = cv2.transform(np.array([centers]), m_transform)[0][:, 0:2]

    # Create labeled mask and debug image of color chips
    labeled_mask, debug_img = _draw_color_chips(debug_img, new_centers, radius)

    return labeled_mask, debug_img, marea, mheight, mwidth, bounding_mask


def _find_aruco_tags(img, aruco_dict):
    """Search for aruco tags in a specified tag dictionary

    Parameters
    ----------
    img : np.ndarray
        Input RGB or Grayscale image data containing aruco tags.
    aruco_dict : cv2.aruco.Dictionary
        CV2 Aruco Dictionary containing tags to be located.

    Returns
    -------
    list
        tag bounding boxes, tag IDs, rejected tag bounding boxes
    """
    # TODO: Not needed for current implementation of helper, but might want **kwargs to pass to cv2.aruco.DetectorParameters
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary=aruco_dict, detectorParams=aruco_params)
    tag_bboxes, tag_ids, rejects = detector.detectMarkers(img)

    # Sort bounding boxes by tag ID
    tag_ids, tag_bboxes = zip(*sorted(zip(tag_ids, tag_bboxes), key=lambda x: x[0]))

    return tag_bboxes, tag_ids, rejects


def _get_astro_std_mask():
    """Define reference centers of chips on a 600x700 px astrobotany color card

    Returns
    -------
    numpy.ndarray
        Standard perspective mask of astrobotany color card chips
    """
    # Define center and radii to draw on chps
    centers = [[94, 271],   # Blue
               [222, 271],  # Green
               [350, 271],  # Red
               [478, 271],  # Yellow
               [606, 271],  # Black
               # Gray chips
               [62, 371],   # Value 100 (White)
               [127, 371],  # Value 92
               [192, 371],  # Value 77
               [257, 371],  # Value 67
               [322, 371],  # Value 58
               [387, 371],  # Value 48
               [452, 371],  # Value 36
               [517, 371],  # Value 28
               [582, 371],  # Value 22
               [647, 371]]  # Value 17 (Black)
    radii = [40 if y == 271 else 20 for _, y in centers]

    std_mask = np.zeros(shape=(600, 700), dtype=np.uint8)
    std_mask, _ = _draw_color_chips(std_mask, centers, radii)

    return std_mask


def _astrobotany_card_detection(rgb_img, **kwargs):
    """Algorithm to automatically detect a color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    **kwargs : optional
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------
    list
        Labeled mask of chips, debug img, aligned card image, detected chip areas,
            chip heights, chip widths, and bounding box mask
    """
    # Convert to grayscale and search for aruco tags
    imgray = _rgb2gray(rgb_img=rgb_img)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    tag_bboxes, tag_ids, _ = _find_aruco_tags(imgray, aruco_dict)

    # Check contents of tag_ids against expected tags
    expected_ids = [46, 47, 48, 49]
    missing_ids = []
    for id in expected_ids:
        id_count = tag_ids.count(id)
        if id_count == 0:
            missing_ids.append(id)
        elif id_count > 1:
            fatal_error(f"Expected ArUco tag (ID = {id}) occurs more than once in image. Can not locate color card.")
    # Warn user if some expected tags are not present in image and attempt color correction
    if len(missing_ids) > 3:
        fatal_error("No expected ArUco tags were found in image. Can not locate color card.")
    # Throw a fatal error if none were found
    elif len(missing_ids) > 0:
        warn(f"Missing {len(missing_ids)} aruco tags in image. Attempting color correction, check card alignment!")

    # Generate debug image
    debug_img = np.copy(rgb_img)
    # Dict of pt indices for outer corner of each of glyph ID
    outer_corners = {46: 3, 47: 0, 48: 1, 49: 2}
    corner_pts = []
    for id, bbox in zip(tag_ids, tag_bboxes):
        id = id[0]
        # Draw tags on debug img
        bbox = np.array(bbox.reshape(-1, 2), dtype=np.int32)
        cv2.polylines(debug_img, [bbox], True, (255, 50, 250), thickness=params.line_thickness)
        # Label tags on debug image (centering text)
        text_size, _ = cv2.getTextSize(str(id), cv2.FONT_HERSHEY_SIMPLEX, params.text_size, params.text_thickness)
        center = np.mean(bbox, axis=0)
        offset_dir = np.array([-1, 1])
        text_pos = (center + text_size*offset_dir/2).astype(int)
        cv2.putText(debug_img, str(id), text_pos, cv2.FONT_HERSHEY_SIMPLEX, params.text_size, (255, 50, 250), params.text_thickness)

        # Get outer corner points for bounding mask
        corner_pts.append(bbox[outer_corners[id]])

    # Draw the bounding mask
    bounding_mask = cv2.fillPoly(np.zeros(rgb_img.shape[:2]), np.array([corner_pts]), 255).astype(np.uint8)

    # Build paired lists of points for aligning color card
    tag_topleft = {46: (0, 495), 47: (0, 0), 48: (595, 0), 48: (595, 495)}
    img_pts = []
    ref_pts = []
    for id, bbox in zip(tag_ids, tag_bboxes):
        # Do nothing if not a color card tag ID
        if id not in expected_ids:
            continue

        img_pts.extend(bbox)

        x, y = tag_topleft[id]
        ref_bbox = [[x, y], [x+105, y], [x+105, y+105], [x, y+105]]
        ref_pts.extend(ref_bbox)

    img_pts = np.array(img_pts)
    ref_pts = np.array(ref_pts)
    # Calculate matrix to transform reference chip centers to image
    mat, _ = cv2.findHomography(ref_pts, img_pts, method=0)
    if mat is None:
        fatal_error("Cannot calculate a robust model with given corresponding coordinates!")

    # Apply inverse matrix generate image of aligned color card
    inv_mat = np.linalg.inv(mat)
    card_img = cv2.warpPerspective(rgb_img, M=inv_mat, dsize=(700, 600))

    # Get reference card mask and transform to image position
    std_mask = _get_astro_std_mask()
    img_mask = cv2.warpPerspective(std_mask, mat, dsize=rgb_img.shape[:2])

    return img_mask, debug_img, card_img, marea, mheight, mwidth, bounding_mask


def mask_color_card(rgb_img, card_type=0, **kwargs):
    """Automatically detect a color card and create bounding box mask of the chips detected.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    card_type : int
        reference value indicating the type of card being used for correction:
                card_type = 0: calibrite color card (default)
                card_type = 1: astrobotany.com AIRI calibration sticker
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------
    numpy.ndarray
        Binary bounding box mask of the detected color card chips
    """
    if card_type == 0:
        *_, bounding_mask = _calibrite_card_detection(rgb_img, **kwargs)
    elif card_type == 1:
        *_, bounding_mask = _astrobotany_card_detection(rgb_img, **kwargs)
    else:
        fatal_error("Invalid option passed to <card_type>. Options are 0 (Calibrite) or 1 (Astrobotany)")

    if params.debug is not None:
        # Find contours
        cnt, cnt_str = _cv2_findcontours(bin_img=bounding_mask)

        # Consolidate contours
        obj = _object_composition(contours=cnt, hierarchy=cnt_str)
        bb_debug = cv2.drawContours(np.copy(rgb_img), [obj], -1, (255, 0, 255), params.line_thickness)

        # Debug image handling
        _debug(visual=bb_debug, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return bounding_mask


def detect_color_card(rgb_img, label=None, card_type=0, **kwargs):
    """Automatically detect a color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    card_type : int
        reference value indicating the type of card being used for correction:
                card_type = 0: calibrite color card (default)
                card_type = 1: astrobotany.com AIRI calibration sticker
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)

    Returns
    -------
    numpy.ndarray
        Labeled mask of chips.
    """
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )

    if (card_type != 0) or (card_type != 1):
        # TODO: Check for aruco tags and set card_type accordingly.
        warn("Invalid option for arg:card_type, attempting to automatically determine card type.")
    if card_type == 0:
        # Search image for a Calibrite color card grid
        labeled_mask, debug_img, marea, mheight, mwidth, _ = _calibrite_card_detection(rgb_img, **kwargs)

        # Create dataframe for easy summary stats
        chip_size = np.median(marea)
        chip_height = np.median(mheight)
        chip_width = np.median(mwidth)

        # Save out chip size for pixel to cm standardization
        outputs.add_metadata(term="median_color_chip_size", datatype=float, value=chip_size)
        outputs.add_metadata(term="median_color_chip_width", datatype=float, value=chip_width)
        outputs.add_metadata(term="median_color_chip_height", datatype=float, value=chip_height)

    elif card_type == 1:
        # Search image for an astrobotany.com color card
        labeled_mask, debug_img, card_img, *_ = _astrobotany_card_detection(rgb_img, **kwargs)

        # TODO: Add metadata outputs for size calibration

        # Second debug image of transformed color card
        _debug(visual=card_img, filename=os.path.join(params.debug_outdir, f'{params.device}_reference_color_card.png'))

    else:
        # Throw a fatal error if an invalid value was passed for card_type, and it could not be determined
        fatal_error("Could not automatically determine the type of color card. Specify with the <card_type> parameter.")

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return labeled_mask
