import pytest
from plantcv.plantcv import params
from plantcv.plantcv.homology import space


@pytest.mark.parametrize("debug", ["plot", None])
def test_space(debug, homology_test_data):
    """Test for PlantCV."""
    # Set debug
    params.debug = debug
    # Read input dataframe
    cur_plms = homology_test_data.read_df(homology_test_data.plms)
    df = space(cur_plms=cur_plms, include_bound_dist=True, include_centroid_dist=True, include_orient_angles=True)
    expected = ["group", "plmname", "filename", "plm_x", "plm_y", "SS_x", "SS_y", "TS_x", "TS_y", "CC_ratio",
                "bot_left_dist", "bot_right_dist", "top_left_dist", "top_right_dist", "centroid_dist", "orientation",
                "centroid_orientation"]
    result = list(df.columns)
    assert all([i == j] for i, j in zip(expected, result))
