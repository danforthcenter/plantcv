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
        self.datadir_npq = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "testdata", "cropreporter_npq")
        self.datadir_v653 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "..", "testdata", "cropreporter_v653")
        self.datadir_gfp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "testdata", "cropreporter_gfp")
        self.datadir_rfp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "testdata", "cropreporter_rfp")
        self.datadir_aph = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "testdata", "cropreporter_aph")
        self.datadir_pmt = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "..", "testdata", "cropreporter_pmt")

        # CropReporter data file
        self.cropreporter = os.path.join(self.datadir_v441, "PSII_HDR_020321_WT_TOP_1.INF")
        self.cropreporter_v653 = os.path.join(self.datadir_v653, "HDR_dark_light.INF")
        self.cropreporter_npq = os.path.join(self.datadir_npq, "PSII_HDR_020321_WT_TOP_1.INF")
        self.cropreporter_gfp = os.path.join(self.datadir_gfp, "HDR_DYSeed_20251222191634684.INF")
        self.cropreporter_rfp = os.path.join(self.datadir_rfp, "HDR_DYSeed_20251222191634684.INF")
        self.cropreporter_aph = os.path.join(self.datadir_aph, "HDR_2025-12-12_tob1_20251212205712029.INF")
        self.cropreporter_pmt = os.path.join(self.datadir_pmt, "HDR_E0001P0007N0001_GCU24100090_20260226.INF")
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
        elif var == 'pam_time':
            # Create a mock 4D cube for PMT (x, y, frame, measurement)
            frame_labels = ["Fdark", "F0", "Fm", "Fdarksat", "Flight", "Fsp", "Fmp", "Flightsat", "F0p", "Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp"]
            measurements = ["t0", "t1", "t2"]
            # Generate dummy data for 13 labels across 3 timepoints
            data = np.zeros((10, 10, len(frame_labels), len(measurements)))
            data[5, 5, :, :] = 50  # Mock intensity

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
