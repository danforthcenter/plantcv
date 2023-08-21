import pytest
import cv2
import os
import numpy as np
from plantcv.plantcv.visualize.pixel_scatter_vis import pixel_scatter_plot


@pytest.mark.parametrize("ch", ['R', 'G', 'B', 'l', 'a', 'b', 'h', 's', 'v', 'gray'])
def test_pixel_scatter_plot(ch, tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    rng = np.random.default_rng()
    img_size = (10,10,3)
    # create a random image and write it to the temp directory
    img = rng.integers(low=0, high=255, size=img_size, dtype=np.uint8, endpoint=True)
    path_to_img = os.path.join(cache_dir, 'tmp_img.png')
    cv2.imwrite(path_to_img, img)
    # test the function with a list of one path to the random image
    _, _ = pixel_scatter_plot(paths_to_imgs=[path_to_img], x_channel=ch, y_channel='index')
    assert 1


def test_pixel_scatter_plot_wrong_ch(tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    rng = np.random.default_rng()
    img_size = (10,10,3)
    # create a random image and write it to the temp directory
    img = rng.integers(low=0, high=255, size=img_size, dtype=np.uint8, endpoint=True)
    path_to_img = os.path.join(cache_dir, 'tmp_img.png')
    cv2.imwrite(path_to_img, img)
    # test the function with channel parameter that is not an option
    with pytest.raises(RuntimeError):
        _, _ = pixel_scatter_plot(paths_to_imgs=[path_to_img], x_channel='wrong_ch', y_channel='index')

