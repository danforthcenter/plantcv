from plantcv.plantcv import PSII_data


def test_psii_data(photosynthesis_test_data):
    """Test for PlantCV."""
    psii = PSII_data()
    psii.ojip_dark = photosynthesis_test_data.psii_cropreporter('ojip_dark')
    assert psii.ojip_dark.shape == (10, 10, 4, 1)
