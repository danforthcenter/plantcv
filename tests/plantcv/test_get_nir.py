import os
from plantcv.plantcv import get_nir


def test_get_nir_sv(test_data):
    """Test for PlantCV."""
    nirpath = get_nir(path=test_data.snapshot_dir, filename="VIS_SV_0_z300_h1_g0_e85_v500_93054.png")
    expected = os.path.join(test_data.snapshot_dir, "NIR_SV_0_z300_h1_g0_e15000_v500_93059.png")
    assert nirpath == expected


def test_get_nir_tv(test_data):
    """Test for PlantCV."""
    nirpath = get_nir(path=test_data.snapshot_dir, filename="VIS_TV_0_z300_h1_g0_e85_v500_93054.png")
    expected = os.path.join(test_data.snapshot_dir, "NIR_TV_0_z300_h1_g0_e15000_v500_93059.png")
    assert nirpath == expected
