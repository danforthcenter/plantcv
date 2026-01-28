"""Automatically detect color cards.

Algorithm written by mtwatso2-eng (github). Updated and implemented into PlantCV by Haley Schuhl.
"""

import os
import cv2
import math
import numpy as np
from plantcv.plantcv import params, outputs, fatal_error, warn
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2hsv, _rgb2gray, _cv2_findcontours, _object_composition, _rect_filter
from plantcv.plantcv.transform.color_correction import get_color_matrix


def _is_square(contour, min_size, aspect_ratio=1.27, solidity=0.8):
    """Return list of contours, based on aspect ratio and solidity.

    Parameters
    ----------
    contour : list
        OpenCV contour.
    min_size : int
        Minimum object size to be considered
    aspect_ratio : float
        Filter contours below a given aspect ratio
    solidity : float
        Filter contours below a given solidity

    Returns
    -------
    bool
        True if the contour is square, False otherwise.
    """
    # Take reciprocal if aspect_ratio is smaller than 1
    aspect_ratio = max([aspect_ratio, 1]) / min([aspect_ratio, 1])

    return (
        cv2.contourArea(contour) > min_size
        and
        # Test that the Aspect Ratio (default 1.27)
        # ratio between the width and height of minAreaRect
        # which is like a bounding box but will consider rotation
        max(cv2.minAreaRect(contour)[1]) / min(cv2.minAreaRect(contour)[1]) < aspect_ratio
        and
        # Test that the Solidity (default 0.8)
        # Compare minAreaRect area to the actual contour area, a chip should be mostly solid
        (cv2.contourArea(contour) / np.prod(cv2.minAreaRect(contour)[1])) > solidity
    )


def _find_color_chip_like_objects(rgb_img, **kwargs):
    """Get the square-like and similarly sized objects from an RGB image.

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
        aspect_ratio: countour squareness filters (default 1.27)
        solidity: contour squareness filters (default 0.8)

    Returns
    -------
    list
        List of detected chip contours
    """
    # Get keyword arguments and set defaults if not set
    min_size = kwargs.get("min_size", 1000)  # Minimum size for _is_square chip filtering
    adaptive_method = kwargs.get("adaptive_method", 1)  # cv2.adaptiveThreshold method
    block_size = kwargs.get("block_size", 51)  # cv2.adaptiveThreshold block size
    aspect_ratio = kwargs.get("aspect_ratio", 1.27)  # _is_square aspect-ratio filtering
    solidity = kwargs.get("solidity", 0.8)  # _is_square solidity filtering

    # Throw a fatal error if block_size is not odd or greater than 1
    if not (block_size % 2 == 1 and block_size > 1):
        fatal_error("block_size parameter must be an odd int greater than 1.")

    # Convert to grayscale, threshold, and findContours
    imgray = _rgb2hsv(rgb_img=rgb_img, channel="v")
    gaussian = cv2.GaussianBlur(imgray, (11, 11), 0)
    thresh = cv2.adaptiveThreshold(gaussian, 255, adaptive_method, cv2.THRESH_BINARY_INV, block_size, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Filter contours, keep only square-shaped ones
    filtered_contours = [contour for contour in contours if _is_square(contour, min_size, aspect_ratio, solidity)]
    # Calculate median area of square contours
    target_square_area = np.median([cv2.contourArea(cnt) for cnt in filtered_contours])
    # Filter contours again, keep similar sized objects, only those within 20% of median area
    return [contour for contour in filtered_contours if (0.8 < (cv2.contourArea(contour) / target_square_area) < 1.2)]


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
    centers : numpy.array
        Chip centers after transformation.
    radius : int or list
        Radius of circles to draw on the color chips. If list, must be the same length as `centers` param.

    Returns
    -------
    list
        Labeled mask and debug image.
    """
    # Create blank img for drawing the labeled color card mask
    labeled_mask = np.zeros(rgb_img.shape[0:2])
    debug_img = np.copy(rgb_img)

    offset_dir = np.array([-1, 1])

    # Loop over the new chip centers and draw them on the RGB image and labeled mask
    if type(radius) is int:
        for i, pt in enumerate(centers):
            cv2.circle(labeled_mask, centers[i], radius, [(i + 1) * 10], -1)
            cv2.circle(debug_img, centers[i], radius, (255, 255, 0), -1)

            text_size, _ = cv2.getTextSize(str(i), cv2.FONT_HERSHEY_SIMPLEX, params.text_size, params.text_thickness)
            text_pos = (pt + text_size*offset_dir/2).astype(int)
            cv2.putText(debug_img, text=str(i), org=text_pos, fontScale=params.text_size, color=(0, 0, 0),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)

    elif len(radius) == len(centers):
        for i, pt in enumerate(centers):
            cv2.circle(labeled_mask,  centers[i], radius[i], [(i + 1) * 10], -1)
            cv2.circle(debug_img, centers[i], radius[i], (255, 255, 0), -1)

            text_size, _ = cv2.getTextSize(str(i), cv2.FONT_HERSHEY_SIMPLEX, params.text_size, params.text_thickness)
            text_pos = (pt + text_size*offset_dir/2).astype(int)
            cv2.putText(debug_img, text=str(i), org=text_pos, fontScale=params.text_size, color=(0, 0, 0),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)

    else:
        fatal_error("Radius must be int or list with same length as `centers` param.")

    return labeled_mask, debug_img


def _check_point_per_chip(contours, centers, debug_img):
    """Check that each detected chip ends up with exactly 1 mask inside it

    Parameters
    ----------
    contours : list
             OpenCV contour
    centers : numpy.ndarray
             (X, Y) points of the center of each prospective mask to make
    debug_img : numpy.ndarray
             Debug image to show the problem if a fatal error is generated

    Returns
    -------
    No returns

    Raises
    ------
    fatal_error
          If any contour does not have exactly 1 mask center inside it (not on edge)
    """
    contour_has_n_points = []
    for cont in contours:
        bools = []
        for pt in centers:
            # -1 is outside, 0 is on line, 1 is inside
            bools.append(cv2.pointPolygonTest(cont, (int(pt[0]), int(pt[1])), False) == 1)
        contour_has_n_points.append(sum(bools))

    if any(n != 1 for n in contour_has_n_points):
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f"{params.device}_color_card.png"))
        fatal_error("Centers do not map 1 to 1 with detected color chips")


def _check_no_aruco_tags(img):
    """Check that there are not aruco tags in an image

    Parameters
    ----------
    img : numpy.ndarray
        Input RGB or Grayscale image data.

    Returns
    -------
    No returns

    Raises
    ------
    warning
          If there are aruco tags in an image analysed for a macbeth color card
    """
    # set up default aruco tag detection
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary=aruco_dict, detectorParams=aruco_params)
    tag_bboxes, _, _ = detector.detectMarkers(img)
    if len(tag_bboxes):
        debug_img = np.copy(img)
        cv2.aruco.drawDetectedMarkers(debug_img, tag_bboxes)
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card_has_ArUco.png'))
        warn("Image contains an ArUco tag, should you be using color_chip_size='astro'?")


def _check_corners(img, corners):
    """Check that corners are within an image
    Parameters
    ----------
    img: numpy.ndarray
         An image
    corners: numpy.ndarray
         Corners for some object
    """
    dim = np.shape(img)
    for pt in corners:
        if pt[0] > dim[1] or pt[1] > dim[0] or pt[0] < 0 or pt[1] < 0:
            fatal_error("Color card corners could not be detected accurately")


def _macbeth_card_detection(rgb_img, **kwargs):
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
        aspect_ratio: countour squareness filters (default 1.27)
        solidity: contour squareness filters (default 0.8)

    Returns
    -------
    list
        Color matrix, debug img, detected chip areas, chip heights, chip widths, bounding box mask
    """
    nrows = 6
    ncols = 4
    # Radius of circles to draw on the color chips, adaptive unless set by the user
    radius = kwargs.get("radius")
    filtered_contours = _find_color_chip_like_objects(rgb_img, **kwargs)

    # Throw a fatal error if no color card found
    if len(filtered_contours) == 0:
        fatal_error("No color card found")
    # check if there are aruco tags, warn about possible wrong mode
    _check_no_aruco_tags(rgb_img)
    # Find the bounding box of the detected chips
    x, y, w, h = cv2.boundingRect(np.vstack(filtered_contours))

    # Draw the bound box rectangle
    boundind_mask = cv2.rectangle(np.zeros(rgb_img.shape[0:2]), (x, y), (x + w, y + h), (255), -1).astype(np.uint8)

    # Initialize chip shape lists
    marea, mwidth, mheight = _get_contour_sizes(filtered_contours)

    # Concatenate all detected centers into one array (minimum area rectangle used to find chip centers)
    square_centroids = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])

    # Concatenate all contours into one array and find the minimum area rectangle
    rect = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
    rect = cv2.minAreaRect(rect)
    # Get the corners of the rectangle
    corners = np.array(np.intp(cv2.boxPoints(rect)))
    # Check that corners are in image
    _check_corners(rgb_img, corners)
    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rgb_img[corner[1], corner[0], :], (255, 255, 255))) for corner in corners])
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[0, 1, 3, 2]]]
    rot_img = np.rot90(rgb_img, k=white_index, axes=(0, 1)).copy()
    # rotate the image so that the white color chip is warp-able to the top left position without mirroring the card
    rotations = white_index
    if rotations:  # if the image was rotated, find new contours for chips
        filtered_contours = _find_color_chip_like_objects(rot_img, **kwargs)
        # Find the bounding box of the detected chips
        x, y, w, h = cv2.boundingRect(np.vstack(filtered_contours))
        # Draw the bound box rectangle
        boundind_mask = cv2.rectangle(np.zeros(rot_img.shape[0:2]), (x, y), (x + w, y + h), (255), -1).astype(np.uint8)
        # Initialize chip shape lists
        marea, mwidth, mheight = _get_contour_sizes(filtered_contours)
        # Concatenate all detected centers into one array (minimum area rectangle used to find chip centers)
        square_centroids = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
        # Concatenate all contours into one array and find the minimum area rectangle
        rect = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
        rect = cv2.minAreaRect(rect)
        # Get the corners of the rectangle
        corners = np.array(np.intp(cv2.boxPoints(rect)))

    centers1 = cv2.approxPolyN(curve=square_centroids, nsides=4, ensure_convex=True)

    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rot_img[corner[1], corner[0], :], (255, 255, 255))) for corner in centers1[0]])
    # Get outter corners of corner chips and sort based on card orientation
    corners = cv2.approxPolyN(curve=np.concatenate(filtered_contours), nsides=4, ensure_convex=True)
    corners = np.concatenate(corners)
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[1, 3, 2, 0]]]

    if params.verbose:
        # Draw new contours onto cropped card debug image
        debug_img = np.copy(rot_img)
        cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
        cv2.drawContours(debug_img, [corners], -1, color=(255, 0, 0), thickness=params.line_thickness)
        unrot_debug_img = np.rot90(debug_img, k=-1*rotations, axes=(0, 1)).copy()
        _debug(visual=unrot_debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_detected_color_card.png'))

    # Perspective warp the color card to unskew and square to frame
    pt_A, pt_B, pt_C, pt_D = corners
    input_pts = np.float32([pt_A, pt_B, pt_C, pt_D])

    length_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    length_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    length_card1 = max(int(length_AD), int(length_BC))

    length_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    length_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    length_card2 = max(int(length_AB), int(length_CD))

    output_pts = np.float32([[0, 0], [0, length_card2 - 1], [length_card1 - 1, length_card2 - 1], [length_card1 - 1, 0]])
    # Transform the color card to crop (and unwarp)
    matrix = cv2.getPerspectiveTransform(input_pts, output_pts)
    out = cv2.warpPerspective(
        rot_img, matrix, (min(length_card1, length_card2), max(length_card1, length_card2)), flags=cv2.INTER_LINEAR
    )

    # Increment amount is arbitrary, cell distances rescaled during perspective transform
    increment = 100
    new_centers = [[int(0 + i * increment), int(0 + j * increment)] for j in range(nrows) for i in range(ncols)]
    # Create color card mask based on size of detected color card
    w_increment = int(length_card1 / 3.7) + 1
    h_increment = int(length_card2 / 5.7) + 1
    increment = int((w_increment + h_increment) / 2)
    if not radius:
        radius = int(increment / 15) + 1
    start_x = int(increment * 0.3) + 1
    start_y = int(start_x * 1.1)
    new_centers_w = [
        [int(start_x + i * w_increment), int(start_y + j * h_increment)] for j in range(nrows) for i in range(ncols)
    ]
    # Find contours again to see if alignment of centers passes qc
    filtered_contours = _find_color_chip_like_objects(out, **kwargs)

    # Draw new contours onto cropped card debug image
    debug_img = np.copy(rot_img)
    cv2.drawContours(debug_img, filtered_contours, -1, color=(255, 50, 250), thickness=params.line_thickness)
    # Create labeled mask and debug image of color chips
    labeled_mask, debug_img = _draw_color_chips(out, new_centers_w, radius)
    # Check that new centers are inside each unique filtered_contour
    _check_point_per_chip(filtered_contours, new_centers_w, debug_img)
    # Calculate color matrix from the cropped color card image
    _, color_matrix = get_color_matrix(rgb_img=out, mask=labeled_mask)

    return color_matrix, debug_img, marea, mheight, mwidth, boundind_mask


def _find_aruco_tags(img, aruco_dict):
    """Search for aruco tags in a specified tag dictionary

    Parameters
    ----------
    img : numpy.ndarray
        Input RGB or Grayscale image data.
    aruco_dict : cv2.aruco.Dictionary
        CV2 Aruco Dictionary containing tags to be located.

    Returns
    -------
    tag_bboxes : list
        List of aruco tag bounding boxes, sorted by tag ID
    tag_ids : list
        List of identified aruco tag IDs, sorted by tag ID
    rejects : list
        List of rejected aruco tag bounding boxes
    """
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary=aruco_dict, detectorParams=aruco_params)
    tag_bboxes, tag_ids, rejects = detector.detectMarkers(img)

    # Sort bounding boxes by tag ID, raises TypeError if no tags are detected
    try:
        tag_ids, tag_bboxes = zip(*sorted(zip(tag_ids, tag_bboxes), key=lambda x: x[0]))
    except TypeError:
        fatal_error("No ArUco tags detected in image. Can not locate color card.")

    return tag_bboxes, tag_ids, rejects


def _get_astro_std_mask():
    """Define reference centers of chips on an aligned 600x700 px astrobotany color card

    Returns
    -------
    numpy.ndarray
        Standard perspective mask of astrobotany color card chips
    """
    # Define centers and radii of chips
    centers = [[94, 271],   # Blue
               [222, 271],  # Green
               [350, 271],  # Red
               [478, 271],  # Yellow
               [606, 271],  # Black
               # Grayscale chips
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

    # Top row of chips (BGRYK) are larger than the row of gray scale chips
    radii = [40 if y == 271 else 20 for _, y in centers]

    # Generate empty image and draw chips around centers
    std_mask = np.zeros(shape=(600, 700), dtype=np.uint8)
    std_mask, _ = _draw_color_chips(std_mask, centers, radii)

    return std_mask


def _astrobotany_card_detection(rgb_img, **kwargs):
    """Algorithm to automatically detect an astrobotany.com-style color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
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

    # Generate debug image and draw on detected aruco tags
    debug_img = np.copy(rgb_img)
    for id, bbox in zip(tag_ids, tag_bboxes):
        id = id[0]
        # Outline all aruco tags on debug img
        bbox = np.array(bbox.reshape(-1, 2), dtype=np.int32)
        cv2.polylines(debug_img, [bbox], True, (255, 50, 250), params.line_thickness)
        # Calculate offset to center text on outlined aruco tags
        text_size, _ = cv2.getTextSize(str(id), cv2.FONT_HERSHEY_SIMPLEX, params.text_size, params.text_thickness)
        center = np.mean(bbox, axis=0)
        # Offset needs to shift along -x and +y
        offset_dir = np.array([-1, 1])
        text_pos = (center + text_size*offset_dir/2).astype(int)
        # Label aruco tags on debug image
        cv2.putText(debug_img, str(id), text_pos, cv2.FONT_HERSHEY_SIMPLEX, params.text_size, (255, 50, 250),
                    params.text_thickness)

    # Check contents of tag_ids for absence and duplication
    expected_ids = [46, 47, 48, 49]
    missing_ids = []
    for id in expected_ids:
        id_count = tag_ids.count(id)
        if id_count == 0:
            missing_ids.append(id)
        elif id_count > 1:
            # Show or save debug plot
            _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_duplicate_aruco.png'))
            fatal_error(f"Expected ArUco tag (ID = {id}) occurs more than once in image. Can not locate color card.")
    # Warn user if some expected tags are not present in image and attempt color correction
    if len(missing_ids) > 3:
        # Show or save debug plot
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_no_card.png'))
        fatal_error("No expected ArUco tags were found in image. Can not locate color card.")
    # Throw a fatal error if none were found
    elif len(missing_ids) > 0:
        warn(f"Missing {len(missing_ids)} aruco tag(s) in image. Attempting color correction, check warp alignment!")

    # Coordinates for top-left corner of each aruco tag in a standard-sized 600x700 image
    tag_topleft = {46: (0, 495), 47: (0, 0), 48: (595, 0), 49: (595, 495)}
    img_pts, ref_pts = [], []
    marea, mheight, mwidth = [], [], []
    for id, bbox in zip(tag_ids, tag_bboxes):
        id = id[0]
        # Do nothing if not a color card tag ID
        if id not in expected_ids:
            continue
        # Measure area, height, and width of aruco tag in pixels
        area, height, width = _get_contour_sizes(bbox)
        # Convert measurements to px/sq-cm (area) or px/cm (h/w)
        marea.append(area)
        mheight.append(height)         # Tag height is 0.7975 cm
        mwidth.append(width)           # Tag width is 0.7975 cm
        # Add coordinates of tag corners in image
        img_pts.extend(*bbox)
        # Add coordinates of tag corners on a standard-size color card
        x, y = tag_topleft[id]
        ref_bbox = [[x, y], [x+105, y], [x+105, y+105], [x, y+105]]
        ref_pts.extend(ref_bbox)

    # Convert reference and image points to arrays for cv2.findHomography
    img_pts = np.array(img_pts)
    ref_pts = np.array(ref_pts)

    # Calculate matrix to transform standard-size color card to the image
    mat, _ = cv2.findHomography(ref_pts, img_pts, method=0)

    # Apply inverse matrix to generate image of aligned color card
    inv_mat = np.linalg.inv(np.array(mat).astype(np.float32))
    card_img = cv2.warpPerspective(rgb_img, M=inv_mat, dsize=(700, 600))

    # Get reference card mask and transform to image position
    standard_mask = _get_astro_std_mask()
    labeled_mask = cv2.warpPerspective(standard_mask, mat, dsize=rgb_img.shape[1::-1], flags=cv2.INTER_NEAREST)

    # Draw transformed chips on debug image
    for i in np.unique(labeled_mask):
        if i != 0:
            debug_img[np.where(labeled_mask == i)] = [255, 255, 0]

    # Generate color card bounding mask
    bounding_mask = cv2.warpPerspective(np.ones(shape=(600, 700), dtype=np.uint8)*255, mat, dsize=rgb_img.shape[1::-1],
                                        flags=cv2.INTER_NEAREST)
    # Calculate color matrix from the cropped color card image
    _, color_matrix = get_color_matrix(rgb_img=rgb_img, mask=labeled_mask)
    return color_matrix, debug_img, marea, mheight, mwidth, bounding_mask


def _set_size_scale_from_chip(color_chip_width, color_chip_height, color_chip_size):
    """Set the size scaling factors in Params from the known size of a given color card target.

    Parameters
    ----------
    color_chip_width : float
        Width in pixels of the detected color chips
    color_chip_height : float
        Height in pixels of the detected color chips
    color_chip_size : str, tuple
        Type of supported color card target ("classic", "passport", "nano", "mini", "cameratrax", or "astro"),
        or a tuple of (width, height) of the color card chip real-world dimensions in milimeters.
    """
    # Define known color chip dimensions, all in milimeters
    card_types = {
        "CLASSIC": {
            "chip_width": 40,
            "chip_height": 40
        },
        "PASSPORT": {
            "chip_width": 12,
            "chip_height": 12
        },
        "CAMERATRAX": {
            "chip_width": 11,
            "chip_height": 11
        },
        "NANO": {
            "chip_width": 4,
            "chip_height": 3
        },
        "MINI": {
            "chip_width": 12,
            "chip_height": 12
        }
    }

    # Check if user provided a valid color card type
    if type(color_chip_size) is str and color_chip_size.upper() in card_types:
        # Set size scaling parameters, match larger dimensions with each other
        obs_chip_dims = [color_chip_width, color_chip_height]
        known_chip_dims = [
            card_types[color_chip_size.upper()]["chip_width"],
            card_types[color_chip_size.upper()]["chip_height"],
        ]
        params.px_width = max(known_chip_dims) / max(obs_chip_dims)
        params.px_height = min(known_chip_dims) / min(obs_chip_dims)
    # If not, check to make sure custom dimensions provided are numeric
    else:
        try:
            # Set size scaling parameters
            params.px_width = float(color_chip_size[0]) / color_chip_width
            params.px_height = float(color_chip_size[1]) / color_chip_height
        # Fail if provided color_chip_size is not supported
        except ValueError:
            fatal_error(
                f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly"
            )
        # Fail if provided color_chip_size is integer rather than tuple
        except TypeError:
            fatal_error(
                f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly as a tuple e.g. color_chip_size=(10,10)."
            )
    # If size scaling successful, set units to millimeters
    params.unit = "mm"


def mask_color_card(rgb_img, card_type="macbeth", **kwargs):
    """Automatically detect a color card and create bounding box mask of the chips detected.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    card_type : str, optional
        "macbeth", or "astro" (default = macbeth)
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
    if card_type.upper() == "ASTRO":
        *_, bounding_mask = _astrobotany_card_detection(rgb_img, **kwargs)
    else:
        *_, bounding_mask = _macbeth_card_detection(rgb_img, **kwargs)

    if params.debug is not None:
        # Find contours
        cnt, cnt_str = _cv2_findcontours(bin_img=bounding_mask)

        # Consolidate contours
        obj = _object_composition(contours=cnt, hierarchy=cnt_str)
        bb_debug = cv2.drawContours(np.copy(rgb_img), [obj], -1, (255, 0, 255), params.line_thickness)

        # Debug image handling
        _debug(visual=bb_debug, filename=os.path.join(params.debug_outdir, f"{params.device}_color_card.png"))

    return bounding_mask


def detect_color_card(rgb_img, color_chip_size=None, roi=None, **kwargs):
    """Automatically detects a Macbeth ColorChecker or Astrobotany.com Calibration Sticker style color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini, ""cameratrax", or "astro"; or tuple formatted (width, height)
        in millimeters (default = None)
    roi : plantcv.plantcv.Objects, optional
        A rectangular ROI as returned from pcv.roi.rectangle to detect a color card only in that region.
    **kwargs
        Other keyword arguments passed to cv2.adaptiveThreshold and cv2.circle.

        Valid keyword arguments:
        adaptive_method: 0 (mean) or 1 (Gaussian) (default = 1)
        block_size: int (default = 51)
        radius: int (default = 20)
        min_size: int (default = 1000)
        aspect_ratio: float (default = 1.27)
        solidity: float (default = 0.8)

    Returns
    -------
    numpy.ndarray
        Labeled mask of chips.
    """
    if type(color_chip_size) is str and color_chip_size.upper() == 'ASTRO':
        # Search image for astrobotany.com color card aruco tags labeled_mask, debug_img, card_img, marea, mheight, mwidth, bounding_mask
        color_matrix, debug_img, marea, mheight, mwidth, _ = _rect_filter(rgb_img,
                                                                          roi,
                                                                          function=_astrobotany_card_detection,
                                                                          **kwargs)
        # Create dataframe for easy summary stats
        chip_size = np.median(marea)
        chip_height = np.median(mheight)
        chip_width = np.median(mwidth)

        # Save out size of aruco tags in pixels (measured) and mm (known value)
        outputs.add_metadata(term="mean_aruco_tag_area_px", datatype=float, value=chip_size)
        outputs.add_metadata(term="mean_aruco_tag_width_px", datatype=float, value=chip_width)
        outputs.add_metadata(term="mean_aruco_tag_height_px", datatype=float, value=chip_height)

        # Set size scaling factor if color chip size is provided
        _set_size_scale_from_chip(color_chip_height=chip_height, color_chip_width=chip_width,
                                  color_chip_size=(7.975, 7.975))

        # Save or plot debug image of color card transformed to standard size
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_aligned_color_card.png'))

    else:
        # apply _color_card_detection within bounding box
        color_matrix, debug_img, marea, mheight, mwidth, _ = _rect_filter(rgb_img,
                                                                          roi,
                                                                          function=_macbeth_card_detection,
                                                                          **kwargs)
        # Create dataframe for easy summary stats
        chip_size = np.median(marea)
        chip_height = np.median(mheight)
        chip_width = np.median(mwidth)

        # Save out chip size for pixel to mm standardization
        outputs.add_metadata(term="median_color_chip_size", datatype=float, value=chip_size)
        outputs.add_metadata(term="median_color_chip_width", datatype=float, value=chip_width)
        outputs.add_metadata(term="median_color_chip_height", datatype=float, value=chip_height)

        # Set size scaling factor if color chip size is provided
        if color_chip_size:
            _set_size_scale_from_chip(color_chip_height=chip_height, color_chip_width=chip_width,
                                      color_chip_size=color_chip_size)

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f"{params.device}_color_card.png"))

    return color_matrix
