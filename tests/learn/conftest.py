import pytest
import os
import matplotlib
from tests import synthetic

# Disable plotting
matplotlib.use("Template")


class LearnTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # RGB values table
        self.rgb_values_table = os.path.join(self.datadir, "rgb_values_table.txt")
        # RGB values table with formatting problems
        self.rgb_values_table_bad = os.path.join(self.datadir, "rgb_values_table_bad.txt")
        # ImageJ Pixel Inspector sampled RGB values
        self.rgb_values_file = os.path.join(self.datadir, "pixel_inspector_rgb_values.txt")


@pytest.fixture(scope="session")
def learn_test_data():
    """Test data object for the PlantCV learn submodule."""
    return LearnTestData()


@pytest.fixture
def nb_train_dirs(tmp_path):
    """Naive Bayes training directories (images, masks) holding the synthetic training image and its mask."""
    imgdir, maskdir = tmp_path / "images", tmp_path / "masks"
    synthetic.write_images(imgdir, {"plant.png": synthetic.nb_train_image()})
    synthetic.write_images(maskdir, {"plant.png": synthetic.plant_mask()})
    return str(imgdir), str(maskdir)


@pytest.fixture(params=[False, True], ids=["rgb", "gray"])
def kmeans_train_dir(request, tmp_path):
    """K-means training directory: the synthetic plant (BGR or gray) three times, and a file that is not an image."""
    img = synthetic.plant_gray() if request.param else synthetic.plant_rgb()
    synthetic.write_images(tmp_path, {f"kmeans_train_{i}.png": img for i in (1, 2, 3)})
    (tmp_path / "kmeans_train_notes.txt").write_text("not an image")
    return str(tmp_path), 1 if request.param else 3
