# Fuse two images

import os
import numpy as np
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv import params
from plantcv.plantcv.hyperspectral.read_data import _make_pseudo_rgb
from plantcv.plantcv._debug import _debug


def image_fusion(img1, img2, wvs1, wvs2, array_type=None, filename=None):
    """ Fuse two images of the same size together with given wavelengths representing and make a Spectral_data instance
    img1: 1st image to be fused
    img2: 2nd image to be fused
    wvs1: list of wavelengths represent bands in img1
    wvs2: list of wavelengths represent bands in img2
    array_type: (optional) description of the fused array
    filename: (optional) desired filename of the fused array

    :param img1: numpy.ndarray
    :param img2: numpy.ndarray
    :param wvs1: list
    :param wvs2: list
    :param array_type: str
    :param filename: str
    :return: fused_array (a Spectral_data instance)
    """

    if len(img1.shape) == 2:
        img1 = np.expand_dims(img1, axis=2)
    r1, c1, b1 = img1.shape

    if len(img2.shape) == 2:
        img2 = np.expand_dims(img2, axis=2)
    r2, c2, b2 = img2.shape
    if (r1, c1) != (r2, c2):
        fatal_error("Input images should have the same image size")

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
    array_data = (array_data / 255).astype(np.float32)

    max_pixel = float(np.amax(array_data))
    min_pixel = float(np.amin(array_data))

    d_type = array_data.dtype

    r, c, b = array_data.shape

    fused_array = Spectral_data(array_data=array_data,
                                   max_wavelength=float(max(wavelengths)),
                                   min_wavelength=float(min(wavelengths)),
                                   max_value=max_pixel, min_value=min_pixel,
                                   d_type=d_type,
                                   wavelength_dict=wavelength_dict, samples=int(r * c),
                                   lines=int(b), interleave="bil",
                                   wavelength_units="nm", array_type=array_type,
                                   pseudo_rgb=None, filename=filename, default_bands=None)

    # Make pseudo-rgb image and replace it inside the class instance object
    pseudo_rgb = _make_pseudo_rgb(fused_array)
    fused_array.pseudo_rgb = pseudo_rgb

    _debug(visual=pseudo_rgb, filename=os.path.join(params.debug_outdir, str(params.device) + "_fused_pseudo_rgb.png"))

    return fused_array
