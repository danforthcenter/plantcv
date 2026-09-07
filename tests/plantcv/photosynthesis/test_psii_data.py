from plantcv.plantcv import PSII_data


def test_psii_data(test_data):
    """Test for PlantCV."""
    psii = PSII_data()
    psii.psd = test_data.photosynthesis.psii_cropreporter('ojip_dark')
    assert psii.psd.shape == (10, 10, 4, 1)
