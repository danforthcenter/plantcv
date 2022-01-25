import numpy as np
from plantcv.plantcv.hyperspectral import _inverse_covariance


def test_inverse_covariance(hyperspectral_test_data):
    """Test for PlantCV."""
    inv_cov = _inverse_covariance(hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file))
    assert np.shape(inv_cov) == (978, 978)
