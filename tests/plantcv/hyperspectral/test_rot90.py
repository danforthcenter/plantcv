import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.hyperspectral import rot90
from tests import synthetic


def test_rot90(tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    debug_outdir = params.debug_outdir
    default_debug = params.debug
    params.debug_outdir = str(cache)
    params.debug = "plot"
    spectral_data = synthetic.spectral_data()
    new = rot90(spectral_data=spectral_data, k=1)
    params.debug_outdir = debug_outdir
    params.debug = default_debug
    # A quarter turn swaps the 2 lines and 3 samples; the first line becomes the first column, bottom up
    assert np.shape(new.array_data) == (3, 2, 601)
    assert np.array_equal(new.array_data[:, 0, :], spectral_data.array_data[0, ::-1, :])
