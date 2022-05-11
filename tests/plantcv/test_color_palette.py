import pytest
import numpy as np
from plantcv.plantcv import color_palette, params


@pytest.mark.parametrize("seq", ["sequential", "random"])
def test_color_palette(seq):
    """Test for PlantCV."""
    params.color_sequence = seq
    # Return a color palette
    colors = color_palette(num=10, saved=False)
    assert np.shape(colors) == (10, 3)


def test_plantcv_color_palette_saved():
    """Test for PlantCV."""
    # Return a color palette that was saved
    params.saved_color_scale = [[0, 0, 0], [255, 255, 255]]
    colors = color_palette(num=2, saved=True)
    assert colors == [[0, 0, 0], [255, 255, 255]]
