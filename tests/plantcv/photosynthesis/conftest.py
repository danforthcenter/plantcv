import pytest
import os
import numpy as np
import xarray as xr
import matplotlib

# Disable plotting
matplotlib.use("Template")


class PhotosynthesisTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directories
        self.datadir_v441 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "..", "testdata", "cropreporter_v441")
        self.datadir_v653 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "..", "testdata", "cropreporter_v653")
        # CropReporter data file
        self.cropreporter = os.path.join(self.datadir_v441, "PSII_HDR_020321_WT_TOP_1.INF")
        self.cropreporter_v653 = os.path.join(self.datadir_v653, "HDR_dark_light.INF")
        # Mask image
        self.ps_mask = os.path.join(self.datadir_v441, "PSII_HDR_020321_WT_TOP_1_mask.png")

    @staticmethod
    def create_ps_mask():
        """Create simple mask for PSII"""
        mask = np.zeros((10, 10), dtype=np.uint8)
        mask[5, 5] = 255
        return mask

    def psii_cropreporter(self, var):
        """Create simple data for PSII"""
        # sample images
        f0 = self.create_ps_mask()
        f0[5, 5] = 1
        f1 = self.create_ps_mask()
        f1[5, 5] = 2
        f2 = self.create_ps_mask()
        f2[5, 5] = 10
        f3 = self.create_ps_mask()
        f3[5, 5] = 8

        # set specific labels for xarray for dark and light adapted
        if var == 'ojip_dark':
            frame_labels = ['Fdark', 'F0', 'Fm', '3']
            measurements = ['t0']
        elif var == 'ojip_light':
            frame_labels = ['Fdark', 'Fp', '2', 'Fmp']
            measurements = ['t1']

        # Create DataArray
        da = xr.DataArray(data=np.dstack([f0, f1, f2, f3])[..., None],
                          dims=('x', 'y', 'frame_label', 'measurement'),
                          coords={'frame_label': frame_labels, 'frame_num': ('frame_label', [0, 1, 2, 3]),
                                  'measurement': measurements}, name=var)
        return da


@pytest.fixture(scope="session")
def photosynthesis_test_data():
    """Test data object for the PlantCV photosynthesis submodule."""
    return PhotosynthesisTestData()
