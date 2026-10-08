import os
import cv2
import importlib
import numpy as np
from plantcv.learn.train_kmeans import train_kmeans, _read_by_mode


def test_train_kmeans_subset(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    training_dir = learn_test_data.kmeans_train_dir
    outfile_subset = os.path.join(str(cache_dir), "kmeansout_subset.fit")
    # Train full model and partial model
    train_kmeans(img_dir=training_dir, prefix="kmeans_train",
                 out_path=outfile_subset, k=5, patch_size=4, num_imgs=3)
    assert os.path.exists(outfile_subset)


def test_train_kmeans_full(learn_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    training_dir = learn_test_data.kmeans_train_dir
    outfile_full = os.path.join(str(cache_dir), "kmeansout_full.fit")
    train_kmeans(img_dir=training_dir, prefix="kmeans_train",
                 out_path=outfile_full, k=5, patch_size=4)
    assert os.path.exists(outfile_full)


def test_train_kmeans_subset_gray(learn_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    training_dir_gray = learn_test_data.kmeans_train_gray_dir
    outfile_subset_gray = os.path.join(str(cache_dir), "kmeansout_subset_gray.fit")
    train_kmeans(img_dir=training_dir_gray, prefix="kmeans_train",
                 out_path=outfile_subset_gray, k=5, patch_size=4, num_imgs=3)
    assert os.path.exists(outfile_subset_gray)


def test_train_kmeans_full_gray(learn_test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    training_dir_gray = learn_test_data.kmeans_train_gray_dir
    outfile_full_gray = os.path.join(str(cache_dir), "kmeansout_full_gray.fit")
    train_kmeans(img_dir=training_dir_gray, prefix="kmeans_train",
                 out_path=outfile_full_gray, k=5, patch_size=4)
    assert os.path.exists(outfile_full_gray)


def test_train_kmeans_spectral(test_data, tmp_path, monkeypatch):
    """Test for PlantCV."""
    train_kmeans_module = importlib.import_module("plantcv.learn.train_kmeans")
    array_data = cv2.imread(test_data.small_rgb_img)
    calls = []
    # define a dummy function to return that object
    def fake_read(path, mode):
        calls.append((os.path.basename(path), mode))
        return array_data
    # proxy the reading helper function with mockreturn
    monkeypatch.setattr(train_kmeans_module, "_read_by_mode", fake_read)
    for i in range(2):
        (tmp_path / f"kmeans_train_{i}.raw").touch()
    (tmp_path / "kmeans_train_decoy.jpg").touch()
    outfile_spec = tmp_path / "kmeansout_spec.fit"
    fitted = train_kmeans(img_dir=str(tmp_path), mode="spectral", prefix="kmeans_train",
                          out_path=str(outfile_spec), k=3, patch_size=4)
    assert outfile_spec.exists()
    assert calls == [("kmeans_train_0.raw", "spectral"), ("kmeans_train_1.raw", "spectral")]


def test_read_by_mode(test_data):
    """Test for PlantCV."""
    img = _read_by_mode(test_data.envi_sample_data, mode="spectral")
    assert isinstance(img, np.ndarray)
