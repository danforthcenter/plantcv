import pytest
import os
from plantcv.plantcv import params
from plantcv.plantcv.homology import starscape


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_starscape(debug, tmpdir, homology_test_data):
    """Test for PlantCV."""
    # Set debug
    params.debug = debug
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("sub")
    params.debug_outdir = cache_dir
    # Read input dataframe
    cur_plms = homology_test_data.read_df(homology_test_data.plms_space)
    final_df, _, _ = starscape(cur_plms=cur_plms, group_a="B100_rep1_d10", group_b="B100_rep1_d11",
                               outfile_prefix=os.path.join(cache_dir, "starscape"))
    expected = ["plmname", "filename", "PC1", "PC2", "PC3"]
    result = list(final_df.columns)
    assert all([i == j] for i, j in zip(expected, result))


@pytest.mark.parametrize("debug", ["plot", None])
def test_starscape_2d(debug, homology_test_data):
    """Test for PlantCV."""
    # Set debug
    params.debug = debug
    # Read input dataframe
    cur_plms = homology_test_data.read_df(homology_test_data.plms_space)
    # Drop columns to reduce dataset vars
    cur_plms = cur_plms.drop(columns=["bot_left_dist", "bot_right_dist", "top_left_dist", "top_right_dist",
                                      "centroid_dist", "orientation", "centroid_orientation"])
    final_df, _, _ = starscape(cur_plms=cur_plms, group_a="B100_rep1_d10", group_b="B100_rep1_d11", outfile_prefix="starscape")
    expected = ["plmname", "filename", "PC1", "PC2"]
    result = list(final_df.columns)
    assert all([i == j] for i, j in zip(expected, result))
