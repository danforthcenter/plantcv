import os
import tempfile

__all__ = ["metadata_parser", "job_builder", "process_results", "multiprocess", "check_date_range", "Config"]


class Config:
    def __init__(self, input_dir, json, filename_metadata, output_dir=".", tmp_dir=None, processes=1, start_date=1,
                 end_date=None, imgformat="png", delimiter="_", metadata_filters=None,
                 timestampformat='%Y-%m-%d %H:%M:%S.%f', writeimg=False, other_args=None, coprocess=None):
        # Validate input directory
        if not os.path.exists(input_dir):
            raise IOError("Input directory {0} does not exist!".format(input_dir))
        # Validate output directory or create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Create tmp directory
        tmpdir = tempfile.mkdtemp(dir=tmp_dir)
        # Metadata terms dictionary
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
        # Are the user-defined metadata valid?
        for term in filename_metadata:
            if term not in metadata_terms:
                raise ValueError("The term {0} is not a currently supported metadata type.".format(term))
        # Positional metadata structure
        metadata_structure = {}
        for i, field in enumerate(filename_metadata):
            metadata_structure[field] = i

        # Create class methods
        self.input_dir = input_dir
        self.json = json
        self.filename_metadata = filename_metadata
        self.output_dir = output_dir
        self.tmp_dir = tmpdir
        self.processes = processes
        self.start_date = start_date
        self.end_date = end_date
        self.imgformat = imgformat
        self.delimiter = delimiter
        self.metadata_filters = metadata_filters
        self.timestampformat = timestampformat
        self.writeimg = writeimg
        self.other_args = other_args
        self.metadata_terms = metadata_terms
        self.metadata_structure = metadata_structure
        self.coprocess = coprocess


from plantcv.parallel import Config
from plantcv.parallel.parsers import metadata_parser
from plantcv.parallel.parsers import check_date_range
from plantcv.parallel.job_builder import job_builder
from plantcv.parallel.process_results import process_results
from plantcv.parallel.multiprocess import multiprocess
