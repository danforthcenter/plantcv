import os
import shutil
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter


def test_read_cropreporter(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter)
    assert isinstance(ps, PSII_data) and ps.darkadapted.shape == (966, 1296, 21, 1)

    # Check with different naming conventioned of phenovation
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    alternative_naming = os.path.join(cache_dir, "HDR_PSII_test.INF")

    shutil.copyfile(photosynthesis_test_data.cropreporter, alternative_naming)
    shutil.copyfile(os.path.join(photosynthesis_test_data.datadir,"PSII_CHL_020321_WT_TOP_1.DAT"), os.path.join(cache_dir, "CHL_PSII_test.DAT"))
    shutil.copyfile(os.path.join(photosynthesis_test_data.datadir,"PSII_CLR_020321_WT_TOP_1.DAT"), os.path.join(cache_dir, "CLR_PSII_test.DAT"))
    shutil.copyfile(os.path.join(photosynthesis_test_data.datadir,"PSII_PSD_020321_WT_TOP_1.DAT"), os.path.join(cache_dir, "PSD_PSII_test.DAT"))
    shutil.copyfile(os.path.join(photosynthesis_test_data.datadir,"PSII_PSL_020321_WT_TOP_1.DAT"), os.path.join(cache_dir, "PSL_PSII_test.DAT"))

    ps = read_cropreporter(filename=alternative_naming)
    assert isinstance(ps, PSII_data) and ps.darkadapted.shape == (966, 1296, 21, 1)



def test_read_cropreporter_spc_only(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    # Create dataset with only SPC
    shutil.copyfile(photosynthesis_test_data.cropreporter, os.path.join(cache_dir, "PSII_HDR_test.INF"))
    spc_dat = photosynthesis_test_data.cropreporter.replace("HDR", "SPC")
    spc_dat = spc_dat.replace("INF", "DAT")
    shutil.copyfile(spc_dat, os.path.join(cache_dir, "PSII_SPC_test.DAT"))
    fluor_filename = os.path.join(cache_dir, "PSII_HDR_test.INF")
    ps = read_cropreporter(filename=fluor_filename)
    print(os.listdir(cache_dir))
    assert isinstance(ps, PSII_data) and ps.spectral.array_data.shape == (966, 1296, 3)
