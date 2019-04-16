# Find geodesic lengths of skeleton segments

import os
import cv2
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image


def segment_path_length(segmented_img, objects):
    """ Use segments to calculate geodesic distance per segment

        Inputs:
        segmented_img = Segmented image to plot lengths on
        objects       = List of contours

        Returns:
        path_length_header = Path length data header
        path_length_data   = Path length data values
        labeled_img        = Segmented debugging image with lengths labeled

        :param segmented_img: numpy.ndarray
        :param objects: list
        :return labeled_img: numpy.ndarray
        :return path_length_header: list
        :return path_length_data: list

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

    path_length_header = ['HEADER_PATH_LENGTH']
    path_length_data = ['PATH_LENGTH_DATA']

    # Put labels of length
    for c, value in enumerate(segment_lengths):
        text = "{:.2f}".format(c, value)
        w = label_coord_x[c]
        h = label_coord_y[c]
        cv2.putText(img=labeled_img, text=text, org=(w, h), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.4,
                    color=(150, 150, 150), thickness=1)
        segment_label = "ID" + str(c)
        path_length_header.append(segment_label)
        path_length_data.append(segment_lengths[c])

    if 'morphology_data' not in outputs.measurements:
        outputs.measurements['morphology_data'] = {}
    outputs.measurements['morphology_data']['segment_path_lengths'] = segment_lengths

    # Auto-increment device
    params.device += 1

    if params.debug == 'print':
        print_image(labeled_img, os.path.join(params.debug_outdir, str(params.device) + '_segment_path_lengths.png'))
    elif params.debug == 'plot':
        plot_image(labeled_img)

    return path_length_header, path_length_data, labeled_img
