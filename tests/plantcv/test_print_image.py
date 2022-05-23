import pytest
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import ggplot
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


def test_print_image_plotnine(tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    dataset = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]})
    img = ggplot(data=dataset)
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    print_image(img=img, filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


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
    da = test_data.psii_cropreporter('darkadapted').squeeze('measurement', drop=True)
    filename = os.path.join(cache_dir, 'plantcv_print_image.png')
    print_image(img=da, col='frame_label', filename=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


def test_print_image_psiidata():
    """Test for PlantCV."""
    psii = PSII_data()
    with pytest.raises(RuntimeError):
        print_image(img=psii, filename='/dev/null')
