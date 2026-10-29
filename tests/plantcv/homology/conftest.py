import pytest
import os
import pandas as pd
import matplotlib

# Disable plotting
matplotlib.use("Template")


class HomologyTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
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
    def read_df(csv):
        """Load CSV file into a dataframe."""
        return pd.read_csv(csv)


@pytest.fixture(scope="session")
def homology_test_data():
    """Test data object for the PlantCV homology submodule."""
    return HomologyTestData()
