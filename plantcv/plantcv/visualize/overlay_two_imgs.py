# Overlay two input images

"""
Created on Tue. September 01 21:00:01 2020
A function
@author: hudanyunsheng
"""

import os
import cv2
import numpy as np
import copy
from plantcv.plantcv import fatal_error
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import params
from plantcv.plantcv.transform import resize
import warnings


# def _resize_img(img, new_size):
#     """Resize the image to the given new size
#     :param img: RGB or grayscale image data (numpy.ndarray)
#     :param new_size: New dimensions of the output image (tuple)
#     :return output_img: resized output image (numpy.ndarray)
#     Note:
#     If the given size is larger than the original image size, zero-pad the image.
#     If the given size is smaller than the original image size, crop the image (right & bottom).
#     """
#
#     # original image size
#     r_ori, c_ori = img.shape[0], img.shape[1]
#     r, c = new_size[0], new_size[1]
#
#     # check whether the input image is RGB or binary
#     if len(img.shape) > 2:
#         b_ori = np.shape(img)[2]
#         junk = copy.deepcopy(img)
#     else:
#         b_ori = 1
#         junk = np.expand_dims(img, axis=2)
#
#     # deal with rows
#     img1 = copy.deepcopy(junk)
#     if r < r_ori:
#         img1 = junk[0:r, :, :]
#     elif r > r_ori:
#         img1 = np.zeros_like(junk, shape=[r, c_ori, b_ori])
#         img1[0:r_ori, :, :] = junk
#
#     # update
#     r_ori, c_ori = img1.shape[0], img1.shape[1]
#     img2 = copy.deepcopy(img1)
#
#     # deal with columns
#     if c < c_ori:
#         img2 = img1[:, 0:c, :]
#     elif c > c_ori:
#         img2 = np.zeros_like(img1, shape=[r_ori, c, b_ori])
#         img2[:, 0:c_ori, :] = img1
#
#     if b_ori == 1:
#         output_img = np.squeeze(img2, axis=2)
#     else:
#         output_img = img2
#     return output_img

def overlay_two_imgs(img1, img2, alpha=0.5, size_img=None):
    """    A function used to overlay two images with a given alpha value (alpha indicated how opaque the 1st image is)
    Input grayscale images would be converted to RGB first
    :param img1 : (numpy.ndarray) ndarray, can be either 3-dimensional (RGB image) or 2-dimensional (graysacle)
    :param img2: (numpy.ndarray) ndarray, can be either 3-dimensional (RGB image) or 2-dimensional (graysacle)
    :param alpha: (float) desired opacity of 1st image, range: (0,1), default value=0.5
    :param size_img: (tuple) desired size of the image, (width, height), default value=None (if there is no desired size, the
                  output image size would be equal to the larger size of the two)
    :return: out_img: (numpy.ndarray) blended output image
    """

    if alpha > 1 or alpha < 0:
        fatal_error("The value of alpha should be in the range of (0,1)!")

    ## check the dimensions of both images
    if len(img1.shape) == 3:
        img1_ = copy.deepcopy(img1)
    elif len(img1.shape) == 2:
        img1_ = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    if len(img2.shape) == 3:
        img2_ = copy.deepcopy(img2)
    elif len(img2.shape) == 2:
        img2_ = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    ## sizing
    sz_img1 = img1_.shape[0:2]
    sz_img2 = img2_.shape[0:2]

    # if the desired size is not given, use the larger one
    if size_img is None:
        size_img = np.max([sz_img1[0], sz_img2[0]]), np.max([sz_img1[1], sz_img2[1]])

    # initialize the output image
    out_img = np.zeros(size_img + (3,), dtype='uint8')

    # check if sizes are the same
    if sz_img1 != size_img:
        img1_ = resize(img1_, size_img, interpolation=False)
        warnings.warn(
            "Image1 has a size of {}x{}, which is different from the desired size of {}x{}, an image resizing (cropping or zero-padding) will be done before overlay them!".format(
                sz_img1[0], sz_img1[1], size_img[0], size_img[1]))
    if sz_img2 != size_img:
        img2_ = resize(img2_, size_img, interpolation=False)
        warnings.warn(
            "Image1 has a size of {}x{}, which is different from the desired size of {}x{}, an image resizing (cropping or zero-padding) will be done before overlay them!".format(
                sz_img2[0], sz_img2[1], size_img[0], size_img[1]))

    # blending
    out_img[:, :, :] = (alpha * img1_[:, :, :]) + ((1 - alpha) * img2_[:, :, :])

    params.device += 1
    if params.debug == 'print':
        print_image(out_img, os.path.join(params.debug_outdir, str(params.device) + '_overlay.png'))
    elif params.debug == 'plot':
        plot_image(out_img)
    return out_img
