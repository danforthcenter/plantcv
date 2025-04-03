import pytest
import os
import matplotlib

# Disable plotting
matplotlib.use("Template")


class LearnTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # Training data directory
        self.train_data = os.path.join(self.datadir, "ml_train")
        # RGB values table
        self.rgb_values_table = os.path.join(self.datadir, "rgb_values_table.txt")
        # Kmeans training directory
        self.kmeans_train_dir = os.path.join(self.datadir, "kmeans_train_dir")
        # Kmeans training grayscale directory
        self.kmeans_train_gray_dir = os.path.join(self.datadir, "kmeans_train_gray_dir")


@pytest.fixture(scope="session")
def learn_test_data():
    """Test data object for the PlantCV learn submodule."""
    return LearnTestData()
