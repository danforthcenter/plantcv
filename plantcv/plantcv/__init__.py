class Params:
    """PlantCV parameters class
    Keyword arguments/parameters:
    device       = device number. Used to count steps in the pipeline. (default: 0)
    debug        = None, print, or plot. Print = save to file, Plot = print to screen. (default: None)
    debug_outdir = Debug images output directory. (default: .)
    :param device: int
    :param debug: str
    :param debug_outdir: str
    """
    def __init__(self, device=0, debug=None, debug_outdir="."):
        self.device = device
        self.debug = debug
        self.debug_outdir = debug_outdir


# Initialize an instance of the Params class with default values
# params is available when plantcv is imported
params = Params()

from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.print_image import print_image
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.color_palette import color_palette
# from plantcv.plantcv.plot_colorbar import plot_colorbar
from plantcv.plantcv.apply_mask import apply_mask
from plantcv.plantcv.readimage import readimage
from plantcv.plantcv.readbayer import readbayer
from plantcv.plantcv.laplace_filter import laplace_filter
from plantcv.plantcv.sobel_filter import sobel_filter
from plantcv.plantcv.scharr_filter import scharr_filter
from plantcv.plantcv.hist_equalization import hist_equalization
from plantcv.plantcv.plot_hist import plot_hist
from plantcv.plantcv.image_add import image_add
from plantcv.plantcv.image_subtract import image_subtract
from plantcv.plantcv.erode import erode
from plantcv.plantcv.dilate import dilate
from plantcv.plantcv.watershed import watershed_segmentation
from plantcv.plantcv.rectangle_mask import rectangle_mask
from plantcv.plantcv.rgb2gray_hsv import rgb2gray_hsv
from plantcv.plantcv.rgb2gray_lab import rgb2gray_lab
from plantcv.plantcv.rgb2gray import rgb2gray
from plantcv.plantcv.median_blur import median_blur
from plantcv.plantcv.fill import fill
from plantcv.plantcv.invert import invert
from plantcv.plantcv.logical_and import logical_and
from plantcv.plantcv.logical_or import logical_or
from plantcv.plantcv.logical_xor import logical_xor
from plantcv.plantcv.find_objects import find_objects
from plantcv.plantcv.roi_objects import roi_objects
from plantcv.plantcv.object_composition import object_composition
from plantcv.plantcv.analyze_object import analyze_object
from plantcv.plantcv.analyze_bound_horizontal import analyze_bound_horizontal
from plantcv.plantcv.analyze_bound_vertical import analyze_bound_vertical
from plantcv.plantcv.analyze_color import analyze_color
from plantcv.plantcv.analyze_nir_intensity import analyze_nir_intensity
from plantcv.plantcv.fluor_fvfm import fluor_fvfm
from plantcv.plantcv.print_results import print_results
from plantcv.plantcv.resize import resize
from plantcv.plantcv.flip import flip
from plantcv.plantcv.crop_position_mask import crop_position_mask
from plantcv.plantcv.get_nir import get_nir
from plantcv.plantcv.report_size_marker_area import report_size_marker_area
from plantcv.plantcv.white_balance import white_balance
from plantcv.plantcv.acute_vertex import acute_vertex
from plantcv.plantcv.scale_features import scale_features
from plantcv.plantcv.landmark_reference_pt_dist import landmark_reference_pt_dist
from plantcv.plantcv.x_axis_pseudolandmarks import x_axis_pseudolandmarks
from plantcv.plantcv.y_axis_pseudolandmarks import y_axis_pseudolandmarks
from plantcv.plantcv.gaussian_blur import gaussian_blur
from plantcv.plantcv.cluster_contours import cluster_contours
from plantcv.plantcv.cluster_contour_splitimg import cluster_contour_splitimg
from plantcv.plantcv.rotate import rotate
from plantcv.plantcv.shift_img import shift_img
from plantcv.plantcv.output_mask_ori_img import output_mask
from plantcv.plantcv.auto_crop import auto_crop
from plantcv.plantcv.background_subtraction import background_subtraction
from plantcv.plantcv.naive_bayes_classifier import naive_bayes_classifier
from plantcv.plantcv.acute import acute
from plantcv.plantcv.distance_transform import distance_transform
from plantcv.plantcv.pseudocolor import pseudocolor
from plantcv.plantcv import roi
from plantcv.plantcv import threshold
from plantcv.plantcv import transform
from plantcv.plantcv.canny_edge_detect import canny_edge_detect

# add new functions to end of lists

__all__ = ['fatal_error', 'print_image', 'plot_image', 'color_palette', 'apply_mask', 'readimage',
           'readbayer', 'laplace_filter', 'sobel_filter', 'scharr_filter', 'hist_equalization', 'plot_hist', 'erode',
           'image_add', 'image_subtract', 'dilate', 'watershed', 'rectangle_mask', 'rgb2gray_hsv', 'rgb2gray_lab',
           'rgb2gray', 'median_blur', 'fill', 'invert', 'logical_and', 'logical_or', 'logical_xor',
           'find_objects', 'roi_objects', 'transform', 'object_composition', 'analyze_object',
           'analyze_bound_horizontal', 'analyze_bound_vertical', 'analyze_color', 'analyze_nir_intensity',
           'fluor_fvfm', 'print_results', 'resize', 'flip', 'crop_position_mask', 'get_nir', 'report_size_marker_area',
           'white_balance', 'acute_vertex', 'scale_features', 'landmark_reference_pt_dist',
           'x_axis_pseudolandmarks', 'y_axis_pseudolandmarks', 'gaussian_blur', 'cluster_contours',
           'cluster_contour_splitimg', 'rotate', 'shift_img', 'output_mask', 'auto_crop', 'canny_edge_detect',
           'background_subtraction', 'naive_bayes_classifier', 'acute', 'distance_transform', 'params', 'pseudocolor']


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
