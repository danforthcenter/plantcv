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

    directory = os.getcwd() if outdir is None else outdir

    # Return values
    results = []

    # Save the original image unless mask_only=True
    if not mask_only:
        path = os.path.join(str(directory), "ori-images")
        os.makedirs(path, exist_ok=True)
        imgpath = os.path.join(str(path), str(filename))
        print_image(img, imgpath)
        analysis_images.append(['IMAGE', 'ori-img', imgpath])
        results.append(imgpath)
        # Print/plot original image
        _debug(visual=img, filename=os.path.join(params.debug_outdir, f"{params.device}_ori-img.png"))

    # Save the mask
    path = os.path.join(str(directory), "mask-images")
    os.makedirs(path, exist_ok=True)
    maskpath = os.path.join(str(path), str(filename))
    print_image(mask, maskpath)
    analysis_images.append(['IMAGE', 'mask', maskpath])
    results.append(maskpath)
    # Print/plot mask
    _debug(visual=mask, filename=os.path.join(params.debug_outdir, f"{params.device}_mask-img.png"))

    results.append(analysis_images)

    return results
