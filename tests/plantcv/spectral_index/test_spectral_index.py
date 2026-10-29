import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.spectral_index import spectral_index
from tests import synthetic

R = synthetic.reflectance

# Each index, the distance to use, and its formula applied to the synthetic reflectance. The datacube
# has a band at every whole nanometer, so each index uses exactly the wavelengths in its formula. MTCI
# asks for 681.25, 708.75 and 753.75 nm, and uses the closest bands: 681, 709 and 754 nm.
HSI_INDICES = [
    ("ndvi", 20, lambda: (R(800) - R(670)) / (R(800) + R(670))),
    ("gdvi", 20, lambda: R(800) - R(550)),
    ("gndvi", 20, lambda: (R(800) - R(550)) / (R(800) + R(550))),
    ("savi", 20, lambda: (1.5 * (R(800) - R(680))) / (R(800) + R(680) + 0.5)),
    ("pri", 20, lambda: (R(531) - R(570)) / (R(531) + R(570))),
    ("ari", 20, lambda: (1 / R(550)) - (1 / R(700))),
    ("ci_rededge", 20, lambda: (R(800) / R(700)) - 1),
    ("cri550", 20, lambda: (1 / R(510)) - (1 / R(550))),
    ("cri700", 20, lambda: (1 / R(510)) - (1 / R(700))),
    ("egi", 40, lambda: (2 * R(530) - R(700) - R(460)) / (R(460) + R(530) + R(700))),
    ("evi", 20, lambda: (2.5 * (R(800) - R(670))) / (1 + R(800) + (6 * R(670)) - (7.5 * R(480)))),
    ("gli", 20, lambda: (2 * R(530) - R(670) - R(480)) / (2 * R(530) + R(670) + R(480))),
    ("sci", 40, lambda: (R(700) - R(530)) / (R(700) + R(530))),
    ("bgr", 40, lambda: R(460) / R(530)),
    ("bgi", 40, lambda: (R(530) - R(460)) / (R(530) + R(460))),
    ("mari", 20, lambda: ((1 / R(550)) - (1 / R(700))) * R(800)),
    ("mcari", 20, lambda: ((R(700) - R(670)) - 0.2 * (R(700) - R(550))) * (R(700) / R(670))),
    ("mtci", 20, lambda: (R(754) - R(709)) / (R(709) - R(681))),
    ("ndci", 20, lambda: (R(708) - R(665)) / (R(708) + R(665))),
    ("ndre", 20, lambda: (R(790) - R(720)) / (R(790) + R(720))),
    ("npci", 20, lambda: (R(680) - R(430)) / (R(680) + R(430))),
    ("psnd_chla", 20, lambda: (R(800) - R(680)) / (R(800) + R(680))),
    ("psnd_chlb", 20, lambda: (R(800) - R(635)) / (R(800) + R(635))),
    ("psnd_car", 20, lambda: (R(800) - R(470)) / (R(800) + R(470))),
    ("psri", 20, lambda: (R(678) - R(500)) / R(750)),
    ("pssr_chla", 20, lambda: R(800) / R(680)),
    ("pssr_chlb", 20, lambda: R(800) / R(635)),
    ("pssr_car", 20, lambda: R(800) / R(470)),
    ("rgri", 20, lambda: R(670) / R(560)),
    ("rvsi", 20, lambda: ((R(714) + R(752)) / 2) - R(733)),
    ("sipi", 20, lambda: (R(800) - R(670)) / (R(800) - R(480))),
    ("sr", 20, lambda: R(800) / R(670)),
    ("vari", 20, lambda: (R(550) - R(670)) / (R(550) + R(670) - R(480))),
    ("vi_green", 20, lambda: (R(550) - R(670)) / (R(550) + R(670))),
    ("wi", 20, lambda: R(900) / R(970)),
]


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_ndvi(debug, tmpdir):
    """Test for PlantCV."""
    cache = tmpdir.mkdir("cache")
    debug_outdir = params.debug_outdir
    default_debug = params.debug
    params.debug_outdir = str(cache)
    params.debug = debug
    index_array = spectral_index.ndvi(hsi=synthetic.spectral_data(), distance=20)
    params.debug_outdir = debug_outdir
    params.debug = default_debug
    assert np.shape(index_array.array_data) == (2, 3) and np.nanmax(index_array.pseudo_rgb()) == 255
    np.testing.assert_allclose(index_array.array_data, (R(800) - R(670)) / (R(800) + R(670)), rtol=1e-12)


@pytest.mark.parametrize("name,distance,formula", HSI_INDICES, ids=[i[0] for i in HSI_INDICES])
def test_hsi_index(name, distance, formula):
    """Test for PlantCV."""
    index_array = getattr(spectral_index, name)(synthetic.spectral_data(), distance=distance)
    assert index_array.array_type == "index_" + ("cri510" if name == "cri550" else name)
    assert np.shape(index_array.array_data) == (2, 3) and np.nanmax(index_array.pseudo_rgb()) == 255
    # EGI, GLI, SCI, BGR and BGI compute in float32, and the other indices in float64
    if index_array.array_data.dtype == np.float32:
        np.testing.assert_allclose(index_array.array_data, formula(), rtol=0, atol=1e-6)
    else:
        np.testing.assert_allclose(index_array.array_data, formula(), rtol=1e-12)


@pytest.mark.parametrize("name,distance,formula", HSI_INDICES, ids=[i[0] for i in HSI_INDICES])
def test_hsi_index_bad_input(name, distance, formula):
    """Test for PlantCV."""
    function = getattr(spectral_index, name)
    index_array = function(synthetic.spectral_data(), distance=distance)
    # An index has no wavelengths, so no index can be computed from it
    assert function(index_array, distance=distance) is None


def test_egi_rgb(synthetic_rgb):
    """Test for PlantCV."""
    index_array = spectral_index.egi(img=synthetic_rgb)
    assert np.shape(index_array.array_data) == (100, 120) and np.nanmax(index_array.pseudo_rgb()) == 255


def test_egi_ms():
    """Test for PlantCV"""
    test_array = synthetic.ms_data([460, 530, 700])
    index_array = spectral_index.egi(test_array)
    assert np.shape(index_array.array_data) == (10, 10)


def test_gli_ms():
    """Test for PlantCV"""
    test_array = synthetic.ms_data([480, 530, 670])
    index_array = spectral_index.gli(test_array)
    assert np.shape(index_array.array_data) == (10, 10)


def test_gli_rgb(synthetic_rgb):
    """Test for PlantCV."""
    index_array = spectral_index.gli(img=synthetic_rgb)
    assert np.shape(index_array.array_data) == (100, 120) and np.nanmax(index_array.pseudo_rgb()) == 255


def test_sci_rgb(synthetic_rgb):
    """Test for PlantCV."""
    index_array = spectral_index.sci(img=synthetic_rgb)
    assert np.shape(index_array.array_data) == (100, 120) and np.nanmax(index_array.pseudo_rgb()) == 255


def test_sci_ms():
    """Test for PlantCV"""
    test_array = synthetic.ms_data([530, 700])
    index_array = spectral_index.sci(test_array)
    assert np.shape(index_array.array_data) == (10, 10)


def test_bgr_rgb(synthetic_rgb):
    """Test for PlantCV."""
    index_array = spectral_index.bgr(img=synthetic_rgb)
    assert np.shape(index_array.array_data) == (100, 120) and np.nanmax(index_array.pseudo_rgb()) == 255


def test_bgr_ms():
    """Test for PlantCV"""
    test_array = synthetic.ms_data([460, 530])
    index_array = spectral_index.bgr(test_array)
    assert np.shape(index_array.array_data) == (10, 10)


def test_bgi_rgb(synthetic_rgb):
    """Test for PlantCV."""
    index_array = spectral_index.bgi(img=synthetic_rgb)
    assert np.shape(index_array.array_data) == (100, 120) and np.nanmax(index_array.pseudo_rgb()) == 255


def test_bgi_ms():
    """Test for PlantCV"""
    test_array = synthetic.ms_data([460, 530])
    index_array = spectral_index.bgi(test_array)
    assert np.shape(index_array.array_data) == (10, 10)
