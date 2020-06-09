# Find NIR image

import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import params


def output_mask(img, mask, filename, outdir=None, mask_only=False):
    """Prints ori image and mask to directories.

    Inputs:
    img = original image, read in with plantcv function read_image
    mask  = binary mask image (single chanel)
    filename = vis image file name (output of plantcv read_image function)
    outdir = output directory
    mask_only = bool for printing only mask

    Returns:
    imgpath = path to image
    maskpath path to mask

    :param img: numpy.ndarray
    :param mask: numpy.ndarray
    :param filename: str
    :param outdir: str
    :param mask_only: bool
    :return imgpath: str
    :return maskpath: str
    """

    params.device += 1
    analysis_images = []

    if outdir is None:
        directory = os.getcwd()
    else:
        directory = outdir

    if not mask_only:
        path = os.path.join(str(directory), "ori-images")

        if os.path.exists(path):
            imgpath = os.path.join(str(path), str(filename))
            print_image(img, imgpath)
            analysis_images.append(['IMAGE', 'ori-img', imgpath])

        else:
            os.mkdir(path)
            imgpath = os.path.join(str(path), str(filename))
            print_image(img, imgpath)
            analysis_images.append(['IMAGE', 'ori-img', imgpath])

        path1 = os.path.join(str(directory), "mask-images")

        if os. path.exists(path1):
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])
        else:
            os.mkdir(path1)
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])

        if params.debug == 'print':
            print_image(img, os.path.join(params.debug_outdir, str(params.device) + '_ori-img.png'))
            print_image(mask, os.path.join(params.debug_outdir, str(params.device) + '_mask-img.png'))

        elif params.debug == 'plot':
            if len(np.shape(img)) == 3:
                plot_image(img)
                plot_image(mask, cmap='gray')
            else:
                plot_image(img, cmap='gray')
                plot_image(mask, cmap='gray')

        return imgpath, maskpath, analysis_images

    else:
        path1 = os.path.join(str(directory), "mask-images")

        if os.path.exists(path1):
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])
        else:
            os.mkdir(path1)
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])

        if params.debug == 'print':
            print_image(mask, os.path.join(params.debug_outdir, str(params.device) + '_mask-img.png'))
        elif params.debug == 'plot':
            plot_image(mask, cmap='gray')

        return maskpath, analysis_images
