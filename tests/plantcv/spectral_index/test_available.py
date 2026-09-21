import numpy as np
import pytest

from plantcv.plantcv import Spectral_data
from plantcv.plantcv import spectral_index
from plantcv.plantcv.spectral_index.available import _INDEX_REQUIREMENTS, _RGB_INDICES


def _make_cube(max_wl, min_wl):
    """Build a minimal synthetic Spectral_data datacube spanning min_wl to max_wl."""
    wavelengths = np.linspace(min_wl, max_wl, 10)
    array = np.tile(np.linspace(0.1, 0.9, 10, dtype=np.float32), (1, 1, 1))
    return Spectral_data(array_data=array, max_wavelength=max_wl, min_wavelength=min_wl,
                         max_value=1.0, min_value=0.0, d_type=np.float32,
                         wavelength_dict={wl: i for i, wl in enumerate(wavelengths)},
                         samples=array.shape[1], lines=array.shape[0], interleave="bil",
                         wavelength_units="nm", array_type="datacube", pseudo_rgb=None,
                         filename="test", default_bands=None)


def test_available_hsi_all_indices(spectral_index_test_data):
    """Test for PlantCV."""
    # The test datacube spans ~379-1001 nm so every index is available
    index_names = spectral_index.available(data=spectral_index_test_data.load_hsi())
    assert index_names == sorted(_INDEX_REQUIREMENTS.keys())


def test_available_hsi_reduced_range(spectral_index_test_data):
    """Test for PlantCV."""
    # A narrow visible-range cube: pri (531-570 nm) is available, ndvi (needs 800 nm) is not
    hsi = spectral_index_test_data.load_hsi()
    hsi.max_wavelength = 580.0
    hsi.min_wavelength = 520.0
    assert "pri" in spectral_index.available(data=hsi)
    assert "ndvi" not in spectral_index.available(data=hsi)


def test_available_hsi_explicit_distance(spectral_index_test_data):
    """Test for PlantCV."""
    # ndvi needs max_wavelength + distance >= 800: satisfied at distance=20 but not distance=0
    hsi = spectral_index_test_data.load_hsi()
    hsi.max_wavelength = 790.0
    hsi.min_wavelength = 400.0
    assert "ndvi" in spectral_index.available(data=hsi, distance=20)
    assert "ndvi" not in spectral_index.available(data=hsi, distance=0)


def test_available_hsi_default_distance_per_index(spectral_index_test_data):
    """Test for PlantCV."""
    # With distance=None each index uses its own default. egi and ari both require a 700 nm
    # max wavelength; on this cube egi's default (40) makes it available while ari's default
    # (20) does not, so only the per-index defaults decide the outcome
    hsi = spectral_index_test_data.load_hsi()
    hsi.max_wavelength = 675.0
    hsi.min_wavelength = 485.0
    assert "egi" in spectral_index.available(data=hsi)
    assert "ari" not in spectral_index.available(data=hsi)


def test_available_rgb():
    """Test for PlantCV."""
    # The indices that accept color images directly
    assert spectral_index.available(data=np.zeros((10, 10, 3), dtype=np.uint8)) == ["egi", "gli"]


def test_available_bad_input():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        spectral_index.available(data="not-a-dataset")


def test_available_registry_matches_exports():
    """Test for PlantCV."""
    # Every index exported by the subpackage must be in the registry and vice versa
    # (available is the discovery helper exported alongside the indices, not an index itself)
    index_functions = [name for name in spectral_index.__all__ if name != "available"]
    assert sorted(index_functions) == sorted(_INDEX_REQUIREMENTS.keys())
    assert sorted(_RGB_INDICES) == sorted(
        name for name in _INDEX_REQUIREMENTS if name in ("egi", "gli"))


def test_available_registry_matches_guards():
    """Test for PlantCV."""
    # Pin every registry entry to the actual behavior of its index function: a datacube
    # covering the required range computes the index, one missing the max-wavelength bound
    # triggers the guard (warn + None) exactly like a real call with unsuitable data.
    for name, (max_wavelength, min_wavelength, default_distance) in _INDEX_REQUIREMENTS.items():
        func = getattr(spectral_index, name)
        # egi takes rgb_img, gli takes img, everything else takes hsi
        data_param = "rgb_img" if name == "egi" else "img" if name == "gli" else "hsi"

        # A cube covering the required range must produce an index array
        covering = _make_cube(max_wl=max_wavelength + 10, min_wl=min_wavelength - 10)
        result = func(**{data_param: covering}, distance=default_distance)
        assert result is not None, f"{name}: registry says available but function returned None"
        assert not np.isnan(result.array_data).any(), f"{name}: computed index contains NaNs"

        # A cube missing the max-wavelength bound must be rejected
        short = _make_cube(max_wl=max_wavelength - default_distance - 1, min_wl=min_wavelength - 10)
        result = func(**{data_param: short}, distance=default_distance)
        assert result is None, f"{name}: guard accepted a cube the registry rejects"
