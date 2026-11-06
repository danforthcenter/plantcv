"""Tests for detect_color_card."""
import pytest
import numpy as np
from plantcv.plantcv._globals import params
from plantcv.plantcv.transform.detect_color_card import detect_color_card
from plantcv.plantcv.transform.standard_matrices import std_color_matrix, astro_color_matrix
from tests import synthetic


@pytest.mark.parametrize("rotation", [0, 1, 2, 3])
def test_detect_color_card(rotation):
    """Test for PlantCV."""
    # The card is drawn with the standard chip colors, white chip first; detection rotates the card so the white
    # chip is first whatever the orientation
    rgb_img = synthetic.color_card(rotation=rotation)
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="classic")
    params.function_args = {}
    assert np.allclose(color_matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)


def test_detect_color_card_set_size():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40))
    params.function_args = {}
    assert np.allclose(color_matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)


def test_draw_nonuniform_color_chips():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    # Radii of 5-10 px fit inside the 49 px chips
    radii = [5 + i // 4 for i in range(24)]
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)
    params.function_args = {}
    assert np.allclose(color_matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)


def test_draw_nonuniform_color_chips_len_mismatch():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    radii = [3*(i+1) for i in range(5)]
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=(40, 40), radius=radii)
    params.function_args = {}


def test_detect_color_card_none_found():
    """Test for PlantCV."""
    # The synthetic plant has no square objects of the minimum chip size
    rgb_img = synthetic.plant_rgb()
    with pytest.raises(RuntimeError, match="No color card found"):
        _ = detect_color_card(rgb_img=rgb_img)
    params.function_args = {}


def test_detect_color_card_incorrect_block_size():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, block_size=2)
    params.function_args = {}


def test_detect_color_card_partial_card():
    """Test for PlantCV."""
    # Cut off the bottom row of chips: 5 rows of chips do not fill the 6-row grid of chip centers
    rgb_img = synthetic.color_card()[:-synthetic.COLOR_CARD_MARGIN - synthetic.COLOR_CARD_PITCH]
    with pytest.raises(RuntimeError, match="Centers do not map 1 to 1"):
        _ = detect_color_card(rgb_img=rgb_img, aspect_ratio=2, solidity=0.5)
    params.function_args = {}


def test_detect_color_card_incorrect_card_size():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size=100)
    params.function_args = {}


def test_detect_color_card_incorrect_card_type():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    with pytest.raises(RuntimeError):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="pantone")
    params.function_args = {}


def test_detect_color_card_masked_aruco_tags(capsys):
    """Test for PlantCV."""
    # The scene has both a ColorChecker and an astro card; detection still finds the ColorChecker
    rgb_img = synthetic.color_card_scene()
    color_matrix = detect_color_card(rgb_img=rgb_img)
    params.function_args = {}
    captured = capsys.readouterr()
    assert captured.err == "Warning: Image contains an ArUco tag, should you be using color_chip_size='astro'?\n"
    assert np.allclose(color_matrix, std_color_matrix(pos=3), rtol=0, atol=1e-12)


def test_detect_astro_card():
    """Test for PlantCV."""
    rgb_img = synthetic.astro_card()
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
    assert np.allclose(color_matrix, astro_color_matrix(), rtol=0, atol=1e-12)


def test_detect_astro_card_missing_aruco_tags(capsys):
    """Test for PlantCV."""
    # Leave out tag 49; the other three tags still locate the card
    rgb_img = synthetic.astro_card(tag_ids=(46, 47, 48, None))
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
    captured = capsys.readouterr()
    assert "Missing 1 aruco tag(s) in image" in captured.err
    assert np.allclose(color_matrix, astro_color_matrix(), rtol=0, atol=1e-12)


def test_detect_astro_card_extra_aruco_tag(capsys):
    """Test for PlantCV."""
    # Tag 0 in place of tag 49 is ignored, and tag 49 is missing
    rgb_img = synthetic.astro_card(tag_ids=(46, 47, 48, 0))
    color_matrix = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
    captured = capsys.readouterr()
    assert "Missing 1 aruco tag(s) in image" in captured.err
    assert np.allclose(color_matrix, astro_color_matrix(), rtol=0, atol=1e-12)


def test_detect_astro_card_duplicate_aruco_tags():
    """Test for PlantCV."""
    # Tag 47 in place of tag 46
    rgb_img = synthetic.astro_card(tag_ids=(47, 47, 48, 49))
    with pytest.raises(RuntimeError, match="ID = 47"):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}


def test_detect_astro_card_no_aruco_tags():
    """Test for PlantCV."""
    rgb_img = synthetic.color_card()
    with pytest.raises(RuntimeError, match="No ArUco tags detected"):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}


def test_detect_astro_card_wrong_aruco_tags():
    """Test for PlantCV."""
    # Tags 0-3 are ArUco tags, but not astro card tags
    rgb_img = synthetic.astro_card(tag_ids=(0, 1, 2, 3))
    with pytest.raises(RuntimeError, match="No expected ArUco tags"):
        _ = detect_color_card(rgb_img=rgb_img, color_chip_size="astro")
    params.function_args = {}
