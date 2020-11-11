import pytest
import os
import dask
from dask.distributed import Client
from plantcv.parallel import create_dask_cluster, multiprocess


def test_plantcv_parallel_multiprocess_create_dask_cluster_local(tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=str(tmp_dir))
    client = create_dask_cluster(cluster="LocalCluster", cluster_config={})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_plantcv_parallel_multiprocess_create_dask_cluster(tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=str(tmp_dir))
    client = create_dask_cluster(cluster="HTCondorCluster", cluster_config={"cores": 1, "memory": "1GB", "disk": "1GB"})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_plantcv_parallel_multiprocess_create_dask_cluster_invalid_cluster():
    with pytest.raises(ValueError):
        _ = create_dask_cluster(cluster="Skynet", cluster_config={})


def test_plantcv_parallel_multiprocess(test_data, tmpdir):
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=str(tmp_dir))
    image_name = list(test_data["metadata_vis_only"].keys())[0]
    image_path = os.path.join(test_data["metadata_vis_only"][image_name]['path'], image_name)
    result_file = os.path.join(str(tmp_dir), image_name + '.txt')
    jobs = [['python', test_data["workflow_script"], '--image', image_path, '--outdir', str(tmp_dir), '--result',
             result_file, '--writeimg', '--other', 'on']]
    # Create a dask LocalCluster client
    client = Client(n_workers=1)
    multiprocess(jobs, client=client)
    assert os.path.exists(result_file)
