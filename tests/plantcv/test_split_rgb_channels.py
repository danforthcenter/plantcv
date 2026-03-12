import pytest
import numpy as np
from plantcv.plantcv import split_rgb_channels


def test_split_rgb_channels_wrong_type(test_data):
    """Test for PlantCV."""
    img = np.ones((10, 10, 3), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = split_rgb_channels(img=img)


def test_split_rgb_channels_hyperspectral(test_data):
    """Test for PlantCV."""
    hsi = test_data.load_hsi(test_data.hsi_file)
    r, g, b = split_rgb_channels(img=hsi)
    assert hsi.pseudo_rgb.shape[:2] == r.shape == g.shape == b.shape


def test_split_rgb_channels_missing_pseudorgb(test_data):
    """Test for PlantCV."""
    hsi = test_data.load_hsi(test_data.hsi_file)
    hsi.pseudo_rgb = None
    with pytest.raises(RuntimeError):
        _ = split_rgb_channels(img=hsi)


def test_split_rgb_channels_bad_shape(test_data):
    """Test for PlantCV."""
    img = test_data.load_hsi(test_data.hsi_file)
    img.pseudo_rgb = np.ones((10, 10), dtype=np.uint8)
    with pytest.raises(RuntimeError):
        _ = split_rgb_channels(img=img)
