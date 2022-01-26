from plantcv.plantcv import PSII_data


def test_psii_data(photosynthesis_test_data):
    psii = PSII_data()
    psii.add_data(photosynthesis_test_data.psii_cropreporter('darkadapted'))
    assert repr(psii) == "PSII variables defined:\ndarkadapted"
