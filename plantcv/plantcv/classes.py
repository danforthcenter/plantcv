# PlantCV classes
import os
import json
from plantcv.plantcv import fatal_error


class Params:
    """PlantCV parameters class."""

    def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5, dpi=100, text_size=0.55,
                 text_thickness=2, marker_size=60, color_scale="gist_rainbow", color_sequence="sequential",
                 saved_color_scale=None, verbose=True):
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
        verbose           = Whether or not in verbose mode. (default: True)

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
        :param verbose: bool
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
        self.verbose = verbose


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
        datatype     = The type of data to be stored, e.g. 'int', 'float', 'str', 'list', 'bool', etc.
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

        # Create an empty dictionary for the sample if it does not exist
        if sample not in self.observations:
            self.observations[sample] = {}

        # Supported data types
        supported_dtype = ["int", "float", "str", "list", "bool", "tuple", "dict", "NoneType", "numpy.float64"]
        # Supported class types
        class_list = [f"<class '{cls}'>" for cls in supported_dtype]

        # Send an error message if datatype is not supported by json
        if str(type(value)) not in class_list:
            # String list of supported types
            type_list = ', '.join(map(str, supported_dtype))
            fatal_error(f"The Data type {type(value)} is not compatible with JSON! Please use only these: {type_list}!")

        # Save the observation for the sample and variable
        self.observations[sample][variable] = {
            "trait": trait,
            "method": method,
            "scale": scale,
            "datatype": str(datatype),
            "value": value,
            "label": label
        }

    # Method to save observations to a file
    def save_results(self, filename, outformat="json"):
        """Save results to a file.

        Keyword arguments/parameters:
        filename       = Output filename
        outformat      = Output file format ("json" or "csv"). Default = "json"

        :param filename: str
        :param outformat: str
        """
        if outformat.upper() == "JSON":
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    hierarchical_data = json.load(f)
                    hierarchical_data["observations"] = self.observations
            else:
                hierarchical_data = {"metadata": {}, "observations": self.observations}

            with open(filename, mode='w') as f:
                json.dump(hierarchical_data, f)
        elif outformat.upper() == "CSV":
            # Open output CSV file
            csv_table = open(filename, "w")
            # Write the header
            csv_table.write(",".join(map(str, ["sample", "trait", "value", "label"])) + "\n")
            # Iterate over data samples
            for sample in self.observations:
                # Iterate over traits for each sample
                for var in self.observations[sample]:
                    val = self.observations[sample][var]["value"]
                    # If the data type is a list or tuple we need to unpack the data
                    if isinstance(val, list) or isinstance(val, tuple):
                        # Combine each value with its label
                        for value, label in zip(self.observations[sample][var]["value"],
                                                self.observations[sample][var]["label"]):
                            # Skip list of tuple data types
                            if not isinstance(value, tuple):
                                # Save one row per value-label
                                row = [sample, var, value, label]
                                csv_table.write(",".join(map(str, row)) + "\n")
                    # If the data type is Boolean, store as a numeric 1/0 instead of True/False
                    elif isinstance(val, bool):
                        row = [sample,
                               var,
                               int(self.observations[sample][var]["value"]),
                               self.observations[sample][var]["label"]]
                        csv_table.write(",".join(map(str, row)) + "\n")
                    # For all other supported data types, save one row per trait
                    # Assumes no unusual data types are present (possibly a bad assumption)
                    else:
                        row = [sample,
                               var,
                               self.observations[sample][var]["value"],
                               self.observations[sample][var]["label"]
                               ]
                        csv_table.write(",".join(map(str, row)) + "\n")


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
