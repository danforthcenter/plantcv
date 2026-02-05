import os
import sys
import json
import datetime


class WorkflowConfig:
    """PlantCV Parallel Configuration class"""

    def __init__(self):
        object.__setattr__(self, "input_dir", "")
        object.__setattr__(self, "results", "")
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
        self._metadata_terms = self.metadata_term_definition()

    # set metadata_terms reactively based on filename_metadata
    def __setattr__(self, name, value):
        _config_attr_lookup(self, name, value)
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
        # Validate JSON results file
        if self.results == "":
            print("Error: an output JSON file (results) is required but is currently undefined.", file=sys.stderr)
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

        # Validate the cluster configuration
        if (
                self.cluster_config["n_workers"] * self.cluster_config["cores"] > os.cpu_count()
                and self.cluster == "LocalCluster"
        ):
            print(f"Error: n_workers is {self.cluster_config['n_workers']} and "
                  f"cores is {self.cluster_config['cores']} which requires "
                  f"more than the {os.cpu_count()} available cores.")
            checks.append(False)

        return all(checks)

    # Specify metadata terms
    def metadata_term_definition(self):
        """Add dictionary of metadata terms"""
        metadata_terms = {
            "timestamp": {
                "label": "datetime of image",
                "datatype": "<class 'datetime.datetime'>",
                "value": None
            }
        }
        default_metadata_terms = {
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
        for k in [fm for fm in self.filename_metadata if fm not in default_metadata_terms]:
            metadata_terms[k] = {
                "label": f"{k}",
                "datatype": "<class 'str'>",
                "value": "none"
            }
        # add default terms with their formatting
        for k in [fm for fm in self.filename_metadata if fm in default_metadata_terms]:
            metadata_terms[k] = default_metadata_terms[k]

        return metadata_terms


def _validate_set_attr(val, sentence, expect_type):
    """Validate attributes before setting them in a WorkflowConfig or jupyterconfig object

    Parameters
    ----------
    val         = type flexible, value to assign to configuration attribute.
    sentence    = str, unformatted string to mention what the change will do.
    expect_type = type, expected type for val.

    Returns
    -------
    out         = minimal message about what the change does.

    Raises
    ------
    ValueError if incompatible type between input val and expected type for attribute.

    """
    if not isinstance(val, expect_type):
        raise ValueError("Expected " + expect_type.__name__ + ", got " + type(val).__name__)
    if isinstance(val, list):
        form = ', '.join(val)
    elif isinstance(val, bool):
        form = ['not ', ''][int(val)]
    elif isinstance(val, dict):
        form = ", ".join(val.keys())
    else:
        form = val
    # parse form into sentence string
    out = sentence.format(form)
    return out


def _config_attr_lookup(config, attr, val):
    """Lookup attributes for a WorkflowConfig or jupyterconfig object

    Parameters
    ----------
    config   = plantcv.parallel.workflowconfig or jupyterconfig, configuration file
    attr     = str, name of an attribute to set.
    val      = type flexible, value to assign to configuration attribute.

    Returns
    -------
    message  = minimal message about what the change does.

    Raises
    ------
    ValueError if incompatible type between input val and expected type for attribute.

    """
    # do not do this for hidden attributes
    if attr[0] != "_" and attr != "chkpt_start_dir":
        # for all other attributes, get their data from list
        config_control = {
            "input_dir": ["Images will be read from {}", str],
            "filename_metadata": ["Filenames will be parsed into {}", list],
            "workflow": ["Will run {} python script in each job", str],
            "img_outdir": ["Output images will be written to {}", str],
            "include_all_subdirs": ["Will {} include images from subdirectories", bool],
            "tmp_dir": ["Writing intermediate files to {}", str],
            "start_date": ["Will only include images from after {}", str],
            "end_date": ["Will only include images from before {}", str],
            "imgformat": ["Will include {} images", (str, list)],
            "delimiter": ["Splitting file basenames by '{}'", str],
            "metadata_filters": ["Metadata will only be kept that matches {}", dict],
            "metadata_regex": ["Will filter for file path matches to regex pattern(s)", dict],
            "timestampformat": ["Using timestamp format {} to parse datetimes", str],
            "writeimg": ["Currently 'writeimg' does not control anything", bool],
            "other_args": ["Adding additional arguments", dict],
            "groupby": ["Grouping images by {}, matches will enter one workflow", list],
            "group_name": ["Naming each workflow's images by {}", str],
            "checkpoint": ["Run will {}be checkpointed", bool],
            "cleanup": ["Run will {}be cleaned up", bool],
            "append": ["Results will {}be appended", bool],
            "verbose": ["Run will {}be verbose", bool],
            "cluster": ["Using {} cluster type", str],
            "cluster_config": ["Configuring cluster options", dict],
            "metadata_terms": ["Setting metadata term options (overriding defaults)", dict],
            "_notebook": ["HIDDEN Changing path to jupyter notebook (normally set to active notebook)", str],
            "_workflow": ["HIDDEN Changing script path to {} (normally set to auto-generated script)", str],
            "_config": ["HIDDEN Changing path to save config to {} (normally set to share notebook/script name)", str],
            "_analysis_script": ["HIDDEN This should not generally be changed. Setting to {}ready.", bool],
            "_results": ["HIDDEN output will be written to {}", str],
            "chkpt_start_dir": ["HIDDEN checkpoint data will be read from {}", str],
            "notebook": ["Changing path to jupyter notebook (normally set to active notebook)", str],
            "config": ["Changing path to save config to {} (normally set to share notebook/script name)", str],
            "analysis_script": ["This should not generally be changed. Setting to {}ready.", bool],
            "results": ["output will be written to {}", str]
        }
        # check the proposed new attribute and make message about it
        message = _validate_set_attr(val=val, sentence=config_control[attr][0],
                                     expect_type=config_control[attr][1])
        if config.verbose:
            print(message)
