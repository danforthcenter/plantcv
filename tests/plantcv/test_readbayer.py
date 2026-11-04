import pytest
import numpy as np
from plantcv.plantcv import readbayer
from tests import synthetic


@pytest.fixture
def bayer_img(tmp_path):
    """Bayer mosaic of a uniform BAYER_BGR image, written to a PNG file."""
    img = np.full((*synthetic.PLANT_SHAPE, 3), synthetic.BAYER_BGR, dtype=np.uint8)
    path, = synthetic.write_images(tmp_path, {"bayer_img.png": synthetic.bayer_mosaic(img)})
    return path


@pytest.mark.parametrize("alg, pattern", [["default", 'BG'],
                                          ["default", 'GB'],
                                          ["default", 'RG'],
                                          ["default", 'GR'],
                                          ["edgeaware", 'BG'],
                                          ["edgeaware", 'GB'],
                                          ["edgeaware", 'RG'],
                                          ["edgeaware", 'GR'],
                                          ["variablenumbergradients", 'BG'],
                                          ["variablenumbergradients", 'GB'],
                                          ["variablenumbergradients", 'RG'],
                                          ["variablenumbergradients", 'GR']])
def test_readbayer(alg, pattern, bayer_img):
    """Test for PlantCV."""
    img, _, _ = readbayer(filename=bayer_img, bayerpattern=pattern, alg=alg)
    assert img.shape == (100, 120, 3)
    # The mosaic is in the BG layout: BG gives back the uniform color, and RG swaps blue and red
    expected = {"BG": synthetic.BAYER_BGR, "RG": synthetic.BAYER_BGR[::-1]}
    if pattern in expected:
        assert np.all(img == expected[pattern])


def test_readbayer_default_bad_input():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename="no-image.png", bayerpattern="GR", alg="default")


def test_readbayer_bad_algorithm(bayer_img):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename=bayer_img, bayerpattern="GR", alg="bad_algorithm")


def test_readbayer_bad_bayerpattern(bayer_img):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename=bayer_img, bayerpattern="bad_bayerpattern", alg="default")
