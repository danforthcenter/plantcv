import pytest
import numpy as np
from plantcv.plantcv._helpers import _hough_circle
from tests import synthetic


def _assert_wells(df):
    """Each found circle is one of the 24 wells, to within a pixel."""
    centers = np.array(synthetic.WELL_CENTERS)
    for x, y, radius in df[["x", "y", "radius"]].to_numpy(dtype=int):
        assert np.min(np.max(np.abs(centers - (x, y)), axis=1)) <= 1
        assert abs(radius - synthetic.WELL_RADIUS) <= 1


def test_hough_circle():
    """Test for PlantCV."""
    # Radii 13-18 find the 24 wells but not the two smaller circles
    df, _ = _hough_circle(synthetic.wells_image(), 20, 50, 30, 13, 18, 24)
    assert df.shape == (24, 3)
    _assert_wells(df)


def test_hough_circle_warn(capsys):
    """Test for PlantCV."""
    # Radii 8-18 also find the two smaller circles, 26 in all, so only the first 24 are kept
    df, _ = _hough_circle(synthetic.wells_image(), 20, 50, 30, 8, 18, 24)
    assert df.shape == (24, 3)
    assert "Number of found circles is 26" in capsys.readouterr().err


def test_hough_circle_none():
    """Test for PlantCV."""
    df, _ = _hough_circle(synthetic.wells_image(), 20, 50, 30, 13, 18, None)
    assert df.shape == (24, 3)
    _assert_wells(df)


def test_hough_no_circles():
    """Test for PlantCV."""
    # No circle has radius 30
    with pytest.raises(RuntimeError):
        _, _ = _hough_circle(synthetic.wells_image(), 20, 50, 30, 30, 30, None)
