# define singletons
import os
import json
import datetime
import altair as alt
import pandas as pd
from importlib.metadata import version
from plantcv.plantcv.fatal_error import fatal_error


class Params:
    """PlantCV parameters class."""

    def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5,
                 line_color=(255, 0, 255), dpi=100, text_size=0.55,
                 text_thickness=2, marker_size=60, color_scale="gist_rainbow", color_sequence="sequential",
                 sample_label="default", saved_color_scale=None, verbose=1, unit="pixels", px_height=1, px_width=1):
        """Initialize parameters.

        Parameters
        ----------
        device : int
            Device number. Used to count steps in the pipeline. Default is 0.
        debug : str, optional
            None, print, or plot. Print = save to file, Plot = print to screen. Default is None.
        debug_outdir : str
            Debug images output directory. Default is ".".
        line_thickness : int
            Width of line drawings. Default is 5.
        line_color : tuple
            Color of line annotations. Default is (255, 0, 255).
        dpi : int
            Figure plotting resolution, dots per inch. Default is 100.
        text_size : float
            Size of plotting text. Default is 0.55.
        text_thickness : int
            Thickness of plotting text. Default is 2.
        marker_size : int
            Size of plotting markers. Default is 60.
        color_scale : str
            Name of plotting color scale (matplotlib colormap). Default is "gist_rainbow".
        color_sequence : str
            Build color scales in "sequential" or "random" order. Default is "sequential".
        sample_label : str
            Sample name prefix. Used in analyze functions. Default is "default".
        saved_color_scale : list, optional
            Saved color scale that will be applied next time color_palette is called. Default is None.
        verbose : int
            0:2 representing verbosity level. 0 is least verbose, 2 is most verbose. Default is 1.
        unit : str
            Units of size trait outputs. Default is "pixels".
        px_height : float
            Size scaling information about pixel height. Default is 1.
        px_width : float
            Size scaling information about pixel width. Default is 1.

        """
        self.device = device
        self.debug = debug
        self.debug_outdir = debug_outdir
        self.line_thickness = line_thickness
        self.line_color = line_color
        self.dpi = dpi
        self.text_size = text_size
        self.text_thickness = text_thickness
        self.marker_size = marker_size
        self.color_scale = color_scale
        self.color_sequence = color_sequence
        self.sample_label = sample_label
        self.saved_color_scale = saved_color_scale
        self.verbose = verbose
        self.unit = unit
        self.px_height = px_height
        self.px_width = px_width


class Outputs:
    """PlantCV outputs class"""

    def __init__(self):
        self.measurements = {}
        self.images = []
        self.observations = {}
        self.metadata = {}

        # Add a method to clear measurements
    def clear(self):
        """Clear all measurements"""
        self.measurements = {}
        self.images = []
        self.observations = {}
        self.metadata = {}

    # Method to add observation to outputs
    def add_observation(self, sample, variable, trait, method, scale, datatype, value, label):
        """Add an observation to outputs.

        Parameters
        ----------
        sample : str
            Sample name. Used to distinguish between multiple samples.
        variable : str
            A local unique identifier of a variable, e.g. a short name,
            that is a key linking the definitions of variables with observations.
        trait : str
            A name of the trait mapped to an external ontology; if there is no exact mapping, an informative
            description of the trait.
        method : str
            A name of the measurement method mapped to an external ontology; if there is no exact mapping, an
            informative description of the measurement procedure.
        scale : str
            Units of the measurement or scale in which the observations are expressed; if possible, standard
            units and scales should be used and mapped to existing ontologies; in the case of non-standard
            scale a full explanation should be given.
        datatype : type
            The type of data to be stored, e.g. 'int', 'float', 'str', 'list', 'bool', etc.
        value : any
            The data itself.
        label : str or list
            The label for each value (most useful when the data is a frequency table as in hue,
            or other tables).
        """
        # Create an empty dictionary for the sample if it does not exist
        if sample not in self.observations:
            self.observations[sample] = {}

        # Validate that the data type is supported by JSON
        _ = _validate_data_type(value)

        # Save the observation for the sample and variable
        self.observations[sample][variable] = {
            "trait": trait,
            "method": method,
            "scale": scale,
            "datatype": str(datatype),
            "value": value,
            "label": label
        }

    # Method to add metadata instance to outputs
    def add_metadata(self, term, datatype, value):
        """Add a metadata term and value to outputs.

        Parameters
        ----------
        term : str
            Metadata term/name.
        datatype : type
            The type of data to be stored, e.g. 'int', 'float', 'str', 'list', 'bool', etc.
        value : any
            The data itself.
        """
        # Create an empty dictionary for the sample if it does not exist
        if term not in self.metadata:
            self.metadata[term] = {}

        # Validate that the data type is supported by JSON
        _ = _validate_data_type(value)

        # Save the observation for the sample and variable
        self.metadata[term] = {
            "datatype": str(datatype),
            "value": [value]
        }

    # Method to save observations to a file
    def save_results(self, filename, outformat="json"):
        """Save results to a file.

        Parameters
        ----------
        filename : str
            Output filename.
        outformat : str
            Output file format ("json" or "csv"). Default is "json".
        """
        # Add current date & time to metadata in UTC format
        run_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self.add_metadata(term="run_date", datatype=str, value=run_datetime)
        self.add_metadata(term="plantcv_version", datatype=str, value=version("plantcv"))

        if outformat.upper() == "JSON":
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    hierarchical_data = json.load(f)
                    hierarchical_data["observations"] = self.observations
                    existing_metadata = hierarchical_data["metadata"]
                    for term in self.metadata:
                        save_term = term
                        if term in existing_metadata:
                            save_term = f"{term}_1"
                        hierarchical_data["metadata"][save_term] = self.metadata[term]
            else:
                hierarchical_data = {"metadata": self.metadata, "observations": self.observations}
            with open(filename, mode='w') as f:
                json.dump(hierarchical_data, f)

        elif outformat.upper() == "CSV":
            # Open output CSV file
            with open(filename, "w") as csv_table:
                # Gather any additional metadata
                metadata_key_list = list(self.metadata.keys())
                metadata_val_list = [val["value"] for val in self.metadata.values()]
                # Write the header
                header = metadata_key_list + ["sample", "trait", "value", "label"]
                csv_table.write(",".join(map(str, header)) + "\n")
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
                                    row = metadata_val_list + [sample, var, value, label]
                                    csv_table.write(",".join(map(str, row)) + "\n")
                        # If the data type is Boolean, store as a numeric 1/0 instead of True/False
                        elif isinstance(val, bool):
                            row = metadata_val_list + [sample, var, int(self.observations[sample][var]["value"]),
                                                       self.observations[sample][var]["label"]]
                            csv_table.write(",".join(map(str, row)) + "\n")
                        # For all other supported data types, save one row per trait
                        # Assumes no unusual data types are present (possibly a bad assumption)
                        else:
                            row = metadata_val_list + [sample, var, self.observations[sample][var]["value"],
                                                       self.observations[sample][var]["label"]]
                            csv_table.write(",".join(map(str, row)) + "\n")

    def plot_dists(self, variable):
        """Plot a distribution of data.
        Parameters
        ----------
        variable : str
            A local unique identifier of a variable, e.g. a short name,

        Returns
        -------
        chart : altair.vegalite.v4.api.Chart
            Altair chart object displaying the distribution of the specified variable
            across samples, with faceted rows for each sample and area plot visualization.
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


def _validate_data_type(data):
    """Validate that the data type is supported by JSON.

    Parameters
    ----------
    data : any
        Data to be validated.

    Returns
    -------
    bool
        True if the data type is supported by JSON.

    Raises
    ------
    ValueError
        If the data type is not supported by JSON.
    """
    # Supported data types
    supported_dtype = ["int", "float", "str", "list", "bool", "tuple", "dict", "NoneType", "numpy.float64"]
    # Supported class types
    class_list = [f"<class '{cls}'>" for cls in supported_dtype]

    # Send an error message if datatype is not supported by json
    if str(type(data)) not in class_list:
        # String list of supported types
        type_list = ', '.join(map(str, supported_dtype))
        fatal_error(f"The Data type {type(data)} is not compatible with JSON! Please use only these: {type_list}!")

    return True


params = Params()
outputs = Outputs()
