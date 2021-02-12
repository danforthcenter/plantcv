import os
import matplotlib

observations = {}


class Params:
    """PlantCV parameters class."""

    def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5, dpi=100, text_size=0.55,
                 text_thickness=2, marker_size=60, color_scale="gist_rainbow", color_sequence="sequential",
                 saved_color_scale=None):
        """Initialize parameters.

        Keyword arguments/parameters:
        device            = Device number. Used to count steps in the pipeline. (default: 0)
        debug             = None, print, or plot. Print = save to file, Plot = print to screen. (default: None)
        debug_outdir      = Debug images output directory. (default: .)
        line_thickness    = Width of line drawings. (default: 5)
        dpi               = Figure plotting resolution, dots per inch. (default: 100)
        text_size         = Size of plotting text. (default: 0.55)
        text_thickness    = Thickness of plotting text. (default: 2)
        marker_size       = Size of plotting markers (default: 60)
        color_scale       = Name of plotting color scale (matplotlib colormap). (default: gist_rainbow)
        color_sequence    = Build color scales in "sequential" or "random" order. (default: sequential)
        saved_color_scale = Saved color scale that will be applied next time color_palette is called. (default: None)

        :param device: int
        :param debug: str
        :param debug_outdir: str
        :param line_thickness: numeric
        :param dpi: int
        :param text_size: float
        :param text_thickness: int
        :param marker_size: int
        :param color_scale: str
        :param color_sequence: str
        :param saved_color_scale: list
        """
        self.device = device
        self.debug = debug
        self.debug_outdir = debug_outdir
        self.line_thickness = line_thickness
        self.dpi = dpi
        self.text_size = text_size
        self.text_thickness = text_thickness
        self.marker_size = marker_size
        self.color_scale = color_scale
        self.color_sequence = color_sequence
        self.saved_color_scale = saved_color_scale


class Outputs:
    """PlantCV outputs class

    """

    def __init__(self):
        self.measurements = {}
        self.images = []
        self.observations = {}

        # Add a method to clear measurements
    def clear(self):
        self.measurements = {}
        self.images = []
        self.observations = {}

    # Method to add observation to outputs
    def add_observation(self, sample, variable, trait, method, scale, datatype, value, label):
        """
        Keyword arguments/parameters:
        sample       = Sample name. Used to distinguish between multiple samples
        variable     = A local unique identifier of a variable, e.g. a short name,
                       that is a key linking the definitions of variables with observations.
        trait        = A name of the trait mapped to an external ontology; if there is no exact mapping, an informative
                       description of the trait.
        method       = A name of the measurement method mapped to an external ontology; if there is no exact mapping, an
                       informative description of the measurement procedure
        scale        = Units of the measurement or scale in which the observations are expressed; if possible, standard
                       units and scales should be used and mapped to existing ontologies; in the case of non-standard
                       scale a full explanation should be given
        datatype     = The type of data to be stored, e.g. 'int', 'float', 'str', 'list', etc.
        value        = The data itself
        label        = The label for each value (most useful when the data is a frequency table as in hue,
                       or other tables)

        :param sample: str
        :param variable: str
        :param trait: str
        :param method: str
        :param scale: str
        :param datatype: type
        :param value:
        :param label:
        """
        self.sample = sample
        self.variable = variable
        self.trait = trait
        self.method = method
        self.scale = scale
        self.datatype = datatype
        self.value = value
        self.label = label

        # Create an empty dictionary for the sample if it does not exist
        if sample not in self.observations:
            self.observations[sample] = {}
        # Save the observation for the sample and variable
        self.observations[sample][variable] = {
            "trait": trait,
            "method": method,
            "scale": scale,
            "datatype": str(datatype),
            "value": value,
            "label": label
        }


# Initialize an instance of the Params and Outputs class with default values
# params and outputs are available when plantcv is imported
params = Params()
outputs = Outputs()


class Spectral_data:
    # PlantCV Hyperspectral data class
    def __init__(self, array_data, max_wavelength, min_wavelength, max_value, min_value, d_type, wavelength_dict,
                 samples, lines, interleave, wavelength_units, array_type, pseudo_rgb, filename, default_bands):
        # The actual array/datacube
        self.array_data = array_data
        # Min/max available wavelengths (for spectral datacube)
        self.max_wavelength = max_wavelength
        self.min_wavelength = min_wavelength
        #  Min/max pixel value for single wavelength or index
        self.max_value = max_value
        self.min_value = min_value
        # Numpy data type
        self.d_type = d_type
        # Contains all available wavelengths where keys are wavelength and value are indices
        self.wavelength_dict = wavelength_dict
        # Resolution of a single band of spectral data is (samples, lines) rather than (x,y) with other arrays
        self.samples = samples
        self.lines = lines
        # Interleave type
        self.interleave = interleave
        self.wavelength_units = wavelength_units
        # The type of array data (entire datacube, specific index, first derivative, etc)
        self.array_type = array_type
        # Pseudo-RGB image if the array_type is a datacube
        self.pseudo_rgb = pseudo_rgb
        # The filename where the data originated from
        self.filename = filename
        # The default band indices needed to make an pseudo_rgb image, if not available then store None
        self.default_bands = default_bands

# Example
# spectral_array = Spectral_data(max_wavelength=1000.95, min_wavelength=379.027, d_type=numpy.float32,
#                           wavelength_dict=dictionary, samples=1600, lines=1704, interleave='bil',
#                           wavelength_units='nm', array_type="datacube", filename=fname, default_bands={159,253,520})


from plantcv.plantcv.fatal_error import fatal_error
from plantcv.plantcv.print_image import print_image
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.color_palette import color_palette
from plantcv.plantcv.rgb2gray import rgb2gray
from plantcv.plantcv.rgb2gray_hsv import rgb2gray_hsv
from plantcv.plantcv.rgb2gray_lab import rgb2gray_lab
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

__all__ = ['fatal_error', 'print_image', 'plot_image', 'color_palette', 'apply_mask', 'gaussian_blur', 'transform',
           'hyperspectral', 'readimage',
           'readbayer', 'laplace_filter', 'sobel_filter', 'scharr_filter', 'hist_equalization', 'erode',
           'image_add', 'image_subtract', 'dilate', 'watershed', 'rectangle_mask', 'rgb2gray_hsv', 'rgb2gray_lab',
           'rgb2gray', 'median_blur', 'fill', 'invert', 'logical_and', 'logical_or', 'logical_xor',
           'find_objects', 'roi_objects', 'object_composition', 'analyze_object', 'morphology',
           'analyze_bound_horizontal', 'analyze_bound_vertical', 'analyze_color', 'analyze_nir_intensity',
           'print_results', 'flip', 'crop_position_mask', 'get_nir', 'report_size_marker_area',
           'white_balance', 'acute_vertex', 'scale_features', 'landmark_reference_pt_dist', 'outputs',
           'x_axis_pseudolandmarks', 'y_axis_pseudolandmarks', 'cluster_contours', 'visualize',
           'cluster_contour_splitimg', 'rotate', 'shift_img', 'output_mask', 'auto_crop', 'canny_edge_detect',
           'background_subtraction', 'naive_bayes_classifier', 'acute', 'distance_transform', 'params',
           'cluster_contour_mask', 'analyze_thermal_values', 'opening',
           'closing', 'within_frame', 'fill_holes', 'get_kernel', 'Spectral_data', 'crop', 'stdev_filter',
           'spatial_clustering', 'photosynthesis']


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
