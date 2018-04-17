__version__ = 2.1
__all__ = ['fatal_error', 'print_image', 'plot_image', 'color_palette', 'plot_colorbar', 'apply_mask', 'readimage',
           'laplace_filter', 'sobel_filter', 'scharr_filter', 'hist_equalization', 'plot_hist', 'image_add',
           'image_subtract', 'erode', 'dilate', 'watershed', 'rectangle_mask', 'rgb2gray_hsv', 'rgb2gray_lab',
           'rgb2gray', 'binary_threshold', 'median_blur', 'fill', 'invert', 'logical_and', 'logical_or', 'logical_xor',
           'find_objects', 'define_roi', 'roi_objects', 'object_composition', 'analyze_object', 'analyze_bound_horizontal',
           'analyze_bound_vertical','analyze_bound', 'analyze_color', 'analyze_NIR_intensity', 'fluor_fvfm', 'print_results', 'resize', 'flip',
           'crop_position_mask', 'get_nir', 'adaptive_threshold', 'otsu_auto_threshold', 'report_size_marker_area',
           'white_balance', 'triangle_auto_threshold', 'acute_vertex', 'scale_features', 'landmark_reference_pt_dist',
           'x_axis_pseudolandmarks', 'y_axis_pseudolandmarks', 'gaussian_blur', 'cluster_contours',
           'cluster_contour_splitimg', 'rotate_img', 'rotate','shift_img', 'output_mask', 'auto_crop',
           'background_subtraction', 'naive_bayes_classifier', 'acute','distance_transform']

from plantcv.fatal_error import fatal_error
from plantcv.print_image import print_image
from plantcv.plot_image import plot_image
from plantcv.color_palette import color_palette
from plantcv.plot_colorbar import plot_colorbar
from plantcv.apply_mask import apply_mask
from plantcv.readimage import readimage
from plantcv.laplace_filter import laplace_filter
from plantcv.sobel_filter import sobel_filter
from plantcv.scharr_filter import scharr_filter
from plantcv.hist_equalization import hist_equalization
from plantcv.plot_hist import plot_hist
from plantcv.image_add import image_add
from plantcv.image_subtract import image_subtract
from plantcv.erode import erode
from plantcv.dilate import dilate
from plantcv.watershed import watershed_segmentation
from plantcv.rectangle_mask import rectangle_mask
from plantcv.rgb2gray_hsv import rgb2gray_hsv
from plantcv.rgb2gray_lab import rgb2gray_lab
from plantcv.rgb2gray import rgb2gray
from plantcv.binary_threshold import binary_threshold
from plantcv.median_blur import median_blur
from plantcv.fill import fill
from plantcv.invert import invert
from plantcv.logical_and import logical_and
from plantcv.logical_or import logical_or
from plantcv.logical_xor import logical_xor
from plantcv.find_objects import find_objects
from plantcv.define_roi import define_roi
from plantcv.roi_objects import roi_objects
from plantcv.object_composition import object_composition
from plantcv.analyze_object import analyze_object
from plantcv.analyze_bound_horizontal import analyze_bound_horizontal
from plantcv.analyze_bound_vertical import analyze_bound_vertical
from plantcv.analyze_bound import analyze_bound
from plantcv.analyze_color import analyze_color
from plantcv.analyze_NIR_intensity import analyze_NIR_intensity
from plantcv.fluor_fvfm import fluor_fvfm
from plantcv.print_results import print_results
from plantcv.resize import resize
from plantcv.flip import flip
from plantcv.crop_position_mask import crop_position_mask
from plantcv.get_nir import get_nir
from plantcv.adaptive_threshold import adaptive_threshold
from plantcv.otsu_auto_threshold import otsu_auto_threshold
from plantcv.report_size_marker_area import report_size_marker_area
from plantcv.white_balance import white_balance
from plantcv.triangle_auto_threshold import triangle_auto_threshold
from plantcv.acute_vertex import acute_vertex
from plantcv.scale_features import scale_features
from plantcv.landmark_reference_pt_dist import landmark_reference_pt_dist
from plantcv.x_axis_pseudolandmarks import x_axis_pseudolandmarks
from plantcv.y_axis_pseudolandmarks import y_axis_pseudolandmarks
from plantcv.gaussian_blur import gaussian_blur
from plantcv.cluster_contours import cluster_contours
from plantcv.cluster_contour_splitimg import cluster_contour_splitimg
from plantcv.rotate import rotate
from plantcv.rotate_img import rotate_img
from plantcv.shift_img import shift_img
from plantcv.output_mask_ori_img import output_mask
from plantcv.auto_crop import auto_crop
from plantcv.background_subtraction import background_subtraction
from plantcv.naive_bayes_classifier import naive_bayes_classifier
from plantcv.acute import acute
from plantcv.distance_transform import distance_transform

# add new functions to end of lists


class Params:
    """PlantCV parameters class

    Keyword arguments/parameters:

    device = device number. Used to count steps in the pipeline. (default: 0)
    debug  = None, print, or plot. Print = save to file, Plot = print to screen. (default: None)

    :param device: int
    :param debug: str
    """
    def __init__(self, device=0, debug=None):
        self.device = device
        self.debug = debug


# Initialize an instance of the Params class with default values
# params is available when plantcv is imported
params = Params()
