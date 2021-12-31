import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use("Template")


class TransformTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")

    def create_test_img(self, sz_img):
        img = np.random.randint(np.prod(sz_img), size=sz_img) * 255
        img = img.astype(np.uint8)
        return img

    def create_test_img_bin(self, sz_img):
        img = np.zeros(sz_img)
        img[3:7, 2:8] = 1
        return img


@pytest.fixture(scope="session")
def transform_test_data():
    return TransformTestData()
