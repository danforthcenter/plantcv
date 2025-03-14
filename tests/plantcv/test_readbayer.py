import pytest
from plantcv.plantcv import readbayer


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
def test_readbayer(alg, pattern, test_data):
    """Test for PlantCV."""
    img, _, _ = readbayer(filename=test_data.bayer_img, bayerpattern=pattern, alg=alg)
    assert img.shape == (335, 400, 3)


def test_readbayer_default_bad_image(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename="no-image.png", bayerpattern="GR", alg="default")


def test_readbayer_default_bad_pattern(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename=test_data.bayer_img, bayerpattern="not a pattern", alg="default")


def test_readbayer_default_bad_algo(test_data):
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        _, _, _ = readbayer(filename=test_data.bayer_img, bayerpattern="GR", alg="not an algo")
