import pytest
import os
import pickle as pkl
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib

# Disable plotting
matplotlib.use("Template")


class FilterTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Binary mask for eccentricity filter 
        self.small_bin_fill = os.path.join(self.datadir,"floodfill.png")


@pytest.fixture(scope="session")
def filter_test_data():
    """Test data object for the PlantCV filter submodule."""
    return FilterTestData()