# merging images with a known overlap

import cv2
import os
import numpy as np
import random
from plantcv import plantcv as pcv
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug

def merge_images(img_path, overlap_percentage, direction = "vertical", method = "stacked"):
    """
    Merge together images in a series that overlap by a specified amount.
    Inputs:
    img_path = directory of images for merging
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
    :param img_path: path to directory where images to merge are stored
    :param overlap_percentage: non-negative real number 
    :param direction: str
    :param method: str
    :return combined_image: numpy.ndarray
    """
    image_files = os.listdir(img_path)
    image_files.sort()
    
    # Read the images to get total height/width
    overlap_dims = [0,0]
    for i in image_files:
        height, width, _ = cv2.imread(img_path+i).shape
        overlap_dims[0] += height
        overlap_dims[1] += width
    height, width, _ = cv2.imread(img_path+image_files[0]).shape
   
    # Calculate the overlap in pixels
    #Create a new image with adjusted dimensions accounting for overlap
    if direction == "vertical":
        overlap_pixels_height = int(height * overlap_percentage / 100)
        combined_height = overlap_dims[0] - (overlap_pixels_height*(len(image_files)-1))
        combined_image = np.zeros((combined_height, width, 3), dtype=np.uint8)
    elif direction == "horizontal":
        overlap_pixels_width = int(width * overlap_percentage / 100)
        combined_width = overlap_dims[1] - (overlap_pixels_width*(len(image_files)-1))
        combined_image = np.zeros((height, combined_width, 3), dtype=np.uint8)
    
    if method == "stacked":
        current_position = 0
        for image_file in image_files:
            image = cv2.imread(img_path+image_file)
            if image_file != image_files[-1]:
                if direction == "vertical":
                    combined_image[current_position:current_position + height, :, :] = image
                    current_position += height - overlap_pixels_height
                else:
                    combined_image[:, current_position:current_position + width, :] = image
                    current_position += width - overlap_pixels_width
            elif direction == "vertical":
                combined_image[current_position:, :, :] = image
            else:
                combined_image[:, current_position:, :] = image
    
    elif method in ["average", "gradual", "random"]:
        for i, image_file in enumerate(image_files):
            image = cv2.imread(img_path+image_file)
            if i == 0 and direction == "vertical":  # First image
                combined_image[:height, :] = image
            elif i == 0 and direction == "horizontal":
                combined_image[:, :width] = image
            else:
                if direction == "vertical":
                    start_x = i * (height - overlap_pixels_height)
                    overlap_pixels = overlap_pixels_height
                elif direction == "horizontal":
                    start_x = i * (width - overlap_pixels_width)
                    overlap_pixels = overlap_pixels_width
                if method == "random":
                    top = random.choice([0,1])
                # Blend the overlap by averaging the pixel values
                for x in range(overlap_pixels):
                    if method == "average":
                        beta = 0.5
                    elif method == "gradual":
                        beta = x / overlap_pixels
                    else:
                        beta = top
                    alpha = 1 - beta
                    merged_x = start_x + x
                    if direction == "vertical":
                        combined_image[merged_x, :] = cv2.addWeighted(combined_image[merged_x, :], alpha,
                                                                    image[x, :], beta, 0)
                    else:
                        combined_image[:, merged_x] = cv2.addWeighted(combined_image[:, merged_x], alpha,
                                                                    image[:, x], beta, 0)
                # Copy the non-overlapping part
                non_overlap_start = start_x + overlap_pixels
                if direction == "vertical":
                    non_overlap_end = non_overlap_start + height - overlap_pixels
                    combined_image[non_overlap_start:non_overlap_end, :] = image[overlap_pixels:, :]
                else:
                    non_overlap_end = non_overlap_start + width - overlap_pixels
                    combined_image[:, non_overlap_start:non_overlap_end] = image[:, overlap_pixels:]
                    
    _debug(visual=combined_image, filename=os.path.join(params.debug_outdir, "_merged_image.png"))
    return(combined_image)
