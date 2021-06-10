import os
import matplotlib
from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.classes import Params
from plantcv.plantcv.classes import Outputs
from plantcv.plantcv.classes import Spectral_data
# Initialize an instance of the Params and Outputs class with default values
# params and outputs are available when plantcv is imported
params = Params()
outputs = Outputs()

from plantcv.plantcv.deprecation_warning import deprecation_warning
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
from plantcv.plantcv.rectangle_mask import rectangle_mask
from plantcv.plantcv.median_blur import median_blur
from plantcv.plantcv.fill import fill
from plantcv.plantcv.invert import invert
from plantcv.plantcv.logical_and import logical_and
from plantcv.plantcv.logical_or import logical_or
from plantcv.plantcv.logical_xor import logical_xor
from plantcv.plantcv.find_objects import find_objects
from plantcv.plantcv.roi_objects import roi_objects
from plantcv.plantcv.object_composition import object_composition
from plantcv.plantcv.within_frame import within_frame
from plantcv.plantcv.analyze_object import analyze_object
from plantcv.plantcv.analyze_bound_horizontal import analyze_bound_horizontal
from plantcv.plantcv.analyze_bound_vertical import analyze_bound_vertical
from plantcv.plantcv.analyze_color import analyze_color
from plantcv.plantcv.analyze_nir_intensity import analyze_nir_intensity
from plantcv.plantcv.print_results import print_results
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
from plantcv.plantcv.canny_edge_detect import canny_edge_detect
from plantcv.plantcv.opening import opening
from plantcv.plantcv.closing import closing
from plantcv.plantcv import roi
from plantcv.plantcv import threshold
from plantcv.plantcv.cluster_contour_mask import cluster_contour_mask
from plantcv.plantcv.analyze_thermal_values import analyze_thermal_values
from plantcv.plantcv import visualize
from plantcv.plantcv import morphology
from plantcv.plantcv.fill_holes import fill_holes
from plantcv.plantcv.get_kernel import get_kernel
from plantcv.plantcv.crop import crop
from plantcv.plantcv.stdev_filter import stdev_filter
from plantcv.plantcv.spatial_clustering import spatial_clustering
from plantcv.plantcv import photosynthesis
# add new functions to end of lists

# Auto versioning
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['fatal_error', 'Params', 'Outputs', 'Spectral_data', 'deprecation_warning', 'print_image', 'plot_image',
           'color_palette', 'apply_mask', 'gaussian_blur', 'transform', 'hyperspectral', 'readimage', 'readbayer',
           'laplace_filter', 'sobel_filter', 'scharr_filter', 'hist_equalization', 'erode', 'image_add',
           'image_fusion', 'image_subtract', 'dilate', 'watershed', 'rectangle_mask', 'rgb2gray_hsv', 'rgb2gray_lab',
           'rgb2gray_cmyk', 'rgb2gray', 'median_blur', 'fill', 'invert', 'logical_and', 'logical_or', 'logical_xor',
           'find_objects', 'roi_objects', 'object_composition', 'analyze_object', 'morphology',
           'analyze_bound_horizontal', 'analyze_bound_vertical', 'analyze_color', 'analyze_nir_intensity',
           'print_results', 'flip', 'crop_position_mask', 'get_nir', 'report_size_marker_area',
           'white_balance', 'acute_vertex', 'scale_features', 'landmark_reference_pt_dist', 'outputs',
           'x_axis_pseudolandmarks', 'y_axis_pseudolandmarks', 'cluster_contours', 'visualize',
           'cluster_contour_splitimg', 'rotate', 'shift_img', 'output_mask', 'auto_crop', 'canny_edge_detect',
           'background_subtraction', 'naive_bayes_classifier', 'acute', 'distance_transform', 'params',
           'cluster_contour_mask', 'analyze_thermal_values', 'opening',
           'closing', 'within_frame', 'fill_holes', 'get_kernel',  'crop', 'stdev_filter',
           'spatial_clustering', 'photosynthesis']
