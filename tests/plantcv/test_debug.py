import pytest
import os
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_debug(debug, synthetic_rgb, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache = tmpdir.mkdir("cache")
    output_img = os.path.join(cache, "synthetic_rgb.png")
    params.debug = debug
    img = synthetic_rgb
    _debug(visual=img, filename=output_img)
    assert True
