# PlantCV classes
import os
import json
import numpy as np
from plantcv.plantcv import fatal_error
import altair as alt
import pandas as pd


# Class definitions
class Params:
    """PlantCV parameters class."""

    def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5, dpi=100, text_size=0.55,
                 text_thickness=2, marker_size=60, color_scale="gist_rainbow", color_sequence="sequential",
                 sample_label="default", saved_color_scale=None, verbose=True):
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
        sample_label      = Sample name prefix. Used in analyze functions. (default: "default")
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
        :param sample_label: str
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
        self.sample_label = sample_label
        self.saved_color_scale = saved_color_scale
        self.verbose = verbose


class Outputs:
    """PlantCV outputs class"""

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
                    if isinstance(val, (list, tuple)):
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

    def plot_dists(self, variable):
        """Plot a distribution of data.

        Keyword arguments/parameters:
        variable      = A local unique identifier of a variable, e.g. a short name,
                        that is a key linking the definitions of variables with observations.
        Returns:
        chart          = Altair chart object
        :param variable: str
        :return chart: altair.vegalite.v4.api.Chart
        """
        alt.data_transformers.disable_max_rows()
        data = {"sample": [], "value": [], "label": []}
        # Iterate over measurement sample groups
        for sample in self.observations:
            # If the measurement variable is present in the sample
            # And the data type is a list
            if variable in self.observations[sample] and "list" in (self.observations[sample][variable]["datatype"]):
                data["value"] = data["value"] + self.observations[sample][variable]["value"]
                data["label"] = data["label"] + self.observations[sample][variable]["label"]
                data["sample"] = data["sample"] + [sample] * len(self.observations[sample][variable]["value"])
        df = pd.DataFrame(data)
        step = 10
        overlap = 10
        chart = alt.Chart(df, height=step, width=500).mark_area(
            interpolate="monotone", fillOpacity=0.8, stroke='lightgray', strokeWidth=0.5
        ).encode(
            alt.X('label:Q').title('Bin labels'),
            alt.Y('value:Q').axis(None).scale(range=[step, -step * overlap])
        ).facet(
            alt.Row('sample:N').title(None).header(labelAngle=0, labelAlign='left', labelOrient="left")
        ).configure_facet(
            spacing=0,
            columns=1
        ).properties(
            bounds='flush'
        ).configure_title(
            anchor="end"
        ).configure_view(
            stroke=None
        ).configure_axis(
            grid=False
        )
        return chart


class Spectral_data:
    """PlantCV Hyperspectral data class"""

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


class PSII_data:
    """PSII data class"""

    def __init__(self):
        self.ojip_dark = None
        self.ojip_light = None
        self.pam_dark = None
        self.pam_light = None
        self.spectral = None
        self.chlorophyll = None
        self.datapath = None
        self.filename = None

    def __repr__(self):
        mvars = []
        for k, v in self.__dict__.items():
            if v is not None:
                mvars.append(k)
        return "PSII variables defined:\n" + '\n'.join(mvars)

    def add_data(self, protocol):
        """
        Input:
            protocol: xr.DataArray with name equivalent to initialized attributes
        """
        self.__dict__[protocol.name] = protocol


class Objects:
    """Class for managing image contours/objects and their hierarchical relationships."""
    def __init__(self, contours: list = None, hierarchy: list = None):
        self.contours = contours
        self.hierarchy = hierarchy
        if contours is None:
            self.contours = []
            self.hierarchy = []

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.contours):
            self.n += 1
            return Objects(contours=[self.contours[self.n-1]], hierarchy=[self.hierarchy[self.n-1]])
        else:
            raise StopIteration

    def append(self, contour, h):
        self.contours.append(contour)
        self.hierarchy.append(h)

    def save(self, filename):
        np.savez(filename, contours=self.contours, hierarchy=self.hierarchy)

    @staticmethod
    def load(filename):
        file = np.load(filename)
        obj = Objects(file['contours'].tolist(), file['hierarchy'])
        return obj
