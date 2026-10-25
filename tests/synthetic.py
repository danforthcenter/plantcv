"""Synthetic image and data generators for the PlantCV test suite.

The synthetic plant is drawn on a 100 x 120 (rows x columns) canvas from non-overlapping,
axis-aligned rectangles so that pixel counts and dimensions are exact. Row and column ranges
are half-open, as in NumPy slicing.

    Region          Rows     Columns   Pixels
    stem            30:90    58:62     60 x 4  = 240
    left leaf       40:50    30:58     10 x 28 = 280
    right leaf      55:65    62:90     10 x 28 = 280
    small object    10:14    10:14     4 x 4   = 16

The stem and leaves touch and form one connected plant of 800 pixels whose bounding box is
rows 30:90 and columns 30:90 (60 x 60). The small object is separate from the plant, giving
816 foreground pixels in total.

In the RGB image every foreground pixel is BGR (0, 128, 0), which OpenCV encodes as hue 60
(120 degrees), and the background is BGR (128, 128, 128). In the grayscale image plant pixels
are 200, small object pixels are 120, and background pixels are 50; having three distinct values
means the grayscale image is never mistaken for a binary image.
"""
import os
import numpy as np
from plantcv.plantcv.classes import MS_data

PLANT_SHAPE = (100, 120)
PLANT_RECTS = {
    "stem": (30, 90, 58, 62),
    "left_leaf": (40, 50, 30, 58),
    "right_leaf": (55, 65, 62, 90),
}
SMALL_OBJECT_RECT = (10, 14, 10, 14)
PLANT_BGR = (0, 128, 0)
BACKGROUND_BGR = (128, 128, 128)
PLANT_GRAY = 200
SMALL_OBJECT_GRAY = 120
BACKGROUND_GRAY = 50


def plant_mask(small_object=True):
    """Create the binary mask of the synthetic plant.

    Parameters
    ----------
    small_object : bool
        Include the separate 4 x 4 object (default True).

    Returns
    -------
    numpy.ndarray
        uint8 mask with foreground 255 and background 0.
    """
    mask = np.zeros(PLANT_SHAPE, dtype=np.uint8)
    rects = list(PLANT_RECTS.values())
    if small_object:
        rects.append(SMALL_OBJECT_RECT)
    for y0, y1, x0, x1 in rects:
        mask[y0:y1, x0:x1] = 255
    return mask


def plant_rgb(mask=None):
    """Create a BGR image of the synthetic plant.

    Parameters
    ----------
    mask : numpy.ndarray, optional
        Binary mask of foreground pixels (default plant_mask()).

    Returns
    -------
    numpy.ndarray
        uint8 BGR image with PLANT_BGR foreground and BACKGROUND_BGR background.
    """
    if mask is None:
        mask = plant_mask()
    img = np.full((*mask.shape, 3), BACKGROUND_BGR, dtype=np.uint8)
    img[mask > 0] = PLANT_BGR
    return img


def plant_gray():
    """Create a grayscale image of the synthetic plant.

    Returns
    -------
    numpy.ndarray
        uint8 image with PLANT_GRAY plant, SMALL_OBJECT_GRAY small object, and
        BACKGROUND_GRAY background.
    """
    img = np.full(PLANT_SHAPE, BACKGROUND_GRAY, dtype=np.uint8)
    img[plant_mask(small_object=False) > 0] = PLANT_GRAY
    y0, y1, x0, x1 = SMALL_OBJECT_RECT
    img[y0:y1, x0:x1] = SMALL_OBJECT_GRAY
    return img


def random_image(shape, seed=0):
    """Create an image of uniformly distributed random values.

    Parameters
    ----------
    shape : tuple
        Shape of the image.
    seed : int
        Seed for the random number generator (default 0).

    Returns
    -------
    numpy.ndarray
        uint8 image.
    """
    rng = np.random.default_rng(seed)
    return rng.integers(0, 256, size=shape, dtype=np.uint8)


def binary_rect_image(shape):
    """Create a float image with a rectangle of ones at rows 3:7 and columns 2:8.

    Parameters
    ----------
    shape : tuple
        Shape of the image.

    Returns
    -------
    numpy.ndarray
        float64 image of zeros and ones.
    """
    img = np.zeros(shape)
    img[3:7, 2:8] = 1
    return img


def ms_data(wavelengths):
    """Create a 10 x 10 multispectral data object with every band equal to one.

    Parameters
    ----------
    wavelengths : list
        Wavelengths of the bands.

    Returns
    -------
    plantcv.plantcv.classes.MS_data
        Multispectral data object.
    """
    array_data = np.stack([np.ones((10, 10)) for _ in wavelengths], axis=-1)
    wavelength_dict = {k: i for i, k in enumerate(wavelengths)}
    return MS_data(array_data=array_data, wavelength_dict=wavelength_dict,
                   max_wavelength=max(wavelengths), min_wavelength=min(wavelengths),
                   filename="test")


def write_envi(outdir, filename, default_bands=None):
    """Write a small ENVI datacube and the matching header file.

    The datacube has 2 lines, 3 samples, and 5 bands (500-700 nm in 50 nm steps), stored
    band interleaved by line as unsigned 16-bit integers with values 0-29.

    Parameters
    ----------
    outdir : str
        Directory to write the data and header files to.
    filename : str
        Base name of the data and header files.
    default_bands : str, optional
        Value of the default bands header field, or None to leave the field out.

    Returns
    -------
    str
        Path of the ENVI data file.
    """
    lines, samples, bands = 2, 3, 5
    wavelengths = [500.0, 550.0, 600.0, 650.0, 700.0]
    default = "" if default_bands is None else "default bands = {" + default_bands + "}\n"
    header = ("ENVI\n"
              f"samples = {samples}\n"
              f"lines = {lines}\n"
              f"bands = {bands}\n"
              "header offset = 0\n"
              "file type = ENVI Standard\n"
              "data type = 12\n"
              "interleave = bil\n"
              "byte order = 0\n"
              "wavelength units = nm\n"
              f"{default}"
              "wavelength = {" + ",".join(str(wl) for wl in wavelengths) + "}\n")
    datafile = os.path.join(str(outdir), filename)
    with open(datafile + ".hdr", "w") as fp:
        fp.write(header)
    # Band Interleaved by Line data stored as unsigned 16-bit integers (ENVI data type 12)
    np.arange(lines * bands * samples, dtype=np.uint16).reshape(lines, bands, samples).tofile(datafile)
    return datafile
