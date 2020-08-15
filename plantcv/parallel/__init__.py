import os
import sys
import json
from copy import deepcopy
from plantcv.parallel.parsers import metadata_parser
from plantcv.parallel.parsers import check_date_range
from plantcv.parallel.job_builder import job_builder
from plantcv.parallel.process_results import process_results
from plantcv.parallel.multiprocess import multiprocess

__all__ = ["metadata_parser", "job_builder", "process_results", "multiprocess", "check_date_range", "WorkflowConfig"]


class WorkflowConfig:
    def __init__(self):
        # Private variable _template stores the unmodified configuration template
        self._template = {
            "input_dir": "",
            "json": "",
            "filename_metadata": [],
            "workflow": "",
            "output_dir": "./output_images",
            "tmp_dir": None,
            "processes": 1,
            "start_date": 1,
            "end_date": None,
            "imgformat": "png",
            "delimiter": "_",
            "metadata_filters": {},
            "timestampformat": "%Y-%m-%d %H:%M:%S.%f",
            "writeimg": False,
            "other_args": None,
            "coprocess": None,
            "metadata_terms": {
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
                "plantbarcode": {
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
        }
        # Initialize the config property with the template
        self.config = deepcopy(self._template)

    # Create config template file from the template property
    def create_template(self, config_file):
        """Create configuration template file.

        Input variables:
        config_file = Configuration filename to write template to (text/JSON)

        :param config_file: str
        """
        # Open the file for writing
        with open(config_file, "w") as f:
            # Save the data in JSON format with indentation
            json.dump(obj=self._template, fp=f, indent=4)

    # Class method for importing configs from a file
    def import_config_file(self, config_file):
        """Import configuration from a file.

        Input variables:
        config_file = Configuration file to import from.

        :param config_file: str
        """
        # Open the file for reading
        with open(config_file, "r") as f:
            # Import the JSON configuration to the config property
            self.config = json.load(f)

    # Validation checks on current config
    def validate_config(self):
        """Validation checks on current configuration.
        """
        checks = [True]
        # Validate the configuration is complete
        for prop in self._template:
            if prop not in self.config:
                print("Error: configuration property {0} not found in config, please use a valid template".format(
                    prop))
                checks.append(False)
        # Validate input directory
        if not os.path.exists(self.config.get("input_dir")):
            print("Error: input directory (input_dir) is required and {0} does not exist.".format(
                self.config.get("input_dir")), file=sys.stderr)
            checks.append(False)
        # Validate JSON file
        if self.config.get("json") == "":
            print("Error: an output JSON file (json) is required but is currently undefined.", file=sys.stderr)
            checks.append(False)
        # Validate filename metadata
        if len(self.config.get("filename_metadata")) == 0:
            print("Error: a list of filename metadata terms (filename_metadata) is required but is currently undefined",
                  file=sys.stderr)
            checks.append(False)
        else:
            # Are the user-defined metadata valid?
            for term in self.config.get("filename_metadata"):
                if term not in self.config.get("metadata_terms"):
                    print("Error: the term {0} in filename_metadata is not a currently supported metadata type.".format(
                        term))
                    checks.append(False)
        # Validate workflow script
        if not os.path.exists(self.config.get("workflow")):
            print("Error: PlantCV workflow script (workflow) is required and {0} does not exist.".format(
                self.config.get("workflow")), file=sys.stderr)
            checks.append(False)
        return all(checks)
