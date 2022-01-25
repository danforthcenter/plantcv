import pytest
from plantcv.plantcv import params
from plantcv.plantcv.photosynthesis import read_cropreporter


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_read_cropreporter(debug, photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    params.debug_outdir = cache_dir
    params.debug = debug
    fdark, fmin, fmax = read_cropreporter(filename=photosynthesis_test_data.cropreporter)
    print(fdark.shape, fmin.shape, fmax.shape)
    assert all([fdark.shape == (966, 1296), fmin.shape == (966, 1296), fmax.shape == (966, 1296)])
