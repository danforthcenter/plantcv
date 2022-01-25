import numpy as np
from plantcv.plantcv.hyperspectral import calibrate


def test_calibrate(hyperspectral_test_data):
    """Test for PlantCV."""
    white = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_whiteref_file)
    dark = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_darkref_file)
    raw = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file)
    calibrated = calibrate(raw_data=raw, white_reference=white, dark_reference=dark)
    assert np.shape(calibrated.array_data) == (1, 1600, 978)
