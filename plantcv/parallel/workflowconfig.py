import os
import sys
import json
import datetime


class WorkflowConfig:
    """PlantCV Parallel Configuration class"""

    def __init__(self):
        object.__setattr__(self, "input_dir", "")
        object.__setattr__(self, "json", "")
        object.__setattr__(self, "filename_metadata", [])
        object.__setattr__(self, "workflow", "")
        object.__setattr__(self, "img_outdir", "./output_images")
        object.__setattr__(self, "include_all_subdirs", True)
        object.__setattr__(self, "tmp_dir", ".")
        object.__setattr__(self, "start_date", None)
        object.__setattr__(self, "end_date", None)
        object.__setattr__(self, "imgformat", "all")
        object.__setattr__(self, "delimiter", "_")
        object.__setattr__(self, "metadata_filters", {})
        object.__setattr__(self, "metadata_regex", {})
        object.__setattr__(self, "timestampformat", "%Y-%m-%dT%H:%M:%S.%fZ")
        object.__setattr__(self, "writeimg", False)
        object.__setattr__(self, "other_args", {})
        object.__setattr__(self, "groupby", ["filepath"])
        object.__setattr__(self, "group_name", "auto")
        object.__setattr__(self, "checkpoint", True)
        object.__setattr__(self, "cleanup", True)
        object.__setattr__(self, "append", False)
        object.__setattr__(self, "verbose", True)
        object.__setattr__(self, "cluster", "LocalCluster")
        object.__setattr__(self, "cluster_config", {
            "n_workers": 1,
            "cores": 1,
            "memory": "1GB",
            "disk": "1GB",
            "log_directory": None,
            "local_directory": None,
            "job_extra_directives": None
        })
        object.__setattr__(self, "metadata_terms", self.metadata_term_definition())
    # set metadata_terms reactively based on filename_metadata
    def __setattr__(self, name, value):
        print(f"setting {name} to {value}")
        object.__setattr__(self, name, value)

    @property
    def metadata_terms(self):
        self._metadata_terms = self.metadata_term_definition()
        return self._metadata_terms

    @metadata_terms.setter
    def metadata_terms(self, new):
        object.__setattr__(self, "_metadata_terms", new)

    # Save configuration to a file
    def save_config(self, config_file):
        """Save configuration to a file.

        Input variables:
        config_file = Filename to write configuration to (text/JSON)

        :param config_file: str
        """
        # Open the file for writing
        with open(config_file, "w") as fp:
            # strip the underscore from _metadata_terms before writing
            content = vars(self)
            content = {k.strip("_"): v for k, v in content.items()}
            # Save the data in JSON format with indentation
            json.dump(obj=content, fp=fp, indent=4)

    # Import a configuration from a file
    def import_config(self, config_file):
        """Import a configuration file.

        Input variables:
        config_file = Configuration file to import

        :param config_file: str
        """
        # Open the file for reading
        with open(config_file, "r") as fp:
            # Import the JSON configuration data
            config = json.load(fp)
            for key, value in config.items():
                if key != "_metadata_terms":
                    object.__setattr__(self, key, value)

    # Validation checks on current config
    def validate_config(self):
        """Validation checks on current configuration."""
        checks = [True]
        # Validate input directory
        if not os.path.exists(self.input_dir):
            print(f"Error: input directory (input_dir) is required and {self.input_dir} does not exist.",
                  file=sys.stderr)
            checks.append(False)
        # Validate JSON file
        if self.json == "":
            print("Error: an output JSON file (json) is required but is currently undefined.", file=sys.stderr)
            checks.append(False)
        # Validate workflow script
        if not os.path.exists(self.workflow):
            print(f"Error: PlantCV workflow script (workflow) is required and {self.workflow} does not exist.",
                  file=sys.stderr)
            checks.append(False)

        # Validate start_date and end_date formats
        if self.start_date is not None:
            try:
                _ = datetime.datetime.strptime(
                    self.start_date, self.timestampformat)
            except ValueError as e:
                print(str(e) + '\n  --> Please specify the start_date according to the timestampformat  <--\n')
                checks.append(False)
        if self.end_date is not None:
            try:
                _ = datetime.datetime.strptime(
                    self.end_date, self.timestampformat)
            except ValueError as e:
                print(str(
                    e) + '\n  --> Please specify the end_date according to the timestampformat  <--\n')
                checks.append(False)

        # Validate the cluster type
        valid_clusters = ["HTCondorCluster", "LocalCluster", "LSFCluster", "MoabCluster", "OARCluster", "PBSCluster",
                          "SGECluster", "SLURMCluster"]
        if self.cluster not in valid_clusters:
            print(f"Error: the cluster type {self.cluster} is not a supported cluster provider. "
                  f"Valid clusters include: {', '.join(map(str, valid_clusters))}."
                  )
        return all(checks)

    # Specify metadata terms
    def metadata_term_definition(self):
        """Add dictionary of metadata terms"""
        metadata_terms = {
            # Camera settings
            "camera": {
                "label": "camera identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "imgtype": {
                "label": "image type",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "zoom": {
                "label": "camera zoom setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "exposure": {
                "label": "camera exposure setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "gain": {
                "label": "camera gain setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "frame": {
                "label": "image series frame identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "rotation": {
                "label": "sample rotation in degrees",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "lifter": {
                "label": "imaging platform height setting",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            # Date-Time
            "timestamp": {
                "label": "datetime of image",
                "datatype": "<class 'datetime.datetime'>",
                "value": None
            },
            # Sample attributes
            "id": {
                "label": "image identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "barcode": {
                "label": "plant barcode identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "treatment": {
                "label": "treatment identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            "cartag": {
                "label": "plant carrier identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            # Experiment attributes
            "measurementlabel": {
                "label": "experiment identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            },
            # Other
            "other": {
                "label": "other identifier",
                "datatype": "<class 'str'>",
                "value": "none"
            }
        }
        # add any other metadata terms as strings
        for k in [fm for fm in self.filename_metadata if fm not in metadata_terms]:
            metadata_terms[k] = {
                "label": f"{k}",
                "datatype": "<class 'str'>",
                "value": "none"
            }

        return metadata_terms


def _config_attr_lookup(attr, val):
    """Lookup attributes for a WorkflowConfig or jupyterconfig object

    Parameters
    ----------
    attr     = str, name of an attribute to set.
    
    Returns
    -------
    control  = dict, dictionary of print message and expected dtype.

    """
    config_control = {
        "input_dir": [f"Images will be read from {val}", str],
        "json": [f"output will be written to {val}", str],
        "filename_metadata": [f"Filenames will be parsed into {', '.join(val)}", str],
        "workflow": [f"Will run {val} python script in each job", str],
        "img_outdir": [f"Output images will be written to {val}", str],
        "include_all_subdirs": [f"Will {['Not', ''][int(val)]} include images from subdirectories", bool],
        "tmp_dir": [f"_PCV_PARALLEL_CHECKPOINT_/{val}", str],
        "start_date": [f"Will only include images from after {val}", str],
        "end_date": [f"Will only include images from after {val}", str],
        "imgformat": [f"Will include {val} images", str],
        "delimiter": [f"Splitting file basenames by {val}", str],
        "metadata_filters": [f"Metadata will only be kept that matches {', '.join(val.keys())}", dict],
        "metadata_regex": [f"message for input_dir", str],
        "timestampformat": [f"message for input_dir", str],
        "writeimg": [f"message for input_dir", str],
        "other_args": [f"message for input_dir", str],
        "groupby": [f"message for input_dir", str],
        "group_name": [f"message for input_dir", str],
        "checkpoint": [f"message for input_dir", str],
        "cleanup": [f"message for input_dir", str],
        "append": [f"message for input_dir", str],
        "verbose": [f"message for input_dir", str],
        "cluster": [f"message for input_dir", str],
        "cluster_config": [f"message for input_dir", str],
        "metadata_terms": [f"message for input_dir", str]
    }
    return config_control[attr]
