import numpy as np
from plantcv.plantcv import outputs
from plantcv.plantcv.qc.exposure import exposure


def test_plantcv_quality_control(synthetic_rgb):
    """Test for PlantCV."""
    _ = exposure(synthetic_rgb)
    # Red is 0 in all 816 foreground pixels of the 100 x 120 image: 816 / 12000
    assert np.isclose(outputs.metadata["default_red_percent_bad_exposure_qc"]["value"], 0.068)
