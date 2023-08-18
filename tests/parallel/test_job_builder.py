import os
from plantcv.parallel import job_builder, WorkflowConfig


def test_job_builder_single_image(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.snapshot_imgdir
    config.json = "output.json"
    config.tmp_dir = tmp_dir
    config.filename_metadata = ["imgtype", "camera", "rotation", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = tmp_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = {"other": "on"}
    config.writeimg = True

    jobs = job_builder(meta=parallel_test_data.metadata_snapshot_vis(), config=config)

    image_path = parallel_test_data.image_path
    result_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(image_path))[0] + '.json')

    expected = ['python', parallel_test_data.workflow_script, '--outdir', tmp_dir, '--result', result_file, "--names", "vis",
                '--writeimg', '--other', 'on', image_path]

    assert all([i == j] for i, j in zip(jobs[0], expected))


def test_job_builder_coprocess(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.snapshot_imgdir
    config.json = "output.json"
    config.tmp_dir = tmp_dir
    config.filename_metadata = ["imgtype", "camera", "rotation", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = tmp_dir
    config.metadata_filters = {"camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = {"other": "on"}
    config.writeimg = True
    config.groupby = ["camera", "rotation"]

    jobs = job_builder(meta=parallel_test_data.metadata_snapshot_coprocess(), config=config)

    image_path = parallel_test_data.image_path
    nir_path = parallel_test_data.nir_path
    result_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(image_path))[0] + '.json')

    expected = ['python', parallel_test_data.workflow_script, '--outdir', tmp_dir, '--result', result_file, "--names",
                "vis,nir", '--writeimg', '--other', 'on', image_path, nir_path]

    assert all([i == j] for i, j in zip(jobs[0], expected))


def test_job_builder_auto_name(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.snapshot_imgdir
    config.json = "output.json"
    config.tmp_dir = tmp_dir
    config.filename_metadata = ["imgtype", "camera", "rotation", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = tmp_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = {"other": "on"}
    config.writeimg = True
    config.group_name = "auto"

    jobs = job_builder(meta=parallel_test_data.metadata_snapshot_vis(), config=config)

    image_path = parallel_test_data.image_path
    result_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(image_path))[0] + '.json')

    expected = ['python', parallel_test_data.workflow_script, '--outdir', tmp_dir, '--result', result_file, "--names",
                "image1", '--writeimg', '--other', 'on', image_path]

    assert all([i == j] for i, j in zip(jobs[0], expected))
