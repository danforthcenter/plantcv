import os
import numpy as np
import shutil
from plantcv.plantcv import PSII_data
from plantcv.plantcv.photosynthesis import read_cropreporter


def test_read_cropreporter(photosynthesis_test_data, tmpdir):
    """Test for PlantCV."""
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter)
    assert isinstance(ps, PSII_data) and ps.darkadapted.shape == (966, 1296, 21, 1)

    # Check with different naming conventioned of phenovation
    ps = read_cropreporter(filename=photosynthesis_test_data.cropreporter_v653_ojip)
    assert isinstance(ps, PSII_data) and ps.darkadapted.shape == (1500, 2048, 7, 1)
    # check labels
    true_labels = ['Fdark', 'F0', 'PSD2', 'PSD3', 'Fm', 'PSD5', 'PSD6']
    assert all([a == b for a, b in zip(ps.darkadapted.coords['frame_label'].to_dict()['data'], true_labels)])


    # Create dataset with only 3 frames
    cache_dir = tmpdir.mkdir("sub")
    shutil.copytree(os.path.dirname(photosynthesis_test_data.cropreporter_v653_ojip), cache_dir, dirs_exist_ok=True)
    inffilename = os.path.join(cache_dir, photosynthesis_test_data.cropreporter_v653_ojip.split(os.sep)[-1])

    # Modify the inf file
    metadata_dict = {}
    with open(inffilename, "r") as fp:
        for line in fp:
            if "=" in line:
                key, value = line.rstrip("\n").split("=")
                metadata_dict[key] = value
    metadata_dict['SaveAllFrames'] = 0
    new_text = ""
    for key, value in metadata_dict.items():
        new_text= new_text + f"{key}={value}\n"
    with open(inffilename, "w") as fp:
        fp.writelines(new_text)
    # run test
    ps = read_cropreporter(filename=inffilename)
    # check labels
    true_dark_labels = ['Fdark', 'F0', 'Fm', 'PSD3', 'PSD4', 'PSD5', 'PSD6']
    assert all([a == b for a, b in zip(ps.darkadapted.coords['frame_label'].to_dict()['data'], true_dark_labels)])
    true_light_labels = ['Flight', 'Fp', 'Fmp', 'PSL3', 'PSL4', 'PSL5', 'PSL6']
    assert all([a == b for a, b in zip(ps.lightadapted.coords['frame_label'].to_dict()['data'], true_light_labels)])


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
