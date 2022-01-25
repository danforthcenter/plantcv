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
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = tmp_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True

    jobs = job_builder(meta=parallel_test_data.metadata_snapshot_vis, config=config)

    image_name = list(parallel_test_data.metadata_snapshot_vis.keys())[0]
    result_file = os.path.join(tmp_dir, image_name + '.txt')

    expected = ['python', parallel_test_data.workflow_script, '--image',
                parallel_test_data.metadata_snapshot_vis[image_name]['path'], '--outdir',
                tmp_dir, '--result', result_file, '--writeimg', '--other', 'on']

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
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = tmp_dir
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True
    config.coprocess = "NIR"

    jobs = job_builder(meta=parallel_test_data.metadata_snapshot_coprocess, config=config)

    img_names = list(parallel_test_data.metadata_snapshot_coprocess.keys())
    vis_name = img_names[0]
    vis_path = parallel_test_data.metadata_snapshot_coprocess[vis_name]['path']
    result_file = os.path.join(tmp_dir, vis_name + '.txt')
    nir_name = img_names[1]
    coresult_file = os.path.join(tmp_dir, nir_name + '.txt')

    expected = ['python', parallel_test_data.workflow_script, '--image', vis_path, '--outdir', tmp_dir, '--result',
                result_file, '--coresult', coresult_file, '--writeimg', '--other', 'on']

    assert all([i == j] for i, j in zip(jobs[0], expected))
