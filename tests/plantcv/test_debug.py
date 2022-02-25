import pytest
import os
import cv2
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


@pytest.mark.parametrize("debug", ["print", "plot"])
def test_debug(debug, test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache = tmpdir.mkdir("cache")
    output_img = os.path.join(cache, os.path.basename(test_data.small_rgb_img))
    params.debug = debug
    img = cv2.imread(test_data.small_rgb_img)
    _debug(visual=img, filename=output_img)
    assert True
