"""Tests for pcv.print_image."""
import pytest
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from plantcv.plantcv import print_image, PSII_data


def test_print_image(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Create test image
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


def test_print_image_bad_type():
    """Test for PlantCV."""
    with pytest.raises(RuntimeError):
        print_image(img=[], filename="/dev/null")


def test_print_image_matplotlib(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Create test image
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    plt.figure()
    plt.imshow(img)
    plot = plt.gcf()
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    print_image(img=plot, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


def test_print_image_dataarray(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    da = test_data.psii_cropreporter('ojip_dark').squeeze('measurement', drop=True)
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    print_image(img=da, col='frame_label', filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


def test_print_image_psiidata():
    """Test for PlantCV."""
    psii = PSII_data()
    with pytest.raises(RuntimeError):
        print_image(img=psii, filename='/dev/null')


def test_print_altair_chart(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'chart.html')
    source = pd.DataFrame({
        "x": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
        "y": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "z": ["row", "row", "row", "row", "row", "row", "row", "row", "row"]
    })
    chart = alt.Chart(source).mark_area(interpolate='monotone').encode(alt.X('x:O'), alt.Y('y:Q')).facet(alt.Row("z:O"))
    print_image(img=chart, filename=filename)
    assert os.path.exists(filename)
