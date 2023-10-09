import pytest
import os
import pandas as pd
from plantcv.plantcv import params
from plantcv.plantcv.homology import constella


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_constella(debug, tmpdir, homology_test_data):
    """Test for PlantCV."""
    # Set debug
    params.debug = debug
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    params.debug_outdir = cache_dir
    # Read input dataframes
    cur_plms = homology_test_data.read_df(homology_test_data.plms_space)
    cur_plms.group = None
    starscape_df = homology_test_data.read_df(homology_test_data.plms_starscape)
    cur_plms, _ = constella(cur_plms=cur_plms, pc_starscape=starscape_df, group_iter=1,
                            outfile_prefix=os.path.join(cache_dir, "constella"))
    assert max(cur_plms.group) == 10


def test_constella_one_time(homology_test_data):
    """Test for PlantCV."""
    # Read input dataframes
    cur_plms = homology_test_data.read_df(homology_test_data.plms_space)
    cur_plms.group = None
    starscape_df = homology_test_data.read_df(homology_test_data.plms_starscape)
    cur_plms = cur_plms.loc[cur_plms.filename.eq("B100_rep1_d10")]
    starscape_df = starscape_df.loc[starscape_df.filename.eq("B100_rep1_d10")]
    cur_plms, _ = constella(cur_plms=cur_plms, pc_starscape=starscape_df, group_iter=1, outfile_prefix="constella")
    assert max(cur_plms.group) == 8


def test_constella_redundant_plm(homology_test_data):
    """Test for PlantCV."""
    # Read input dataframes
    cur_plms = homology_test_data.read_df(homology_test_data.plms_space)
    cur_plms.group = None
    starscape_df = homology_test_data.read_df(homology_test_data.plms_starscape)
    # Append duplicate plms
    cur_plms = pd.concat([cur_plms, cur_plms.iloc[0].to_frame().T], ignore_index=True)
    cur_plms = cur_plms.reset_index(drop=True)
    starscape_df = pd.concat([starscape_df, starscape_df.iloc[0].to_frame().T], ignore_index=True)
    starscape_df = starscape_df.reset_index(drop=True)
    cur_plms, _ = constella(cur_plms=cur_plms, pc_starscape=starscape_df, group_iter=1, outfile_prefix="constella")
    assert max(cur_plms.group) == 11
