import os
import pytest
from plantcv.parallel import check_date_range, metadata_parser, WorkflowConfig


def test_plantcv_parallel_metadata_parser_snapshots(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data["metadata_vis_only"]


def test_plantcv_parallel_metadata_parser_snapshots_coimg(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "FAKE"

    meta = metadata_parser(config=config)
    assert meta == test_data["metadata_vis_only"]


def test_plantcv_parallel_metadata_parser_images(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_flatdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014"
    config.end_date = "2014"
    config.timestampformat = '%Y'  # no date in filename so check date range and date_format are ignored
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(test_data["img_flatdir"], 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
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


def test_plantcv_parallel_metadata_parser_regex(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_flatdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.delimiter = r'(VIS)_(SV)_(\d+)_(z1)_(h1)_(g0)_(e82)_(\d+)'

    meta = metadata_parser(config=config)
    expected = {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(test_data["img_flatdir"], 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
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


def test_plantcv_parallel_metadata_parser_images_outside_daterange(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_flatdir_wdates"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "timestamp"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "NIR"}
    config.start_date = "1970-01-01 00_00_00"
    config.end_date = "1970-01-01 00_00_00"
    config.timestampformat = "%Y-%m-%d %H_%M_%S"
    config.imgformat = "jpg"
    config.delimiter = r"(NIR)_(SV)_(\d)_(z1)_(h1)_(g0)_(e65)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})"

    meta = metadata_parser(config=config)
    assert meta == {}


def test_plantcv_parallel_metadata_parser_no_default_dates(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV", "id": "117770"}
    config.start_date = None
    config.end_date = None
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data["metadata_vis_only"]


def test_plantcv_parallel_check_date_range_wrongdateformat():
    start_date = 10
    end_date = 10
    img_time = '2010-10-10'

    with pytest.raises(SystemExit, match=r'does not match format'):
        date_format = '%Y%m%d'
        _ = check_date_range(start_date, end_date, img_time, date_format)


def test_plantcv_parallel_metadata_parser_snapshot_outside_daterange(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)

    assert meta == {}


def test_plantcv_parallel_metadata_parser_fail_images(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"cartag": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)
    assert meta == test_data["metadata_nir_only"]


def test_plantcv_parallel_metadata_parser_images_with_frame(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
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
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
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


def test_plantcv_parallel_metadata_parser_images_no_frame(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "X", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
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
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
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


def test_plantcv_parallel_metadata_parser_images_no_camera(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "X", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == {
        'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
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
            'path': os.path.join(test_data["img_snapshotdir"], 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
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
