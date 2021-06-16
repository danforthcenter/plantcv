# Fuse two images

import os
import numpy as np
from skimage import img_as_ubyte
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv import params
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb
from plantcv.plantcv._debug import _debug


def image_fusion(img1, img2, wvs1, wvs2, array_type="multispectral"):
    """Fuse two images of the same size together to create a multispectral image
    img1: 1st image to be fused
    img2: 2nd image to be fused
    wvs1: list of wavelengths represent bands in img1
    wvs2: list of wavelengths represent bands in img2
    array_type: (optional) description of the fused array

    :param img1: numpy.ndarray
    :param img2: numpy.ndarray
    :param wvs1: list
    :param wvs2: list
    :param array_type: str
    :return fused_array: plantcv.Spectral_data
    """

    # If the image is 2D, expand to 3D to make stackable
    img1 = _expand_img_dims(img1)
    r1, c1, _ = img1.shape

    # If the image is 2D, expand to 3D to make stackable
    img2 = _expand_img_dims(img2)
    r2, c2, _ = img2.shape

    # Fatal error if images are not the same spatial dimensions
    if (r1, c1) != (r2, c2):
        fatal_error("Input images should have the same image size")

    # If the images are not the same data type, convert to 8-bit unsigned integer
    if img1.dtype != img2.dtype:
        img1 = img_as_ubyte(img1)
        img2 = img_as_ubyte(img2)

    # Concatenate the images on the depth/spectral (z) axis
    array_data = np.concatenate((img1, img2), axis=2)

    # sort all wavelengths
    wavelengths = np.array(wvs1 + wvs2)
    ind = np.argsort(wavelengths)
    wavelengths = wavelengths[ind]

    wavelength_dict = dict()
    for (idx, wv) in enumerate(wavelengths):
        wavelength_dict[wv] = float(idx)

    # sort array_data based on wavelengths
    array_data = array_data[:, :, ind]
    # Scale the array data to 0-1 by dividing by the maximum data type value
    array_data = (array_data / np.iinfo(array_data.dtype).max).astype(np.float32)

    r, c, b = array_data.shape

    fused_array = Spectral_data(array_data=array_data,
                                max_wavelength=float(max(wavelengths)),
                                min_wavelength=float(min(wavelengths)),
                                max_value=float(np.amax(array_data)),
                                min_value=float(np.amin(array_data)),
                                d_type=array_data.dtype,
                                wavelength_dict=wavelength_dict,
                                samples=c, lines=r, interleave="NA",
                                wavelength_units="nm", array_type=array_type,
                                pseudo_rgb=None, filename="NA", default_bands=None)

    # Make pseudo-rgb image and replace it inside the class instance object
    pseudo_rgb = _make_pseudo_rgb(fused_array)
    fused_array.pseudo_rgb = pseudo_rgb

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_fused_pseudo_rgb.png"))

    return fused_array


def _expand_img_dims(img):
    """Expand 2D images to 3D

    Inputs:
    img - input image

    Returns:
    img - image with expanded dimensions

    :params img: numpy.ndarray
    :return img: numpy.ndarray
    """
    # If the image is 2D, expand to 3D to make stackable
    if len(img.shape) == 2:
        return np.expand_dims(img, axis=2)
    # Return copy of image to break the reference to the input image
    return img.copy()
