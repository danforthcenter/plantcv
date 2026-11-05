import os
import cv2
import importlib
import numpy as np
import pytest
from joblib import load
from plantcv.learn.train_kmeans import train_kmeans, _read_by_mode
from tests import synthetic


@pytest.mark.parametrize("num_imgs", [0, 3])
def test_train_kmeans(num_imgs, kmeans_train_dir, tmp_path):
    """Test for PlantCV."""
    training_dir, channels = kmeans_train_dir
    outfile = os.path.join(str(tmp_path), "kmeansout.fit")
    # num_imgs=0 trains on every image; num_imgs=3 on 3 drawn at random
    fitted = train_kmeans(img_dir=training_dir, prefix="kmeans_train", out_path=outfile, k=5, patch_size=4,
                          num_imgs=num_imgs)
    model = load(outfile)
    # 5 clusters of 4 x 4 patches with 3 (BGR) or 1 (gray) channels
    assert model.cluster_centers_.shape == fitted.cluster_centers_.shape == (5, 4 * 4 * channels)
    assert np.array_equal(model.cluster_centers_, fitted.cluster_centers_)


def test_train_kmeans_spectral(synthetic_rgb, tmp_path, monkeypatch):
    """Test for PlantCV."""
    train_kmeans_module = importlib.import_module("plantcv.learn.train_kmeans")
    array_data = synthetic_rgb
    calls = []

    # define a dummy function to return that object
    def fake_read(path, mode):
        """patch function for reading HSI data"""
        calls.append((os.path.basename(path), mode))
        return array_data
    # proxy the reading helper function with mockreturn
    monkeypatch.setattr(train_kmeans_module, "_read_by_mode", fake_read)
    for i in range(2):
        (tmp_path / f"kmeans_train_{i}.raw").touch()
    (tmp_path / "kmeans_train_decoy.jpg").touch()
    outfile_spec = tmp_path / "kmeansout_spec.fit"
    _ = train_kmeans(img_dir=str(tmp_path), mode="spectral", prefix="kmeans_train",
                     out_path=str(outfile_spec), k=3, patch_size=4)
    assert outfile_spec.exists()
    assert calls == [("kmeans_train_0.raw", "spectral"), ("kmeans_train_1.raw", "spectral")]


def test_read_by_mode(tmpdir):
    """Test for PlantCV."""
    img = _read_by_mode(synthetic.write_envi(outdir=tmpdir, filename="envi"), mode="spectral")
    assert np.array_equal(img, synthetic.envi_array())


def test_read_by_mode_drop_rgba_alpha(tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    rgba = np.random.randint(0, 255, (20, 20, 4))
    imgname = os.path.join(cache, "img.png")
    cv2.imwrite(imgname, rgba)
    img = _read_by_mode(imgname, None)
    assert np.shape(img) == (20, 20, 3)
