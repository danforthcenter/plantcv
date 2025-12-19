import pytest
import os
import numpy as np
from plantcv.parallel import sample_images


def test_sample_images_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    from plantcv.parallel import WorkflowConfig
    working = os.getcwd()
    os.chdir(tmpdir.mkdir("cache"))
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.save_config("testsample_config.json")
    img_outdir = "output_goes_here"
    sample_images(source="testsample_config.json", dest_path=img_outdir, num=3)
    random_images = os.listdir(img_outdir)
    os.chdir(working)
    assert all([len(random_images) == 3, len(np.unique(random_images)) == 3])


def test_sample_images_snapshot(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    snapshot_dir = parallel_test_data.snapshot_imgdir
    img_outdir = os.path.join(str(tmp_dir), "snapshot")
    sample_images(source=snapshot_dir, dest_path=img_outdir, num=3)
    random_images = os.listdir(img_outdir)
    assert all([len(random_images) == 3, len(np.unique(random_images)) == 3])


def test_sample_images_flatdir(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    flat_dir = parallel_test_data.flat_imgdir
    img_outdir = os.path.join(str(tmp_dir), "images")
    sample_images(source=flat_dir, dest_path=img_outdir, num=1)
    random_images = os.listdir(img_outdir)
    assert all([len(random_images) == 1, len(np.unique(random_images)) == 1])


def test_sample_images_bad_source(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    fake_dir = "path_that_does_not_exist"
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(IOError):
        sample_images(source=fake_dir, dest_path=img_outdir, num=3)


def test_sample_images_bad_flat_num(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    flat_dir = parallel_test_data.flat_imgdir
    img_outdir = os.path.join(str(tmp_dir), "images")
    sample_images(source=flat_dir, dest_path=img_outdir, num=300)
    random_images = os.listdir(img_outdir)
    assert len(random_images) == 2


def test_sample_images_bad_phenofront_num(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    snapshot_dir = parallel_test_data.snapshot_imgdir
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(RuntimeError):
        sample_images(source=snapshot_dir, dest_path=img_outdir, num=300)


def test_sample_images_phenodata(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    phenodata_dir = parallel_test_data.phenodata_dir
    img_outdir = os.path.join(str(tmp_dir), "images")
    sample_images(source=phenodata_dir, dest_path=img_outdir, num=1)
    random_images = os.listdir(img_outdir)
    assert len(random_images) == 2


def test_sample_images_phenodata_bad_num(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    phenodata_dir = parallel_test_data.phenodata_dir
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(RuntimeError):
        sample_images(source=phenodata_dir, dest_path=img_outdir, num=300)
