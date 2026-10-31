import pytest
import os
import cv2
import numpy as np
from plantcv.plantcv import readimage
from tests import synthetic


def _write_img(tmp_path, filename, img):
    """Write an image to tmp_path and return its path."""
    path = os.path.join(tmp_path, filename)
    cv2.imwrite(path, img)
    return path


def test_plantcv_readimage_native(tmp_path):
    """Test for PlantCV."""
    filename = _write_img(tmp_path, "plant_rgb.png", synthetic.plant_rgb())
    img, path, img_name = readimage(filename=filename, mode='native')
    expected = [3] + list(os.path.split(filename))
    # Assert that the image name returned equals the name of the input image
    # Assert that the path of the image returned equals the path of the input image
    # Assert that the dimensions of the returned image equals the expected dimensions
    assert [img.shape[2], path, img_name] == expected


@pytest.mark.parametrize("mode", ["gray", "grey"])
def test_readimage_grayscale(mode, tmp_path):
    """Test for PlantCV."""
    filename = _write_img(tmp_path, "plant_gray.png", synthetic.plant_gray())
    img, _, _ = readimage(filename=filename, mode=mode)
    assert len(img.shape) == 2


def test_readimage_rgb(tmp_path):
    """Test for PlantCV."""
    filename = _write_img(tmp_path, "plant_gray.png", synthetic.plant_gray())
    img, _, _ = readimage(filename=filename, mode="rgb")
    assert len(img.shape) == 3


def test_readimage_normalized(tmp_path):
    """Test for PlantCV."""
    filename = _write_img(tmp_path, "plant_gray.png", synthetic.plant_gray())
    img, _, _ = readimage(filename=filename, mode="normalize")
    assert len(img.shape) == 2


@pytest.mark.parametrize("mode,depth", [["rgba", 4], ["native", 3]])
def test_readimage_rgba(mode, depth, tmp_path):
    """Test for PlantCV."""
    # BGRA image with the plant opaque and the background transparent
    mask = synthetic.plant_mask()
    filename = _write_img(tmp_path, "plant_rgba.png", np.dstack((synthetic.plant_rgb(mask=mask), mask)))
    img, _, _ = readimage(filename=filename, mode=mode)
    assert img.shape[2] == depth


def test_readimage_csv(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.thermal_img, mode="csv")
    assert len(img.shape) == 2


def test_readimage_envi(tmpdir):
    """Test for PlantCV."""
    hsi = readimage(filename=synthetic.write_envi(outdir=tmpdir, filename="envi"), mode="envi")
    assert hsi.array_data.shape[2] == 5


def test_readimage_nd2(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.nd2_img, mode="nd2")
    assert len(img.shape) == 3


def test_readimage_thermal(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.flir_img, mode="thermal")
    assert len(img.shape) == 2


def test_readimage_heic(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.heic_img, mode="heic")
    assert len(img.shape) == 3
    img, _, _ = readimage(filename=test_data.heic_img, mode="native")
    assert len(img.shape) == 3


def test_readimage_bad_file():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = readimage(filename="test.png")
