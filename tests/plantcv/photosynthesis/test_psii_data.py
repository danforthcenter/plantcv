from plantcv.plantcv import PSII_data
from tests import synthetic


def test_psii_data():
    """Test for PlantCV."""
    psii = PSII_data()
    psii.psd = synthetic.psii_dataarray('ojip_dark')
    assert psii.psd.shape == (10, 10, 4, 1)
