import pytest
import os
import numpy as np
import matplotlib

# Disable plotting
matplotlib.use("Template")


class MorphologyTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        # Binary mask
        self.bin_img = os.path.join(self.datadir, "morphology_bin_img.png")
        # Skeleton image
        self.skel_img = os.path.join(self.datadir, "morphology_skel_img.png")
        # Skeleton segments
        self.segments_file = os.path.join(self.datadir, "morphology_segments.npz")
        # Mask image
        self.ps_mask = os.path.join(self.datadir, "FLUO_TV_MASK.png")

    @staticmethod
    def load_segments(npz_file, segment):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1", allow_pickle=True)
        return data[segment].tolist()


@pytest.fixture(scope="session")
def morphology_test_data():
    """Test data object for the PlantCV morphology submodule."""
    return MorphologyTestData()
