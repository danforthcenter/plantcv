"""Tests for the open_url function."""
import pytest
from plantcv.plantcv.io import open_url


def test_open_url():
    """PlantCV Test"""
    url = ("https://github.com/danforthcenter/plantcv-tutorial-simple-rgb-workflow/blob/" +
           "af312af00e21c84efe942132a1910359faadd49a/img/1_B73_sand_C_2023-04-14_10_19_07.jpg?raw=true")
    rgb_img = open_url(url=url)
    assert rgb_img.shape == (3456, 4608, 3)


def test_open_url_unsupported():
    """PlantCV Test"""
    url = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif"
    with pytest.raises(RuntimeError):
        _ = open_url(url=url)
