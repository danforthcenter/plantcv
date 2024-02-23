# merging images with a known overlap

import cv2
import os
import numpy as np
import random
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def merge_images(paths_to_imgs, overlap_percentage, direction="vertical", method="stacked"):
    """
    Merge together images in a series that overlap by a specified amount.
    Inputs:
    paths_to_imgs = List of paths to the images
    overlap_percentage = percent of each image that overlaps with adjacent images
    direction = Available options are vertical or horizontal and indicate
        how the images should be merged
        - 'horizontal' : merge images on the x-axis
        - 'vertical' : (default) merge images on the y-axis
    method = Available options are stacked, random, average, and gradual and dictate
        how the overlap region should be handled
        - 'stacked' : (default), image i+1 stacks on top of image i
        - 'random' : randomly choose either image i or i+1 to go on top
        - 'average' : pixels are averaged between image i values and image i+1 values
        - 'gradual' : pixels are averaged with a weight that corresponds to
                      proximity to image i or image i+1
    :param paths_to_imgs: list
    :param overlap_percentage: non-negative real number
    :param direction: str
    :param method: str
    :return combined_image: numpy.ndarray
    """
    paths_to_imgs.sort()

    # Read the images to get total height/width
    overlap_dims = [0, 0]
    for imgfile in paths_to_imgs:
        height, width, _ = cv2.imread(imgfile).shape
        overlap_dims[0] += height
        overlap_dims[1] += width
    height, width, _ = cv2.imread(paths_to_imgs[0]).shape

    # Calculate the overlap in pixels
    # Create a new image with adjusted dimensions accounting for overlap
    if direction == "vertical":
        overlap_pixels_height = int(height * overlap_percentage / 100)
        combined_height = overlap_dims[0] - (overlap_pixels_height*(len(paths_to_imgs)-1))
        blank_image = np.zeros((combined_height, width, 3), dtype=np.uint8)
        combined_image = _mergevert(paths_to_imgs, blank_image, height, overlap_pixels_height, method)

    elif direction == "horizontal":
        overlap_pixels_width = int(width * overlap_percentage / 100)
        combined_width = overlap_dims[1] - (overlap_pixels_width*(len(paths_to_imgs)-1))
        blank_image = np.zeros((height, combined_width, 3), dtype=np.uint8)
        combined_image = _mergehoriz(paths_to_imgs, blank_image, width, overlap_pixels_width, method)

    _debug(visual=combined_image, filename=os.path.join(params.debug_outdir, "_merged_image.png"))
    return combined_image


def _mergevert(image_files, combined_image, height, overlap_pixels, method="stacked"):
    """
    Private function to reduce if/else statements. Merges images vertically.
    Inputs: same as above with the addition of calculated overlap pixels and
            dimensions of combined image.
    """
    top = 0  # Setting a dummy variable in case method not random
    for i, image_file in enumerate(image_files):
        image = cv2.imread(image_file)
        if i == 0:  # First image
            combined_image[:height, :] = image
        else:
            start_x = i * (height - overlap_pixels)
            if method == "random":
                top = random.choice([0, 1])
            # Blend the overlap by averaging the pixel values
            for x in range(overlap_pixels):
                betalist = [["stacked", "average", "gradual", "random"], [1, 0.5, x/overlap_pixels, top]]
                beta = betalist[1][betalist[0].index(method)]
                alpha = 1 - beta
                merged_x = start_x + x
                combined_image[merged_x, :] = cv2.addWeighted(combined_image[merged_x, :], alpha,
                                                              image[x, :], beta, 0)
            # Copy the non-overlapping part
            non_overlap_start = start_x + overlap_pixels
            non_overlap_end = non_overlap_start + height - overlap_pixels
            combined_image[non_overlap_start:non_overlap_end, :] = image[overlap_pixels:, :]
    return combined_image


def _mergehoriz(image_files, combined_image, width, overlap_pixels, method="stacked"):
    """
    Private function to reduce if/else statements. Merges images horizontally.
    Inputs: same as above with the addition of calculated overlap pixels and
            dimensions of combined image.
    """
    top = 0  # Setting a dummy variable in case method not random
    for i, image_file in enumerate(image_files):
        image = cv2.imread(image_file)
        if i == 0:  # First image
            combined_image[:, :width] = image
        else:
            start_x = i * (width - overlap_pixels)
            if method == "random":
                top = random.choice([0, 1])
            # Blend the overlap by averaging the pixel values
            for x in range(overlap_pixels):
                betalist = [["stacked", "average", "gradual", "random"], [1, 0.5, x/overlap_pixels, top]]
                beta = betalist[1][betalist[0].index(method)]
                alpha = 1 - beta
                merged_x = start_x + x
                combined_image[:, merged_x] = cv2.addWeighted(combined_image[:, merged_x], alpha,
                                                              image[:, x], beta, 0)
            # Copy the non-overlapping part
            non_overlap_start = start_x + overlap_pixels
            non_overlap_end = non_overlap_start + width - overlap_pixels
            combined_image[:, non_overlap_start:non_overlap_end] = image[:, overlap_pixels:]
    return combined_image
