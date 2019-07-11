# cluster objects and split into masks

import os
import numpy as np
import cv2
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params
from plantcv.plantcv import apply_mask


def cluster_contour_mask(rgb_img, clusters_i, contours, hierarchies):
    """Outputs masks for the grouped clusters. Since there can be a variable number of
    clusters/masks the output is a list of arrays.

    Inputs:
    rgb_img       = RGB image data
    clusters_i    = clusters, output from cluster_contours function
    contours      = contours, contours from cluster_contours function
    hierarchies   = hierarchies, hierarchies from cluster_contours function

    Returns:
    output_masks  = resulting masks
    masked_images  = masked_images

    :param rgb_img: numpy.ndarray
    :param clusters_i: numpy array
    :param contours: numpy array
    :param hierarchies: numpy array
    :return output_masks: list of resulting masks
    :return masked_images: list of masked images
    """

    # WORK IN PROGRESS
    # CURRENTLY DISCUSSING THE POSSIBILITY OF A LARGE RESTRUCTURING WHERE WE HIDE CONTOURS AND HIERARCHIES FROM
    # USERS AND USE MASKS AND find_objects() INSIDE FUNCTIONS TO SIMPLIFY INPUTS AND OUTPUTS

    # params.device += 1
    #
    # output_masks = []
    # masked_images = []
    #
    # for y, x in enumerate(clusters_i):
    #     iy, ix, iz = np.shape(rgb_img)
    #     mask = np.zeros((iy, ix, 3), dtype=np.uint8)
    #     masked_img = np.copy(rgb_img)
    #     for a in x:
    #         if hierarchies[0][a][3] > -1:
    #             cv2.drawContours(mask, contours, a, (0, 0, 0), -1, lineType=8, hierarchy=hierarchies)
    #         else:
    #             cv2.drawContours(mask, contours, a, (255, 255, 255), -1, lineType=8, hierarchy=hierarchies)
    #
    #     mask_binary = mask[:, :, 0]
    #     output_masks.append(mask_binary)
    #
    #     if np.sum(mask_binary) == 0:
    #         pass
    #     else:
    #         retval, mask_binary = cv2.threshold(mask_binary, 254, 255, cv2.THRESH_BINARY)
    #         masked1 = apply_mask(masked_img, mask_binary, 'white')
    #         masked_images.append(masked1)
    #
    #         if params.debug == 'print':
    #             print_image(masked1,
    #                         os.path.join(params.debug_outdir, str(params.device) + '_clusters_' + str(y) + ".png"))
    #             print_image(mask_binary,
    #                         os.path.join(params.debug_outdir, str(params.device) + '_clusters_mask_' + str(y) + ".png"))
    #         elif params.debug == 'plot':
    #             plot_image(masked1)
    #             plot_image(mask_binary, cmap='gray')
    #
    # return output_masks, masked_images
