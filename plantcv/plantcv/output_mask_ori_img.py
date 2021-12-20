# Find NIR image

import os
from plantcv.plantcv import print_image
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


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
    analysis_images = []

    directory = outdir
    if outdir is None:
        directory = os.getcwd()

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

        _debug(visual=img, filename=os.path.join(params.debug_outdir, f"{params.device}_ori-img.png"))
        _debug(visual=mask, filename=os.path.join(params.debug_outdir, f"{params.device}_mask-img.png"))

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

        _debug(visual=mask, filename=os.path.join(params.debug_outdir, f"{params.device}_mask-img.png"))

        return maskpath, analysis_images
