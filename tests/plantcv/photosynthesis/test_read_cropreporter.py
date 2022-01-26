import os
import shutil
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter


def test_read_cropreporter(photosynthesis_test_data):
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter)
    assert isinstance(ps, PSII_data) and ps.darkadapted.shape == (966, 1296, 21, 1)


def test_read_cropreporter_spc_only(photosynthesis_test_data, tmpdir):
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
