# Find angles in degrees of skeleton segments

import os
import cv2
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import color_palette


def segment_angles(segmented_img, objects):
    """ Segment a skeleton image into pieces and gather measurements per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours

        Returns:
        labeled_img   = Segmented debugging image with angles labeled
        leaf_angles   = List of leaf lengths

        :param segmented_img: numpy.ndarray
        :param objects: list
        :return labeled_img: numpy.ndarray
        :return leaf_angles: list

        """
    label_coord_x = []
    label_coord_y = []
    degrees_angles = []
    rows, cols = segmented_img.shape[:2]

    labeled_img = segmented_img.copy()

    rand_color = color_palette(len(objects))

    for i, cnt in enumerate(objects):
        # Find line fit to each segment
        [vx, vy, x, y] = cv2.fitLine(objects[i], cv2.DIST_L2, 0, 0.01, 0.01)
        left_pt = int((-x * vy / vx) + y)
        right_pt = int(((cols - x) * vy / vx) + y)

        # Draw slope lines
        cv2.line(labeled_img, (cols - 1, right_pt), (0, left_pt), rand_color[i], 1)

        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

        # Calculate degrees from slopes
        slope = -vy / vx
        degrees_angles.append(np.arctan(slope[0]) * 180 / np.pi)

    for i, cnt in enumerate(objects):
        # Label slope lines
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = "{:.2f}".format(degrees_angles[i])
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=.4, color=(255, 255, 255), thickness=1)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, degrees_angles
