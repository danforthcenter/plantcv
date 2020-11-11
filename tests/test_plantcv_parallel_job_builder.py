import os
from plantcv.parallel import job_builder
from plantcv.parallel import WorkflowConfig


def test_plantcv_parallel_job_builder_single_image(test_data, tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.tmp_dir = str(tmp_dir)
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.img_outdir = "img_outdir"
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True

    jobs = job_builder(meta=test_data["metadata_vis_only"], config=config)

    image_name = list(test_data["metadata_vis_only"].keys())[0]
    result_file = os.path.join("tmp_dir", image_name + '.txt')

    expected = ['python', test_data["workflow_script"], '--image', test_data["metadata_vis_only"][image_name]['path'],
                '--outdir', "img_outdir", '--result', result_file, '--writeimg', '--other', 'on']

    if len(expected) != len(jobs[0]):
        assert False
    else:
        assert all([i == j] for i, j in zip(jobs[0], expected))


def test_plantcv_parallel_job_builder_coprocess(test_data, tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data["img_snapshotdir"]
    config.json = "output.json"
    config.tmp_dir = str(tmp_dir)
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data["workflow_script"]
    config.img_outdir = "img_outdir"
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.other_args = ["--other", "on"]
    config.writeimg = True
    config.coprocess = "NIR"

    jobs = job_builder(meta=test_data["metadata_coprocess"], config=config)

    img_names = list(test_data["metadata_coprocess"].keys())
    vis_name = img_names[0]
    vis_path = test_data["metadata_coprocess"][vis_name]['path']
    result_file = os.path.join("tmp_dir", vis_name + '.txt')
    nir_name = img_names[1]
    coresult_file = os.path.join("tmp_dir", nir_name + '.txt')

    expected = ['python', test_data["workflow_script"], '--image', vis_path, '--outdir', "img_outdir", '--result',
                result_file, '--coresult', coresult_file, '--writeimg', '--other', 'on']

    if len(expected) != len(jobs[0]):
        assert False
    else:
        assert all([i == j] for i, j in zip(jobs[0], expected))
