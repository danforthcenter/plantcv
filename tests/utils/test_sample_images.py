import pytest
import os
import numpy as np
from plantcv.utils import sample_images


def test_sample_images_snapshot(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    snapshot_dir = utils_test_data.snapshot_imgdir
    img_outdir = os.path.join(str(tmp_dir), "snapshot")
    sample_images(source_path=snapshot_dir, dest_path=img_outdir, num=3)
    random_images = os.listdir(img_outdir)
    assert all([len(random_images) == 3, len(np.unique(random_images)) == 3])


def test_sample_images_flatdir(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    flat_dir = utils_test_data.flat_imgdir
    img_outdir = os.path.join(str(tmp_dir), "images")
    sample_images(source_path=flat_dir, dest_path=img_outdir, num=1)
    random_images = os.listdir(img_outdir)
    assert all([len(random_images) == 1, len(np.unique(random_images)) == 1])


def test_sample_images_bad_source(tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    fake_dir = "snapshot"
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(IOError):
        sample_images(source_path=fake_dir, dest_path=img_outdir, num=3)


def test_sample_images_bad_flat_num(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    flat_dir = utils_test_data.datadir
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(RuntimeError):
        sample_images(source_path=flat_dir, dest_path=img_outdir, num=300)


def test_sample_images_bad_phenofront_num(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    snapshot_dir = utils_test_data.snapshot_imgdir
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(RuntimeError):
        sample_images(source_path=snapshot_dir, dest_path=img_outdir, num=300)


def test_sample_images_phenodata(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    phenodata_dir = utils_test_data.phenodata_dir
    img_outdir = os.path.join(str(tmp_dir), "images")
    sample_images(source_path=phenodata_dir, dest_path=img_outdir, num=1)
    random_images = os.listdir(img_outdir)
    assert len(random_images) == 2


def test_sample_images_phenodata_bad_num(utils_test_data, tmpdir):
    """Test for PlantCV."""
    # Create tmp directory
    tmp_dir = tmpdir.mkdir("cache")
    phenodata_dir = utils_test_data.phenodata_dir
    img_outdir = os.path.join(str(tmp_dir), "images")
    with pytest.raises(RuntimeError):
        sample_images(source_path=phenodata_dir, dest_path=img_outdir, num=300)
