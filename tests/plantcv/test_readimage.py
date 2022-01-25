import pytest
import os
from plantcv.plantcv import readimage


def test_plantcv_readimage_native(test_data):
    """Test for PlantCV."""
    img, path, img_name = readimage(filename=test_data.small_rgb_img, mode='native')
    expected = [3] + list(os.path.split(test_data.small_rgb_img))
    # Assert that the image name returned equals the name of the input image
    # Assert that the path of the image returned equals the path of the input image
    # Assert that the dimensions of the returned image equals the expected dimensions
    assert [img.shape[2], path, img_name] == expected


@pytest.mark.parametrize("mode", ["gray", "grey"])
def test_readimage_grayscale(mode, test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.small_gray_img, mode=mode)
    assert len(img.shape) == 2


def test_readimage_rgb(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.small_gray_img, mode="rgb")
    assert len(img.shape) == 3


@pytest.mark.parametrize("mode,depth", [["rgba", 4], ["native", 3]])
def test_readimage_rgba(mode, depth, test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.rgba_img, mode=mode)
    assert img.shape[2] == depth


def test_readimage_csv(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.thermal_img, mode="csv")
    assert len(img.shape) == 2


def test_readimage_envi(test_data):
    """Test for PlantCV."""
    hsi = readimage(filename=test_data.envi_bil_file, mode="envi")
    assert hsi.array_data.shape[2] == 978


def test_readimage_bad_file():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _ = readimage(filename="test.png")
