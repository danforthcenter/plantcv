# Find angles in degrees of skeleton segments

import os
import cv2
import numpy as np
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import color_palette


def segment_angle(segmented_img, objects, label="default"):
    """ Calculate angle of segments (in degrees) by fitting a linear regression line to segments.

        Inputs:
        segmented_img  = Segmented image to plot slope lines and angles on
        objects        = List of contours
        label          = optional label parameter, modifies the variable name of observations recorded

        Returns:
        labeled_img    = Segmented debugging image with angles labeled


        :param segmented_img: numpy.ndarray
        :param objects: list
        :param label: str
        :return labeled_img: numpy.ndarray
        """

    label_coord_x = []
    label_coord_y = []
    segment_angles = []

    labeled_img = segmented_img.copy()

    # Use a previously saved color scale if available
    rand_color = color_palette(num=len(objects), saved=True)

    for i, cnt in enumerate(objects):
        # Find bounds for regression lines to get drawn
        rect = cv2.minAreaRect(cnt)
        pts = cv2.boxPoints(rect)
        df = pd.DataFrame(pts, columns=('x', 'y'))
        x_max = int(df['x'].max())
        x_min = int(df['x'].min())

        # Find line fit to each segment
        [vx, vy, x, y] = cv2.fitLine(objects[i], cv2.DIST_L2, 0, 0.01, 0.01)
        slope = -vy / vx
        left_list = int(((x - x_min) * slope) + y)
        right_list = int(((x - x_max) * slope) + y)

        if slope > 1000000 or slope < -1000000:
            print("Slope of contour with ID#", i, "is", slope, "and cannot be plotted.")
        else:
            # Draw slope lines
            cv2.line(labeled_img, (x_max - 1, right_list), (x_min, left_list), rand_color[i], 1)

        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

        # Calculate degrees from slopes
        segment_angles.append(np.arctan(slope[0]) * 180 / np.pi)

    segment_ids = []
    for i, cnt in enumerate(objects):
        # Label slope lines
        w = label_coord_x[i]
        h = label_coord_y[i]
        text = "{:.2f}".format(segment_angles[i])
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        # segment_label = "ID" + str(i)
        segment_ids.append(i)

    outputs.add_observation(sample=label, variable='segment_angle', trait='segment angle',
                            method='plantcv.plantcv.morphology.segment_angle', scale='degrees', datatype=list,
                            value=segment_angles, label=segment_ids)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segmented_angles.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img
