import os
import re
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv.classes import MS_data
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.transform.rescale import rescale
from plantcv.plantcv.hyperspectral.read_data import _find_closest


def _ms_make_pseudo_rgb(ms_array):
    """Create pseudo-rgb image rom a multispectral class image

    Parameters:
    -----------
        ms_array = MS_data instance

    Returns:
    --------
        numpy.ndarray     = Pseudo-rgb image
    """
    # Make shorter variable names for data from the spectral class instance object
    array_data = ms_array.array_data
    waves = ms_array.wavelengths

    max_wavelength = max(float(i) for i in waves)
    min_wavelength = min(float(i) for i in waves)
    # Check range of available wavelength
    if max_wavelength >= 600 and min_wavelength <= 490:
        id_red = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=630)
        id_green = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=540)
        id_blue = _find_closest(spectral_array=np.array([float(i) for i in waves]), target=480)

        pseudo_rgb = cv2.merge((array_data[:, :, [id_blue]],
                                array_data[:, :, [id_green]],
                                array_data[:, :, [id_red]]))
    else:
        # Otherwise take 3 wavelengths, first, middle and last available wavelength
        id_red = int(len(waves)) - 1
        id_green = int(id_red / 2)
        pseudo_rgb = cv2.merge((array_data[:, :, [0]],
                                array_data[:, :, [id_green]],
                                array_data[:, :, [id_red]]))

    # Gamma correct pseudo_rgb image
    pseudo_rgb = pseudo_rgb ** (1 / 2.2)
    # Scale each of the channels up to 255
    debug = params.debug
    params.debug = None
    pseudo_rgb = cv2.merge((rescale(pseudo_rgb[:, :, 0]),
                            rescale(pseudo_rgb[:, :, 1]),
                            rescale(pseudo_rgb[:, :, 2])))

    # Reset debugging mode
    params.debug = debug

    return pseudo_rgb


def _ms_file_matcher(pattern, filelist, ref):
    """"""
    ref_match = re.search(pattern, ref)
    keep = []
    for s in filelist:
        s_match = re.search(pattern, s)
        if s_match:
            keep_s = True
            for g in range(2, re.compile(pattern).groups):
                if ref_match.group(g + 1) != s_match.group(g + 1):
                    keep_s = False
            if keep_s:
                keep.append(s)
    return keep


def _standardize_sources(source, pattern):
    """Standardize directory, file, and list sources

    Parameters:
    -----------
    source     = list or str,
        list of files, directory, or image filepath.
    pattern    = str,
        regex pattern for file matching

    Returns:
    --------
    MS_list           = list,
        files to be read
    source_str        = str,
        source as a string
    starts_from_file  = bool,
        Did the data start from a file?
        Useful for knowing if the wavelength in the source file is meaningful.
    base              = str,
        file basename
    """
    # standardize directory to filename
    starts_from_file = True
    # if given a list of filepaths then use it as is
    if isinstance(source, list):
        starts_from_file = False
        MS_list = source
        source_str = os.path.dirname(source[0])
        return MS_list, source_str, starts_from_file, source_str
    # set source string to source
    source_str = source
    # if source is a directory then grab an image from it to use as the reference
    # this is a little more ambiguous and is not recommended
    if os.path.isdir(source):
        starts_from_file = False
        for root, _, files in os.walk(source):
            for f in files:
                if re.search(pattern, f):
                    source = os.path.join(root, f)
    # strip basename
    path = os.path.dirname(source)
    base = os.path.basename(source)
    _, ext = os.path.splitext(source)
    # make a list of all the MS image paths
    MS_list = []
    for root, _, files in os.walk(path):
        for f in files:
            if re.search(pattern, f):
                MS_list.append(os.path.join(root, f))
    # MS_list has everything that matches the pattern at this point
    # but we don't just want to match the pattern, we need the matches
    # to be the same, so another helper
    MS_list = _ms_file_matcher(pattern, filelist=MS_list, ref=base)

    return MS_list, source_str, starts_from_file, base


def read_ms(source, wavelengths=None, pattern="MS(\\d+)_((SV|TV))_BP0_(\\d+).*"):
    """read ms data to plantcv.plantcv.MS_data object

    Parameters:
    -----------
    source      = list or str,
        Path to a single MS grayscale image, directory of such images,
        or a list of image paths
    wavelengths = list,
        Other wavelengths to include. Defaults to None.
        Will use each MS[wavelength].* file in
        the directory of the filename.

    Returns:
    --------
    ms = plantcv.plantcv.MS_data object
        Multi-spectral image object
    """
    MS_list, source_str, starts_from_file, base = _standardize_sources(source, pattern)
    # filter for wavelengths if specified
    if wavelengths:
        if starts_from_file:
            wavelengths.append(int(re.search(pattern, base).group(1)))
        pat = "MS[" + "|".join(str(n) for n in set(wavelengths)) + "]"
        MS_list = [x for x in MS_list if re.search(pat, x)]
    MS_arrays = [cv2.imread(f, -1).astype(np.uint8) for f in MS_list]
    MS_wavelengths = [int(re.sub("^MS(\\d+).*", "\\1", os.path.basename(w))) for w in MS_list]
    # check shapes
    if len({a.shape[0] for a in MS_arrays}) > 1 or len({a.shape[1] for a in MS_arrays}) > 1:
        fatal_error("MS images have different shapes!")
    array_data = np.stack(MS_arrays, axis=-1)
    meta = {"directory": base, "files": [os.path.basename(f) for f in MS_list]}

    ms = MS_data(
        array_data=array_data,
        wavelengths=MS_wavelengths,
        pseudo_rgb=None,
        filename=source_str,
        metadata=meta
    )
    ms.pseudo_rgb = _ms_make_pseudo_rgb(ms)
    _debug(visual=ms.pseudo_rgb, filename=os.path.join(params.debug_outdir, "input_ms_pseudocolor.png"))

    return ms
