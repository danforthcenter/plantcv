"""Automatically detect color cards.

Algorithm written by mtwatso2-eng (github). Updated and implemented into PlantCV by Haley Schuhl.
"""
import os
import cv2
import math
import numpy as np
from plantcv.plantcv import params, outputs, fatal_error, deprecation_warning
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._helpers import _rgb2gray, _cv2_findcontours, _object_composition, _rect_filter, _rect_replace


def _is_square(contour, min_size, aspect_ratio=1.27, solidity=.8):
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

    return (cv2.contourArea(contour) > min_size and
            # Test that the Aspect Ratio (default 1.27)
            # ratio between the width and height of minAreaRect
            # which is like a bounding box but will consider rotation
            max(cv2.minAreaRect(contour)[1]) / min(cv2.minAreaRect(contour)[1]) < aspect_ratio and
            # Test that the Solidity (default 0.8)
            # Compare minAreaRect area to the actual contour area, a chip should be mostly solid
            (cv2.contourArea(contour) / np.prod(cv2.minAreaRect(contour)[1])) > solidity)


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


def _draw_color_chips(rgb_img, new_centers, radius):
    """Create labeled mask and debug image of color chips.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    new_centers : numpy.array
        Chip centers after transformation.
    radius : int
        Radius of circles to draw on the color chips.

    Returns
    -------
    list
        Labeled mask and debug image.
    """
    # Create blank img for drawing the labeled color card mask
    labeled_mask = np.zeros(rgb_img.shape[0:2])
    debug_img = np.copy(rgb_img)

    # Loop over the new chip centers and draw them on the RGB image and labeled mask
    for i, pt in enumerate(new_centers):
        cv2.circle(labeled_mask, new_centers[i], radius, (i + 1) * 10, -1)
        cv2.circle(debug_img, new_centers[i], radius, (255, 255, 0), -1)
        cv2.putText(debug_img, text=str(i), org=pt, fontScale=params.text_size, color=(0, 0, 0),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)
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
        _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))
        fatal_error("Centers do not map 1 to 1 with detected color chips")


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
            fatal_error('Color card corners could not be detected accurately')


def _color_card_detection(rgb_img, **kwargs):
    """Algorithm to automatically detect a color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
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
        Labeled mask of chips, debug img, detected chip areas, chip heights, chip widths, bounding box mask
    """
    # Get keyword arguments and set defaults if not set
    min_size = kwargs.get("min_size", 1000)  # Minimum size for _is_square chip filtering
    radius = kwargs.get("radius", 20)  # Radius of circles to draw on the color chips
    adaptive_method = kwargs.get("adaptive_method", 1)  # cv2.adaptiveThreshold method
    block_size = kwargs.get("block_size", 51)  # cv2.adaptiveThreshold block size
    aspect_ratio = kwargs.get("aspect_ratio", 1.27)  # _is_square aspect-ratio filtering
    solidity = kwargs.get("solidity", 0.8)  # _is_square solidity filtering

    # Throw a fatal error if block_size is not odd or greater than 1
    if not (block_size % 2 == 1 and block_size > 1):
        fatal_error('block_size parameter must be an odd int greater than 1.')

    # Hard code since we don't currently support other color cards
    nrows = 6
    ncols = 4

    # Convert to grayscale, threshold, and findContours
    imgray = _rgb2gray(rgb_img=rgb_img)
    gaussian = cv2.GaussianBlur(imgray, (11, 11), 0)
    thresh = cv2.adaptiveThreshold(gaussian, 255, adaptive_method,
                                   cv2.THRESH_BINARY_INV, block_size, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours, keep only square-shaped ones
    filtered_contours = [contour for contour in contours if _is_square(contour, min_size, aspect_ratio, solidity)]
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
    boundind_mask = cv2.rectangle(np.zeros(rgb_img.shape[0:2]), (x, y), (x + w, y + h), (255), -1).astype(np.uint8)

    # Initialize chip shape lists
    marea, mwidth, mheight = _get_contour_sizes(filtered_contours)

    # Concatenate all contours into one array and find the minimum area rectangle
    rect = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
    rect = cv2.minAreaRect(rect)
    # Get the corners of the rectangle
    corners = np.array(np.intp(cv2.boxPoints(rect)))
    # Check that corners are in image
    _check_corners(imgray, corners)
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
    # Check that new centers are inside each unique filtered_contour
    _check_point_per_chip(filtered_contours, new_centers, debug_img)

    return labeled_mask, debug_img, marea, mheight, mwidth, boundind_mask


def _set_size_scale_from_chip(color_chip_width, color_chip_height, color_chip_size):
    """Set the size scaling factors in Params from the known size of a given color card target.

    Parameters
    ----------
    color_chip_width : float
        Width in pixels of the detected color chips
    color_chip_height : float
        Height in pixels of the detected color chips
    color_chip_size : str, tuple
        Type of supported color card target ("classic", "passport", "nano", "mini", or "cameratrax"),
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
        known_chip_dims = [card_types[color_chip_size.upper()]["chip_width"],
                           card_types[color_chip_size.upper()]["chip_height"]]
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
            fatal_error(f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly")
        # Fail if provided color_chip_size is integer rather than tuple
        except TypeError:
            fatal_error(f"Invalid input '{color_chip_size}'. Choose from {list(card_types.keys())}\
            or provide your color card chip dimensions explicitly as a tuple e.g. color_chip_size=(10,10).")
    # If size scaling successful, set units to millimeters
    params.unit = "mm"


def mask_color_card(rgb_img, **kwargs):
    """Automatically detect a color card and create bounding box mask of the chips detected.

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

    numpy.ndarray
        Binary bounding box mask of the detected color card chips
    """
    _, _, _, _, _, bounding_mask = _color_card_detection(rgb_img, **kwargs)

    if params.debug is not None:
        # Find contours
        cnt, cnt_str = _cv2_findcontours(bin_img=bounding_mask)

        # Consolidate contours
        obj = _object_composition(contours=cnt, hierarchy=cnt_str)
        bb_debug = cv2.drawContours(np.copy(rgb_img), [obj], -1, (255, 0, 255), params.line_thickness)

        # Debug image handling
        _debug(visual=bb_debug, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return bounding_mask


def detect_color_card(rgb_img, label=None, color_chip_size=None, roi=None, **kwargs):
    """Automatically detect a Macbeth ColorChecker style color card.

    Parameters
    ----------
    rgb_img : numpy.ndarray
        Input RGB image data containing a color card.
    label : str, optional
        modifies the variable name of observations recorded (default = pcv.params.sample_label).
    color_chip_size: str, tuple, optional
        "passport", "classic", "nano", "mini", or "cameratrax"; or tuple formatted (width, height)
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
    # Set lable to params.sample_label if None
    if label is None:
        label = params.sample_label
    deprecation_warning(
        "The 'label' parameter is no longer utilized, since color chip size is now metadata. "
        "It will be removed in PlantCV v5.0."
        )
    # apply _color_card_detection within bounding box
    sub_mask, debug_img, marea, mheight, mwidth, _ = _rect_filter(rgb_img,
                                                                  roi,
                                                                  function=_color_card_detection,
                                                                  **kwargs)
    # slice sub_mask from bounding box into mask of original image size
    empty_mask = np.zeros((np.shape(rgb_img)[0], np.shape(rgb_img)[1]))
    labeled_mask = _rect_replace(empty_mask, sub_mask, roi)

    # Create dataframe for easy summary stats
    chip_size = np.median(marea)
    chip_height = np.median(mheight)
    chip_width = np.median(mwidth)

    # Save out chip size for pixel to mm standardization
    outputs.add_metadata(term="median_color_chip_size", datatype=float, value=chip_size)
    outputs.add_metadata(term="median_color_chip_width", datatype=float, value=chip_width)
    outputs.add_metadata(term="median_color_chip_height", datatype=float, value=chip_height)

    # Set size scaling factor if card type is provided
    if color_chip_size:
        _set_size_scale_from_chip(color_chip_height=chip_height, color_chip_width=chip_width, color_chip_size=color_chip_size)

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, f'{params.device}_color_card.png'))

    return labeled_mask
