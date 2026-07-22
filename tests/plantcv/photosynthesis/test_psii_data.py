from plantcv.plantcv import PSII_data


def test_psii_data(photosynthesis_test_data):
    """Test for PlantCV."""
    psii = PSII_data()
    psii.psd = photosynthesis_test_data.psii_cropreporter('ojip_dark')
    assert psii.psd.shape == (10, 10, 4, 1)
