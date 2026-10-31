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

The two-plant mask is 50 x 125 with two separate disks of radius 12 centered at (row 25,
column 30) and (row 25, column 90). A disk includes every pixel whose center is within the
radius, so each disk has 441 pixels.

The squares mask is 60 x 250 with seven separate squares in rows 10 onward. Filled squares have
solidity 1. A frame (a square outline of a given thickness) has the filled square as its convex
hull, so its solidity is the frame area divided by the square area.

    Columns   Size   Thickness   Pixels   Solidity
    10:20     10     filled      100      1
    30:50     20     filled      400      1
    60:80     20     4           256      0.64
    90:120    30     5           500      0.5556
    130:150   20     2           144      0.36
    160:180   20     1           76       0.19
    190:230   40     1           156      0.0975

The skeleton is a 1-pixel-wide, 8-connected line drawing on the 100 x 120 canvas. Its points are
given as (x, y) = (column, row), as in OpenCV.

    Branch            Pixels                                       Tip
    stem              x = 60, y = 45..89                           (60, 89)
    upper left leaf   (60 - k, 45 - k), k = 1..20                  (40, 25)
    upper right leaf  (60 + k, 45 - k), k = 1..20                  (80, 25)
    lower left leaf   y = 70, x = 31..59                           (31, 70)
    right leaf        y = 58, x = 61..79, then x = 80, y = 59..68  (80, 68)

The skeleton has 143 pixels, 5 tips and 3 branch points: (60, 45), where the upper leaves leave the
top of the stem, and (60, 58) and (60, 70). Removing the 3 x 3 block around each branch point, as
plantcv.morphology.segment_skeleton does, leaves 7 segments:

    Segment           Pixels   Ends
    lower left leaf   28       (31, 70), (58, 70)
    right leaf        28       (62, 58), (80, 68); it bends from horizontal to vertical
    upper left leaf   19       (40, 25), (58, 43)
    upper right leaf  19       (62, 43), (80, 25)
    stem (bottom)     18       (60, 72), (60, 89)
    stem (middle)     9        (60, 60), (60, 68)
    stem (top)        10       (60, 47), (60, 56)

The cycle option adds the outline of the square x, y = 5..14, separate from the plant, which
encloses one cycle. The skeleton mask is the skeleton dilated by a 3 x 3 square.

The hyperspectral datacube has 2 lines, 3 samples, and one band per nanometer from 400 to 1000 nm
(601 bands), so the band closest to any whole-nanometer wavelength in that range is exactly that
wavelength. Pixel p = 3 * line + sample (0 to 5) has reflectance (wavelength / 700) ** (p - 2.5). Every
pixel has reflectance 1 at 700 nm; pixels 0 to 2 fall and pixels 3 to 5 rise with wavelength, each
along a different curve. Every spectral index therefore takes several distinct non-negative values,
which a pseudo-RGB image of the index needs. The hyperspectral mask selects the middle column,
pixels 1 and 4, whose reflectance is (wavelength / 700) ** -1.5 and (wavelength / 700) ** 1.5.

The CropReporter datasets are 10 x 12 (rows x columns). Each header is a real CropReporter .INF file
(CROPREPORTER_TEMPLATES) with ImageRows and ImageCols set to 10 and 12. Every frame is uniform and
takes its value from these fluorescence levels (CROPREPORTER_LEVELS):

    Dark-adapted       Light-adapted
    Fdark      10      Flight      20
    F0         300     Fp          150
    Fm         1000    Fmp         250
    Fdarksat   500     Flightsat   200

So Fv/Fm = (1000 - 300) / 1000 = 0.7, Fq'/Fm' = (250 - 150) / 250 = 0.4, and NPQ = Fm / Fmp - 1 = 3.

    Dataset   Template   Frames
    PSD       v441       Fdark, F0, 400, 500, 600, 700, Fm, 990, 980, ..., 860 (21 frames)
    PSL       v441       Flight, Fp, 170, 190, 210, 230, Fmp, 245, 240, ..., 180 (21 frames)
    NPQ       v441       Fdark, F0, Fm, Flight, Fp, Fmp
    CHL       v441       Fdark, 1200
    CLR       v441       25600, 38400, 51200 (red, green, blue; 100, 150, 200 as 8-bit values)
    SPC       v441       13107, 26214, 39321 (540, 710, 770 nm; 0.2, 0.4, 0.6 of the 16-bit range)
    PMD       v653       Fdark, F0, Fm, Fdarksat
    PML       v653       Flight, Fp, Fmp, Flightsat

The v441 header puts F0 and Fp at frame 1 and Fm and Fmp at frame 6 (FvFmFrameF0=0, FvFmFrameFm=5,
FqFmFrameFsp=0, FqFmFrameFmp=5), and in PSD and PSL every later frame is lower than Fm or Fmp. In every
dataset Fm and Fmp are the brightest frames after F0 and Fp.
"""
import os
import cv2
import numpy as np
from plantcv.plantcv.classes import MS_data, Spectral_data

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
TWO_PLANTS_SHAPE = (50, 125)
TWO_PLANTS_CENTERS = ((25, 30), (25, 90))
TWO_PLANTS_RADIUS = 12
SQUARES_SHAPE = (60, 250)
SKELETON_TIPS = ((60, 89), (31, 70), (80, 68), (80, 25), (40, 25))
SKELETON_BRANCH_PTS = ((60, 45), (60, 58), (60, 70))
SPECTRAL_SHAPE = (2, 3)
SPECTRAL_WAVELENGTHS = range(400, 1001)
# (row, column, size, thickness) of each square; thickness 0 means filled
SQUARES = ((10, 10, 10, 0), (10, 30, 20, 0), (10, 60, 20, 4), (10, 90, 30, 5),
           (10, 130, 20, 2), (10, 160, 20, 1), (10, 190, 40, 1))
TESTDATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
CROPREPORTER_SHAPE = (10, 12)
CROPREPORTER_TEMPLATES = {
    "v441": os.path.join(TESTDATA, "cropreporter_v441", "PSII_HDR_020321_WT_TOP_1.INF"),
    "v653": os.path.join(TESTDATA, "cropreporter_v653", "HDR_dark_light.INF"),
}
CROPREPORTER_LEVELS = {"Fdark": 10, "F0": 300, "Fm": 1000, "Fdarksat": 500,
                       "Flight": 20, "Fp": 150, "Fmp": 250, "Flightsat": 200}
_LVL = CROPREPORTER_LEVELS
CROPREPORTER_FRAMES = {
    "PSD": ([_LVL["Fdark"], _LVL["F0"]] + [_LVL["F0"] + 100 * k for k in range(1, 5)] + [_LVL["Fm"]] +
            [_LVL["Fm"] - 10 * k for k in range(1, 15)]),
    "PSL": ([_LVL["Flight"], _LVL["Fp"]] + [_LVL["Fp"] + 20 * k for k in range(1, 5)] + [_LVL["Fmp"]] +
            [_LVL["Fmp"] - 5 * k for k in range(1, 15)]),
    "NPQ": [_LVL[f] for f in ("Fdark", "F0", "Fm", "Flight", "Fp", "Fmp")],
    "CHL": [_LVL["Fdark"], 1200],
    "CLR": [25600, 38400, 51200],
    "SPC": [13107, 26214, 39321],
    "PMD": [_LVL[f] for f in ("Fdark", "F0", "Fm", "Fdarksat")],
    "PML": [_LVL[f] for f in ("Flight", "Fp", "Fmp", "Flightsat")],
}


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


def disk_mask(shape, centers, radius):
    """Create a binary mask of filled disks.

    Parameters
    ----------
    shape : tuple
        Shape of the mask (rows, columns).
    centers : list
        Disk centers as (row, column) tuples.
    radius : int
        Radius of every disk in pixels.

    Returns
    -------
    numpy.ndarray
        uint8 mask with pixels within radius of a center set to 255.
    """
    rows, cols = np.ogrid[:shape[0], :shape[1]]
    mask = np.zeros(shape, dtype=np.uint8)
    for cy, cx in centers:
        mask[(rows - cy) ** 2 + (cols - cx) ** 2 <= radius ** 2] = 255
    return mask


def two_plants_mask():
    """Create a binary mask of two separate disk-shaped plants.

    Returns
    -------
    numpy.ndarray
        uint8 mask with foreground 255 and background 0.
    """
    return disk_mask(TWO_PLANTS_SHAPE, TWO_PLANTS_CENTERS, TWO_PLANTS_RADIUS)


def squares_mask():
    """Create a binary mask of filled squares and square frames.

    Returns
    -------
    numpy.ndarray
        uint8 mask with foreground 255 and background 0.
    """
    mask = np.zeros(SQUARES_SHAPE, dtype=np.uint8)
    for y, x, size, thickness in SQUARES:
        mask[y:y + size, x:x + size] = 255
        if thickness:
            mask[y + thickness:y + size - thickness, x + thickness:x + size - thickness] = 0
    return mask


def _skeleton_branches():
    """List the pixels of each branch of the synthetic skeleton.

    Returns
    -------
    dict
        Branch name mapped to a list of (x, y) pixel coordinates.
    """
    return {
        "stem": [(60, y) for y in range(45, 90)],
        "lower_left_leaf": [(x, 70) for x in range(31, 60)],
        "right_leaf": [(x, 58) for x in range(61, 80)] + [(80, y) for y in range(59, 69)],
        "upper_left_leaf": [(60 - k, 45 - k) for k in range(1, 21)],
        "upper_right_leaf": [(60 + k, 45 - k) for k in range(1, 21)],
    }


def _draw_pixels(points):
    """Draw pixels on a blank canvas the size of the synthetic plant.

    Parameters
    ----------
    points : list
        (x, y) pixel coordinates.

    Returns
    -------
    numpy.ndarray
        uint8 image with the points set to 255.
    """
    img = np.zeros(PLANT_SHAPE, dtype=np.uint8)
    for x, y in points:
        img[y, x] = 255
    return img


def skeleton(cycle=False):
    """Create the synthetic plant skeleton.

    Parameters
    ----------
    cycle : bool
        Add a separate square outline that encloses one cycle (default False).

    Returns
    -------
    numpy.ndarray
        uint8 image with skeleton pixels 255 and background 0.
    """
    img = _draw_pixels([p for points in _skeleton_branches().values() for p in points])
    if cycle:
        cv2.rectangle(img, (5, 5), (14, 14), 255, 1)
    return img


def skeleton_mask():
    """Create a binary mask around the synthetic plant skeleton.

    Returns
    -------
    numpy.ndarray
        uint8 mask of the skeleton dilated by a 3 x 3 square.
    """
    return cv2.dilate(skeleton(), np.ones((3, 3), dtype=np.uint8))


def skeleton_segments():
    """Create the contours of the synthetic skeleton segments.

    The segments are the skeleton branches with the 3 x 3 block around each branch point removed.

    Returns
    -------
    tuple
        Leaf segment contours (lower left, right, upper left and upper right leaf) and stem segment
        contours (bottom to top), each a list of numpy.ndarray.
    """
    branches = _skeleton_branches()
    leaves = []
    stem = []
    for name, points in branches.items():
        kept = [(x, y) for x, y in points
                if all(max(abs(x - bx), abs(y - by)) > 1 for bx, by in SKELETON_BRANCH_PTS)]
        contours, _ = find_contours(_draw_pixels(kept))
        if name == "stem":
            stem = sorted(contours, key=lambda c: c[:, 0, 1].max(), reverse=True)
        else:
            leaves.append(contours[0])
    return leaves, stem


def find_contours(mask):
    """Find all contours of a binary mask with their hierarchy.

    Parameters
    ----------
    mask : numpy.ndarray
        Binary mask.

    Returns
    -------
    tuple
        Contours (tuple of numpy.ndarray) and hierarchy (numpy.ndarray), as returned by
        cv2.findContours with RETR_TREE and CHAIN_APPROX_NONE.
    """
    return cv2.findContours(np.copy(mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


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


def reflectance(wavelength):
    """Compute the reflectance of every pixel of the hyperspectral datacube at one wavelength.

    Parameters
    ----------
    wavelength : float
        Wavelength in nanometers.

    Returns
    -------
    numpy.ndarray
        2 x 3 float64 array of (wavelength / 700) ** (p - 2.5) for pixel p = 3 * line + sample.
    """
    pixel = np.arange(SPECTRAL_SHAPE[0] * SPECTRAL_SHAPE[1]).reshape(SPECTRAL_SHAPE)
    return (wavelength / 700) ** (pixel - 2.5)


def spectral_data():
    """Create the hyperspectral datacube.

    Returns
    -------
    plantcv.plantcv.classes.Spectral_data
        Hyperspectral data object with reflectance(wavelength) in each band and no default bands.
    """
    array_data = np.stack([reflectance(wl) for wl in SPECTRAL_WAVELENGTHS], axis=-1)
    return Spectral_data(array_data=array_data, max_wavelength=float(max(SPECTRAL_WAVELENGTHS)),
                         min_wavelength=float(min(SPECTRAL_WAVELENGTHS)), max_value=float(np.amax(array_data)),
                         min_value=float(np.amin(array_data)), d_type=array_data.dtype,
                         wavelength_dict={float(wl): float(i) for i, wl in enumerate(SPECTRAL_WAVELENGTHS)},
                         samples=SPECTRAL_SHAPE[1], lines=SPECTRAL_SHAPE[0], interleave="bil",
                         wavelength_units="nm", array_type="datacube", filename="synthetic", default_bands=None)


def spectral_mask():
    """Create a binary mask of the middle column of the hyperspectral datacube.

    Returns
    -------
    numpy.ndarray
        2 x 3 uint8 mask with pixels 1 and 4 set to 255.
    """
    mask = np.zeros(SPECTRAL_SHAPE, dtype=np.uint8)
    mask[:, 1] = 255
    return mask


def envi_array():
    """Create the datacube that write_envi and write_arcgis store.

    Returns
    -------
    numpy.ndarray
        2 x 3 x 5 (lines x samples x bands) uint16 array of the values 0-29, numbered in band
        interleaved by line order: value = 15 * line + 3 * band + sample.
    """
    return np.arange(30, dtype=np.uint16).reshape(2, 5, 3).transpose(0, 2, 1)


def write_envi(outdir, filename, default_bands=None, wavelengths=None, wavelength_units="nm", interleave="bil"):
    """Write a small ENVI datacube and the matching header file.

    The datacube is envi_array(): 2 lines, 3 samples, and 5 bands, stored band interleaved by line
    as unsigned 16-bit integers with values 0-29.

    Parameters
    ----------
    outdir : str
        Directory to write the data and header files to.
    filename : str
        Base name of the data and header files.
    default_bands : str, optional
        Value of the default bands header field, or None to leave the field out.
    wavelengths : list, optional
        The 5 band wavelengths (default 500-700 nm in 50 nm steps).
    wavelength_units : str, optional
        Value of the wavelength units header field (default "nm"), or None to leave the field out.
    interleave : str
        Value of the interleave header field (default "bil"). The data is always stored band
        interleaved by line.

    Returns
    -------
    str
        Path of the ENVI data file.
    """
    lines, samples, bands = 2, 3, 5
    if wavelengths is None:
        wavelengths = [500.0, 550.0, 600.0, 650.0, 700.0]
    default = "" if default_bands is None else "default bands = {" + default_bands + "}\n"
    units = "" if wavelength_units is None else f"wavelength units = {wavelength_units}\n"
    header = ("ENVI\n"
              f"samples = {samples}\n"
              f"lines = {lines}\n"
              f"bands = {bands}\n"
              "header offset = 0\n"
              "file type = ENVI Standard\n"
              "data type = 12\n"
              f"interleave = {interleave}\n"
              "byte order = 0\n"
              f"{units}"
              f"{default}"
              "wavelength = {" + ",".join(str(wl) for wl in wavelengths) + "}\n")
    datafile = os.path.join(str(outdir), filename)
    with open(datafile + ".hdr", "w") as fp:
        fp.write(header)
    # Band Interleaved by Line data stored as unsigned 16-bit integers (ENVI data type 12)
    envi_array().transpose(0, 2, 1).tofile(datafile)
    return datafile


def write_arcgis(outdir, filename):
    """Write the datacube of write_envi with an ArcGIS-style header file.

    The header gives the layout as keyword and value pairs and lists the wavelengths (500-700 nm
    in 50 nm steps) between WAVELENGTHS and WAVELENGTHS_END. The data is stored band interleaved by
    line as 16-bit integers.

    Parameters
    ----------
    outdir : str
        Directory to write the data and header files to.
    filename : str
        Base name of the data and header files.

    Returns
    -------
    str
        Path of the data file.
    """
    header = ("BYTEORDER I\n"
              "LAYOUT BIL\n"
              "NROWS 2\n"
              "NCOLS 3\n"
              "NBANDS 5\n"
              "NBITS 16\n"
              "BANDROWBYTES 6\n"
              "TOTALROWBYTES 30\n"
              "WAVELENGTHS\n"
              "500.0\n550.0\n600.0\n650.0\n700.0\n"
              "WAVELENGTHS_END\n")
    datafile = os.path.join(str(outdir), filename)
    with open(datafile + ".hdr", "w") as fp:
        fp.write(header)
    envi_array().astype(np.int16).transpose(0, 2, 1).tofile(datafile)
    return datafile


def write_cropreporter(outdir, template, datasets, metadata=None, shape=CROPREPORTER_SHAPE):
    """Write a CropReporter dataset: an .INF header and one .DAT file per dataset.

    Parameters
    ----------
    outdir : str
        Directory to write the files to.
    template : str
        Key of the CROPREPORTER_TEMPLATES header to start from. The files keep its name, with HDR
        replaced by the dataset key for each .DAT file.
    datasets : list or dict
        Dataset keys (e.g. ["PSD", "PSL"]) whose frames come from CROPREPORTER_FRAMES, or a dict
        mapping each dataset key to its frames. A frame is a number (a uniform frame) or an array
        of the given shape.
    metadata : dict, optional
        Header keys to replace or add.
    shape : tuple
        Frame shape (rows, columns) (default CROPREPORTER_SHAPE). It sets ImageRows and ImageCols.

    Returns
    -------
    str
        Path of the .INF file.
    """
    if not isinstance(datasets, dict):
        datasets = {key: CROPREPORTER_FRAMES[key] for key in datasets}
    metadata = {"ImageRows": shape[0], "ImageCols": shape[1], **(metadata or {})}
    with open(CROPREPORTER_TEMPLATES[template], "r") as fp:
        header = fp.read().splitlines()
    for i, line in enumerate(header):
        key = line.split("=")[0]
        if key in metadata:
            header[i] = f"{key}={metadata.pop(key)}"
    header += [f"{key}={value}" for key, value in metadata.items()]
    filename = os.path.basename(CROPREPORTER_TEMPLATES[template])
    inf = os.path.join(str(outdir), filename)
    with open(inf, "w") as fp:
        fp.write("\n".join(header) + "\n")
    for key, frames in datasets.items():
        cube = np.stack([np.broadcast_to(frame, shape) for frame in frames]).astype(np.uint16)
        parts = filename.split("_")
        parts[parts.index("HDR")] = key
        # Unsigned 16-bit frames one after another, each stored column by column
        cube.transpose(0, 2, 1).tofile(os.path.join(str(outdir), "_".join(parts).replace(".INF", ".DAT")))
    return inf
