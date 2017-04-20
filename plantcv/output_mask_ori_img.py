# Find NIR image

import os
import numpy as np
from . import print_image
from . import plot_image


def output_mask(device, img, mask, filename, outdir=None, mask_only=False, debug=None):
    """Prints ori image and mask to directories.

    Inputs:
    device   = pipeline step counter
    img = original image, read in with plantcv function read_image
    mask  = binary mask image (single chanel)
    filename = vis image file name (output of plantcv read_image function)
    outdir = output directory
    debug    = None, print, or plot. Print = save to file, Plot = print to screen.

    Returns:
    device   = device number
    imgpath = path to image
    maskpath path to mask

    :param img: array
    :param mask: array
    :param filename: str
    :param outdir: str
    :param device: int
    :param debug: str
    :return device: int
    :return imgpath: str
    :return maskpath: str

    """

    device += 1
    analysis_images = []

    if outdir == None:
        directory = os.getcwd()
    else:
        directory = outdir

    if mask_only == False:
        path = os.path.join(str(directory), "ori-images")

        if os.path.exists(path) == True:
            imgpath = os.path.join(str(path), str(filename))
            print_image(img, imgpath)
            analysis_images.append(['IMAGE', 'ori-img', imgpath])

        else:
            os.mkdir(path)
            imgpath = os.path.join(str(path), str(filename))
            print_image(img, imgpath)
            analysis_images.append(['IMAGE', 'ori-img', imgpath])

        path1 = os.path.join(str(directory), "mask-images")

        if os. path.exists(path1) == True:
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])
        else:
            os.mkdir(path1)
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])

        if debug == 'print':
            print_image(img, (str(device) + '_ori-img.png'))
            print_image(mask, (str(device) + '_mask-img.png'))

        elif debug == 'plot':
            if len(np.shape(img)) == 3:
                plot_image(img)
                plot_image(mask, cmap='gray')
            else:
                plot_image(img, cmap='gray')
                plot_image(mask, cmap='gray')

        return device, imgpath, maskpath, analysis_images

    else:
        path1 = os.path.join(str(directory), "mask-images")

        if os.path.exists(path1) == True:
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])
        else:
            os.mkdir(path1)
            maskpath = os.path.join(str(path1), str(filename))
            print_image(mask, maskpath)
            analysis_images.append(['IMAGE', 'mask', maskpath])

        if debug == 'print':
            print_image(mask, (str(device) + '_mask-img.png'))
        elif debug == 'plot':
                plot_image(mask, cmap='gray')

        return device, maskpath, analysis_images
