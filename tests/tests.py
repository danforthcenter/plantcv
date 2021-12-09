#!/usr/bin/env python

import pytest
import os
import shutil
import json
import numpy as np
import cv2
import sys
import pandas as pd
from plotnine import ggplot
from plantcv import plantcv as pcv
import plantcv.learn
import plantcv.parallel
import plantcv.utils
# Import matplotlib and use a null Template to block plotting to screen
# This will let us test debug = "plot"
import matplotlib
import matplotlib.pyplot as plt
import dask
from dask.distributed import Client
from skimage import img_as_ubyte

PARALLEL_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parallel_data")
TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
TEST_IMG_DIR = "images"
TEST_IMG_DIR2 = "images_w_date"
TEST_SNAPSHOT_DIR = "snapshots"
TEST_PIPELINE = os.path.join(PARALLEL_TEST_DATA, "plantcv-script.py")
META_FIELDS = {"imgtype": 0, "camera": 1, "frame": 2, "zoom": 3, "lifter": 4, "gain": 5, "exposure": 6, "id": 7}
VALID_META = {
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

METADATA_COPROCESS = {
    'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
        'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
        'camera': 'SV',
        'imgtype': 'VIS',
        'zoom': 'z1',
        'exposure': 'e82',
        'gain': 'g0',
        'frame': '0',
        'lifter': 'h1',
        'timestamp': '2014-10-22 17:49:35.187',
        'id': '117770',
        'plantbarcode': 'Ca031AA010564',
        'treatment': 'none',
        'cartag': '2143',
        'measurementlabel': 'C002ch_092214_biomass',
        'other': 'none',
        'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
    },
    'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
        'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
        'camera': 'SV',
        'imgtype': 'NIR',
        'zoom': 'z1',
        'exposure': 'e65',
        'gain': 'g0',
        'frame': '0',
        'lifter': 'h1',
        'timestamp': '2014-10-22 17:49:35.187',
        'id': '117779',
        'plantbarcode': 'Ca031AA010564',
        'treatment': 'none',
        'cartag': '2143',
        'measurementlabel': 'C002ch_092214_biomass',
        'other': 'none'
    }
}
METADATA_VIS_ONLY = {
    'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
        'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
        'camera': 'SV',
        'imgtype': 'VIS',
        'zoom': 'z1',
        'exposure': 'e82',
        'gain': 'g0',
        'frame': '0',
        'lifter': 'h1',
        'timestamp': '2014-10-22 17:49:35.187',
        'id': '117770',
        'plantbarcode': 'Ca031AA010564',
        'treatment': 'none',
        'cartag': '2143',
        'measurementlabel': 'C002ch_092214_biomass',
        'other': 'none'
    }
}
METADATA_NIR_ONLY = {
    'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
        'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
        'camera': 'SV',
        'imgtype': 'NIR',
        'zoom': 'z1',
        'exposure': 'e65',
        'gain': 'g0',
        'frame': '0',
        'lifter': 'h1',
        'timestamp': '2014-10-22 17:49:35.187',
        'id': '117779',
        'plantbarcode': 'Ca031AA010564',
        'treatment': 'none',
        'cartag': '2143',
        'measurementlabel': 'C002ch_092214_biomass',
        'other': 'none'
    }
}
# Set the temp directory for dask
dask.config.set(temporary_directory=TEST_TMPDIR)


# ##########################
# Tests setup function
# ##########################
def setup_function():
    if not os.path.exists(TEST_TMPDIR):
        os.mkdir(TEST_TMPDIR)


# ##############################
# Tests for the parallel subpackage
# ##############################
def test_plantcv_parallel_workflowconfig_save_config_file():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_save_config_file")
    os.mkdir(cache_dir)
    # Define output path/filename
    template_file = os.path.join(cache_dir, "config.json")
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Save template file
    config.save_config(config_file=template_file)

    assert os.path.exists(template_file)


def test_plantcv_parallel_workflowconfig_import_config_file():
    # Define input path/filename
    config_file = os.path.join(PARALLEL_TEST_DATA, "workflow_config_template.json")
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # import config file
    config.import_config(config_file=config_file)

    assert config.cluster == "LocalCluster"


def test_plantcv_parallel_workflowconfig_validate_config():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_validate_config")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set valid values in config
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, "images")
    config.json = os.path.join(cache_dir, "valid_config.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.img_outdir = cache_dir
    # Validate config
    assert config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_startdate():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_invalid_startdate")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set valid values in config
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, "images")
    config.json = os.path.join(cache_dir, "valid_config.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.img_outdir = cache_dir
    config.start_date = "2020-05-10"
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_enddate():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_invalid_enddate")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set valid values in config
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, "images")
    config.json = os.path.join(cache_dir, "valid_config.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.img_outdir = cache_dir
    config.end_date = "2020-05-10"
    config.timestampformat = "%Y%m%d"
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_metadata_terms():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_invalid_metadata_terms")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set an incorrect metadata term
    config.filename_metadata.append("invalid")
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_filename_metadata():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_invalid_filename_metadata")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Do not set required filename_metadata
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_workflowconfig_invalid_cluster():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_workflowconfig_invalid_cluster")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    # Set invalid values in config
    # input_dir and json are not defined by default, but are required
    # Set invalid cluster type
    config.cluster = "MyCluster"
    # Validate config
    assert not config.validate_config()


def test_plantcv_parallel_metadata_parser_snapshots():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_snapshots", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == METADATA_VIS_ONLY


def test_plantcv_parallel_metadata_parser_snapshots_coimg():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_snapshots_coimg", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "FAKE"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == METADATA_VIS_ONLY


def test_plantcv_parallel_metadata_parser_images():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014"
    config.end_date = "2014"
    config.timestampformat = '%Y'  # no date in filename so check date range and date_format are ignored
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'images', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': None,
            'id': '117770',
            'plantbarcode': 'none',
            'treatment': 'none',
            'cartag': 'none',
            'measurementlabel': 'none',
            'other': 'none'}
    }
    assert meta == expected
    config.include_all_subdirs = False
    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == expected


def test_plantcv_parallel_metadata_parser_multivalue_filter():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": ["VIS", "NIR"]}
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR, 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': None,
            'id': '117770',
            'plantbarcode': 'none',
            'treatment': 'none',
            'cartag': 'none',
            'measurementlabel': 'none',
            'other': 'none'
        },
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR, 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'SV',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': None,
            'id': '117779',
            'plantbarcode': 'none',
            'treatment': 'none',
            'cartag': 'none',
            'measurementlabel': 'none',
            'other': 'none'
        }
    }
    assert meta == expected


def test_plantcv_parallel_metadata_parser_multivalue_filter_nomatch():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": ["VIS", "PSII"]}
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR, 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': None,
            'id': '117770',
            'plantbarcode': 'none',
            'treatment': 'none',
            'cartag': 'none',
            'measurementlabel': 'none',
            'other': 'none'
        }
    }
    assert meta == expected


def test_plantcv_parallel_metadata_parser_regex():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.delimiter = r'(VIS)_(SV)_(\d+)_(z1)_(h1)_(g0)_(e82)_(\d+)'

    meta = plantcv.parallel.metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'images', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': None,
            'id': '117770',
            'plantbarcode': 'none',
            'treatment': 'none',
            'cartag': 'none',
            'measurementlabel': 'none',
            'other': 'none'}
    }
    assert meta == expected


def test_plantcv_parallel_metadata_parser_images_outside_daterange():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR2)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images_outside_daterange",
                               "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "timestamp"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "NIR"}
    config.start_date = "1970-01-01 00_00_00"
    config.end_date = "1970-01-01 00_00_00"
    config.timestampformat = "%Y-%m-%d %H_%M_%S"
    config.imgformat = "jpg"
    config.delimiter = r"(NIR)_(SV)_(\d)_(z1)_(h1)_(g0)_(e65)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == {}


def test_plantcv_parallel_metadata_parser_no_default_dates():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_no_default_dates", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV", "id": "117770"}
    config.start_date = None
    config.end_date = None
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == METADATA_VIS_ONLY


def test_plantcv_parallel_workflowconfig_subdaily_timestampformat():
    '''
    timestampformats with only hours and smaller units of time were failing if the script was run earlier in the day than the images were taken. this was fixed by setting end_date to 23-59-59 if we don't detect the year-month-day
    '''
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_IMG_DIR2)
    config.json = os.path.join(
        TEST_IMG_DIR2, "test_plantcv_parallel_metadata_parser_subdaily_timestampformat", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "timestamp"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "NIR", "camera": "SV"}
    config.start_date = None
    config.end_date = None
    config.timestampformat = "%H_%M_%S"
    config.imgformat = "jpg"

    config.delimiter = r"(NIR)_(SV)_(\d)_(z1)_(h1)_(g0)_(e65)_(\d{2}_\d{2}_\d{2})"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == {
        'NIR_SV_0_z1_h1_g0_e65_23_59_59.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'images_w_date', 'NIR_SV_0_z1_h1_g0_e65_23_59_59.jpg'),
            'imgtype': 'NIR',
            'camera': 'SV',
            'frame': '0',
            'zoom': 'z1',
            'lifter': 'h1',
            'gain': 'g0',
            'exposure': 'e65',
            'timestamp': '23_59_59',
            'measurementlabel': 'none',
            'cartag': 'none',
            'id': 'none',
            'treatment': 'none',
            'plantbarcode': 'none',
            'other': 'none'
        }
    }


def test_plantcv_parallel_check_date_range_wrongdateformat():
    start_date = 10
    end_date = 10
    img_time = '2010-10-10'

    with pytest.raises(SystemExit, match=r'does not match format'):
        date_format = '%Y%m%d'
        _ = plantcv.parallel.check_date_range(
            start_date, end_date, img_time, date_format)


def test_plantcv_parallel_metadata_parser_snapshot_outside_daterange():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_snapshot_outside_daterange",
                               "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = plantcv.parallel.metadata_parser(config=config)

    assert meta == {}


def test_plantcv_parallel_metadata_parser_fail_images():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_fail_images", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"cartag": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = plantcv.parallel.metadata_parser(config=config)
    assert meta == METADATA_NIR_ONLY


def test_plantcv_parallel_metadata_parser_images_with_frame():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images_with_frame", "output.json")
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = plantcv.parallel.metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117770',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none',
            'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
        },
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'SV',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117779',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }


def test_plantcv_parallel_metadata_parser_images_no_frame():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images_no_frame",
                               "output.json")
    config.filename_metadata = ["imgtype", "camera", "X", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = plantcv.parallel.metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'SV',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': 'none',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117770',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none',
            'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
        },
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'SV',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': 'none',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117779',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }


def test_plantcv_parallel_metadata_parser_images_no_camera():
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_images_no_frame", "output.json")
    config.filename_metadata = ["imgtype", "X", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = plantcv.parallel.metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
            'camera': 'none',
            'imgtype': 'VIS',
            'zoom': 'z1',
            'exposure': 'e82',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117770',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none',
            'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
        },
        'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
            'path': os.path.join(PARALLEL_TEST_DATA, 'snapshots', 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
            'camera': 'none',
            'imgtype': 'NIR',
            'zoom': 'z1',
            'exposure': 'e65',
            'gain': 'g0',
            'frame': '0',
            'lifter': 'h1',
            'timestamp': '2014-10-22 17:49:35.187',
            'id': '117779',
            'plantbarcode': 'Ca031AA010564',
            'treatment': 'none',
            'cartag': '2143',
            'measurementlabel': 'C002ch_092214_biomass',
            'other': 'none'
        }
    }


def test_plantcv_parallel_job_builder_single_image():
    # Create cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_job_builder_single_image")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(cache_dir, "output.json")
    config.tmp_dir = cache_dir
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.img_outdir = cache_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True

    jobs = plantcv.parallel.job_builder(meta=METADATA_VIS_ONLY, config=config)

    image_name = list(METADATA_VIS_ONLY.keys())[0]
    result_file = os.path.join(cache_dir, image_name + '.txt')

    expected = ['python', TEST_PIPELINE, '--image', METADATA_VIS_ONLY[image_name]['path'], '--outdir',
                cache_dir, '--result', result_file, '--writeimg', '--other', 'on']

    if len(expected) != len(jobs[0]):
        assert False
    else:
        assert all([i == j] for i, j in zip(jobs[0], expected))


def test_plantcv_parallel_job_builder_coprocess():
    # Create cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_job_builder_coprocess")
    os.mkdir(cache_dir)
    # Create config instance
    config = plantcv.parallel.WorkflowConfig()
    config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    config.json = os.path.join(cache_dir, "output.json")
    config.tmp_dir = cache_dir
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = TEST_PIPELINE
    config.img_outdir = cache_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True
    config.coprocess = "NIR"

    jobs = plantcv.parallel.job_builder(meta=METADATA_COPROCESS, config=config)

    img_names = list(METADATA_COPROCESS.keys())
    vis_name = img_names[0]
    vis_path = METADATA_COPROCESS[vis_name]['path']
    result_file = os.path.join(cache_dir, vis_name + '.txt')
    nir_name = img_names[1]
    coresult_file = os.path.join(cache_dir, nir_name + '.txt')

    expected = ['python', TEST_PIPELINE, '--image', vis_path, '--outdir', cache_dir, '--result', result_file,
                '--coresult', coresult_file, '--writeimg', '--other', 'on']

    if len(expected) != len(jobs[0]):
        assert False
    else:
        assert all([i == j] for i, j in zip(jobs[0], expected))


def test_plantcv_parallel_multiprocess_create_dask_cluster_local():
    client = plantcv.parallel.create_dask_cluster(cluster="LocalCluster", cluster_config={})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_plantcv_parallel_multiprocess_create_dask_cluster():
    client = plantcv.parallel.create_dask_cluster(cluster="HTCondorCluster", cluster_config={"cores": 1,
                                                                                             "memory": "1GB",
                                                                                             "disk": "1GB"})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_plantcv_parallel_multiprocess_create_dask_cluster_invalid_cluster():
    with pytest.raises(ValueError):
        _ = plantcv.parallel.create_dask_cluster(cluster="Skynet", cluster_config={})


def test_plantcv_parallel_convert_datetime_to_unixtime():
    unix_time = plantcv.parallel.convert_datetime_to_unixtime(timestamp_str="1970-01-01", date_format="%Y-%m-%d")
    assert unix_time == 0


def test_plantcv_parallel_convert_datetime_to_unixtime_bad_strptime():
    with pytest.raises(SystemExit):
        _ = plantcv.parallel.convert_datetime_to_unixtime(timestamp_str="1970-01-01", date_format="%Y-%m")


def test_plantcv_parallel_multiprocess():
    image_name = list(METADATA_VIS_ONLY.keys())[0]
    image_path = os.path.join(METADATA_VIS_ONLY[image_name]['path'], image_name)
    result_file = os.path.join(TEST_TMPDIR, image_name + '.txt')
    jobs = [['python', TEST_PIPELINE, '--image', image_path, '--outdir', TEST_TMPDIR, '--result', result_file,
             '--writeimg', '--other', 'on']]
    # Create a dask LocalCluster client
    client = Client(n_workers=1)
    plantcv.parallel.multiprocess(jobs, client=client)
    assert os.path.exists(result_file)


def test_plantcv_parallel_process_results():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_process_results")
    os.mkdir(cache_dir)
    plantcv.parallel.process_results(job_dir=os.path.join(PARALLEL_TEST_DATA, "results"),
                                     json_file=os.path.join(cache_dir, 'appended_results.json'))
    plantcv.parallel.process_results(job_dir=os.path.join(PARALLEL_TEST_DATA, "results"),
                                     json_file=os.path.join(cache_dir, 'appended_results.json'))
    # Assert that the output JSON file matches the expected output JSON file
    result_file = open(os.path.join(cache_dir, "appended_results.json"), "r")
    results = json.load(result_file)
    result_file.close()
    expected_file = open(os.path.join(PARALLEL_TEST_DATA, "appended_results.json"))
    expected = json.load(expected_file)
    expected_file.close()
    assert results == expected


def test_plantcv_parallel_process_results_new_output():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_process_results_new_output")
    os.mkdir(cache_dir)
    plantcv.parallel.process_results(job_dir=os.path.join(PARALLEL_TEST_DATA, "results"),
                                     json_file=os.path.join(cache_dir, 'new_result.json'))
    # Assert output matches expected values
    result_file = open(os.path.join(cache_dir, "new_result.json"), "r")
    results = json.load(result_file)
    result_file.close()
    expected_file = open(os.path.join(PARALLEL_TEST_DATA, "new_result.json"))
    expected = json.load(expected_file)
    expected_file.close()
    assert results == expected


def test_plantcv_parallel_process_results_valid_json():
    # Test when the file is a valid json file but doesn't contain expected keys
    with pytest.raises(RuntimeError):
        plantcv.parallel.process_results(job_dir=os.path.join(PARALLEL_TEST_DATA, "results"),
                                         json_file=os.path.join(PARALLEL_TEST_DATA, "valid.json"))


def test_plantcv_parallel_process_results_invalid_json():
    # Create a test tmp directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_process_results_invalid_json")
    os.mkdir(cache_dir)
    # Move the test data to the tmp directory
    shutil.copytree(os.path.join(PARALLEL_TEST_DATA, "bad_results"), os.path.join(cache_dir, "bad_results"))
    with pytest.raises(RuntimeError):
        plantcv.parallel.process_results(job_dir=os.path.join(cache_dir, "bad_results"),
                                         json_file=os.path.join(cache_dir, "bad_results", "invalid.txt"))


# ####################################################################################################################
# ########################################### PLANTCV MAIN PACKAGE ###################################################
matplotlib.use('Template')

TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HYPERSPECTRAL_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hyperspectral_data")
HYPERSPECTRAL_DATA = "darkReference"
HYPERSPECTRAL_WHITE = "darkReference_whiteReference"
HYPERSPECTRAL_DARK = "darkReference_darkReference"
HYPERSPECTRAL_HDR = "darkReference.hdr"
HYPERSPECTRAL_MASK = "darkReference_mask.png"
HYPERSPECTRAL_DATA_NO_DEFAULT = "darkReference2"
HYPERSPECTRAL_HDR_NO_DEFAULT = "darkReference2.hdr"
HYPERSPECTRAL_DATA_APPROX_PSEUDO = "darkReference3"
HYPERSPECTRAL_HDR_APPROX_PSEUDO = "darkReference3.hdr"
HYPERSPECTRAL_DATA_BAD_INTERLEAVE = "darkReference4"
HYPERSPECTRAL_HDR_BAD_INTERLEAVE = "darkReference4.hdr"
HYPERSPECTRAL_HDR_SMALL_RANGE = {'description': '{[HEADWALL Hyperspec III]}', 'samples': '800', 'lines': '1',
                                 'bands': '978', 'header offset': '0', 'file type': 'ENVI Standard',
                                 'interleave': 'bil', 'sensor type': 'Unknown', 'byte order': '0',
                                 'default bands': '159,253,520', 'wavelength units': 'nm',
                                 'wavelength': ['379.027', '379.663', '380.3', '380.936', '381.573', '382.209']}
FLUOR_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photosynthesis_data")
FLUOR_IMG = "PSII_PSD_supopt_temp_btx623_22_rep1.DAT"
TEST_COLOR_DIM = (2056, 2454, 3)
TEST_GRAY_DIM = (2056, 2454)
TEST_BINARY_DIM = TEST_GRAY_DIM
TEST_INPUT_COLOR = "input_color_img.jpg"
TEST_INPUT_GRAY = "input_gray_img.jpg"
TEST_INPUT_GRAY_SMALL = "input_gray_img_small.jpg"
TEST_INPUT_BINARY = "input_binary_img.png"
# Image from http://www.libpng.org/pub/png/png-OwlAlpha.html
# This image may be used, edited and reproduced freely.
TEST_INPUT_RGBA = "input_rgba.png"
TEST_INPUT_BAYER = "bayer_img.png"
TEST_INPUT_ROI_CONTOUR = "input_roi_contour.npz"
TEST_INPUT_ROI_HIERARCHY = "input_roi_hierarchy.npz"
TEST_INPUT_CONTOURS = "input_contours.npz"
TEST_INPUT_OBJECT_CONTOURS = "input_object_contours.npz"
TEST_INPUT_OBJECT_HIERARCHY = "input_object_hierarchy.npz"
TEST_VIS = "VIS_SV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR = "NIR_SV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_VIS_TV = "VIS_TV_0_z300_h1_g0_e85_v500_93054.png"
TEST_NIR_TV = "NIR_TV_0_z300_h1_g0_e15000_v500_93059.png"
TEST_INPUT_MASK = "input_mask_binary.png"
TEST_INPUT_MASK_OOB = "mask_outbounds.png"
TEST_INPUT_MASK_RESIZE = "input_mask_resize.png"
TEST_INPUT_NIR_MASK = "input_nir.png"
TEST_INPUT_FDARK = "FLUO_TV_dark.png"
TEST_INPUT_FDARK_LARGE = "FLUO_TV_DARK_large"
TEST_INPUT_FMIN = "FLUO_TV_min.png"
TEST_INPUT_FMAX = "FLUO_TV_max.png"
TEST_INPUT_FMASK = "FLUO_TV_MASK.png"
TEST_INPUT_GREENMAG = "input_green-magenta.jpg"
TEST_INPUT_MULTI = "multi_ori_image.jpg"
TEST_INPUT_MULTI_MASK = "multi_ori_mask.jpg"
TEST_INPUT_MULTI_OBJECT = "roi_objects.npz"
TEST_INPUT_MULTI_CONTOUR = "multi_contours.npz"
TEST_INPUT_ClUSTER_CONTOUR = "clusters_i.npz"
TEST_INPUT_MULTI_HIERARCHY = "multi_hierarchy.npz"
TEST_INPUT_VISUALIZE_CONTOUR = "roi_objects_visualize.npz"
TEST_INPUT_VISUALIZE_HIERARCHY = "roi_obj_hierarchy_visualize.npz"
TEST_INPUT_VISUALIZE_CLUSTERS = "clusters_i_visualize.npz"
TEST_INPUT_VISUALIZE_BACKGROUND = "visualize_background_img.png"
TEST_INPUT_GENOTXT = "cluster_names.txt"
TEST_INPUT_GENOTXT_TOO_MANY = "cluster_names_too_many.txt"
TEST_INPUT_CROPPED = 'cropped_img.jpg'
TEST_INPUT_CROPPED_MASK = 'cropped-mask.png'
TEST_INPUT_MARKER = 'seed-image.jpg'
TEST_INPUT_SKELETON = 'input_skeleton.png'
TEST_INPUT_SKELETON_PRUNED = 'input_pruned_skeleton.png'
TEST_FOREGROUND = "TEST_FOREGROUND.jpg"
TEST_BACKGROUND = "TEST_BACKGROUND.jpg"
TEST_PDFS = "naive_bayes_pdfs.txt"
TEST_PDFS_BAD = "naive_bayes_pdfs_bad.txt"
TEST_VIS_SMALL = "setaria_small_vis.png"
TEST_MASK_SMALL = "setaria_small_mask.png"
TEST_VIS_COMP_CONTOUR = "setaria_composed_contours.npz"
TEST_ACUTE_RESULT = np.asarray([[[119, 285]], [[151, 280]], [[168, 267]], [[168, 262]], [[171, 261]], [[224, 269]],
                                [[246, 271]], [[260, 277]], [[141, 248]], [[183, 194]], [[188, 237]], [[173, 240]],
                                [[186, 260]], [[147, 244]], [[163, 246]], [[173, 268]], [[170, 272]], [[151, 320]],
                                [[195, 289]], [[228, 272]], [[210, 272]], [[209, 247]], [[210, 232]]])
TEST_VIS_SMALL_PLANT = "setaria_small_plant_vis.png"
TEST_MASK_SMALL_PLANT = "setaria_small_plant_mask.png"
TEST_VIS_COMP_CONTOUR_SMALL_PLANT = "setaria_small_plant_composed_contours.npz"
TEST_SAMPLED_RGB_POINTS = "sampled_rgb_points.txt"
TEST_TARGET_IMG = "target_img.png"
TEST_TARGET_IMG_WITH_HEXAGON = "target_img_w_hexagon.png"
TEST_TARGET_IMG_TRIANGLE = "target_img copy.png"
TEST_SOURCE1_IMG = "source1_img.png"
TEST_SOURCE2_IMG = "source2_img.png"
TEST_TARGET_MASK = "mask_img.png"
TEST_TARGET_IMG_COLOR_CARD = "color_card_target.png"
TEST_SOURCE2_MASK = "mask2_img.png"
TEST_TARGET_MATRIX = "target_matrix.npz"
TEST_SOURCE1_MATRIX = "source1_matrix.npz"
TEST_SOURCE2_MATRIX = "source2_matrix.npz"
TEST_MATRIX_B1 = "matrix_b1.npz"
TEST_MATRIX_B2 = "matrix_b2.npz"
TEST_TRANSFORM1 = "transformation_matrix1.npz"
TEST_MATRIX_M1 = "matrix_m1.npz"
TEST_MATRIX_M2 = "matrix_m2.npz"
TEST_S1_CORRECTED = "source_corrected.png"
TEST_SKELETON_OBJECTS = "skeleton_objects.npz"
TEST_SKELETON_HIERARCHIES = "skeleton_hierarchies.npz"
TEST_THERMAL_ARRAY = "thermal_img.npz"
TEST_THERMAL_IMG_MASK = "thermal_img_mask.png"
TEST_INPUT_THERMAL_CSV = "FLIR2600.csv"
# TEST_BAD_MASK = "bad_mask_test.pkl"
# TEST_IM_BAD_NONE = "bad_mask_none.pkl"
# TEST_IM_BAD_BOTH = "bad_mask_both.pkl"
# TEST_IM_BAD_NAN = "bad_mask_nan.pkl"
# TEST_IM_BAD_INF = "bad_mask_inf.pkl"
PIXEL_VALUES = "pixel_inspector_rgb_values.txt"
TEST_INPUT_LEAF_MASK = "leaves_mask.png"


# ##########################
# Tests for the main package
# ##########################
@pytest.mark.parametrize("debug", ["print", "plot"])
def test_plantcv_debug(debug, tmpdir):
    from plantcv.plantcv._debug import _debug
    # Create a test tmp directory
    img_outdir = tmpdir.mkdir("sub")
    pcv.params.debug = debug
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    _debug(visual=img, filename=os.path.join(img_outdir, TEST_INPUT_COLOR))
    assert True


@pytest.mark.parametrize("datatype,value", [[list, []], [int, 2], [float, 2.2], [bool, True], [str, "2"], [dict, {}],
                                            [tuple, ()], [None, None]])
def test_plantcv_outputs_add_observation(datatype, value):
    # Create output instance
    outputs = pcv.Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='type', scale='none',
                            datatype=datatype, value=value, label=[])
    assert outputs.observations["default"]["test"]["value"] == value


def test_plantcv_outputs_add_observation_invalid_type():
    # Create output instance
    outputs = pcv.Outputs()
    with pytest.raises(RuntimeError):
        outputs.add_observation(sample='default', variable='test', trait='test variable', method='type', scale='none',
                                datatype=list, value=np.array([2]), label=[])


def test_plantcv_outputs_save_results_json_newfile(tmpdir):
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    outfile = os.path.join(cache_dir, "results.json")
    # Create output instance
    outputs = pcv.Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json")
    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "test"


def test_plantcv_outputs_save_results_json_existing_file(tmpdir):
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    outfile = os.path.join(cache_dir, "data_results.txt")
    shutil.copyfile(os.path.join(TEST_DATA, "data_results.txt"), outfile)
    # Create output instance
    outputs = pcv.Outputs()
    outputs.add_observation(sample='default', variable='test', trait='test variable', method='test', scale='none',
                            datatype=str, value="test", label="none")
    outputs.save_results(filename=outfile, outformat="json")
    with open(outfile, "r") as fp:
        results = json.load(fp)
        assert results["observations"]["default"]["test"]["value"] == "test"


def test_plantcv_outputs_save_results_csv(tmpdir):
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    outfile = os.path.join(cache_dir, "results.csv")
    testfile = os.path.join(TEST_DATA, "data_results.csv")
    # Create output instance
    outputs = pcv.Outputs()
    outputs.add_observation(sample='default', variable='string', trait='string variable', method='string', scale='none',
                            datatype=str, value="string", label="none")
    outputs.add_observation(sample='default', variable='boolean', trait='boolean variable', method='boolean',
                            scale='none', datatype=bool, value=True, label="none")
    outputs.add_observation(sample='default', variable='list', trait='list variable', method='list',
                            scale='none', datatype=list, value=[1, 2, 3], label=[1, 2, 3])
    outputs.add_observation(sample='default', variable='tuple', trait='tuple variable', method='tuple',
                            scale='none', datatype=tuple, value=(1, 2), label=(1, 2))
    outputs.add_observation(sample='default', variable='tuple_list', trait='list of tuples variable',
                            method='tuple_list', scale='none', datatype=list, value=[(1, 2), (3, 4)], label=[1, 2])
    outputs.save_results(filename=outfile, outformat="csv")
    with open(outfile, "r") as fp:
        results = fp.read()
    with open(testfile, "r") as fp:
        test_results = fp.read()
    assert results == test_results


def test_plantcv_acute():
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask)
    _ = pcv.acute(obj=obj_contour, win=0, thresh=15, mask=mask)
    _ = pcv.acute(obj=np.array(([[213, 190]], [[83, 61]], [[149, 246]])), win=84, thresh=192, mask=mask)
    _ = pcv.acute(obj=np.array(([[3, 29]], [[31, 102]], [[161, 63]])), win=148, thresh=56, mask=mask)
    _ = pcv.acute(obj=np.array(([[103, 154]], [[27, 227]], [[152, 83]])), win=35, thresh=0, mask=mask)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.acute(obj=np.array(([[103, 154]], [[27, 227]], [[152, 83]])), win=35, thresh=0, mask=mask)
    _ = pcv.acute(obj=obj_contour, win=0, thresh=15, mask=mask)
    homology_pts = pcv.acute(obj=obj_contour, win=5, thresh=15, mask=mask)
    assert all([i == j] for i, j in zip(np.shape(homology_pts), (29, 1, 2)))


def test_plantcv_acute_vertex():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    acute = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert all([i == j] for i, j in zip(np.shape(acute), np.shape(TEST_ACUTE_RESULT)))
    pcv.outputs.clear()


def test_plantcv_acute_vertex_bad_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.acute_vertex(obj=obj_contour, win=5, thresh=15, sep=5, img=img)
    assert all([i == j] for i, j in zip(result, [0, ("NA", "NA")]))
    pcv.outputs.clear()


def test_plantcv_analyze_bound_horizontal():
    # Clear previous outputs
    pcv.outputs.clear()
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_above_bound_only = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    pcv.params.debug = None
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=300, label="prefix")
    pcv.outputs.clear()
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=100)
    _ = pcv.analyze_bound_horizontal(img=img_above_bound_only, obj=object_contours, mask=mask, line_position=1756)
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=1756)
    assert len(pcv.outputs.observations["default"]) == 7


def test_plantcv_analyze_bound_horizontal_grayscale_image():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with a grayscale reference image and debug="plot"
    pcv.params.debug = "plot"
    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=1756)
    assert len(np.shape(boundary_img1)) == 3


def test_plantcv_analyze_bound_horizontal_neg_y():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_horizontal")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug=None, line position that will trigger -y
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=-1000)
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=0)
    _ = pcv.analyze_bound_horizontal(img=img, obj=object_contours, mask=mask, line_position=2056)
    assert pcv.outputs.observations['default']['height_above_reference']['value'] == 713


def test_plantcv_analyze_bound_vertical():
    # Clear previous outputs
    pcv.outputs.clear()
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    assert pcv.outputs.observations['default']['width_left_reference']['value'] == 94


def test_plantcv_analyze_bound_vertical_grayscale_image():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_vertical")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with a grayscale reference image and debug="plot"
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1000)
    assert pcv.outputs.observations['default']['width_left_reference']['value'] == 94
    pcv.outputs.clear()


def test_plantcv_analyze_bound_vertical_neg_x():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_vertical")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug="plot", line position that will trigger -x
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=2454)
    assert pcv.outputs.observations['default']['width_left_reference']['value'] == 441


def test_plantcv_analyze_bound_vertical_small_x():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_bound_vertical")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    object_contours = contours_npz['arr_0']
    # Test with debug='plot', line position that will trigger -x, and two channel object
    pcv.params.debug = "plot"
    _ = pcv.analyze_bound_vertical(img=img, obj=object_contours, mask=mask, line_position=1)
    assert pcv.outputs.observations['default']['width_right_reference']['value'] == 441


def test_plantcv_analyze_color():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="all")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None, label="prefix")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='lab')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='hsv')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)

    # Test with debug = "print"
    # pcv.params.debug = "print"
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="all")
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None, label="prefix")

    # Test with debug = "plot"
    # pcv.params.debug = "plot"
    # _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='lab')
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='hsv')
    # _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type=None)

    # Test with debug = None
    # pcv.params.debug = None
    _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='rgb')
    assert pcv.outputs.observations['default']['hue_median']['value'] == 84.0


def test_plantcv_analyze_color_incorrect_image():
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(rgb_img=img_binary, mask=mask, hist_plot_type=None)
#
#


def test_plantcv_analyze_color_bad_hist_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = "plot"
    with pytest.raises(RuntimeError):
        _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='bgr')


def test_plantcv_analyze_color_incorrect_hist_plot_type():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="bgr")


def test_plantcv_analyze_nir():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug=None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)

    _ = pcv.analyze_nir_intensity(gray_img=img, mask=mask, bins=256, histplot=True)
    result = len(pcv.outputs.observations['default']['nir_frequencies']['value'])
    assert result == 256


def test_plantcv_analyze_nir_16bit():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test with debug=None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)

    _ = pcv.analyze_nir_intensity(gray_img=np.uint16(img), mask=mask, bins=256, histplot=True)
    result = len(pcv.outputs.observations['default']['nir_frequencies']['value'])
    assert result == 256


def test_plantcv_analyze_object():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    pcv.outputs.clear()
    assert len(obj_images) != 0


def test_plantcv_analyze_object_grayscale_input():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 1


def test_plantcv_analyze_object_zero_slope():
    # Test with debug = None
    pcv.params.debug = None
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:11, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[11, 10]], [[12, 10]], [[13, 10]], [[14, 10]], [[15, 10]], [[16, 10]],
                            [[17, 10]], [[18, 10]], [[19, 10]], [[20, 10]], [[21, 10]], [[22, 10]], [[23, 10]],
                            [[24, 10]], [[25, 10]], [[26, 10]], [[27, 10]], [[28, 10]], [[29, 10]], [[30, 10]],
                            [[31, 10]], [[32, 10]], [[33, 10]], [[34, 10]], [[35, 10]], [[36, 10]], [[37, 10]],
                            [[38, 10]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]], [[34, 10]],
                            [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]], [[27, 10]],
                            [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]], [[20, 10]],
                            [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]], [[13, 10]],
                            [[12, 10]], [[11, 10]]], dtype=np.int32)
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_longest_axis_2d():
    # Test with debug = None
    pcv.params.debug = None
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[0:5, 45:49, 0] = 255
    img[0:5, 0:5, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[45, 1]], [[45, 2]], [[45, 3]], [[45, 4]], [[46, 4]], [[47, 4]], [[48, 4]],
                            [[48, 3]], [[48, 2]], [[48, 1]], [[47, 1]], [[46, 1]], [[1, 1]], [[1, 2]],
                            [[1, 3]], [[1, 4]], [[2, 4]], [[3, 4]], [[4, 4]], [[4, 3]], [[4, 2]],
                            [[4, 1]], [[3, 1]], [[2, 1]]], dtype=np.int32)
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_longest_axis_2e():
    # Test with debug = None
    pcv.params.debug = None
    # Create a test image
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    img[10:15, 10:40, 0] = 255
    mask = img[:, :, 0]
    obj_contour = np.array([[[10, 10]], [[10, 11]], [[10, 12]], [[10, 13]], [[10, 14]], [[11, 14]], [[12, 14]],
                            [[13, 14]], [[14, 14]], [[15, 14]], [[16, 14]], [[17, 14]], [[18, 14]], [[19, 14]],
                            [[20, 14]], [[21, 14]], [[22, 14]], [[23, 14]], [[24, 14]], [[25, 14]], [[26, 14]],
                            [[27, 14]], [[28, 14]], [[29, 14]], [[30, 14]], [[31, 14]], [[32, 14]], [[33, 14]],
                            [[34, 14]], [[35, 14]], [[36, 14]], [[37, 14]], [[38, 14]], [[39, 14]], [[39, 13]],
                            [[39, 12]], [[39, 11]], [[39, 10]], [[38, 10]], [[37, 10]], [[36, 10]], [[35, 10]],
                            [[34, 10]], [[33, 10]], [[32, 10]], [[31, 10]], [[30, 10]], [[29, 10]], [[28, 10]],
                            [[27, 10]], [[26, 10]], [[25, 10]], [[24, 10]], [[23, 10]], [[22, 10]], [[21, 10]],
                            [[20, 10]], [[19, 10]], [[18, 10]], [[17, 10]], [[16, 10]], [[15, 10]], [[14, 10]],
                            [[13, 10]], [[12, 10]], [[11, 10]]], dtype=np.int32)
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert len(obj_images) != 0


def test_plantcv_analyze_object_small_contour():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_contour = [np.array([[[0, 0]], [[0, 50]], [[50, 50]], [[50, 0]]], dtype=np.int32)]
    obj_images = pcv.analyze_object(img=img, obj=obj_contour, mask=mask)
    assert obj_images is None


def test_plantcv_analyze_thermal_values():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_thermal_values")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    # img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_THERMAL_IMG_MASK), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_THERMAL_ARRAY), encoding="latin1")
    img = contours_npz['arr_0']

    pcv.params.debug = None
    thermal_hist = pcv.analyze_thermal_values(thermal_array=img, mask=mask, histplot=True)
    assert thermal_hist is not None and pcv.outputs.observations['default']['median_temp']['value'] == 33.20922


def test_plantcv_apply_mask_white():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_apply_mask_white")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    masked_img = pcv.apply_mask(img=img, mask=mask, mask_color="white")
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_apply_mask_black():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_apply_mask_black")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    masked_img = pcv.apply_mask(img=img, mask=mask, mask_color="black")
    assert all([i == j] for i, j in zip(np.shape(masked_img), TEST_COLOR_DIM))


def test_plantcv_apply_mask_hyperspectral():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_apply_mask_hyperspectral")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    hyper_array = pcv.hyperspectral.read_data(filename=spectral_filename)

    img = np.ones((2056, 2454))
    img_stacked = cv2.merge((img, img, img, img))
    # Test with debug = none
    pcv.params.debug = None
    masked_array = pcv.apply_mask(img=hyper_array.array_data, mask=img, mask_color="black")
    assert np.mean(masked_array) == 13.97111260224949


def test_plantcv_apply_mask_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = "plot"
        _ = pcv.apply_mask(img=img, mask=mask, mask_color="wite")


def test_plantcv_auto_crop():
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    # Test with debug = None
    pcv.params.debug = None
    # padding as tuple
    _ = pcv.auto_crop(img=img1, obj=roi_contours[1], padding_x=(20, 10), padding_y=(20, 10), color='black')
    # padding 0 so crop same as image
    _ = pcv.auto_crop(img=img1, obj=roi_contours[1], color='image')
    # padding as int
    cropped = pcv.auto_crop(img=img1, obj=roi_contours[1], padding_x=20, padding_y=20, color='image')
    x, y, z = np.shape(img1)
    x1, y1, z1 = np.shape(cropped)
    assert x > x1


def test_plantcv_auto_crop_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_auto_crop_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    cropped = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x=20, padding_y=20, color='white')
    x, y = np.shape(gray_img)
    x1, y1 = np.shape(cropped)
    assert x > x1


def test_plantcv_auto_crop_bad_color_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    with pytest.raises(RuntimeError):
        _ = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x=20, padding_y=20, color='wite')


def test_plantcv_auto_crop_bad_padding_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    roi_contours = [contours[arr_n] for arr_n in contours]
    with pytest.raises(RuntimeError):
        _ = pcv.auto_crop(img=gray_img, obj=roi_contours[1], padding_x="one", padding_y=20, color='white')


def test_plantcv_canny_edge_detect():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_canny_edge_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    _ = pcv.canny_edge_detect(img=rgb_img, mask=mask, mask_color='white')
    _ = pcv.canny_edge_detect(img=img, mask=mask, mask_color='black')
    _ = pcv.canny_edge_detect(img=img, thickness=2)
    # Test with debug = None
    pcv.params.debug = None
    edge_img = pcv.canny_edge_detect(img=img)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(edge_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(edge_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_canny_edge_detect_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_canny_edge_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.canny_edge_detect(img=img, mask=mask, mask_color="gray")


def test_plantcv_closing():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_closing")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug=None
    pcv.params.debug = None
    _ = pcv.closing(gray_img, np.ones((4, 4), np.uint8))
    filtered_img = pcv.closing(bin_img)
    assert np.sum(filtered_img) == 16261860


def test_plantcv_closing_bad_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.closing(rgb_img)


def test_plantcv_cluster_contours():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierarchy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierarchy['arr_0']
    # Test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, show_grid=True)
    # Test with debug = None
    pcv.params.debug = None
    clusters_i, contours, hierarchy = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy,
                                                           nrow=4, ncol=6)
    lenori = len(objs)
    lenclust = len(clusters_i)
    assert lenori > lenclust


def test_plantcv_cluster_contours_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), 0)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_OBJECT), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy, show_grid=True)
    # Test with debug = None
    pcv.params.debug = None
    clusters_i, contours, hierachy = pcv.cluster_contours(img=img1, roi_objects=objs, roi_obj_hierarchy=obj_hierarchy,
                                                          nrow=4, ncol=6)
    lenori = len(objs)
    lenclust = len(clusters_i)
    assert lenori > lenclust


def test_plantcv_cluster_contours_splitimg():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_splitimg")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR), encoding="latin1")
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    cluster_names = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT)
    cluster_names_too_many = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT_TOO_MANY)
    roi_contours = [contours[arr_n] for arr_n in contours]
    cluster_contours = [clusters[arr_n] for arr_n in clusters]
    obj_hierarchy = hierachy['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=cache_dir, file=None, filenames=None)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=[[0]], contours=[],
                                           hierarchy=np.array([[[1, -1, -1, -1]]]))
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=cache_dir, file='multi', filenames=None)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=None, file=None, filenames=cluster_names)
    _, _, _ = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                           contours=roi_contours,
                                           hierarchy=obj_hierarchy, outdir=None, file=None,
                                           filenames=cluster_names_too_many)
    output_path, imgs, masks = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                                            contours=roi_contours, hierarchy=obj_hierarchy, outdir=None,
                                                            file=None,
                                                            filenames=None)
    assert len(output_path) != 0


def test_plantcv_cluster_contours_splitimg_grayscale():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_cluster_contours_splitimg_grayscale")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), 0)
    contours = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_CONTOUR), encoding="latin1")
    clusters = np.load(os.path.join(TEST_DATA, TEST_INPUT_ClUSTER_CONTOUR), encoding="latin1")
    hierachy = np.load(os.path.join(TEST_DATA, TEST_INPUT_MULTI_HIERARCHY), encoding="latin1")
    cluster_names = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT)
    cluster_names_too_many = os.path.join(TEST_DATA, TEST_INPUT_GENOTXT_TOO_MANY)
    roi_contours = [contours[arr_n] for arr_n in contours]
    cluster_contours = [clusters[arr_n] for arr_n in clusters]
    obj_hierarchy = hierachy['arr_0']
    pcv.params.debug = None
    output_path, imgs, masks = pcv.cluster_contour_splitimg(img=img1, grouped_contour_indexes=cluster_contours,
                                                            contours=roi_contours, hierarchy=obj_hierarchy, outdir=None,
                                                            file=None,
                                                            filenames=None)
    assert len(output_path) != 0


def test_plantcv_color_palette():
    # Return a color palette
    colors = pcv.color_palette(num=10, saved=False)
    assert np.shape(colors) == (10, 3)


def test_plantcv_color_palette_random():
    # Return a color palette in random order
    pcv.params.color_sequence = "random"
    colors = pcv.color_palette(num=10, saved=False)
    assert np.shape(colors) == (10, 3)


def test_plantcv_color_palette_saved():
    # Return a color palette that was saved
    pcv.params.saved_color_scale = [[0, 0, 0], [255, 255, 255]]
    colors = pcv.color_palette(num=2, saved=True)
    assert colors == [[0, 0, 0], [255, 255, 255]]


def test_plantcv_crop():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img, _, _ = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), 'gray')
    pcv.params.debug = None
    cropped = pcv.crop(img=img, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50)


def test_plantcv_crop_hyperspectral():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_hyperspectral")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = np.ones((2056, 2454))
    img_stacked = cv2.merge((img, img, img, img))
    pcv.params.debug = None
    cropped = pcv.crop(img=img_stacked, x=10, y=10, h=50, w=50)
    assert np.shape(cropped) == (50, 50, 4)


def test_plantcv_crop_position_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), 'gray')
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_three_channel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_resize = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_RESIZE), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_resize, x=40, y=3, v_pos="top", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_three_channel, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "print" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="bottom", h_pos="left")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "plot" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=45, y=2, v_pos="bottom", h_pos="left")
    # Test with debug = None
    pcv.params.debug = None
    newmask = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    assert np.sum(newmask) == 707115


def test_plantcv_crop_position_mask_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_COLOR), mode='native')
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_resize = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_RESIZE))
    mask_non_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "print" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="bottom", h_pos="left")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    # Test with debug = "plot" with bottom
    _ = pcv.crop_position_mask(nir, mask, x=45, y=2, v_pos="bottom", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="bottom", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="top", h_pos="left")
    _ = pcv.crop_position_mask(nir, mask_non_binary, x=45, y=2, v_pos="bottom", h_pos="right")
    _ = pcv.crop_position_mask(nir, mask_resize, x=45, y=2, v_pos="top", h_pos="left")

    # Test with debug = None
    pcv.params.debug = None
    newmask = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="right")
    assert np.sum(newmask) == 707115


def test_plantcv_crop_position_mask_bad_input_x():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=-1, y=-1, v_pos="top", h_pos="right")


def test_plantcv_crop_position_mask_bad_input_vpos():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="below", h_pos="right")


def test_plantcv_crop_position_mask_bad_input_hpos():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_crop_position_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    # Read in test data
    nir, path1, filename1 = pcv.readimage(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.crop_position_mask(nir, mask, x=40, y=3, v_pos="top", h_pos="starboard")


def test_plantcv_dilate():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_dilate")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    dilate_img = pcv.dilate(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(dilate_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(dilate_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_dilate_small_k():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(ValueError):
        _ = pcv.dilate(img, 1, 1)


def test_plantcv_erode():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_erode")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    erode_img = pcv.erode(gray_img=img, ksize=5, i=1)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(erode_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(erode_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_erode_small_k():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(ValueError):
        _ = pcv.erode(img, 1, 1)


def test_plantcv_distance_transform():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_distance_transform")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = None
    pcv.params.debug = None
    distance_transform_img = pcv.distance_transform(bin_img=mask, distance_type=1, mask_size=3)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(distance_transform_img), np.shape(mask)))


def test_plantcv_fatal_error():
    # Verify that the fatal_error function raises a RuntimeError
    with pytest.raises(RuntimeError):
        pcv.fatal_error("Test error")


def test_plantcv_fill():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    fill_img = pcv.fill(bin_img=img, size=63632)
    # Assert that the output image has the dimensions of the input image
    # assert all([i == j] for i, j in zip(np.shape(fill_img), TEST_BINARY_DIM))
    assert np.sum(fill_img) == 0


def test_plantcv_fill_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.fill(bin_img=img, size=1)


def test_plantcv_fill_holes():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_holes")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    fill_img = pcv.fill_holes(bin_img=img)
    assert np.sum(fill_img) > np.sum(img)


def test_plantcv_fill_holes_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_fill_holes_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.fill_holes(bin_img=img)


def test_plantcv_find_objects():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    assert len(contours) == 2


def test_plantcv_find_objects_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_find_objects_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    contours, hierarchy = pcv.find_objects(img=img, mask=mask)
    # Assert the correct number of contours are found
    assert len(contours) == 2


def test_plantcv_flip():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_flip")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_binary = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.flip(img=img_binary, direction="vertical")
    flipped_img = pcv.flip(img=img, direction="horizontal")
    assert all([i == j] for i, j in zip(np.shape(flipped_img), TEST_COLOR_DIM))


def test_plantcv_flip_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.flip(img=img, direction="vert")


def test_plantcv_gaussian_blur():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_gaussian_blur")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.gaussian_blur(img=img_color, ksize=(51, 51), sigma_x=0, sigma_y=None)
    gaussian_img = pcv.gaussian_blur(img=img, ksize=(51, 51), sigma_x=0, sigma_y=None)
    imgavg = np.average(img)
    gavg = np.average(gaussian_img)
    assert gavg != imgavg


def test_plantcv_get_kernel_cross():
    kernel = pcv.get_kernel(size=(3, 3), shape="cross")
    assert (kernel == np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])).all()


def test_plantcv_get_kernel_rectangle():
    kernel = pcv.get_kernel(size=(3, 3), shape="rectangle")
    assert (kernel == np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])).all()


def test_plantcv_get_kernel_ellipse():
    kernel = pcv.get_kernel(size=(3, 3), shape="ellipse")
    assert (kernel == np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])).all()


def test_plantcv_get_kernel_bad_input_size():
    with pytest.raises(ValueError):
        _ = pcv.get_kernel(size=(1, 1), shape="ellipse")


def test_plantcv_get_kernel_bad_input_shape():
    with pytest.raises(RuntimeError):
        _ = pcv.get_kernel(size=(3, 1), shape="square")


def test_plantcv_get_nir_sv():
    nirpath = pcv.get_nir(TEST_DATA, TEST_VIS)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR)
    assert nirpath == nirpath1


def test_plantcv_get_nir_tv():
    nirpath = pcv.get_nir(TEST_DATA, TEST_VIS_TV)
    nirpath1 = os.path.join(TEST_DATA, TEST_NIR_TV)
    assert nirpath == nirpath1


def test_plantcv_hist_equalization():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hist_equalization")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    hist = pcv.hist_equalization(gray_img=img)
    histavg = np.average(hist)
    imgavg = np.average(img)
    assert histavg != imgavg


def test_plantcv_hist_equalization_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hist_equalization_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.hist_equalization(gray_img=img)


def test_plantcv_image_add():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_image_add")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = None
    pcv.params.debug = None
    added_img = pcv.image_add(gray_img1=img1, gray_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(added_img), TEST_BINARY_DIM))


def test_plantcv_image_fusion():
    # Read in test data
    # 16-bit image
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN))
    # 8-bit image
    img2 = img_as_ubyte(img2)
    fused_img = pcv.image_fusion(img1, img2, [480.0], [550.0, 640.0, 800.0])
    assert str(type(fused_img)) == "<class 'plantcv.plantcv.classes.Spectral_data'>"


def test_plantcv_image_fusion_size_diff():
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), 0)
    img2 = np.copy(img1)
    img2 = img2[0:10, 0:10]
    with pytest.raises(RuntimeError):
        _ = pcv.image_fusion(img1, img2, [480.0, 550.0, 670.0], [480.0, 550.0, 670.0])


def test_plantcv_image_subtract():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_image_sub")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # read in images
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = None
    pcv.params.debug = None
    new_img = pcv.image_subtract(img1, img2)
    assert np.array_equal(new_img, np.zeros(np.shape(new_img), np.uint8))


def test_plantcv_image_subtract_fail():
    # read in images
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))
    # test
    with pytest.raises(RuntimeError):
        _ = pcv.image_subtract(img1, img2)


def test_plantcv_invert():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_invert")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    inverted_img = pcv.invert(gray_img=img)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(inverted_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(inverted_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_landmark_reference_pt_dist():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_landmark_reference")
    os.mkdir(cache_dir)
    points_rescaled = [(0.0139, 0.2569), (0.2361, 0.2917), (0.3542, 0.3819), (0.3542, 0.4167), (0.375, 0.4236),
                       (0.7431, 0.3681), (0.8958, 0.3542), (0.9931, 0.3125), (0.1667, 0.5139), (0.4583, 0.8889),
                       (0.4931, 0.5903), (0.3889, 0.5694), (0.4792, 0.4306), (0.2083, 0.5417), (0.3194, 0.5278),
                       (0.3889, 0.375), (0.3681, 0.3472), (0.2361, 0.0139), (0.5417, 0.2292), (0.7708, 0.3472),
                       (0.6458, 0.3472), (0.6389, 0.5208), (0.6458, 0.625)]
    centroid_rescaled = (0.4685, 0.4945)
    bottomline_rescaled = (0.4685, 0.2569)
    _ = pcv.landmark_reference_pt_dist(points_r=[], centroid_r=('a', 'b'), bline_r=(0, 0))
    _ = pcv.landmark_reference_pt_dist(points_r=[(10, 1000)], centroid_r=(10, 10), bline_r=(10, 10))
    _ = pcv.landmark_reference_pt_dist(points_r=[], centroid_r=(0, 0), bline_r=(0, 0))
    _ = pcv.landmark_reference_pt_dist(points_r=points_rescaled, centroid_r=centroid_rescaled,
                                       bline_r=bottomline_rescaled, label="prefix")
    assert len(pcv.outputs.observations['prefix'].keys()) == 8


def test_plantcv_laplace_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_laplace_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    lp_img = pcv.laplace_filter(gray_img=img, ksize=1, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(lp_img), TEST_GRAY_DIM))


def test_plantcv_logical_and():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_and")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = None
    pcv.params.debug = None
    and_img = pcv.logical_and(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(and_img), TEST_BINARY_DIM))


def test_plantcv_logical_or():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_or")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = None
    pcv.params.debug = None
    or_img = pcv.logical_or(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(or_img), TEST_BINARY_DIM))


def test_plantcv_logical_xor():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_logical_xor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = np.copy(img1)
    # Test with debug = None
    pcv.params.debug = None
    xor_img = pcv.logical_xor(bin_img1=img1, bin_img2=img2)
    assert all([i == j] for i, j in zip(np.shape(xor_img), TEST_BINARY_DIM))


def test_plantcv_median_blur():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_median_blur")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.median_blur(gray_img=img, ksize=(5, 5))
    blur_img = pcv.median_blur(gray_img=img, ksize=5)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(blur_img), TEST_BINARY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(blur_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_median_blur_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_median_blur_bad_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.median_blur(img, 5.)


def test_plantcv_naive_bayes_classifier():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_naive_bayes_classifier")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS))
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS))

    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(mask), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(mask), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_naive_bayes_classifier_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.naive_bayes_classifier(rgb_img=img, pdf_file=os.path.join(TEST_DATA, TEST_PDFS_BAD))


def test_plantcv_object_composition():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_object_composition")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.object_composition(img=img, contours=[], hierarchy=object_hierarchy)
    contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)  # type: tuple
    assert contour_shape[1] == 1


def test_plantcv_object_composition_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_object_composition_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    contours, mask = pcv.object_composition(img=img, contours=object_contours, hierarchy=object_hierarchy)
    # Assert that the objects have been combined
    contour_shape = np.shape(contours)  # type: tuple
    assert contour_shape[1] == 1


def test_plantcv_within_frame():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_within_frame")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask_ib = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    mask_oob = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK_OOB), -1)
    in_bounds_ib = pcv.within_frame(mask=mask_ib, border_width=1, label="prefix")
    in_bounds_oob = pcv.within_frame(mask=mask_oob, border_width=1)
    assert (in_bounds_ib is True and in_bounds_oob is False)


def test_plantcv_within_frame_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_within_frame")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    grayscale_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    with pytest.raises(RuntimeError):
        _ = pcv.within_frame(grayscale_img)


def test_plantcv_opening():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_closing")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    gray_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)
    bin_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug=None
    pcv.params.debug = None
    _ = pcv.opening(gray_img)
    _ = pcv.opening(bin_img, np.ones((4, 4), np.uint8))
    filtered_img = pcv.opening(bin_img)
    assert np.sum(filtered_img) == 16184595


def test_plantcv_opening_bad_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.opening(rgb_img)


def test_plantcv_output_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_output_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=None, mask_only=False)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=False)
    _ = pcv.output_mask(img=img_color, mask=mask, filename='test.png', outdir=None, mask_only=False)
    # Remove tmp files in working direcctory
    shutil.rmtree("ori-images")
    shutil.rmtree("mask-images")
    # Test with debug = None
    pcv.params.debug = None
    imgpath, maskpath, analysis_images = pcv.output_mask(img=img, mask=mask, filename='test.png',
                                                         outdir=cache_dir, mask_only=False)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])


def test_plantcv_output_mask_true():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_output_mask")
    pcv.params.debug_outdir = cache_dir
    os.mkdir(cache_dir)
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir, mask_only=True)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.output_mask(img=img_color, mask=mask, filename='test.png', outdir=cache_dir, mask_only=True)
    pcv.params.debug = None
    imgpath, maskpath, analysis_images = pcv.output_mask(img=img, mask=mask, filename='test.png', outdir=cache_dir,
                                                         mask_only=False)
    assert all([os.path.exists(imgpath) is True, os.path.exists(maskpath) is True])


def test_plantcv_plot_image_matplotlib_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pimg = pcv.visualize.pseudocolor(gray_img=img, mask=mask, min_value=10, max_value=200)
    with pytest.raises(RuntimeError):
        pcv.plot_image(pimg)


def test_plantcv_plot_image_plotnine():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_image_plotnine")
    os.mkdir(cache_dir)
    dataset = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]})
    img = ggplot(data=dataset)
    try:
        pcv.plot_image(img=img)
    except RuntimeError:
        assert False
    # Assert that the image was plotted without error
    assert True


def test_plantcv_print_image():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_print_image")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    pcv.print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename) is True


def test_plantcv_print_image_bad_type():
    with pytest.raises(RuntimeError):
        pcv.print_image(img=[], filename="/dev/null")


def test_plantcv_print_image_plotnine():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_print_image_plotnine")
    os.mkdir(cache_dir)
    dataset = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]})
    img = ggplot(data=dataset)
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    pcv.print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename) is True


def test_plantcv_print_image_matplotlib():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_print_image_plotnine")
    os.mkdir(cache_dir)
    # Input data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    plt.figure()
    plt.imshow(img)
    plot = plt.gcf()
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    pcv.print_image(img=plot, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename) is True


def test_plantcv_print_results(tmpdir):
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("sub")
    outfile = os.path.join(cache_dir, "results.json")
    pcv.print_results(filename=outfile)
    assert os.path.exists(outfile)


def test_plantcv_readimage_native():
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR), mode='rgba')
    _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_COLOR), mode='native')
    # Assert that the image name returned equals the name of the input image
    # Assert that the path of the image returned equals the path of the input image
    # Assert that the dimensions of the returned image equals the expected dimensions
    if img_name == TEST_INPUT_COLOR and path == TEST_DATA:
        if all([i == j] for i, j in zip(np.shape(img), TEST_COLOR_DIM)):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_readimage_grayscale():
    # Test with debug = None
    pcv.params.debug = None
    _, _, _ = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_GRAY), mode="grey")
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_GRAY), mode="gray")
    assert len(np.shape(img)) == 2


def test_plantcv_readimage_rgb():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_GRAY), mode="rgb")
    assert len(np.shape(img)) == 3


def test_plantcv_readimage_rgba_as_rgb():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_RGBA), mode="native")
    assert np.shape(img)[2] == 3


def test_plantcv_readimage_csv():
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readimage(filename=os.path.join(TEST_DATA, TEST_INPUT_THERMAL_CSV), mode="csv")
    assert len(np.shape(img)) == 2


def test_plantcv_readimage_envi():
    # Test with debug = None
    pcv.params.debug = None
    array_data = pcv.readimage(filename=os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA), mode="envi")
    if sys.version_info[0] < 3:
        assert len(array_data.array_type) == 8


def test_plantcv_readimage_bad_file():
    with pytest.raises(RuntimeError):
        _ = pcv.readimage(filename=TEST_INPUT_COLOR)


@pytest.mark.parametrize("alg, pattern", [["default", 'BG'],
                                          ["default", 'GB'],
                                          ["default", 'RG'],
                                          ["default", 'GR'],
                                          ["edgeaware", 'BG'],
                                          ["edgeaware", 'GB'],
                                          ["edgeaware", 'RG'],
                                          ["edgeaware", 'GR'],
                                          ["variablenumbergradients", 'BG'],
                                          ["variablenumbergradients", 'GB'],
                                          ["variablenumbergradients", 'RG'],
                                          ["variablenumbergradients", 'GR']])
def test_plantcv_readbayer(alg, pattern):
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_readbayer_default_bg")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = None
    pcv.params.debug = None
    img, path, img_name = pcv.readbayer(filename=os.path.join(TEST_DATA, TEST_INPUT_BAYER),
                                        bayerpattern=pattern, alg=alg)
    assert all([i == j] for i, j in zip(np.shape(img), (335, 400, 3)))


def test_plantcv_readbayer_default_bad_input():
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _, _, _ = pcv.readbayer(filename=os.path.join(TEST_DATA, "no-image.png"), bayerpattern="GR", alg="default")


def test_plantcv_rectangle_mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rectangle_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img_color = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="white")
    _ = pcv.rectangle_mask(img=img_color, p1=(0, 0), p2=(2454, 2056), color="gray")
    masked, hist, contour, heir = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="black")
    maskedsum = np.sum(masked)
    imgsum = np.sum(img)
    assert maskedsum < imgsum


def test_plantcv_rectangle_mask_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rectangle_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rectangle_mask(img=img, p1=(0, 0), p2=(2454, 2056), color="whit")


def test_plantcv_report_size_marker_detect():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_report_size_marker_detect")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                         objcolor='light', thresh_channel='s', thresh=120)
    pcv.outputs.clear()
    assert len(images) != 0


def test_plantcv_report_size_marker_define():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='define',
                                         objcolor='light', thresh_channel='s', thresh=120)
    assert len(images) != 0


def test_plantcv_report_size_marker_grayscale_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # ROI contour
    roi_contour = [np.array([[[0, 0]], [[0, 49]], [[49, 49]], [[49, 0]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)

    # Test with debug = None
    pcv.params.debug = None
    images = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='define',
                                         objcolor='light', thresh_channel='s', thresh=120)
    assert len(images) != 0


def test_plantcv_report_size_marker_bad_marker_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='none',
                                        objcolor='light', thresh_channel='s', thresh=120)


def test_plantcv_report_size_marker_bad_threshold_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER), -1)
    # ROI contour
    roi_contour = [np.array([[[3550, 850]], [[3550, 1349]], [[4049, 1349]], [[4049, 850]]], dtype=np.int32)]
    roi_hierarchy = np.array([[[-1, -1, -1, -1]]], dtype=np.int32)
    with pytest.raises(RuntimeError):
        _ = pcv.report_size_marker_area(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, marker='detect',
                                        objcolor='light', thresh_channel=None, thresh=120)


def test_plantcv_rgb2gray_cmyk():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    c = pcv.rgb2gray_cmyk(rgb_img=img, channel="c")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(c), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_cmyk_bad_channel():
    # Test with debug = None
    pcv.params.debug = None
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        # Channel S is not in CMYK
        _ = pcv.rgb2gray_cmyk(rgb_img=img, channel="s")


def test_plantcv_rgb2gray_hsv():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray_hsv")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    s = pcv.rgb2gray_hsv(rgb_img=img, channel="s")
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(s), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_hsv_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rgb2gray_hsv(rgb_img=img, channel="l")


def test_plantcv_rgb2gray_lab():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray_lab")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(b), TEST_GRAY_DIM))


def test_plantcv_rgb2gray_lab_bad_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.rgb2gray_lab(rgb_img=img, channel="v")


def test_plantcv_rgb2gray():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rgb2gray")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    gray = pcv.rgb2gray(rgb_img=img)
    # Assert that the output image has the dimensions of the input image but is only a single channel
    assert all([i == j] for i, j in zip(np.shape(gray), TEST_GRAY_DIM))


def test_plantcv_roi2mask():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_acute_vertex")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    pcv.params.debug = None
    mask = pcv.roi.roi2mask(img=img, contour=obj_contour)
    assert np.shape(mask)[0:2] == np.shape(img)[0:2] and np.sum(mask) == 255


def test_plantcv_roi_objects():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_objects")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.roi_objects(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, roi_type="largest")
    _ = pcv.roi_objects(img=img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                        object_contour=object_contours, obj_hierarchy=object_hierarchy, roi_type="cutto")
    # Test with debug = None
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy, roi_type="partial")
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 9


def test_plantcv_roi_objects_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.roi_objects(img=img, roi_type="cut", roi_contour=roi_contour, roi_hierarchy=roi_hierarchy,
                            object_contour=object_contours, obj_hierarchy=object_hierarchy)


def test_plantcv_roi_objects_grayscale_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_objects_grayscale_input")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR), 0)
    roi_contour_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_CONTOUR), encoding="latin1")
    roi_contour = [roi_contour_npz[arr_n] for arr_n in roi_contour_npz]
    roi_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_ROI_HIERARCHY), encoding="latin1")
    roi_hierarchy = roi_hierarchy_npz['arr_0']
    object_contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_CONTOURS), encoding="latin1")
    object_contours = [object_contours_npz[arr_n] for arr_n in object_contours_npz]
    object_hierarchy_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_OBJECT_HIERARCHY), encoding="latin1")
    object_hierarchy = object_hierarchy_npz['arr_0']
    pcv.params.debug = None
    kept_contours, kept_hierarchy, mask, area = pcv.roi_objects(img=img, roi_type="partial", roi_contour=roi_contour,
                                                                roi_hierarchy=roi_hierarchy,
                                                                object_contour=object_contours,
                                                                obj_hierarchy=object_hierarchy)
    # Assert that the contours were filtered as expected
    assert len(kept_contours) == 9


def test_plantcv_rotate():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    rotated = pcv.rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_transform_rotate():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_rotate_img")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.rotate(img=img, rotation_deg=45, crop=True)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.rotate(img=img, rotation_deg=45, crop=True)
    # Test with debug = None
    pcv.params.debug = None
    rotated = pcv.transform.rotate(img=img, rotation_deg=45, crop=True)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_transform_rotate_gray():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.rotate(img=img, rotation_deg=45, crop=False)
    # Test with debug = None
    pcv.params.debug = None
    rotated = pcv.transform.rotate(img=img, rotation_deg=45, crop=False)
    imgavg = np.average(img)
    rotateavg = np.average(rotated)
    assert rotateavg != imgavg


def test_plantcv_scale_features():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scale_features")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # test with debug = 'plot' to cover plotting logic
    pcv.params.debug = 'plot'
    _ = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, line_position='NA')
    # Test with debug = None
    pcv.params.debug = None
    points_rescaled, centroid_rescaled, bottomline_rescaled = pcv.scale_features(obj=obj_contour, mask=mask,
                                                                                 points=TEST_ACUTE_RESULT,
                                                                                 line_position=50)
    assert len(points_rescaled) == 23


def test_plantcv_scale_features_bad_input():
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.scale_features(obj=obj_contour, mask=mask, points=TEST_ACUTE_RESULT, line_position=50)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_scharr_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_scharr_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    scharr_img = pcv.scharr_filter(img=img, dx=1, dy=0, scale=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(scharr_img), TEST_GRAY_DIM))


def test_plantcv_shift_img():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_shift_img")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = None
    _ = pcv.shift_img(img=img, number=300, side="bottom")
    _ = pcv.shift_img(img=img, number=300, side="right")
    _ = pcv.shift_img(img=mask, number=300, side="left")
    rotated = pcv.shift_img(img=img, number=300, side="top")
    imgavg = np.average(img)
    shiftavg = np.average(rotated)
    assert shiftavg != imgavg


def test_plantcv_shift_img_bad_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.shift_img(img=img, number=-300, side="top")


def test_plantcv_shift_img_bad_side_input():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.shift_img(img=img, number=300, side="starboard")


def test_plantcv_sobel_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_sobel_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    sobel_img = pcv.sobel_filter(gray_img=img, dx=1, dy=0, ksize=1)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(sobel_img), TEST_GRAY_DIM))


def test_plantcv_stdev_filter():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_sobel_filter")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    pcv.params.debug = None
    filter_img = pcv.stdev_filter(img=img, ksize=11)
    assert (np.shape(filter_img) == np.shape(img))


def test_plantcv_watershed_segmentation():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_watershed_segmentation")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED_MASK), -1)
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.watershed_segmentation(rgb_img=img, mask=mask, distance=10, label='prefix')
    assert pcv.outputs.observations['prefix']['estimated_object_count']['value'] > 9


def test_plantcv_white_balance_gray_16bit():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_gray_16bit")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_gray_8bit():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_gray_8bit")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Test without an ROI
    pcv.params.debug = None
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


def test_plantcv_white_balance_rgb():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_white_balance_rgb")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER))
    pcv.params.debug = None
    # Test without an ROI
    _ = pcv.white_balance(img=img, mode='max', roi=None)
    # Test with debug = None
    white_balanced = pcv.white_balance(img=img, mode='hist', roi=(5, 5, 80, 80))
    imgavg = np.average(img)
    balancedavg = np.average(white_balanced)
    assert balancedavg != imgavg


@pytest.mark.parametrize("mode, roi", [['hist', (5, 5, 5, 5, 5)],  # too many points
                                       ['hist', (5., 5, 5, 5)],  # not all integers
                                       ['histogram', (5, 5, 80, 80)]])  # bad mode
def test_plantcv_white_balance_bad_input(mode, roi):
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_NIR_MASK), -1)
    # Test with debug = None
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.white_balance(img=img, mode=mode, roi=roi)


def test_plantcv_x_axis_pseudolandmarks():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_x_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img, label="prefix")
    _ = pcv.x_axis_pseudolandmarks(obj=np.array([[0, 0], [0, 0]]), mask=np.array([[0, 0], [0, 0]]), img=img)
    _ = pcv.x_axis_pseudolandmarks(obj=np.array(([[89, 222]], [[252, 39]], [[89, 207]])),
                                   mask=np.array(([[42, 161]], [[2, 47]], [[211, 222]])), img=img)

    _ = pcv.x_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_small_obj():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    _, _, _ = pcv.x_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    top, bottom, center_v = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([all([i == j] for i, j in zip(np.shape(top), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(bottom), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_v), (20, 1, 2)))])


def test_plantcv_x_axis_pseudolandmarks_bad_input():
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.x_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_x_axis_pseudolandmarks_bad_obj_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    with pytest.raises(RuntimeError):
        _ = pcv.x_axis_pseudolandmarks(obj=np.array([[-2, -2], [-2, -2]]), mask=np.array([[-2, -2], [-2, -2]]), img=img)


def test_plantcv_y_axis_pseudolandmarks():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    # Test with debug = None
    pcv.params.debug = None
    _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=(), mask=mask, img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=np.array(([[89, 222]], [[252, 39]], [[89, 207]])),
                                   mask=np.array(([[42, 161]], [[2, 47]], [[211, 222]])), img=img)
    _ = pcv.y_axis_pseudolandmarks(obj=np.array(([[21, 11]], [[159, 155]], [[237, 11]])),
                                   mask=np.array(([[38, 54]], [[144, 169]], [[81, 137]])), img=img)
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_small_obj():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_MASK_SMALL_PLANT), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_VIS_COMP_CONTOUR_SMALL_PLANT), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    pcv.params.debug = None
    _, _, _ = pcv.y_axis_pseudolandmarks(obj=[], mask=mask, img=img)
    pcv.outputs.clear()
    left, right, center_h = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([all([i == j] for i, j in zip(np.shape(left), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(right), (20, 1, 2))),
                all([i == j] for i, j in zip(np.shape(center_h), (20, 1, 2)))])


def test_plantcv_y_axis_pseudolandmarks_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_y_axis_pseudolandmarks_debug")
    os.mkdir(cache_dir)
    img = np.array([])
    mask = np.array([])
    obj_contour = np.array([])
    pcv.params.debug = None
    result = pcv.y_axis_pseudolandmarks(obj=obj_contour, mask=mask, img=img)
    pcv.outputs.clear()
    assert all([i == j] for i, j in zip(result, [("NA", "NA"), ("NA", "NA"), ("NA", "NA")]))


def test_plantcv_y_axis_pseudolandmarks_bad_obj_input():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_VIS_SMALL_PLANT))
    with pytest.raises(RuntimeError):
        _ = pcv.y_axis_pseudolandmarks(obj=np.array([[-2, -2], [-2, -2]]), mask=np.array([[-2, -2], [-2, -2]]), img=img)


def test_plantcv_background_subtraction():
    # List to hold result of all tests.
    truths = []
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    big_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Testing if background subtraction is actually still working.
    # This should return an array whose sum is greater than one
    pcv.params.debug = None
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) > 0)
    fgmask = pcv.background_subtraction(background_image=big_img, foreground_image=bg_img)
    truths.append(np.sum(fgmask) > 0)
    # The same foreground subtracted from itself should be 0
    fgmask = pcv.background_subtraction(background_image=fg_img, foreground_image=fg_img)
    truths.append(np.sum(fgmask) == 0)
    # The same background subtracted from itself should be 0
    fgmask = pcv.background_subtraction(background_image=bg_img, foreground_image=bg_img)
    truths.append(np.sum(fgmask) == 0)
    # All of these should be true for the function to pass testing.
    assert (all(truths))


def test_plantcv_background_subtraction_bad_img_type():
    fg_color = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_gray = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND), 0)
    pcv.params.debug = None
    with pytest.raises(RuntimeError):
        _ = pcv.background_subtraction(background_image=bg_gray, foreground_image=fg_color)


def test_plantcv_background_subtraction_different_sizes():
    fg_img = cv2.imread(os.path.join(TEST_DATA, TEST_FOREGROUND))
    bg_img = cv2.imread(os.path.join(TEST_DATA, TEST_BACKGROUND))
    bg_shp = np.shape(bg_img)  # type: tuple
    bg_img_resized = cv2.resize(bg_img, (int(bg_shp[0] / 2), int(bg_shp[1] / 2)), interpolation=cv2.INTER_AREA)
    pcv.params.debug = None
    fgmask = pcv.background_subtraction(background_image=bg_img_resized, foreground_image=fg_img)
    assert np.sum(fgmask) > 0


@pytest.mark.parametrize("alg, min_size, max_size", [['DBSCAN', 10, None],
                                                     ['OPTICS', 100, 5000]]
                         )
def test_plantcv_spatial_clustering(alg, min_size, max_size):
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_spatial_clustering_dbscan")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI_MASK), -1)
    pcv.params.debug = None
    spmask = pcv.spatial_clustering(img, algorithm=alg, min_cluster_size=min_size, max_distance=max_size)
    assert len(spmask[1]) == 2


def test_plantcv_spatial_clustering_badinput():
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MULTI_MASK), -1)
    pcv.params.debug = None
    with pytest.raises(NameError):
        _ = pcv.spatial_clustering(img, algorithm="Hydra", min_cluster_size=5, max_distance=100)


# ##############################
# Tests for the learn subpackage
# ##############################
def test_plantcv_learn_naive_bayes():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_learn_naive_bayes")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    maskdir = os.path.join(cache_dir, "masks")
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    if not os.path.exists(maskdir):
        os.mkdir(maskdir)
    # Copy and image and mask to the image/mask directories
    shutil.copyfile(os.path.join(TEST_DATA, TEST_VIS_SMALL), os.path.join(imgdir, "image.png"))
    shutil.copyfile(os.path.join(TEST_DATA, TEST_MASK_SMALL), os.path.join(maskdir, "image.png"))
    # Run the naive Bayes training module
    outfile = os.path.join(cache_dir, "naive_bayes_pdfs.txt")
    plantcv.learn.naive_bayes(imgdir=imgdir, maskdir=maskdir, outfile=outfile, mkplots=True)
    assert os.path.exists(outfile)


def test_plantcv_learn_naive_bayes_multiclass():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_learn_naive_bayes_multiclass")
    os.mkdir(cache_dir)
    # Run the naive Bayes multiclass training module
    outfile = os.path.join(cache_dir, "naive_bayes_multiclass_pdfs.txt")
    plantcv.learn.naive_bayes_multiclass(samples_file=os.path.join(TEST_DATA, TEST_SAMPLED_RGB_POINTS), outfile=outfile,
                                         mkplots=True)
    assert os.path.exists(outfile)


# ####################################
# Tests for the morphology subpackage
# ####################################
def test_plantcv_morphology_segment_curvature():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_curvature")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = "print"
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    pcv.outputs.clear()
    _ = pcv.morphology.segment_curvature(segmented_img, seg_objects, label="prefix")
    pcv.params.debug = "plot"
    pcv.outputs.clear()
    _ = pcv.morphology.segment_curvature(segmented_img, seg_objects)
    assert len(pcv.outputs.observations['default']['segment_curvature']['value']) == 22


def test_plantcv_morphology_check_cycles():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_branches")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.check_cycles(mask, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.check_cycles(mask)
    pcv.params.debug = None
    _ = pcv.morphology.check_cycles(mask)
    assert pcv.outputs.observations['default']['num_cycles']['value'] == 1


def test_plantcv_morphology_find_branch_pts():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_branches")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.find_branch_pts(skel_img=skeleton, mask=mask, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.find_branch_pts(skel_img=skeleton)
    pcv.params.debug = None
    branches = pcv.morphology.find_branch_pts(skel_img=skeleton)
    assert np.sum(branches) == 9435


def test_plantcv_morphology_find_tips():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_tips")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.find_tips(skel_img=skeleton, mask=mask, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.find_tips(skel_img=skeleton)
    pcv.params.debug = None
    tips = pcv.morphology.find_tips(skel_img=skeleton)
    assert np.sum(tips) == 9435


def test_plantcv_morphology_prune():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_pruned")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.prune(skel_img=skeleton, size=1)
    pcv.params.debug = "plot"
    _ = pcv.morphology.prune(skel_img=skeleton, size=1, mask=skeleton)
    pcv.params.debug = None
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_prune_size0():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_pruned")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img, _, _ = pcv.morphology.prune(skel_img=skeleton, size=0)
    assert np.sum(pruned_img) == np.sum(skeleton)


def test_plantcv_morphology_iterative_prune():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_pruned")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned_img = pcv.morphology._iterative_prune(skel_img=skeleton, size=3)
    assert np.sum(pruned_img) < np.sum(skeleton)


def test_plantcv_morphology_segment_skeleton():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_skeleton")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.segment_skeleton(skel_img=skeleton, mask=mask)
    pcv.params.debug = "plot"
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    assert len(segment_objects) == 73


def test_plantcv_morphology_fill_segments():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj)
    tests = [pcv.outputs.observations['default']['segment_area']['value'][42] == 5529,
             pcv.outputs.observations['default']['segment_area']['value'][20] == 5057,
             pcv.outputs.observations['default']['segment_area']['value'][49] == 3323]
    assert all(tests)


def test_plantcv_morphology_fill_segments_with_stem():
    # Clear previous outputs
    pcv.outputs.clear()
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    obj_dic = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS))
    obj = []
    for key, val in obj_dic.items():
        obj.append(val)

    stem_obj = obj[0:4]
    pcv.params.debug = None
    _ = pcv.morphology.fill_segments(mask, obj, stem_obj)
    num_objects = len(pcv.outputs.observations['default']['leaf_area']['value'])
    assert num_objects == 69


def test_plantcv_morphology_segment_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_angles")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = "print"
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img=segmented_img, objects=segment_objects, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.segment_angle(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 22


def test_plantcv_morphology_segment_angle_overflow():
    # Clear previous outputs
    pcv.outputs.clear()
    # Don't prune, would usually give overflow error without extra if statement in segment_angle
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_angles")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_angle(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_angle']['value']) == 73


def test_plantcv_morphology_segment_euclidean_length():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_eu_length")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = "print"
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_eu_length']['value']) == 22


def test_plantcv_morphology_segment_euclidean_length_bad_input():
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    skel = pcv.morphology.skeletonize(mask=mask)
    pcv.params.debug = None
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_euclidean_length(segmented_img, segment_objects)


def test_plantcv_morphology_segment_path_length():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_path_length")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    pcv.params.debug = "print"
    segmented_img, segment_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    _ = pcv.morphology.segment_path_length(segmented_img, segment_objects, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.segment_path_length(segmented_img, segment_objects)
    assert len(pcv.outputs.observations['default']['segment_path_length']['value']) == 22


def test_plantcv_morphology_skeletonize():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_skeletonize")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    input_skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pcv.params.debug = "print"
    _ = pcv.morphology.skeletonize(mask=mask)
    pcv.params.debug = "plot"
    _ = pcv.morphology.skeletonize(mask=mask)
    pcv.params.debug = None
    skeleton = pcv.morphology.skeletonize(mask=mask)
    arr = np.array(skeleton == input_skeleton)
    assert arr.all()


def test_plantcv_morphology_segment_sort():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_sort")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skeleton)
    pcv.params.debug = "print"
    _ = pcv.morphology.segment_sort(skeleton, seg_objects, mask=skeleton)
    pcv.params.debug = "plot"
    leaf_obj, stem_obj = pcv.morphology.segment_sort(skeleton, seg_objects)
    assert len(leaf_obj) == 36


def test_plantcv_morphology_segment_tangent_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_tangent_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    pcv.params.debug = "print"
    _ = pcv.morphology.segment_tangent_angle(skel, objs, 2, label="prefix")
    pcv.params.debug = "plot"
    _ = pcv.morphology.segment_tangent_angle(skel, objs, 2)
    assert len(pcv.outputs.observations['default']['segment_tangent_angle']['value']) == 73


def test_plantcv_morphology_segment_id():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_tangent_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    objects = np.load(os.path.join(TEST_DATA, TEST_SKELETON_OBJECTS), encoding="latin1")
    objs = [objects[arr_n] for arr_n in objects]
    pcv.params.debug = "print"
    _ = pcv.morphology.segment_id(skel, objs)
    pcv.params.debug = "plot"
    _, labeled_img = pcv.morphology.segment_id(skel, objs, mask=skel)
    assert np.sum(labeled_img) > np.sum(skel)


def test_plantcv_morphology_segment_insertion_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_insertion_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    pcv.params.debug = "plot"
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 3, label="prefix")
    pcv.params.debug = "print"
    _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)
    assert pcv.outputs.observations['default']['segment_insertion_angle']['value'][:6] == ['NA', 'NA', 'NA',
                                                                                           24.956918822001636,
                                                                                           50.7313343343401,
                                                                                           56.427712102130734]


def test_plantcv_morphology_segment_insertion_angle_bad_stem():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_insertion_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    stem_obj = [leaf_obj[0], leaf_obj[10]]
    with pytest.raises(RuntimeError):
        _ = pcv.morphology.segment_insertion_angle(pruned, segmented_img, leaf_obj, stem_obj, 10)


def test_plantcv_morphology_segment_combine():
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    pcv.params.debug = "plot"
    # Test with list of IDs input
    _, new_objects = pcv.morphology.segment_combine([0, 1], seg_objects, skel)
    assert len(new_objects) + 1 == len(seg_objects)


def test_plantcv_morphology_segment_combine_lists():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_insertion_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    pcv.params.debug = "print"
    # Test with list of lists input
    _, new_objects = pcv.morphology.segment_combine([[0, 1, 2], [3, 4]], seg_objects, skel)
    assert len(new_objects) + 3 == len(seg_objects)


def test_plantcv_morphology_segment_combine_bad_input():
    skel = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON_PRUNED), -1)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=skel)
    pcv.params.debug = "plot"
    with pytest.raises(RuntimeError):
        _, new_objects = pcv.morphology.segment_combine([0.5, 1.5], seg_objects, skel)


def test_plantcv_morphology_analyze_stem():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_analyze_stem")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, segmented_img, _ = pcv.morphology.prune(skel_img=skeleton, size=6)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    leaf_obj, stem_obj = pcv.morphology.segment_sort(pruned, seg_objects)
    pcv.params.debug = "plot"
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj, label="prefix")
    pcv.params.debug = "print"
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == -12.531776428222656


def test_plantcv_morphology_analyze_stem_bad_angle():
    # Clear previous outputs
    pcv.outputs.clear()
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_morphology_segment_insertion_angle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    skeleton = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_SKELETON), -1)
    pruned, _, _ = pcv.morphology.prune(skel_img=skeleton, size=5)
    segmented_img, seg_objects = pcv.morphology.segment_skeleton(skel_img=pruned)
    _, _ = pcv.morphology.segment_sort(pruned, seg_objects)
    # print([stem_obj[3]])
    # stem_obj = [stem_obj[3]]
    stem_obj = [[[[1116, 1728]], [[1116, 1]]]]
    _ = pcv.morphology.analyze_stem(rgb_img=segmented_img, stem_objects=stem_obj)
    assert pcv.outputs.observations['default']['stem_angle']['value'] == 22877334.0


# ########################################
# Tests for the hyperspectral subpackage
# ########################################
def test_plantcv_hyperspectral_read_data_default():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_read_data_default")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = "plot"
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    _ = pcv.hyperspectral.read_data(filename=spectral_filename)
    pcv.params.debug = "print"
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_plantcv_hyperspectral_read_data_no_default_bands():
    pcv.params.debug = "plot"
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA_NO_DEFAULT)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_plantcv_hyperspectral_read_data_approx_pseudorgb():
    pcv.params.debug = "plot"
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA_APPROX_PSEUDO)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    assert np.shape(array_data.array_data) == (1, 1600, 978)


def test_plantcv_hyperspectral_read_data_bad_interleave():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA_BAD_INTERLEAVE)
    with pytest.raises(RuntimeError):
        _ = pcv.hyperspectral.read_data(filename=spectral_filename)


def test_plantcv_spectral_index_ndvi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_ndvi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ndvi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_ndvi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ndvi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.ndvi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_gdvi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_gdvi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.gdvi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_gdvi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.gdvi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.gdvi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_savi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_savi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_savi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.savi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_pri():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_pri")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pri(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_pri_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pri(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.pri(hsi=index_array, distance=20)


def test_plantcv_spectral_index_ari():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_ari")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ari(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_ari_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ari(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.ari(hsi=index_array, distance=20)


def test_plantcv_spectral_index_ci_rededge():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_ci_rededge")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ci_rededge(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_ci_rededge_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ci_rededge(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.ci_rededge(hsi=index_array, distance=20)


def test_plantcv_spectral_index_cri550():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_cri550")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.cri550(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_cri550_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.cri550(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.cri550(hsi=index_array, distance=20)


def test_plantcv_spectral_index_cri700():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_cri700")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.cri700(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_cri700_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.cri700(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.cri700(hsi=index_array, distance=20)


def test_plantcv_spectral_index_egi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_egi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    index_array = pcv.spectral_index.egi(rgb_img=rgb_img)
    assert np.shape(index_array.array_data) == (2056, 2454) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_evi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_evi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.evi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_evi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.evi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.evi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_mari():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_mari")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mari(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_mari_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mari(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.mari(hsi=index_array, distance=20)


def test_plantcv_spectral_index_mcari():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_mcari")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mcari(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_mcari_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mcari(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.mcari(hsi=index_array, distance=20)


def test_plantcv_spectral_index_mtci():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_mtci")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mtci(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_mtci_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.mtci(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.mtci(hsi=index_array, distance=20)


def test_plantcv_spectral_index_ndre():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_ndre")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ndre(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_ndre_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.ndre(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.ndre(hsi=index_array, distance=20)


def test_plantcv_spectral_index_psnd_chla():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_psnd_chla")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_chla(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_psnd_chla_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_chla(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.psnd_chla(hsi=index_array, distance=20)


def test_plantcv_spectral_index_psnd_chlb():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_psnd_chlb")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_chlb(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_psnd_chlb_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_chlb(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.psnd_chlb(hsi=index_array, distance=20)


def test_plantcv_spectral_index_psnd_car():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_psnd_car")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_car(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_psnd_car_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psnd_car(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.psnd_car(hsi=index_array, distance=20)


def test_plantcv_spectral_index_psri():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_psri")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psri(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_psri_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.psri(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.psri(hsi=index_array, distance=20)


def test_plantcv_spectral_index_pssr_chla():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_pssr_chla")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_chla(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_pssr_chla_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_chla(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.pssr_chla(hsi=index_array, distance=20)


def test_plantcv_spectral_index_pssr_chlb():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_pssr_chlb")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_chlb(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_pssr_chlb_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_chlb(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.pssr_chlb(hsi=index_array, distance=20)


def test_plantcv_spectral_index_pssr_car():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_pssr_car")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_car(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_pssr_car_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.pssr_car(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.pssr_car(hsi=index_array, distance=20)


def test_plantcv_spectral_index_rgri():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_rgri")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.rgri(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_rgri_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.rgri(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.rgri(hsi=index_array, distance=20)


def test_plantcv_spectral_index_rvsi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_rvsi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.rvsi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_rvsi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.rvsi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.rvsi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_sipi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_sipi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.sipi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_sipi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.sipi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.sipi(hsi=index_array, distance=20)


def test_plantcv_spectral_index_sr():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_sr")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.sr(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_sr_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.sr(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.sr(hsi=index_array, distance=20)


def test_plantcv_spectral_index_vari():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_vari")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.vari(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_vari_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.vari(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.vari(hsi=index_array, distance=20)


def test_plantcv_spectral_index_vi_green():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_vi_green")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.vi_green(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_vi_green_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.vi_green(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.vi_green(hsi=index_array, distance=20)


def test_plantcv_spectral_index_wi():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_index_wi")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.wi(hsi=array_data, distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_plantcv_spectral_index_wi_bad_input():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    pcv.params.debug = None
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.wi(hsi=array_data, distance=20)
    with pytest.raises(RuntimeError):
        _ = pcv.spectral_index.wi(hsi=index_array, distance=20)


def test_plantcv_hyperspectral_analyze_spectral():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_analyze_spectral")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    mask = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK), -1)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    # pcv.params.debug = "plot"
    # _ = pcv.hyperspectral.analyze_spectral(array=array_data, mask=mask, histplot=True)
    # pcv.params.debug = "print"
    # _ = pcv.hyperspectral.analyze_spectral(array=array_data, mask=mask, histplot=True, label="prefix")
    pcv.params.debug = None
    _ = pcv.hyperspectral.analyze_spectral(array=array_data, mask=mask, histplot=True, label="prefix")
    assert len(pcv.outputs.observations['prefix']['spectral_frequencies']['value']) == 978


def test_plantcv_hyperspectral_analyze_index():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_analyze_index")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    # pcv.params.debug = "print"
    # pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, histplot=True)
    # pcv.params.debug = "plot"
    # pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, histplot=True)

    pcv.params.debug = None
    pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, histplot=True)

    assert pcv.outputs.observations['default']['mean_index_savi']['value'] > 0


def test_plantcv_hyperspectral_analyze_index_set_range():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_analyze_index_set_range")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    pcv.params.debug = None
    pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, histplot=True, min_bin=0, max_bin=1)
    assert pcv.outputs.observations['default']['mean_index_savi']['value'] > 0


def test_plantcv_hyperspectral_analyze_index_auto_range():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_analyze_index_auto_range")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    pcv.params.debug = None
    pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, min_bin="auto", max_bin="auto")
    assert pcv.outputs.observations['default']['mean_index_savi']['value'] > 0


def test_plantcv_hyperspectral_analyze_index_outside_range_warning():
    import io
    from contextlib import redirect_stdout
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_analyze_index_auto_range")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = np.ones(np.shape(index_array.array_data), dtype=np.uint8) * 255
    f = io.StringIO()
    with redirect_stdout(f):
        pcv.params.debug = None
        pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img, min_bin=.5, max_bin=.55, label="i")
    out = f.getvalue()
    # assert os.listdir(cache_dir) is 0
    assert out[0:10] == 'WARNING!!!'


def test_plantcv_hyperspectral_analyze_index_bad_input_mask():
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK))
    with pytest.raises(RuntimeError):
        pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img)


def test_plantcv_hyperspectral_analyze_index_bad_input_index():
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    index_array = pcv.spectral_index.savi(hsi=array_data, distance=801)
    mask_img = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK), -1)
    index_array.array_data = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK))
    with pytest.raises(RuntimeError):
        pcv.hyperspectral.analyze_index(index_array=index_array, mask=mask_img)


def test_plantcv_hyperspectral_analyze_index_bad_input_datatype():
    pcv.params.debug = None
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array_data = pcv.hyperspectral.read_data(filename=spectral_filename)
    mask_img = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK), -1)
    with pytest.raises(RuntimeError):
        pcv.hyperspectral.analyze_index(index_array=array_data, mask=mask_img)


def test_plantcv_hyperspectral_calibrate():
    raw = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    white = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_WHITE)
    dark = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DARK)
    raw = pcv.hyperspectral.read_data(filename=raw)
    white = pcv.hyperspectral.read_data(filename=white)
    dark = pcv.hyperspectral.read_data(filename=dark)
    calibrated = pcv.hyperspectral.calibrate(raw_data=raw, white_reference=white, dark_reference=dark)
    assert np.shape(calibrated.array_data) == (1, 1600, 978)


def test_plantcv_hyperspectral_extract_wavelength():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_hyperspectral_extract_wavelength")
    os.mkdir(cache_dir)
    spectral = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    spectral = pcv.hyperspectral.read_data(filename=spectral)
    pcv.params.debug = "plot"
    _ = pcv.hyperspectral.extract_wavelength(spectral_data=spectral, wavelength=500)
    pcv.params.debug = "print"
    new = pcv.hyperspectral.extract_wavelength(spectral_data=spectral, wavelength=500)
    assert np.shape(new.array_data) == (1, 1600)


def test_plantcv_hyperspectral_avg_reflectance():
    spectral = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    mask_img = cv2.imread(os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_MASK), -1)
    spectral = pcv.hyperspectral.read_data(filename=spectral)
    avg_reflect = pcv.hyperspectral._avg_reflectance(spectral, mask=mask_img)
    assert len(avg_reflect) == 978


def test_plantcv_hyperspectral_inverse_covariance():
    spectral = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    spectral = pcv.hyperspectral.read_data(filename=spectral)
    inv_cov = pcv.hyperspectral._inverse_covariance(spectral)
    assert np.shape(inv_cov) == (978, 978)


# ########################################
# Tests for the photosynthesis subpackage
# ########################################
def test_plantcv_photosynthesis_read_dat():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_photosynthesis_read_dat")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    pcv.params.debug = "plot"
    fluor_filename = os.path.join(FLUOR_TEST_DATA, FLUOR_IMG)
    _, _, _ = pcv.photosynthesis.read_cropreporter(filename=fluor_filename)
    pcv.params.debug = "print"
    fdark, fmin, fmax = pcv.photosynthesis.read_cropreporter(filename=fluor_filename)
    assert np.sum(fmin) < np.sum(fmax)


def test_plantcv_photosynthesis_analyze_fvfm():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # filename = os.path.join(cache_dir, 'plantcv_fvfm_hist.png')
    # Read in test data
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000, label="prefix")
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    fvfm_images = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    assert len(fvfm_images) != 0


def test_plantcv_photosynthesis_analyze_fvfm_print_analysis_results():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    result_file = os.path.join(cache_dir, "results.txt")
    pcv.print_results(result_file)
    pcv.outputs.clear()
    assert os.path.exists(result_file)


def test_plantcv_photosynthesis_analyze_fvfm_bad_fdark():
    # Clear previous outputs
    pcv.outputs.clear()
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_analyze_fvfm")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FDARK), -1)
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark + 3000, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)
    check = pcv.outputs.observations['default']['fdark_passed_qc']['value'] is False
    assert check


def test_plantcv_photosynthesis_analyze_fvfm_bad_input():
    fdark = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    fmin = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMIN), -1)
    fmax = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMAX), -1)
    fmask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_FMASK), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.photosynthesis.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=fmask, bins=1000)


# ##############################
# Tests for the roi subpackage
# ##############################
def test_plantcv_roi_from_binary_image():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_from_binary_image")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Create a binary image
    bin_img = np.zeros(np.shape(rgb_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (1000, 1000), 255, -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.from_binary_image(bin_img=bin_img, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 3600, 1, 2)


def test_plantcv_roi_from_binary_image_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Create a binary image
    bin_img = np.zeros(np.shape(gray_img)[0:2], dtype=np.uint8)
    cv2.rectangle(bin_img, (100, 100), (1000, 1000), 255, -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.from_binary_image(bin_img=bin_img, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 3600, 1, 2)


def test_plantcv_roi_from_binary_image_bad_binary_input():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Binary input is required but an RGB input is provided
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.from_binary_image(bin_img=rgb_img, img=rgb_img)


def test_plantcv_roi_rectangle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_rectangle")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 4, 1, 2)


def test_plantcv_roi_rectangle_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.rectangle(x=100, y=100, h=500, w=500, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 4, 1, 2)


def test_plantcv_roi_rectangle_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.rectangle(x=100, y=100, h=500, w=3000, img=rgb_img)


def test_plantcv_roi_circle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_circle")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.circle(x=100, y=100, r=50, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.circle(x=100, y=100, r=50, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.circle(x=200, y=225, r=75, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 424, 1, 2)


def test_plantcv_roi_circle_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.circle(x=200, y=225, r=75, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 424, 1, 2)


def test_plantcv_roi_circle_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.circle(x=50, y=225, r=75, img=rgb_img)


def test_plantcv_roi_ellipse():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_roi_ellipse")
    os.mkdir(cache_dir)
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = cache_dir
    _, _ = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _ = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Test with debug = None
    pcv.params.debug = None
    roi_contour, roi_hierarchy = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=rgb_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 360, 1, 2)


def test_plantcv_roi_ellipse_grayscale_input():
    # Read in a test grayscale image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    roi_contour, roi_hierarchy = pcv.roi.ellipse(x=200, y=200, r1=75, r2=50, angle=0, img=gray_img)
    # Assert the contours and hierarchy lists contain only the ROI
    assert np.shape(roi_contour) == (1, 360, 1, 2)


def test_plantcv_roi_ellipse_out_of_frame():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The resulting rectangle needs to be within the dimensions of the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.ellipse(x=50, y=225, r1=75, r2=50, angle=0, img=rgb_img)


def test_plantcv_roi_multi():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.roi.multi(rgb_img, coord=[(25, 120), (100, 100)], radius=20)
    # Test with debug = None
    pcv.params.debug = None
    rois1, roi_hierarchy1 = pcv.roi.multi(rgb_img, coord=(25, 120), radius=20, spacing=(10, 10), nrows=3, ncols=6)
    # Assert the contours has 18 ROIs
    assert len(rois1) == 18


def test_plantcv_roi_multi_bad_input():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # The user must input a list of custom coordinates OR inputs to make a grid. Not both
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.multi(rgb_img, coord=[(25, 120), (100, 100)], radius=20, spacing=(10, 10), nrows=3, ncols=6)


def test_plantcv_roi_multi_bad_input_oob():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # nputs to make a grid make ROIs that go off the screen
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.multi(rgb_img, coord=(25000, 12000), radius=2, spacing=(1, 1), nrows=3, ncols=6)


def test_plantcv_roi_multi_bad_input_oob_list():
    # Read in test RGB image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # All vertices in the list of centers must draw roi's that are inside the image
    with pytest.raises(RuntimeError):
        _, _ = pcv.roi.multi(rgb_img, coord=[(25000, 25000), (25000, 12000), (12000, 12000)], radius=20)


def test_plantcv_roi_custom():
    # Read in test RGB image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = "plot"
    cnt, hier = pcv.roi.custom(img=img, vertices=[[226, 1], [313, 184], [240, 202], [220, 229], [161, 171]])
    assert np.shape(cnt) == (1, 5, 2)


def test_plantcv_roi_custom_bad_input():
    # Read in test RGB image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # ROI goes out of bounds
    with pytest.raises(RuntimeError):
        _ = pcv.roi.custom(img=img, vertices=[[226, -1], [3130, 1848], [2404, 2029], [2205, 2298], [1617, 1761]])


# ##############################
# Tests for the transform subpackage
# ##############################
def test_plantcv_transform_get_color_matrix():
    # load in target_matrix
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # Read in rgb_img and gray-scale mask
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    # The result should be a len(np.unique(mask))-1 x 4 matrix
    headers, matrix = pcv.transform.get_color_matrix(rgb_img, mask)
    assert np.array_equal(matrix, matrix_compare)


def test_plantcv_transform_get_color_matrix_img():
    # Read in two gray-scale images
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.get_color_matrix(rgb_img, mask)


def test_plantcv_transform_get_color_matrix_mask():
    # Read in two gray-scale images
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK))
    # The input for rgb_img needs to be an RGB image
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.get_color_matrix(rgb_img, mask)


def test_plantcv_transform_get_matrix_m():
    # load in comparison matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_compare_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_compare_b = matrix_b_file['arr_0']
    # read in matrices
    t_matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    t_matrix = t_matrix_file['arr_0']
    s_matrix_file = np.load(os.path.join(TEST_DATA, TEST_SOURCE1_MATRIX), encoding="latin1")
    s_matrix = s_matrix_file['arr_0']
    # apply matrices to function
    matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_plantcv_transform_get_matrix_m_unequal_data():
    # load in comparison matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M2), encoding="latin1")
    matrix_compare_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B2), encoding="latin1")
    matrix_compare_b = matrix_b_file['arr_0']
    # read in matrices
    t_matrix_file = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    t_matrix = t_matrix_file['arr_0']
    s_matrix_file = np.load(os.path.join(TEST_DATA, TEST_SOURCE2_MATRIX), encoding="latin1")
    s_matrix = s_matrix_file['arr_0']
    # apply matrices to function
    matrix_a, matrix_m, matrix_b = pcv.transform.get_matrix_m(t_matrix, s_matrix)
    matrix_compare_m = np.rint(matrix_compare_m)
    matrix_compare_b = np.rint(matrix_compare_b)
    matrix_m = np.rint(matrix_m)
    matrix_b = np.rint(matrix_b)
    assert np.array_equal(matrix_m, matrix_compare_m) and np.array_equal(matrix_b, matrix_compare_b)


def test_plantcv_transform_calc_transformation_matrix():
    # load in comparison matrices
    matrix_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_compare = matrix_file['arr_0']
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    # apply to function
    _, matrix_t = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b)
    matrix_t = np.rint(matrix_t)
    matrix_compare = np.rint(matrix_compare)
    assert np.array_equal(matrix_t, matrix_compare)


def test_plantcv_transform_calc_transformation_matrix_b_incorrect():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    matrix_b = np.asmatrix(matrix_b, float)
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b.T)


def test_plantcv_transform_calc_transformation_matrix_not_mult():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m, matrix_b[:3])


def test_plantcv_transform_calc_transformation_matrix_not_mat():
    # read in matrices
    matrix_m_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_M1), encoding="latin1")
    matrix_m = matrix_m_file['arr_0']
    matrix_b_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_b = matrix_b_file['arr_0']
    with pytest.raises(RuntimeError):
        _, _ = pcv.transform.calc_transformation_matrix(matrix_m[:, 1], matrix_b[:, 1])


def test_plantcv_transform_apply_transformation():
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # Test with debug = None
    pcv.params.debug = None
    corrected_img = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)
    # assert source and corrected have same shape
    assert np.array_equal(corrected_img, corrected_compare)


def test_plantcv_transform_apply_transformation_incorrect_t():
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_MATRIX_B1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    with pytest.raises(RuntimeError):
        _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)


def test_plantcv_transform_apply_transformation_incorrect_img():
    # read in matrices
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # read in images
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.transform.apply_transformation_matrix(source_img, target_img, matrix_t)


def test_plantcv_transform_save_matrix():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # read in matrix
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # .npz filename
    filename = os.path.join(cache_dir, 'test.npz')
    pcv.transform.save_matrix(matrix_t, filename)
    assert os.path.exists(filename) is True


def test_plantcv_transform_save_matrix_incorrect_filename():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # read in matrix
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # .npz filename
    filename = "test"
    with pytest.raises(RuntimeError):
        pcv.transform.save_matrix(matrix_t, filename)


def test_plantcv_transform_load_matrix():
    # read in matrix_t
    matrix_t_file = np.load(os.path.join(TEST_DATA, TEST_TRANSFORM1), encoding="latin1")
    matrix_t = matrix_t_file['arr_0']
    # test load function with matrix_t
    matrix_t_loaded = pcv.transform.load_matrix(os.path.join(TEST_DATA, TEST_TRANSFORM1))
    assert np.array_equal(matrix_t, matrix_t_loaded)


def test_plantcv_transform_correct_color():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform")
    os.mkdir(cache_dir)
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_correct_color")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    matdir = os.path.join(cache_dir, "saved_matrices")
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    output_path = os.path.join(matdir)
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, cache_dir)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = None
    pcv.params.debug = None
    _, _, matrix_t, corrected_img = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # assert source and corrected have same shape
    assert all([np.array_equal(corrected_img, corrected_compare),
                os.path.exists(os.path.join(output_path, "target_matrix.npz")) is True,
                os.path.exists(os.path.join(output_path, "source_matrix.npz")) is True,
                os.path.exists(os.path.join(output_path, "transformation_matrix.npz")) is True])


def test_plantcv_transform_correct_color_output_dne():
    # load corrected image to compare
    corrected_compare = cv2.imread(os.path.join(TEST_DATA, TEST_S1_CORRECTED))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_correct_color_output_dne")
    os.mkdir(cache_dir)
    # Make image and mask directories in the cache directory
    imgdir = os.path.join(cache_dir, "images")
    # Read in target, source, and gray-scale mask
    target_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    source_img = cv2.imread(os.path.join(TEST_DATA, TEST_SOURCE1_IMG))
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_MASK), -1)
    output_path = os.path.join(cache_dir, "saved_matrices_1")  # output_directory that does not currently exist
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.params.debug_outdir = imgdir
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _, _, _, _ = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # Test with debug = None
    pcv.params.debug = None
    _, _, matrix_t, corrected_img = pcv.transform.correct_color(target_img, mask, source_img, mask, output_path)
    # assert source and corrected have same shape
    assert all([np.array_equal(corrected_img, corrected_compare),
                os.path.exists(os.path.join(output_path, "target_matrix.npz")) is True,
                os.path.exists(os.path.join(output_path, "source_matrix.npz")) is True,
                os.path.exists(os.path.join(output_path, "transformation_matrix.npz")) is True])


def test_plantcv_transform_create_color_card_mask():
    # Load target image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_create_color_card_mask")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                             spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                             spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=(166, 166),
                                                spacing=(21, 21), nrows=6, ncols=4, exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_plantcv_transform_quick_color_check():
    # Load target image
    t_matrix = np.load(os.path.join(TEST_DATA, TEST_TARGET_MATRIX), encoding="latin1")
    target_matrix = t_matrix['arr_0']
    s_matrix = np.load(os.path.join(TEST_DATA, TEST_SOURCE1_MATRIX), encoding="latin1")
    source_matrix = s_matrix['arr_0']
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_quick_color_check")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with debug = "print"
    pcv.params.debug = "print"
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    # Test with debug = None
    pcv.params.debug = None
    pcv.transform.quick_color_check(target_matrix, source_matrix, num_chips=22)
    assert os.path.exists(os.path.join(cache_dir, "color_quick_check.png"))


def test_plantcv_transform_find_color_card():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    df, start, space = pcv.transform.find_color_card(rgb_img=rgb_img, threshold_type='adaptgauss', blurry=False,
                                                     threshvalue=90)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                             spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = "plot"
    pcv.params.debug = "plot"
    _ = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                             spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    # Test with debug = None
    pcv.params.debug = None
    mask = pcv.transform.create_color_card_mask(rgb_img=rgb_img, radius=6, start_coord=start,
                                                spacing=space, nrows=6, ncols=4, exclude=[20, 0])
    assert all([i == j] for i, j in zip(np.unique(mask), np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                                                                   120, 130, 140, 150, 160, 170, 180, 190, 200, 210,
                                                                   220], dtype=np.uint8)))


def test_plantcv_transform_find_color_card_optional_parameters():
    # Clear previous outputs
    pcv.outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with threshold ='normal'
    df1, start1, space1 = pcv.transform.find_color_card(rgb_img=rgb_img, threshold_type='normal', blurry=True,
                                                        background='light', threshvalue=90, label="prefix")
    assert pcv.outputs.observations["prefix"]["color_chip_size"]["value"] > 15000


def test_plantcv_transform_find_color_card_otsu():
    # Clear previous outputs
    pcv.outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card_otsu")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Test with threshold ='normal'
    df1, start1, space1 = pcv.transform.find_color_card(rgb_img=rgb_img, threshold_type='otsu', blurry=True,
                                                        background='light', threshvalue=90, label="prefix")
    assert pcv.outputs.observations["prefix"]["color_chip_size"]["value"] > 15000


def test_plantcv_transform_find_color_card_optional_size_parameters():
    # Clear previous outputs
    pcv.outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, record_chip_size="mean")
    assert pcv.outputs.observations["default"]["color_chip_size"]["value"] > 15000


def test_plantcv_transform_find_color_card_optional_size_parameters_none():
    # Clear previous outputs
    pcv.outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_COLOR_CARD))
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_find_color_card")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, record_chip_size=None)
    assert pcv.outputs.observations.get("default") is None


def test_plantcv_transform_find_color_card_bad_record_chip_size():
    # Clear previous outputs
    pcv.outputs.clear()
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    pcv.params.debug = None
    _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, record_chip_size='averageeeed')
    assert pcv.outputs.observations["default"]["color_chip_size"]["value"] is None


def test_plantcv_transform_find_color_card_bad_thresh_input():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, threshold_type='gaussian')


def test_plantcv_transform_find_color_card_bad_background_input():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img, background='lite')


def test_plantcv_transform_find_color_card_bad_colorcard():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG_WITH_HEXAGON))
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _, _, _ = pcv.transform.find_color_card(rgb_img=rgb_img)


def test_plantcv_transform_rescale():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_rescale")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = "print"
    pcv.params.debug = "print"
    _ = pcv.transform.rescale(gray_img=gray_img, min_value=0, max_value=100)
    pcv.params.debug = "plot"
    rescaled_img = pcv.transform.rescale(gray_img=gray_img, min_value=0, max_value=100)
    assert max(np.unique(rescaled_img)) == 100


def test_plantcv_transform_rescale_bad_input():
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    with pytest.raises(RuntimeError):
        _ = pcv.transform.rescale(gray_img=rgb_img)


def test_plantcv_transform_resize():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_trancform_resize")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    size = (100, 100)
    # Test with debug "print"
    pcv.params.debug = "print"
    _ = pcv.transform.resize(img=gray_img, size=size, interpolation="auto")
    # Test with debug "plot"
    pcv.params.debug = "plot"
    resized_img = pcv.transform.resize(img=gray_img, size=size, interpolation="auto")
    assert resized_img.shape == size


def test_plantcv_transform_resize_unsupported_method():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.transform.resize(img=gray_img, size=(100, 100), interpolation="mymethod")


def test_plantcv_transform_resize_crop():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    size = (20, 20)
    resized_im = pcv.transform.resize(img=gray_img, size=size, interpolation=None)
    assert resized_im.shape == size


def test_plantcv_transform_resize_pad():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    size = (100, 100)
    resized_im = pcv.transform.resize(img=gray_img, size=size, interpolation=None)
    assert resized_im.shape == size


def test_plantcv_transform_resize_pad_crop_color():
    color_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL))
    size = (100, 100)
    resized_im = pcv.transform.resize(img=color_img, size=size, interpolation=None)
    assert resized_im.shape == (size[1], size[0], 3)


def test_plantcv_transform_resize_factor():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_trancform_resize_factor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    # Resizing factors
    factor_x = 0.5
    factor_y = 0.2
    # Test with debug "print"
    pcv.params.debug = "print"
    _ = pcv.transform.resize_factor(img=gray_img, factors=(factor_x, factor_y), interpolation="auto")
    # Test with debug "plot"
    pcv.params.debug = "plot"
    resized_img = pcv.transform.resize_factor(img=gray_img, factors=(factor_x, factor_y), interpolation="auto")
    output_size = resized_img.shape
    expected_size = (int(gray_img.shape[0] * factor_y), int(gray_img.shape[1] * factor_x))
    assert output_size == expected_size


def test_plantcv_transform_resize_factor_bad_input():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.transform.resize_factor(img=gray_img, factors=(0, 2), interpolation="auto")


def test_plantcv_transform_nonuniform_illumination_rgb():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_nonuniform_illumination")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Load rgb image
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_TARGET_IMG))
    pcv.params.debug = "plot"
    _ = pcv.transform.nonuniform_illumination(img=rgb_img, ksize=11)
    pcv.params.debug = "print"
    corrected = pcv.transform.nonuniform_illumination(img=rgb_img, ksize=11)
    assert np.mean(corrected) < np.mean(rgb_img)


def test_plantcv_transform_nonuniform_illumination_gray():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_transform_nonuniform_illumination")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Load rgb image
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    pcv.params.debug = "plot"
    _ = pcv.transform.nonuniform_illumination(img=gray_img, ksize=11)
    pcv.params.debug = "print"
    corrected = pcv.transform.nonuniform_illumination(img=gray_img, ksize=11)
    assert np.shape(corrected) == np.shape(gray_img)


def test_plantcv_transform_warp_default():
    pcv.params.debug = "plot"
    img = create_test_img((12, 10, 3))
    refimg = create_test_img((12, 10, 3))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    warped_img, mat = pcv.transform.warp(img, refimg, pts, refpts, method="default")
    assert mat.shape == (3, 3)


def test_plantcv_transform_warp_lmeds():
    pcv.params.debug = "plot"
    img = create_test_img((10, 10, 3))
    refimg = create_test_img((11, 11))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    warped_img, mat = pcv.transform.warp(img, refimg, pts, refpts, method="lmeds")
    assert mat.shape == (3, 3)


def test_plantcv_transform_warp_rho():
    pcv.params.debug = "plot"
    img = create_test_img_bin((10, 10))
    refimg = create_test_img((11, 11))
    pts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    refpts = [(0, 0), (1, 0), (0, 3), (4, 4)]
    warped_img, mat = pcv.transform.warp(img, refimg, pts, refpts, method="rho")
    assert mat.shape == (3, 3)


def test_plantcv_transform_warp_ransac():
    pcv.params.debug = "plot"
    img = create_test_img((100, 150))
    refimg = create_test_img((10, 15))
    pts = [(0, 0), (149, 0), (99, 149), (0, 99), (3, 3)]
    refpts = [(0, 0), (0, 14), (9, 14), (0, 9), (3, 3)]
    warped_img, mat = pcv.transform.warp(img, refimg, pts, refpts, method="ransac")
    assert mat.shape == (3, 3)


@pytest.mark.parametrize("pts, refpts", [
    [[(0, 0)], [(0, 0), (0, 1)]],  # different # of points provided for img and refimg
    [[(0, 0)], [(0, 0)]],  # not enough pairs of points provided
    [[(0, 0), (0, 14), (9, 14), (0, 9), (3, 3)],
     [(0, 0), (149, 0), (99, 149), (0, 99), (3, 3)]]  # homography not able to be calculated (cannot converge)
])
def test_plantcv_transform_warp_err(pts, refpts):
    img = create_test_img((10, 15))
    refimg = create_test_img((100, 150))
    method = "rho"
    with pytest.raises(RuntimeError):
        pcv.transform.warp(img, refimg, pts, refpts, method=method)


def test_plantcv_transform_warp_align():
    img = create_test_img((10, 10, 3))
    refimg = create_test_img((11, 11))
    mat = np.array([[1.00000000e+00,  1.04238500e-15, -7.69185075e-16],
                    [1.44375646e-16,  1.00000000e+00,  0.00000000e+00],
                    [-5.41315251e-16,  1.78930521e-15,  1.00000000e+00]])
    warp_img = pcv.transform.warp_align(img=img, mat=mat, refimg=refimg)
    assert warp_img.shape == (11, 11, 3)


def test_plantcv_transform_gamma_correct():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MARKER))
    # Test
    gamma_corrected = pcv.transform.gamma_correct(img=img, gamma=2, gain=1)
    imgavg = np.average(img)
    correctedavg = np.average(gamma_corrected)
    assert correctedavg != imgavg


# ##############################
# Tests for the threshold subpackage
# ##############################
@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_plantcv_threshold_binary(objtype):
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    binary_img = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_binary_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.binary(gray_img=gray_img, threshold=25, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_plantcv_threshold_gaussian(objtype):
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    binary_img = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_gaussian_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.gaussian(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_plantcv_threshold_mean(objtype):
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with object type = dark
    pcv.params.debug = None
    binary_img = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_mean_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.mean(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("objtype", ["dark", "light"])
def test_plantcv_threshold_otsu(objtype):
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GREENMAG), -1)
    # Test with object set to light
    pcv.params.debug = None
    binary_img = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type=objtype)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_otsu_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.otsu(gray_img=gray_img, max_value=255, object_type="lite")


@pytest.mark.parametrize("channel,lower_thresh,upper_thresh", [["HSV", [0, 0, 0], [255, 255, 255]],
                                                               ["LAB", [0, 0, 0], [255, 255, 255]],
                                                               ["RGB", [0, 0, 0], [255, 255, 255]],
                                                               ["GRAY", [0], [255]]])
def test_plantcv_threshold_custom_range_rgb(channel, lower_thresh, upper_thresh):
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    mask, binary_img = pcv.threshold.custom_range(img, lower_thresh=lower_thresh, upper_thresh=upper_thresh,
                                                  channel=channel)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_custom_range_grayscale():
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    # Test with debug = None
    pcv.params.debug = None
    # # Test channel='gray'
    mask, binary_img = pcv.threshold.custom_range(gray_img, lower_thresh=[0], upper_thresh=[255], channel='gray')
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_custom_range_bad_input_hsv():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _, _ = pcv.threshold.custom_range(img, lower_thresh=[0, 0], upper_thresh=[2, 2, 2, 2], channel='HSV')


def test_plantcv_threshold_custom_range_bad_input_rgb():
    # Read in test data
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _, _ = pcv.threshold.custom_range(img, lower_thresh=[0, 0], upper_thresh=[2, 2, 2, 2], channel='RGB')


def test_plantcv_threshold_custom_range_bad_input_lab():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _, _ = pcv.threshold.custom_range(img, lower_thresh=[0, 0], upper_thresh=[2, 2, 2], channel='LAB')


def test_plantcv_threshold_custom_range_bad_input_gray():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _, _ = pcv.threshold.custom_range(img, lower_thresh=[0, 0], upper_thresh=[2], channel='gray')


def test_plantcv_threshold_custom_range_bad_input_channel():
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _, _ = pcv.threshold.custom_range(img, lower_thresh=[0], upper_thresh=[2], channel='CMYK')


@pytest.mark.parametrize("channel", ["all", "any"])
def test_plantcv_threshold_saturation(channel):
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    # Test with debug = None
    pcv.params.debug = None
    thresh = pcv.threshold.saturation(rgb_img=rgb_img, threshold=254, channel=channel)
    assert len(np.unique(thresh)) == 2


def test_plantcv_threshold_saturation_bad_input():
    # Read in test data
    rgb_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.threshold.saturation(rgb_img=rgb_img, threshold=254, channel="red")


def test_plantcv_threshold_triangle():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_threshold_triangle")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)

    pcv.params.debug = None
    _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="dark", xstep=10)
    pcv.params.debug = "plot"
    _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="light", xstep=10)
    pcv.params.debug = "print"
    binary_img = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="light", xstep=10)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def test_plantcv_threshold_triangle_incorrect_object_type():
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        pcv.params.debug = None
        _ = pcv.threshold.triangle(gray_img=gray_img, max_value=255, object_type="lite", xstep=10)


def test_plantcv_threshold_texture():
    # Test with debug = None
    pcv.params.debug = None
    gray_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY_SMALL), -1)
    binary_img = pcv.threshold.texture(gray_img, ksize=6, threshold=7, offset=3, texture_method='dissimilarity',
                                       borders='nearest', max_value=255)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(binary_img), TEST_GRAY_DIM)):
        # Assert that the image is binary
        if all([i == j] for i, j in zip(np.unique(binary_img), [0, 255])):
            assert 1
        else:
            assert 0
    else:
        assert 0


def create_test_img(sz_img):
    img = np.random.randint(np.prod(sz_img), size=sz_img) * 255
    img = img.astype(np.uint8)
    return img


def create_test_img_bin(sz_img):
    img = np.zeros(sz_img)
    img[3:7, 2:8] = 1
    return img


@pytest.mark.parametrize("bad_type", ["native", "nan", "inf"])
def test_plantcv_threshold_mask_bad(bad_type):
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    bad_img[2, 2] = np.inf
    bad_img[2, 3] = np.nan
    sz = np.shape(bad_img)
    pcv.params.debug = None
    mask = pcv.threshold.mask_bad(bad_img, bad_type=bad_type)
    assert((np.shape(mask) == sz) and (len(np.unique(mask)) == 2))


def test_plantcv_threshold_mask_bad_native_bad_input():
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    sz = np.shape(bad_img)
    mask10 = pcv.threshold.mask_bad(bad_img, bad_type='native')

    assert mask10.all() == np.zeros(sz, dtype='uint8').all()


def test_plantcv_threshold_mask_bad_nan_bad_input():
    # Create a synthetic bad image
    bad_img = np.reshape(np.random.rand(25), (5, 5))
    bad_img[2, 2] = np.inf
    sz = np.shape(bad_img)
    mask11 = pcv.threshold.mask_bad(bad_img, bad_type='nan')

    assert mask11.all() == np.zeros(sz, dtype='uint8').all()


def test_plantcv_threshold_mask_bad_input_color_img():
    # Read in test data
    bad_img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        pcv.threshold.mask_bad(bad_img, bad_type='nan')


# ###################################
# Tests for the visualize subpackage
# ###################################
def test_plantcv_visualize_auto_threshold_methods_bad_input():
    # Test with debug = None
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.auto_threshold_methods(gray_img=img)


def test_plantcv_visualize_auto_threshold_methods():
    # Test with debug = None
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    labeled_imgs = pcv.visualize.auto_threshold_methods(gray_img=img)
    assert len(labeled_imgs) == 5 and np.shape(labeled_imgs[0])[0] == np.shape(img)[0]


@pytest.mark.parametrize("debug,axes", [["print", True], ["plot", False]])
def test_plantcv_visualize_pseudocolor(debug, axes, tmpdir):
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("sub")
    pcv.params.debug_outdir = cache_dir
    # Input image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    r, c = img.shape
    # generate 200 "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad = np.reshape(mask_bad, (-1, 1))
    mask_bad[0:100] = 255
    mask_bad = np.reshape(mask_bad, (r, c))
    # Debug mode
    pcv.params.debug = debug
    pseudo_img = pcv.visualize.pseudocolor(gray_img=img, mask=None, title="Pseudocolored image", axes=axes,
                                           bad_mask=mask_bad)
    # Assert that the output image has the dimensions of the input image
    assert all([i == j] for i, j in zip(np.shape(pseudo_img), TEST_BINARY_DIM))


@pytest.mark.parametrize("bkgrd,axes,pad", [["image", True, "auto"], ["white", False, 1], ["black", True, "auto"]])
def test_plantcv_visualize_pseudocolor_mask(bkgrd, axes, pad):
    # Test with debug = None
    pcv.params.debug = None
    # Input image
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Input mask
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    # Input contours
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    r, c = img.shape
    # generate 200 "bad" pixels
    mask_bad = np.zeros((r, c), dtype=np.uint8)
    mask_bad = np.reshape(mask_bad, (-1, 1))
    mask_bad[0:100] = 255
    mask_bad = np.reshape(mask_bad, (r, c))
    pseudo_img = pcv.visualize.pseudocolor(gray_img=img, obj=obj_contour, mask=mask, background=bkgrd,
                                           bad_mask=mask_bad, title="Pseudocolored image", axes=axes, obj_padding=pad)
    # Assert that the output image has the dimensions of the input image
    if all([i == j] for i, j in zip(np.shape(pseudo_img), TEST_BINARY_DIM)):
        assert 1
    else:
        assert 0


def test_plantcv_visualize_pseudocolor_bad_input():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img)


def test_plantcv_visualize_pseudocolor_bad_background():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor_bad_background")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img, mask=mask, background="pink")


def test_plantcv_visualize_pseudocolor_bad_padding():
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_pseudocolor_bad_background")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    contours_npz = np.load(os.path.join(TEST_DATA, TEST_INPUT_CONTOURS), encoding="latin1")
    obj_contour = contours_npz['arr_0']
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.pseudocolor(gray_img=img, mask=mask, obj=obj_contour, obj_padding="pink")


def test_plantcv_visualize_pseudocolor_bad_mask():
    # Test with debug = None
    pcv.params.debug = None


@pytest.mark.parametrize('colors', [['red', 'blue'], [(0, 0, 255), (255, 0, 0)]])
def test_plantcv_visualize_colorize_masks(colors):
    # Test with debug = None
    pcv.params.debug = None
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    colored_img = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=colors)
    # Assert that the output image has the dimensions of the input image
    assert not np.average(colored_img) == 0


def test_plantcv_visualize_colorize_masks_bad_input_empty():
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[], colors=[])


def test_plantcv_visualize_colorize_masks_bad_input_mismatch_number():
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=['red', 'green', 'blue'])


def test_plantcv_visualize_colorize_masks_bad_color_input():
    # Create test data
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.copy(mask1)
    mask1[0:50, 0:50] = 255
    mask2[50:100, 50:100] = 255
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorize_masks(masks=[mask1, mask2], colors=['red', 1.123])


def test_plantcv_visualize_colorize_label_img():
    label_img = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    pcv.params.debug = None
    colored_img = pcv.visualize.colorize_label_img(label_img)
    assert (colored_img.shape[0:-1] == label_img.shape) and colored_img.shape[-1] == 3


@pytest.mark.parametrize("bins,lb,ub,title", [[200, 0, 255, "Include Title"], [100, None, None, None]])
def test_plantcv_visualize_histogram(bins, lb, ub, title):
    # Test with debug = None
    pcv.params.debug = None
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    fig_hist, hist_df = pcv.visualize.histogram(img=img, mask=mask, bins=bins, lower_bound=lb, upper_bound=ub,
                                                title=title, hist_data=True)
    assert all([isinstance(fig_hist, ggplot), isinstance(hist_df, pd.core.frame.DataFrame)])


def test_plantcv_visualize_histogram_no_mask():
    # Test with debug = None
    pcv.params.debug = None
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    fig_hist = pcv.visualize.histogram(img=img, mask=None)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_rgb_img():
    # Test with debug = None
    pcv.params.debug = None
    # Test RGB input image
    img_rgb = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    fig_hist = pcv.visualize.histogram(img=img_rgb)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_multispectral_img():
    # Test with debug = None
    pcv.params.debug = None
    # Test multi-spectral image
    img_rgb = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img_multi = np.concatenate((img_rgb, img_rgb), axis=2)
    fig_hist = pcv.visualize.histogram(img=img_multi)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_histogram_no_img():
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.histogram(img=None)


def test_plantcv_visualize_histogram_array():
    # Read test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.histogram(img=img[0, :])


@pytest.mark.parametrize("wavelengths", [[], [390, 500, 640, 992, 990]])
def test_plantcv_visualize_hyper_histogram(wavelengths):
    # Test with debug = None
    pcv.params.debug = None

    # Read in test data
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    mask = np.ones((array.lines, array.samples))

    fig_hist = pcv.visualize.hyper_histogram(array, mask, wvlengths=wavelengths, title="Hyper Histogram Test")
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_hyper_histogram_wv_out_range():
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.hyper_histogram(array, wvlengths=[200,  550])


def test_plantcv_visualize_hyper_histogram_extreme_wvs():
    # Test with debug = None
    pcv.params.debug = None

    # Read in test data
    spectral_filename = os.path.join(HYPERSPECTRAL_TEST_DATA, HYPERSPECTRAL_DATA)
    array = pcv.hyperspectral.read_data(filename=spectral_filename)
    mask = np.ones((array.lines, array.samples))

    wv_keys = list(array.wavelength_dict.keys())
    wavelengths = [250, 270, 1800, 2500]
    # change first 4 keys
    for (k_, k) in zip(wv_keys[0:5], wavelengths):
        array.wavelength_dict[k] = array.wavelength_dict.pop(k_)
    array.min_wavelength, array.max_wavelength = min(array.wavelength_dict), max(array.wavelength_dict)
    fig_hist = pcv.visualize.hyper_histogram(array, mask, wvlengths=wavelengths)
    assert isinstance(fig_hist, ggplot)


def test_plantcv_visualize_clustered_contours():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_BACKGROUND), -1)
    roi_objects = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_CONTOUR), encoding="latin1")
    hierarchy = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_HIERARCHY), encoding="latin1")
    cluster_i = np.load(os.path.join(TEST_DATA, TEST_INPUT_VISUALIZE_CLUSTERS), encoding="latin1")
    objs = [roi_objects[arr_n] for arr_n in roi_objects]
    obj_hierarchy = hierarchy['arr_0']
    cluster = [cluster_i[arr_n] for arr_n in cluster_i]
    # Test in plot mode
    pcv.params.debug = "plot"
    # Reset the saved color scale (can be saved between tests)
    pcv.params.saved_color_scale = None
    _ = pcv.visualize.clustered_contours(img=img1, grouped_contour_indices=cluster, roi_objects=objs,
                                         roi_obj_hierarchy=obj_hierarchy, bounding=False)
    # Test in print mode
    pcv.params.debug = "print"
    # Reset the saved color scale (can be saved between tests)
    pcv.params.saved_color_scale = None
    cluster_img = pcv.visualize.clustered_contours(img=img, grouped_contour_indices=cluster, roi_objects=objs,
                                                   roi_obj_hierarchy=obj_hierarchy, nrow=2, ncol=2, bounding=True)
    assert np.sum(cluster_img) > np.sum(img)


def test_plantcv_visualize_colorspaces():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    pcv.params.debug = "plot"
    vis_img_small = pcv.visualize.colorspaces(rgb_img=img, original_img=False)
    pcv.params.debug = "print"
    vis_img = pcv.visualize.colorspaces(rgb_img=img)
    assert np.shape(vis_img)[1] > (np.shape(img)[1]) and np.shape(vis_img_small)[1] > (np.shape(img)[1])


def test_plantcv_visualize_colorspaces_bad_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_plot_hist")
    os.mkdir(cache_dir)
    pcv.params.debug_outdir = cache_dir
    # Read in test data
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_GRAY), -1)
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.colorspaces(rgb_img=img)


def test_plantcv_visualize_overlay_two_imgs():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))

    pcv.params.debug = None
    out_img = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = img1[1445, 1154]
    sample_pt2 = img2[1445, 1154]
    sample_pt3 = out_img[1445, 1154]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_plantcv_visualize_overlay_two_imgs_grayscale():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_grayscale")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY), -1)
    out_img = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)
    sample_pt1 = np.array([255, 255, 255], dtype=np.uint8)
    sample_pt2 = np.array([255, 255, 255], dtype=np.uint8)
    sample_pt3 = out_img[1445, 1154]
    pred_rgb = (sample_pt1 * 0.5) + (sample_pt2 * 0.5)
    pred_rgb = pred_rgb.astype(np.uint8)
    assert np.array_equal(sample_pt3, pred_rgb)


def test_plantcv_visualize_overlay_two_imgs_bad_alpha():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_bad_alpha")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_BINARY))
    alpha = -1
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2, alpha=alpha)


def test_plantcv_visualize_overlay_two_imgs_size_mismatch():
    pcv.params.debug = None
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_visualize_overlay_two_imgs_size_mismatch")
    os.mkdir(cache_dir)
    img1 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_COLOR))
    img2 = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_CROPPED))
    with pytest.raises(RuntimeError):
        _ = pcv.visualize.overlay_two_imgs(img1=img1, img2=img2)


@pytest.mark.parametrize("num,expected", [[100, 35], [30, 33]])
def test_plantcv_visualize_size(num, expected):
    pcv.params.debug = None
    img = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_LEAF_MASK), -1)
    visualization = pcv.visualize.obj_sizes(img=img, mask=img, num_objects=num)
    # Output unique colors are the 32 objects, the gray text, the black background, and white unlabeled leaves
    assert len(np.unique(visualization.reshape(-1, visualization.shape[2]), axis=0)) == expected


@pytest.mark.parametrize("title", ["Include Title", None])
def test_plantcv_visualize_obj_size_ecdf(title):
    pcv.params.debug = None
    mask = cv2.imread(os.path.join(TEST_DATA, TEST_INPUT_MASK), -1)
    fig_ecdf = plantcv.plantcv.visualize.obj_size_ecdf(mask=mask, title=title)
    assert isinstance(fig_ecdf, ggplot)


# ##############################
# Tests for the utils subpackage
# ##############################

def test_plantcv_utils_json2csv():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_json2csv")
    os.mkdir(cache_dir)
    plantcv.utils.json2csv(json_file=os.path.join(TEST_DATA, "merged_output.json"),
                           csv_file=os.path.join(cache_dir, "exports"))
    assert all([os.path.exists(os.path.join(cache_dir, "exports-single-value-traits.csv")),
                os.path.exists(os.path.join(cache_dir, "exports-multi-value-traits.csv"))])


def test_plantcv_utils_json2csv_no_json():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_json2csv_no_json")
    os.mkdir(cache_dir)
    with pytest.raises(IOError):
        plantcv.utils.json2csv(json_file=os.path.join(TEST_DATA, "not_a_file.json"),
                               csv_file=os.path.join(cache_dir, "exports"))


def test_plantcv_utils_json2csv_bad_json():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_json2csv_bad_json")
    os.mkdir(cache_dir)
    with pytest.raises(ValueError):
        plantcv.utils.json2csv(json_file=os.path.join(TEST_DATA, "incorrect_json_data.txt"),
                               csv_file=os.path.join(cache_dir, "exports"))


def test_plantcv_utils_sample_images_snapshot():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_sample_images")
    os.mkdir(cache_dir)
    snapshot_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    img_outdir = os.path.join(cache_dir, "snapshot")
    plantcv.utils.sample_images(source_path=snapshot_dir, dest_path=img_outdir, num=3)
    assert os.path.exists(os.path.join(cache_dir, "snapshot"))


def test_plantcv_utils_sample_images_flatdir():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_sample_images")
    os.mkdir(cache_dir)
    flat_dir = os.path.join(TEST_DATA)
    img_outdir = os.path.join(cache_dir, "images")
    plantcv.utils.sample_images(source_path=flat_dir, dest_path=img_outdir, num=30)
    random_images = os.listdir(img_outdir)
    assert all([len(random_images) == 30, len(np.unique(random_images)) == 30])


def test_plantcv_utils_sample_images_bad_source():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_sample_images")
    os.mkdir(cache_dir)
    fake_dir = os.path.join(TEST_DATA, "snapshot")
    img_outdir = os.path.join(cache_dir, "images")
    with pytest.raises(IOError):
        plantcv.utils.sample_images(source_path=fake_dir, dest_path=img_outdir, num=3)


def test_plantcv_utils_sample_images_bad_flat_num():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_sample_images")
    os.mkdir(cache_dir)
    flat_dir = os.path.join(TEST_DATA)
    img_outdir = os.path.join(cache_dir, "images")
    with pytest.raises(RuntimeError):
        plantcv.utils.sample_images(source_path=flat_dir, dest_path=img_outdir, num=300)


def test_plantcv_utils_sample_images_bad_phenofront_num():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_sample_images")
    os.mkdir(cache_dir)
    snapshot_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
    img_outdir = os.path.join(cache_dir, "images")
    with pytest.raises(RuntimeError):
        plantcv.utils.sample_images(source_path=snapshot_dir, dest_path=img_outdir, num=300)


def test_plantcv_utils_tabulate_bayes_classes():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_tabulate_bayes_classes")
    os.mkdir(cache_dir)
    outfile = os.path.join(cache_dir, "rgb_table.txt")
    plantcv.utils.tabulate_bayes_classes(input_file=os.path.join(TEST_DATA, PIXEL_VALUES), output_file=outfile)
    table = pd.read_csv(outfile, sep="\t")
    assert table.shape == (228, 2)


def test_plantcv_utils_tabulate_bayes_classes_missing_input():
    # Test cache directory
    cache_dir = os.path.join(TEST_TMPDIR, "test_plantcv_utils_tabulate_bayes_classes_missing_input")
    os.mkdir(cache_dir)
    outfile = os.path.join(cache_dir, "rgb_table.txt")
    with pytest.raises(IOError):
        plantcv.utils.tabulate_bayes_classes(input_file=os.path.join(PIXEL_VALUES), output_file=outfile)


# ##############################
# Clean up test files
# ##############################
def teardown_function():
    shutil.rmtree(TEST_TMPDIR)
