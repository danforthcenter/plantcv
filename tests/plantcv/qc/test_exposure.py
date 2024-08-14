import cv2
import pytest
from plantcv.plantcv import params, outputs
from plantcv.plantcv.qc import exposure


@pytest.mark.parametrize("mode", ["print", "plot"])
def test_plantcv_quality_control(mode, test_data, tmpdir):
    """Test for PlantCV."""
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    img = cv2.imread(test_data.small_rgb_img, -1)
    params.debug = mode
    exposure(img)
    assert outputs.metadata["red_percent_bad_exposure_qc"]["value"] == 0.0007238805970149253
