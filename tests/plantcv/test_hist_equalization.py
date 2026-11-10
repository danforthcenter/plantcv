import pytest
import numpy as np
from plantcv.plantcv import hist_equalization


def test_hist_equalization(synthetic_gray):
    """Test for PlantCV."""
    img = synthetic_gray
    hist = hist_equalization(gray_img=img)
    assert np.average(hist) != np.average(img)


def test_hist_equalization_bad_input(synthetic_rgb):
    """Test for PlantCV."""
    img = synthetic_rgb
    with pytest.raises(RuntimeError):
        _ = hist_equalization(gray_img=img)
