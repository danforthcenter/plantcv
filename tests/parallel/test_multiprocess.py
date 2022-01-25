import pytest
import os
import dask
from dask.distributed import Client
from plantcv.parallel import create_dask_cluster, multiprocess


def test_create_dask_cluster_local(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    client = create_dask_cluster(cluster="LocalCluster", cluster_config={})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_create_dask_cluster(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    client = create_dask_cluster(cluster="HTCondorCluster", cluster_config={"cores": 1, "memory": "1GB", "disk": "1GB"})
    status = client.status
    client.shutdown()
    assert status == "running"


def test_create_dask_cluster_invalid_cluster():
    """Test for PlantCV."""
    with pytest.raises(ValueError):
        _ = create_dask_cluster(cluster="Skynet", cluster_config={})


def test_plantcv_parallel_multiprocess(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    image_name = list(parallel_test_data.metadata_snapshot_vis.keys())[0]
    image_path = os.path.join(parallel_test_data.metadata_snapshot_vis[image_name]['path'], image_name)
    result_file = os.path.join(tmp_dir, image_name + '.txt')
    jobs = [['python', parallel_test_data.workflow_script, '--image', image_path, '--outdir', tmp_dir, '--result', result_file,
             '--writeimg', '--other', 'on']]
    # Create a dask LocalCluster client
    client = Client(n_workers=1)
    multiprocess(jobs, client=client)
    assert os.path.exists(result_file)
