import os
import sys
import json
import datetime


class WorkflowConfig:
    """PlantCV Parallel Configuration class"""

    def __init__(self):
        self.input_dir = ""
        self.json = ""
        self.filename_metadata = []
        self.workflow = ""
        self.img_outdir = "./output_images"
        self.include_all_subdirs = True
        self.tmp_dir = "."
        self.start_date = None
        self.end_date = None
        self.imgformat = "all"
        self.delimiter = "_"
        self.metadata_filters = {}
        self.metadata_regex = {}
        self.timestampformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.writeimg = False
        self.other_args = {}
        self.groupby = ["filepath"]
        self.group_name = "auto"
        self.cleanup = True
        self.append = False
        self.cluster = "LocalCluster"
        self.cluster_config = {
            "n_workers": 1,
            "cores": 1,
            "memory": "1GB",
            "disk": "1GB",
            "log_directory": None,
            "local_directory": None,
            "job_extra_directives": None
        }
        self.metadata_terms = self.metadata_term_definition()
    # set metadata_terms reactively based on filename_metadata

    @property
    def metadata_terms(self):
        self._metadata_terms = self.metadata_term_definition()
        return self._metadata_terms

    @metadata_terms.setter
    def metadata_terms(self, new):
        self._metadata_terms = new

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
                    setattr(self, key, value)

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
