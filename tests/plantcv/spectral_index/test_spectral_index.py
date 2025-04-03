import numpy as np
import cv2
from plantcv.plantcv import spectral_index


def test_ndvi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ndvi(hsi=spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_ndvi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ndvi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.ndvi(hsi=index_array, distance=20) is None


def test_gdvi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.gdvi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_gdvi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.gdvi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.gdvi(hsi=index_array, distance=20) is None


def test_savi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.savi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_savi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.savi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.savi(hsi=index_array, distance=20) is None


def test_pri(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pri(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_pri_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pri(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.pri(hsi=index_array, distance=20) is None


def test_ari(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ari(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_ari_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ari(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.ari(hsi=index_array, distance=20) is None


def test_ci_rededge(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ci_rededge(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_ci_rededge_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ci_rededge(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.ci_rededge(hsi=index_array, distance=20) is None


def test_cri550(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.cri550(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_cri550_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.cri550(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.cri550(hsi=index_array, distance=20) is None


def test_cri700(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.cri700(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_cri700_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.cri700(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.cri700(hsi=index_array, distance=20) is None


def test_egi_rgb(spectral_index_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(spectral_index_test_data.small_rgb_img)
    index_array = spectral_index.egi(rgb_img=rgb_img)
    assert np.shape(index_array.array_data) == (335, 400) and np.nanmax(index_array.pseudo_rgb) == 255


def test_egi_hsi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.egi(spectral_index_test_data.load_hsi(), distance=40)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_egi_hsi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.egi(spectral_index_test_data.load_hsi(), distance=40)
    assert spectral_index.egi(rgb_img=index_array, distance=40) is None


def test_evi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.evi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_evi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.evi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.evi(hsi=index_array, distance=20) is None


def test_gli_hsi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.gli(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_gli_rgb(spectral_index_test_data):
    """Test for PlantCV."""
    rgb_img = cv2.imread(spectral_index_test_data.small_rgb_img)
    index_array = spectral_index.gli(img=rgb_img)
    assert np.shape(index_array.array_data) == (335, 400) and np.nanmax(index_array.pseudo_rgb) == 255


def test_gli_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.gli(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.gli(img=index_array, distance=20) is None


def test_mari(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mari(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_mari_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mari(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.mari(hsi=index_array, distance=20) is None


def test_mcari(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mcari(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_mcari_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mcari(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.mcari(hsi=index_array, distance=20) is None


def test_mtci(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mtci(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_mtci_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.mtci(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.mtci(hsi=index_array, distance=20) is None


def test_ndre(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ndre(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_ndre_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.ndre(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.ndre(hsi=index_array, distance=20) is None


def test_npci(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.npci(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_npci_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.npci(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.npci(hsi=index_array, distance=20) is None


def test_psnd_chla(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_chla(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_psnd_chla_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_chla(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.psnd_chla(hsi=index_array, distance=20) is None


def test_psnd_chlb(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_chlb(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_psnd_chlb_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_chlb(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.psnd_chlb(hsi=index_array, distance=20) is None


def test_psnd_car(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_car(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_psnd_car_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psnd_car(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.psnd_car(hsi=index_array, distance=20) is None


def test_psri(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psri(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_psri_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.psri(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.psri(hsi=index_array, distance=20) is None


def test_pssr_chla(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_chla(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_pssr_chla_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_chla(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.pssr_chla(hsi=index_array, distance=20) is None


def test_pssr_chlb(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_chlb(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_pssr_chlb_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_chlb(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.pssr_chlb(hsi=index_array, distance=20) is None


def test_pssr_car(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_car(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_pssr_car_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.pssr_car(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.pssr_car(hsi=index_array, distance=20) is None


def test_rgri(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.rgri(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_rgri_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.rgri(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.rgri(hsi=index_array, distance=20) is None


def test_rvsi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.rvsi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_rvsi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.rvsi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.rvsi(hsi=index_array, distance=20) is None


def test_sipi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.sipi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_sipi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.sipi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.sipi(hsi=index_array, distance=20) is None


def test_sr(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.sr(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_sr_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.sr(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.sr(hsi=index_array, distance=20) is None


def test_vari(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.vari(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_vari_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.vari(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.vari(hsi=index_array, distance=20) is None


def test_vi_green(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.vi_green(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_vi_green_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.vi_green(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.vi_green(hsi=index_array, distance=20) is None


def test_wi(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.wi(spectral_index_test_data.load_hsi(), distance=20)
    assert np.shape(index_array.array_data) == (1, 1600) and np.nanmax(index_array.pseudo_rgb) == 255


def test_wi_bad_input(spectral_index_test_data):
    """Test for PlantCV."""
    index_array = spectral_index.wi(spectral_index_test_data.load_hsi(), distance=20)
    assert spectral_index.wi(hsi=index_array, distance=20) is None
