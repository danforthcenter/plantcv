from plantcv.plantcv import outputs
from plantcv.plantcv import readimage
from plantcv.plantcv import quality_control


def test_plantcv_quality_control(test_data):
    """Test for PlantCV."""
    img, _, _ = readimage(filename=test_data.small_rgb_img, mode='native')
    quality_control(img)
    assert outputs.metadata["red_percent_bad_exposure_qc"]["value"] == 0.0007238805970149253
