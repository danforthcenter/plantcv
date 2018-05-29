from plantcv.base.fatal_error import fatal_error
from plantcv.base.print_image import print_image
from plantcv.base.plot_image import plot_image
from plantcv.base.color_palette import color_palette
from plantcv.base.plot_colorbar import plot_colorbar
from plantcv.base.apply_mask import apply_mask
from plantcv.base.readimage import readimage
from plantcv.base.laplace_filter import laplace_filter
from plantcv.base.sobel_filter import sobel_filter
from plantcv.base.scharr_filter import scharr_filter
from plantcv.base.hist_equalization import hist_equalization
from plantcv.base.plot_hist import plot_hist
from plantcv.base.image_add import image_add
from plantcv.base.image_subtract import image_subtract
from plantcv.base.erode import erode
from plantcv.base.dilate import dilate
from plantcv.base.watershed import watershed_segmentation
from plantcv.base.rectangle_mask import rectangle_mask
from plantcv.base.rgb2gray_hsv import rgb2gray_hsv
from plantcv.base.rgb2gray_lab import rgb2gray_lab
from plantcv.base.rgb2gray import rgb2gray
from plantcv.base.binary_threshold import binary_threshold
from plantcv.base.median_blur import median_blur
from plantcv.base.fill import fill
from plantcv.base.invert import invert
from plantcv.base.logical_and import logical_and
from plantcv.base.logical_or import logical_or
from plantcv.base.logical_xor import logical_xor
from plantcv.base.find_objects import find_objects
from plantcv.base.define_roi import define_roi
from plantcv.base.roi_objects import roi_objects
from plantcv.base.object_composition import object_composition
from plantcv.base.analyze_object import analyze_object
from plantcv.base.analyze_bound_horizontal import analyze_bound_horizontal
from plantcv.base.analyze_bound_vertical import analyze_bound_vertical
from plantcv.base.analyze_bound import analyze_bound
from plantcv.base.analyze_color import analyze_color
from plantcv.base.analyze_NIR_intensity import analyze_NIR_intensity
from plantcv.base.fluor_fvfm import fluor_fvfm
from plantcv.base.print_results import print_results
from plantcv.base.resize import resize
from plantcv.base.flip import flip
from plantcv.base.crop_position_mask import crop_position_mask
from plantcv.base.get_nir import get_nir
from plantcv.base.adaptive_threshold import adaptive_threshold
from plantcv.base.otsu_auto_threshold import otsu_auto_threshold
from plantcv.base.report_size_marker_area import report_size_marker_area
from plantcv.base.white_balance import white_balance
from plantcv.base.triangle_auto_threshold import triangle_auto_threshold
from plantcv.base.acute_vertex import acute_vertex
from plantcv.base.scale_features import scale_features
from plantcv.base.landmark_reference_pt_dist import landmark_reference_pt_dist
from plantcv.base.x_axis_pseudolandmarks import x_axis_pseudolandmarks
from plantcv.base.y_axis_pseudolandmarks import y_axis_pseudolandmarks
from plantcv.base.gaussian_blur import gaussian_blur
from plantcv.base.cluster_contours import cluster_contours
from plantcv.base.cluster_contour_splitimg import cluster_contour_splitimg
from plantcv.base.rotate import rotate
from plantcv.base.rotate_img import rotate_img
from plantcv.base.shift_img import shift_img
from plantcv.base.output_mask_ori_img import output_mask
from plantcv.base.auto_crop import auto_crop
from plantcv.base.background_subtraction import background_subtraction
from plantcv.base.naive_bayes_classifier import naive_bayes_classifier
from plantcv.base.acute import acute
from plantcv.base.distance_transform import distance_transform

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

__version__ = 2.1
__all__ = ['fatal_error', 'print_image', 'plot_image', 'color_palette', 'plot_colorbar', 'apply_mask', 'readimage',
           'laplace_filter', 'sobel_filter', 'scharr_filter', 'hist_equalization', 'plot_hist', 'image_add',
           'image_subtract', 'erode', 'dilate', 'watershed', 'rectangle_mask', 'rgb2gray_hsv', 'rgb2gray_lab',
           'rgb2gray', 'binary_threshold', 'median_blur', 'fill', 'invert', 'logical_and', 'logical_or', 'logical_xor',
           'find_objects', 'define_roi', 'roi_objects', 'object_composition', 'analyze_object',
           'analyze_bound_horizontal', 'analyze_bound_vertical', 'analyze_bound', 'analyze_color',
           'analyze_NIR_intensity', 'fluor_fvfm', 'print_results', 'resize', 'flip', 'crop_position_mask', 'get_nir',
           'adaptive_threshold', 'otsu_auto_threshold', 'report_size_marker_area', 'white_balance',
           'triangle_auto_threshold', 'acute_vertex', 'scale_features', 'landmark_reference_pt_dist',
           'x_axis_pseudolandmarks', 'y_axis_pseudolandmarks', 'gaussian_blur', 'cluster_contours',
           'cluster_contour_splitimg', 'rotate_img', 'rotate', 'shift_img', 'output_mask', 'auto_crop',
           'background_subtraction', 'naive_bayes_classifier', 'acute', 'distance_transform']
