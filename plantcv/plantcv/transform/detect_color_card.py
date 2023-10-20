"""Automatically detect color cards."""
import os
import cv2
import math
import numpy as np
import pandas as pd
from plantcv.plantcv import params, outputs, fatal_error
from plantcv.plantcv._debug import _debug


def _is_square(contour):
    """Determine if a contour is square or not

        Inputs:
    contour          = cv2 contour

        Outputs:
    bool             = True or False
    """
    return (cv2.contourArea(contour) > 1000 and
            max(cv2.minAreaRect(contour)[1]) / min(cv2.minAreaRect(contour)[1]) < 1.2 and
            (cv2.contourArea(contour) / np.prod(cv2.minAreaRect(contour)[1])) > 0.8)


def detect_color_card(rgb_img, label=None):
    """Automatically detect a color card.

    Algorithm written by mtwatso2-eng (github). Updated and implemented into PlantCV by Haley Schuhl.

        Inputs:
    rgb_img          = Input RGB image data containing a color card.
    label            = Optional label parameter, modifies the variable name of
                       observations recorded (default = pcv.params.sample_label).

    Returns:
    labeled_mask       = Labeled mask of chips

    :param rgb_img: numpy.ndarray
    :param label: str
    :return labeled_mask: numpy.ndarray
    """
    # Hard code since we don't currently support other color cards
    nrows = 6
    ncols = 4

    # Convert to grayscale, threshold, and findContours
    imgray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 127, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size and shape
    filtered_contours = [contour for contour in contours if _is_square(contour)]
    target_square_area = np.median([cv2.contourArea(cnt) for cnt in filtered_contours])
    filtered_contours = [contour for contour in filtered_contours if
                         (0.8 < (cv2.contourArea(contour) / target_square_area) < 1.2)]

    # Throw a fatal error if no color card found
    if len(filtered_contours) == 0:
        fatal_error('No color card found')

    # Initialize chip shape lists
    mindex, marea, mwidth, mheight = [], [], [], []
    # Loop over our contours and size data about them
    for index, c in enumerate(filtered_contours):
        marea.append(cv2.contourArea(filtered_contours[index]))
        _, wh, _ = cv2.minAreaRect(c)  # Rotated rectangle
        mwidth.append(wh[0])
        mheight.append(wh[1])
        mindex.append(index)
    # Create dataframe for easy summary stats
    df = pd.DataFrame({'index': mindex, 'width': mwidth, 'height': mheight, 'area': marea})
    chip_size = df.loc[:, "area"].median()
    chip_height = df.loc[:, "height"].median()
    chip_width = df.loc[:, "width"].median()

    rect = np.concatenate([[np.array(cv2.minAreaRect(i)[0]).astype(int)] for i in filtered_contours])
    rect = cv2.minAreaRect(rect)
    corners = np.array(np.intp(cv2.boxPoints(rect)))
    # Determine which corner most likely contains the white chip
    white_index = np.argmin([np.mean(math.dist(rgb_img[corner[1], corner[0], :], (255, 255, 255))) for corner in corners])
    corners = corners[np.argsort([math.dist(corner, corners[white_index]) for corner in corners])[[0, 1, 3, 2]]]
    # Increment amount is arbitrary, cell distances rescaled during perspective transform
    increment = 100
    centers = [[int(0 + i * increment), int(0 + j * increment)] for j in range(nrows) for i in range(ncols)]

    new_rect = cv2.minAreaRect(np.array(centers))
    box_points = cv2.boxPoints(new_rect).astype("float32")
    m_transform = cv2.getPerspectiveTransform(box_points, corners.astype("float32"))
    new_centers = cv2.transform(np.array([centers]), m_transform)[0][:, 0:2]
    this_sequence = np.array(list(range(nrows * ncols)))

    # Create blank img for drawing the labeled color card mask
    labeled_mask = np.zeros(imgray.shape)
    debug_img = np.copy(rgb_img)

    for i, pt in enumerate(new_centers):
        cv2.circle(labeled_mask, new_centers[i], 20, (int(this_sequence[i]) + 1) * 10, -1)
        cv2.circle(debug_img, new_centers[i], 20, (255, 255, 0), -1)
        cv2.putText(debug_img, text=str(i), org=pt, fontScale=params.text_size, color=(0, 0, 0),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, thickness=params.text_thickness)

    # Save out chip size for pixel to cm standardization
    outputs.add_observation(sample=label, variable='median_color_chip_size', trait='size of color card chips identified',
                            method='plantcv.plantcv.transform.detect_color_card', scale='square pixels',
                            datatype=float, value=chip_size, label="median")
    outputs.add_observation(sample=label, variable='median_color_chip_width', trait='width of color card chips identified',
                            method='plantcv.plantcv.transform.detect_color_card', scale='pixels',
                            datatype=float, value=chip_width, label="width")
    outputs.add_observation(sample=label, variable='median_color_chip_height', trait='height of color card chips identified',
                            method='plantcv.plantcv.transform.detect_color_card', scale='pixels',
                            datatype=float, value=chip_height, label="height")

    # Debugging
    _debug(visual=debug_img, filename=os.path.join(params.debug_outdir, str(params.device) + '_color_card.png'))

    return labeled_mask
