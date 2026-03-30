"""Tests for the open_url function."""
import pytest
from plantcv.plantcv.io import open_url


def test_open_url():
    """PlantCV Test"""
    url = ("https://datasci.danforthcenter.org/test.jpg")
    rgb_img = open_url(url=url)
    assert rgb_img.shape == (2464, 3280, 3)


def test_open_url_unsupported():
    """PlantCV Test"""
    url = "https://datasci.danforthcenter.org/test.gif"
    with pytest.raises(RuntimeError):
        _ = open_url(url=url)
