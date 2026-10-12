import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.hyperspectral import rot90


def test_rot90(hyperspectral_test_data, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    debug_outdir = params.debug_outdir
    default_debug = params.debug
    params.debug_outdir = str(cache)
    params.debug = "plot"
    spectral_data = hyperspectral_test_data.load_hsi(hyperspectral_test_data.hsi_file)
    new = rot90(spectral_data=spectral_data, k=1)
    params.debug_outdir = debug_outdir
    params.debug = default_debug
    assert np.shape(new.array_data) == (1600, 1, 978)
