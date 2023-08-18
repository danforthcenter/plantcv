from plantcv.plantcv import PSII_data


def test_psii_data(photosynthesis_test_data):
    """Test for PlantCV."""
    psii = PSII_data()
    psii.add_data(photosynthesis_test_data.psii_cropreporter('ojip_dark'))
    assert repr(psii) == "PSII variables defined:\nojip_dark"
