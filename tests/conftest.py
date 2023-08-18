import pytest
import os
import pickle as pkl
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib

# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # Flat image directory
        self.snapshot_dir = os.path.join(self.datadir, "snapshot_dir")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Binary mask for RGB image
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_plant_mask.png")
        # Gray image
        self.small_gray_img = os.path.join(self.datadir, "setaria_small_plant_gray.png")
        # Contours file
        self.small_contours_file = os.path.join(self.datadir, "setaria_small_plant_contours.npz")
        # Composed contours file
        self.small_composed_contours_file = os.path.join(self.datadir, "setaria_small_plant_composed_contours.npz")
        # PlantCV Spectral_data object
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        # Binary mask for HSI
        self.hsi_mask_file = os.path.join(self.datadir, "hsi_mask.png")
        # SAVI index file
        self.savi_file = os.path.join(self.datadir, "savi.pkl")
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")
        # RGBA image
        # Image from http://www.libpng.org/pub/png/png-OwlAlpha.html
        # This image may be used, edited and reproduced freely.
        self.rgba_img = os.path.join(self.datadir, "owl_rgba_img.png")
        # ENVI hyperspectral data
        self.envi_bil_file = os.path.join(self.datadir, "darkReference")
        # ENVI hyperspectral data
        self.envi_sample_data = os.path.join(self.datadir,"corn-kernel-hyperspectral.raw")
        # Thermal image
        self.thermal_img = os.path.join(self.datadir, "FLIR2600.csv")
        # Thermal image data
        self.thermal_obj_file = os.path.join(self.datadir, "thermal_img.npz")
        # Thermal image mask
        self.thermal_mask = os.path.join(self.datadir, "thermal_img_mask.png")
        # Bayer image
        self.bayer_img = os.path.join(self.datadir, "bayer_img.png")
        # Naive Bayes trained model file
        self.nb_trained_model = os.path.join(self.datadir, "naive_bayes_pdfs.txt")
        # Naive Bayes bad model file
        self.nb_bad_model = os.path.join(self.datadir, "naive_bayes_pdfs_bad.txt")
        # acute example results
        self.acute_results = np.asarray([[[119, 285]], [[151, 280]], [[168, 267]], [[168, 262]], [[171, 261]], [[224, 269]],
                                         [[246, 271]], [[260, 277]], [[141, 248]], [[183, 194]], [[188, 237]], [[173, 240]],
                                         [[186, 260]], [[147, 244]], [[163, 246]], [[173, 268]], [[170, 272]], [[151, 320]],
                                         [[195, 289]], [[228, 272]], [[210, 272]], [[209, 247]], [[210, 232]]])
        # Fmin image
        self.fmin = os.path.join(self.datadir, "FLUO_TV_min.png")
        # Fmax image
        self.fmax = os.path.join(self.datadir, "FLUO_TV_max.png")
        # Mask image
        self.ps_mask = os.path.join(self.datadir, "FLUO_TV_MASK.png")
        # Multi-plant RGB image
        self.multi_rgb_img = os.path.join(self.datadir, "brassica_multi_rgb_img.jpg")
        # Multi-plant contours file
        self.multi_contours_file = os.path.join(self.datadir, "brassica_multi_contours.npz")
        # Two plants binary mask
        self.multi_bin_img = os.path.join(self.datadir, "brassica_2plants_bin_img.png")
        # Clustered contours names file
        self.cluster_names = os.path.join(self.datadir, "cluster_names.txt")
        # Clustered contours names file with too many labels
        self.cluster_names_too_many = os.path.join(self.datadir, "cluster_names_too_many.txt")

    @staticmethod
    def load_hsi(pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)

    @staticmethod
    def load_contours(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1", allow_pickle=True)
        return data['contours'], data['hierarchy']

    @staticmethod
    def load_composed_contours(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['contour']

    @staticmethod
    def load_npz(npz_file):
        """Load data saved in a NumPy .npz file."""
        data = np.load(npz_file, encoding="latin1")
        return data['arr_0']

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

    @staticmethod
    def psii_walz(var):
        """Create and return synthetic psii dataarrays from walz"""
        # create darkadapted
        if var == 'ojip_dark':
            i = 0
            fmin = np.ones((10, 10), dtype='uint8') * ((i+15)*2)
            fmax = np.ones((10, 10), dtype='uint8') * (200-i*15)
            data = np.stack([fmin, fmax], axis=2)

            frame_nums = range(0, 2)
            indf = ['F0', 'Fm']
            ps_da = xr.DataArray(
                data=data[..., None],
                dims=('x', 'y', 'frame_label', 'measurement'),
                coords={'frame_label': indf,
                        'frame_num': ('frame_label', frame_nums),
                        'measurement': ['t0']},
                name='ojip_dark'
            )

        # create lightadapted
        elif var == 'ojip_light':
            da_list = []
            measurement = []

            for i in np.arange(1, 3):
                indf = ['Fp', 'Fmp']
                fmin = np.ones((10, 10), dtype='uint8') * ((i+15)*2)
                fmax = np.ones((10, 10), dtype='uint8') * (200-i*15)
                data = np.stack([fmin, fmax], axis=2)

                lightadapted = xr.DataArray(
                    data=data[..., None],
                    dims=('x', 'y', 'frame_label', 'measurement'),
                    coords={'frame_label': indf,
                            'frame_num': ('frame_label', range(0, 2))}
                )

                measurement.append((f't{i*40}'))
                da_list.append(lightadapted)

            prop_idx = pd.Index(measurement)
            ps_da = xr.concat(da_list, 'measurement')
            ps_da.name = 'ojip_light'
            ps_da.coords['measurement'] = prop_idx

        return ps_da


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
