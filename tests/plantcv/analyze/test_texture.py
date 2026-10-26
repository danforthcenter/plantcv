import pytest
import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.analyze.texture import texture


def test_analyze_texture(synthetic_gray, synthetic_mask):
    """Test for PlantCV."""
    outputs.clear()
    _ = texture(synthetic_gray, synthetic_mask)
    assert isinstance(outputs.observations["default_1"]["contrast_1_0"]["value"], np.float64)
    # Of the 100 x 119 horizontal pixel pairs, each of the 60 plant rows has two 0/200 edges and
    # each of the 4 small object rows two 0/120 edges: (120 * 200^2 + 8 * 120^2) / 11900
    assert outputs.observations["default_1"]["contrast_1_0"]["value"] == pytest.approx(49152 / 119)


def test_analyze_texture_rgb(synthetic_rgb, synthetic_mask):
    """Test for PlantCV."""
    outputs.clear()
    _ = texture(synthetic_rgb, synthetic_mask)
    assert isinstance(outputs.observations["default_1"]["contrast_1_0"]["value"], np.float64)
    # Foreground converts to gray 0.587 * 128 = 75, so 128 edges of 0/75 among 11900 pairs
    assert outputs.observations["default_1"]["contrast_1_0"]["value"] == pytest.approx(7200 / 119)
