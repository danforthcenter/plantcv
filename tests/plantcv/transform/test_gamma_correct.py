import numpy as np
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.transform import gamma_correct


def test_gamma_correct(synthetic_rgb):
    """Test for PlantCV."""
    outputs.clear()
    img = synthetic_rgb
    # Test
    gamma_corrected = gamma_correct(img=img, gamma=2, gain=1)
    imgavg = np.average(img)
    correctedavg = np.average(gamma_corrected)
    assert correctedavg != imgavg
