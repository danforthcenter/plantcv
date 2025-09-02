from importlib.metadata import version

# Auto versioning
__version__ = version("plantcv")

from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.classes import Params
from plantcv.plantcv.classes import Outputs
from plantcv.plantcv.classes import Spectral_data
from plantcv.plantcv.classes import PSII_data
from plantcv.plantcv.classes import Points
from plantcv.plantcv.classes import Objects

# Initialize an instance of the Params and Outputs class with default values
# params and outputs are available when plantcv is imported
params = Params()
outputs = Outputs()

from plantcv.plantcv.deprecation_warning import deprecation_warning
from plantcv.plantcv.warn import warn
from plantcv.plantcv.print_image import print_image
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv.rgb2gray import rgb2gray
from plantcv.plantcv.rgb2gray_hsv import rgb2gray_hsv
from plantcv.plantcv.rgb2gray_lab import rgb2gray_lab
from plantcv.plantcv.rgb2gray_cmyk import rgb2gray_cmyk
from plantcv.plantcv.gaussian_blur import gaussian_blur
from plantcv.plantcv import transform
from plantcv.plantcv import hyperspectral
from plantcv.plantcv import spectral_index
from plantcv.plantcv.apply_mask import apply_mask
from plantcv.plantcv.readimage import readimage
from plantcv.plantcv.readbayer import readbayer
from plantcv.plantcv.laplace_filter import laplace_filter
from plantcv.plantcv.sobel_filter import sobel_filter
from plantcv.plantcv.scharr_filter import scharr_filter
from plantcv.plantcv.hist_equalization import hist_equalization
from plantcv.plantcv.image_add import image_add
from plantcv.plantcv.image_fusion import image_fusion
from plantcv.plantcv.image_subtract import image_subtract
from plantcv.plantcv.erode import erode
from plantcv.plantcv.dilate import dilate
from plantcv.plantcv.watershed import watershed_segmentation
from plantcv.plantcv.median_blur import median_blur
from plantcv.plantcv.fill import fill
from plantcv.plantcv.invert import invert
from plantcv.plantcv.logical_and import logical_and
from plantcv.plantcv.logical_or import logical_or
from plantcv.plantcv.logical_xor import logical_xor
from plantcv.plantcv.within_frame import within_frame
from plantcv.plantcv.flip import flip
from plantcv.plantcv.crop_position_mask import crop_position_mask
from plantcv.plantcv.report_size_marker_area import report_size_marker_area
from plantcv.plantcv.white_balance import white_balance
from plantcv.plantcv.shift_img import shift_img
from plantcv.plantcv.output_mask_ori_img import output_mask
from plantcv.plantcv.auto_crop import auto_crop
from plantcv.plantcv.background_subtraction import background_subtraction
from plantcv.plantcv.naive_bayes_classifier import naive_bayes_classifier
from plantcv.plantcv import homology
from plantcv.plantcv.distance_transform import distance_transform
from plantcv.plantcv.canny_edge_detect import canny_edge_detect
from plantcv.plantcv.opening import opening
from plantcv.plantcv.closing import closing
from plantcv.plantcv import roi
from plantcv.plantcv import threshold
from plantcv.plantcv import visualize
from plantcv.plantcv import morphology
from plantcv.plantcv.fill_holes import fill_holes
from plantcv.plantcv.get_kernel import get_kernel
from plantcv.plantcv.crop import crop
from plantcv.plantcv.stdev_filter import stdev_filter
from plantcv.plantcv.spatial_clustering import spatial_clustering
from plantcv.plantcv import photosynthesis
from plantcv.plantcv import annotate
from plantcv.plantcv import io
from plantcv.plantcv.segment_image_series import segment_image_series
from plantcv.plantcv.create_labels import create_labels
from plantcv.plantcv.floodfill import floodfill
from plantcv.plantcv import analyze
from plantcv.plantcv import filters
from plantcv.plantcv.kmeans_classifier import predict_kmeans
from plantcv.plantcv.kmeans_classifier import mask_kmeans
from plantcv.plantcv import qc
# add new functions to end of lists

__all__ = [
    "fatal_error",
    "Params",
    "Outputs",
    "Spectral_data",
    'PSII_data',
    'Points',
    "Objects",
    "deprecation_warning",
    "warn",
    "print_image",
    "plot_image",
    "color_palette",
    "rgb2gray",
    "rgb2gray_hsv",
    "rgb2gray_lab",
    "rgb2gray_cmyk",
    "gaussian_blur",
    "transform",
    "hyperspectral",
    "spectral_index",
    "apply_mask",
    "readimage",
    "readbayer",
    "laplace_filter",
    "sobel_filter",
    "scharr_filter",
    "hist_equalization",
    "image_add",
    "image_fusion",
    "image_subtract",
    "erode",
    "dilate",
    "watershed_segmentation",
    "median_blur",
    "fill",
    "invert",
    "logical_and",
    "logical_or",
    "logical_xor",
    "within_frame",
    "flip",
    "crop_position_mask",
    "report_size_marker_area",
    "white_balance",
    "shift_img",
    "output_mask",
    "auto_crop",
    "background_subtraction",
    "naive_bayes_classifier",
    "distance_transform",
    "canny_edge_detect",
    "opening",
    "closing",
    "roi",
    "threshold",
    "visualize",
    "morphology",
    "fill_holes",
    "get_kernel",
    "crop",
    "stdev_filter",
    "spatial_clustering",
    "photosynthesis",
    "homology",
    "annotate",
    "io",
    "segment_image_series",
    "create_labels",
    "analyze",
    "floodfill",
    "filters",
    "predict_kmeans",
    "mask_kmeans",
    "qc"
]
