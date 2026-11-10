import pytest
from plantcv.plantcv.visualize import colorspaces


def test_colorspaces(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    vis_img = colorspaces(rgb_img=img)
    assert vis_img.shape[1] == 3 * img.shape[1]


def test_colorspaces_bad_input(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    with pytest.raises(RuntimeError):
        _ = colorspaces(rgb_img=img)
