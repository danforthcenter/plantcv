import os
import re
import cv2
import numpy as np
from plantcv.plantcv._debug import _debug
from plantcv.plantcv._globals import params
from plantcv.plantcv.classes import MS_data
from plantcv.plantcv.fatal_error import fatal_error


def _ms_file_matcher(pattern, filelist, ref):
    """Filter a list of file names to match capture groups in a reference name

    Parameters:
    -----------
    pattern     = str,
        Regular expression used to match images that are of the same subject from the same angle, etc.
        This should include a capture group for the wavelength, which is expected to be the *first* capture group.
        Subsequent capture groups are used to match against other candidate image files.
    filelist    = list,
        list of str filenames
    ref         = str,
        filename of the initial image given (values from 2nd+ capture group here are used as the filter condition)

    Returns:
    --------
    list,
        Filtered list of file names
    """
    ref_match = re.search(pattern, ref)
    keep = []
    for s in filelist:
        s_match = re.search(pattern, s)
        if s_match:
            keep_s = True
            for g in range(2, re.compile(pattern).groups + 1):
                if ref_match.group(g) != s_match.group(g):
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
            matching = [f for f in files if re.search(pattern, f)]
            if matching:
                source = os.path.join(root, matching[0])
                break
    # strip basename
    path = os.path.dirname(source)
    base = os.path.basename(source)
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
    pattern     = str,
        Regular expression used to match images that are of the same subject from the same angle, etc.
        This should include a capture group for the wavelength, which is expected to be the *first* capture group.
        Subsequent capture groups are used to match against other candidate image files.

    Returns:
    --------
    ms = plantcv.plantcv.MS_data object
        Multi-spectral image object
    """
    MS_list, source_str, starts_from_file, base = _standardize_sources(source, pattern)
    # filter for wavelengths if specified
    if wavelengths:
        if starts_from_file:
            wavelengths = list(wavelengths) + [int(re.search(pattern, base).group(1))]
        pat = r"MS(" + "|".join(re.escape(str(n)) for n in set(wavelengths)) + r")"
        MS_list = [x for x in MS_list if re.search(pat, os.path.basename(x))]
    # NOTE we only collect 0-255 png images with the tool this is built for.
    # potentially other tools could be non-uint8 compatible by default.
    MS_arrays = [cv2.imread(f, -1).astype(np.uint8) for f in MS_list]
    MS_wavelengths = [int(re.sub("^MS(\\d+).*", "\\1", os.path.basename(w))) for w in MS_list]
    MS_wavelengths_dict = {}
    for v, k in enumerate(MS_wavelengths):
        MS_wavelengths_dict[k] = v
    # check shapes
    if len({a.shape[0] for a in MS_arrays}) > 1 or len({a.shape[1] for a in MS_arrays}) > 1:
        fatal_error("MS images have different shapes!")
    array_data = np.stack(MS_arrays, axis=-1)
    meta = {"directory": source_str, "files": [os.path.basename(f) for f in MS_list]}

    ms = MS_data(
        array_data=array_data,
        wavelength_dict=MS_wavelengths_dict,
        max_wavelength=max(MS_wavelengths),
        min_wavelength=min(MS_wavelengths),
        filename=source_str,
        metadata=meta
    )

    _debug(visual=ms.pseudo_rgb(), filename=os.path.join(params.debug_outdir, "input_ms_pseudocolor.png"))

    return ms
