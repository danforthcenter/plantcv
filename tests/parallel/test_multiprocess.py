import pytest
import os
import dask
from dask.distributed import Client
from plantcv.parallel import create_dask_cluster, multiprocess
from plantcv.parallel.multiprocess import _process_images_multiproc


def test_create_dask_cluster_local(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    client = create_dask_cluster(cluster="LocalCluster", cluster_config={})
    status = client.status
    assert status == "running"


def test_create_dask_cluster(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    client = create_dask_cluster(cluster="HTCondorCluster", cluster_config={"cores": 1, "memory": "1GB", "disk": "1GB"})
    status = client.status
    assert status == "running"


def test_create_dask_cluster_invalid_cluster():
    """Test for PlantCV."""
    with pytest.raises(ValueError):
        _ = create_dask_cluster(cluster="Skynet", cluster_config={})


def test_multiprocess(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("sub")
    # Set the temp directory for dask
    dask.config.set(temporary_directory=tmp_dir)
    image_path = parallel_test_data.image_path
    result_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(image_path))[0] + '.json')
    jobs = [['python', parallel_test_data.workflow_script, '--outdir', tmp_dir, '--result', result_file, "--names", "vis",
             '--writeimg', '--other', 'on', image_path]]
    # Create a dask LocalCluster client
    client = Client(n_workers=1)
    multiprocess(jobs, client=client)
    assert os.path.exists(result_file)


def test_process_images_multiproc():
    """Test for PlantCV."""
    result = _process_images_multiproc(['python', '-c', 'print("Hello World!")'])
    assert result is None
