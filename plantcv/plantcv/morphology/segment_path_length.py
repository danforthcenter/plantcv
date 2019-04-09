# Find geodesic lenghts of skeleton segments

import os
import cv2
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image


def segment_path_length(segmented_img, objects):
    """ Segment a skeleton image into pieces and gather measurements per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours

        Returns:
        labeled_img   = Segmented debugging image with lengths labeled
        leaf_lengths  = List of leaf lengths

        :param segmented_img: numpy.ndarray
        :param objects: list
        :return labeled_img: numpy.ndarray
        :return segment_lengths: list

        """

    label_coord_x = []
    label_coord_y = []
    segment_lengths = []
    labeled_img = segmented_img.copy()

    for i, cnt in enumerate(objects):
        # Calculate geodesic distance, divide by two since cv2 seems to be taking the perimeter of the contour
        segment_lengths.append(cv2.arcLength(objects[i], False)/2)
        # Store coordinates for labels
        label_coord_x.append(objects[i][0][0][0])
        label_coord_y.append(objects[i][0][0][1])

    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = "id:{} length:{:.1f}".format(c, value)
        w = label_coord_x[c]
        h = label_coord_y[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.4,
                    color=(150, 150, 150), thickness=1)

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_path_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return labeled_img, segment_lengths
