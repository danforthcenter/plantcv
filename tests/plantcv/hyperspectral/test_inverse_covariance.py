import numpy as np
from plantcv.plantcv.hyperspectral import _inverse_covariance
from tests import synthetic


def test_inverse_covariance():
    """Test for PlantCV."""
    inv_cov = _inverse_covariance(synthetic.spectral_data())
    # One row and column per band
    assert np.shape(inv_cov) == (601, 601)
