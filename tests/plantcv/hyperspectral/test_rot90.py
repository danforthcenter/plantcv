import numpy as np
from plantcv.plantcv.hyperspectral import rot90


def test_rot90(hyperspectral_test_data):
    """Test for PlantCV."""
    spectral_data = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file)
    new = rot90(spectral_data=spectral_data, k=1)

    assert np.shape(new.array_data) == (1600, 1, 978)
