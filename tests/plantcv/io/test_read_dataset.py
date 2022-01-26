import pytest
import os
import cv2
import numpy as np
from plantcv.plantcv.io import read_dataset


def test_read_dataset_non_existent_path():
    """Test for PlantCV."""
    with pytest.raises(IOError):
        _ = read_dataset(source_path='./non_existent_dir', pattern='')


@pytest.mark.parametrize("test_pattern,expected", [['', 5], ['0', 1]])
def test_read_dataset(test_pattern, expected, tmpdir):
    """Test for PlantCV."""
    # Create a tmp directory
    cache_dir = tmpdir.mkdir("cache")
    rng = np.random.default_rng()
    n_images = 5  # must be the same as 'expected' when pattern is ''
    img_size = (10, 10, 3)
    # create several random images and write them to the temporary directory
    for i in range(n_images):
        img = rng.integers(low=0, high=255, size=img_size, dtype=np.uint8, endpoint=True)
        cv2.imwrite(os.path.join(cache_dir, f"tmp_img_{i}.png"), img)
    # run the function to read the temporary directory
    img_paths = read_dataset(source_path=cache_dir, pattern=test_pattern)
    assert len(img_paths) == expected
