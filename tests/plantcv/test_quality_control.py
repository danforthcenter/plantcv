import cv2
import pytest
from plantcv.plantcv import params
from plantcv.plantcv import outputs
from plantcv.plantcv import readimage
from plantcv.plantcv import quality_control


@pytest.mark.parametrize("mode", ["print", "plot"])
def test_plantcv_quality_control(mode, test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    img = cv2.imread(test_data.small_rgb_img, -1)
    params.debug = mode
    quality_control(img)
    assert outputs.metadata["red_percent_bad_exposure_qc"]["value"] == 0.0007238805970149253
