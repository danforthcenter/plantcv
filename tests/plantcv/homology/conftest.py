import pytest
import os
import numpy as np
import pandas as pd
import matplotlib

# Disable plotting
matplotlib.use("Template")


class HomologyTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")
        # Binary mask for RGB image
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_plant_mask.png")
        # Composed contours file
        self.small_composed_contours_file = os.path.join(self.datadir, "setaria_small_plant_composed_contours.npz")
        # Pseudolandmarks CSV file
        self.plms = os.path.join(self.datadir, "plms_df.csv")
        # Pseudolandmarks Space CSV file
        self.plms_space = os.path.join(self.datadir, "plms_space_df.csv")
        # Pseudolandmarks Starscape CSV file
        self.plms_starscape = os.path.join(self.datadir, "plms_starscape_df.csv")
        # Pseudolandmarks Landmarks CSV file
        self.plms_landmarks = os.path.join(self.datadir, "plms_landmarks.csv")
        # Annotated pseudolandmarks
        self.plms_annotated = os.path.join(self.datadir, "plms_annotated.csv")

    @staticmethod
    def load_composed_contours(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['contour']

    @staticmethod
    def read_df(csv):
        """Load CSV file into a dataframe."""
        return pd.read_csv(csv)


@pytest.fixture(scope="session")
def homology_test_data():
    """Test data object for the PlantCV homology submodule."""
    return HomologyTestData()
