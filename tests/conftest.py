import pytest
import os
import json
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib
from tests import synthetic

# Disable plotting
matplotlib.use("Template")


class PhotosynthesisTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directories
        self.datadir_v441 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "testdata", "cropreporter_v441")
        self.datadir_npq = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "testdata", "cropreporter_npq")
        self.datadir_v653 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "testdata", "cropreporter_v653")
        self.datadir_gfp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "testdata", "cropreporter_gfp")
        self.datadir_rfp = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "testdata", "cropreporter_rfp")
        self.datadir_aph = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "testdata", "cropreporter_aph")
        self.datadir_pmt = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "testdata", "cropreporter_pmt")

        # CropReporter data file
        self.cropreporter = os.path.join(self.datadir_v441, "PSII_HDR_020321_WT_TOP_1.INF")
        self.cropreporter_v653 = os.path.join(self.datadir_v653, "HDR_dark_light.INF")
        self.cropreporter_npq = os.path.join(self.datadir_npq, "PSII_HDR_020321_WT_TOP_1.INF")
        self.cropreporter_gfp = os.path.join(self.datadir_gfp, "HDR_DYSeed_20251222191634684.INF")
        self.cropreporter_rfp = os.path.join(self.datadir_rfp, "HDR_DYSeed_20251222191634684.INF")
        self.cropreporter_aph = os.path.join(self.datadir_aph, "HDR_2025-12-12_tob1_20251212205712029.INF")
        self.cropreporter_pmt = os.path.join(self.datadir_pmt, "HDR_E0001P0007N0001_GCU24100090_20260226.INF")

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
            data = np.dstack([f0, f1, f2, f3])[..., None]
        elif var == 'ojip_light':
            frame_labels = ['Fdark', 'Fp', '2', 'Fmp']
            measurements = ['t1']
            data = np.dstack([f0, f1, f2, f3])[..., None]
        elif var == 'pam_time':
            # Create a mock 4D cube for PMT (x, y, frame, measurement)
            frame_labels = ["Fdark", "F0", "Fm", "Fdarksat", "Flight", "Fp", "Fmp", "Flightsat", "F0p", "Fdarkpp", "F0pp",
                            "Fmpp", "Fdarksatpp"]
            measurements = ["t0", "t1", "t2"]
            # Generate dummy data for 13 labels across 3 timepoints
            data = np.zeros((10, 10, len(frame_labels), len(measurements)))
            data[5, 5, :, :] = 50  # Mock intensity

        # Generate a frame_num list that matches the length of frame_labels
        frame_numbers = list(range(len(frame_labels)))

        # Create DataArray
        da = xr.DataArray(data=data,
                          dims=('x', 'y', 'frame_label', 'measurement'),
                          coords={'frame_label': frame_labels, 'frame_num': ('frame_label', frame_numbers),
                                  'measurement': measurements}, name=var)
        return da


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # heic image
        self.heic_img = os.path.join(self.datadir, "example.HEIC")
        # Outputs results file - JSON
        self.outputs_results_json = os.path.join(self.datadir, "outputs_results.json")
        # Outputs results file - CSV
        self.outputs_results_csv = os.path.join(self.datadir, "outputs_results.csv")
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
        # Fmin image
        self.fmin = os.path.join(self.datadir, "FLUO_TV_min.png")
        # Fmax image
        self.fmax = os.path.join(self.datadir, "FLUO_TV_max.png")
        # Kmeans classifier directory
        self.kmeans_classifier_dir = os.path.join(self.datadir, "kmeans_classifier_dir")
        # Circle Wells for Hough Circle
        self.hough_circle = os.path.join(self.datadir, "circle-wells.png")
        # Kmeans classifier grayscale directory
        self.kmeans_classifier_gray_dir = os.path.join(self.datadir, "kmeans_classifier_gray_dir")
        # nd2 file
        self.nd2_img = os.path.join(self.datadir, "test_nd2_img.nd2")
        # flir thermal img
        self.flir_img = os.path.join(self.datadir, "FLIR_test.jpg")
        # parallel results to process
        self.parallel_results_dir = os.path.join(self.datadir, "parallel_results")
        # appended results file
        self.appended_results_file = os.path.join(self.datadir, "appended_results.json")
        # new results file
        self.new_results_file = os.path.join(self.datadir, "new_results.json")
        # valid results file
        self.valid_json_file = os.path.join(self.datadir, "valid.json")
        # invalid results file
        self.invalid_results_file = os.path.join(self.datadir, "invalid_results.json")
        # plantcv general results file
        self.plantcv_results_file = os.path.join(self.datadir, "plantcv_results.json")
        # List of masks
        self.masks_list = os.path.join(self.datadir, "masks_list.pkl")
        # photosynthesis test data class as attribute
        self.photosynthesis = PhotosynthesisTestData()

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

    @staticmethod
    def load_json(json_file):
        """JSON loader helper function."""
        with open(json_file, "r") as fp:
            data = json.load(fp)
            return data

    def new_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.new_results_file)

    def appended_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.appended_results_file)

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

    def _make_dummy_npq(self, f0, f1, f2, f3):
        """Create PSII data with two frames"""
        # Create DataArray
        ojip_dark = xr.DataArray(data=np.dstack([f0, f1, f2, f3])[..., None],
                                 dims=('x', 'y', 'frame_label', 'measurement'),
                                 coords={'frame_label': ['Fdark', 'F0', 'Fm', '3'],
                                         'frame_num': ('frame_label', [0, 1, 2, 3]),
                                         'measurement': ['t0']}, name="ojip_dark")
        ojip_light = xr.DataArray(data=np.dstack([f1, f2, f3, f0])[..., None],
                                  dims=('x', 'y', 'frame_label', 'measurement'),
                                  coords={'frame_label': ['Flight', 'Fp', 'Fmp', 'Flightsat'],
                                          'frame_num': ('frame_label', [0, 1, 2, 3]),
                                          'measurement': ['t1']}, name="ojip_light")

        sub_psd = type("subpsdata", (object,), {
            "ojip_dark": ojip_dark
        })
        sub_psl = type("subpsdata2", (object,), {
            "ojip_light": ojip_light
        })

        ps = type("psdata", (object,), {
            'metadata': {
                "ImageRows": 10,
                "ImageCols": 10
            },
            "psl": sub_psl,
            "psd": sub_psd,
            "pml": None,
            "pmd": None,
            "ojip_dark": ojip_dark,
            "ojip_light": ojip_light
        })
        return ps

    def psii_cropreporter_new(self, var):
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

        atts = ["APH", "CHL", "CLR", "PSD", "PSL", "SPECTRAL", "NPQ", "GFP", "RFP", "OJIP_LIGHT", "OJIP_DARK", "PAM_TIME",
                "PAM_LIGHT", "PAM_DARK"]

        # set specific labels for xarray for dark and light adapted
        if var == 'ojip_dark':
            d = np.dstack([f0, f1, f2, f3])[..., None]
            frame_labels = ['Fdark', 'F0', 'Fm', '3']
            frame_nums = [0, 1, 2, 3]
            measurements = ['t0']
            keyname = "ojip_dark"
            var = "psd"
        elif var == 'ojip_light':
            d = np.dstack([f0, f1, f2, f3])[..., None]
            frame_labels = ['Fdark', 'Fp', '2', 'Fmp']
            frame_nums = [0, 1, 2, 3]
            measurements = ['t1']
            keyname = "ojip_light"
            var = "psl"
        elif var == "ojip_bad":
            d = np.dstack([f0, f1, f2, f3])[..., None]
            frame_labels = ['Fdark', 'Fp', '2', 'Fmp']
            frame_nums = [0, 1, 2, 3]
            measurements = ['t1']
            keyname = "bad"
            atts = ["pmt", "worse", "terrible", "nogood"]
            var = "bad"
        elif var == "ojip_both":
            ps = self._make_dummy_npq(f0, f1, f2, f3)
            var = "npq"
        elif var == "pam_time":
            d = np.dstack([f0, f1, f2, f3,
                           f3, f3, f3, f3,
                           f3, f3, f3, f3])[..., None]
            frame_labels = ["Fdark", "F0", "Fm", "Fdarksat",
                            "Flight", "Fp", "Fmp", "Flightsat",
                            "Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp"]
            frame_nums = [i for i in range(12)]
            measurements = ["t1"]
            keyname = "pmt"
        if var != "npq":
            # Create DataArray
            da = xr.DataArray(data=d,
                              dims=('x', 'y', 'frame_label', 'measurement'),
                              coords={'frame_label': frame_labels,
                                      'frame_num': ('frame_label', frame_nums),
                                      'measurement': measurements},
                              name=var)
            if var not in ["ojip_light", "ojip_dark"]:
                sub_ps = type("subpsdata", (object,), {
                    keyname: da
                })
            else:
                sub_ps = da

            ps = type("psdata", (object,), {
                'metadata': {
                    "ImageRows": 10,
                    "ImageCols": 10
                },
                var: sub_ps
            })
        # set other attributes to None
        for att in atts:
            if not hasattr(ps, att.lower()):
                setattr(ps, att.lower(), None)
        return ps

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

    @staticmethod
    def psii_walz_new(var):
        """Create and return synthetic psii dataarrays from walz"""
        # create darkadapted
        if var in ['ojip_dark', 'ojip_both']:
            keyname = "psd"
            other_keyname = "psl"
            i = 0
            fmin = np.ones((10, 10), dtype='uint8') * ((i+15)*2)
            fmax = np.ones((10, 10), dtype='uint8') * (200-i*15)
            data = np.stack([fmin, fmax], axis=2)

            frame_nums = range(0, 2)
            indf = ['F0', 'Fm']
            ps_dad = xr.DataArray(
                data=data[..., None],
                dims=('x', 'y', 'frame_label', 'measurement'),
                coords={'frame_label': indf,
                        'frame_num': ('frame_label', frame_nums),
                        'measurement': ['t0']},
                name='ojip_dark'
            )

            if var == "ojip_dark":
                sub_ps = type("subpsdata", (object,), {
                    var: ps_dad
                })
                ps = type("psdata", (object,), {
                    'metadata': {
                        "ImageRows": 10,
                        "ImageCols": 10
                    },
                    keyname: sub_ps,
                    other_keyname: None,
                    "pmt": None,
                    "pml": None,
                    "pmd": None,
                    var: ps_dad
                })
                return ps

        # create lightadapted
        if var in ['ojip_light', 'ojip_both']:
            da_list = []
            measurement = []
            keyname = "psl"
            other_keyname = "psd"

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
            ps_dal = xr.concat(da_list, 'measurement')
            ps_dal.name = 'ojip_light'
            ps_dal.coords['measurement'] = prop_idx

            if var == 'ojip_light':
                sub_ps = type("subpsdata", (object,), {
                    var: ps_dal
                })
                ps = type("psdata", (object,), {
                    'metadata': {
                        "ImageRows": 10,
                        "ImageCols": 10
                    },
                    keyname: sub_ps,
                    other_keyname: None,
                    "pmt": None,
                    "pml": None,
                    "pmd": None,
                    var: ps_dal
                })
                return ps

        if var == "ojip_both":
            sub_psd = type("subpsdata", (object,), {
                "ojip_dark": ps_dad
            })
            sub_psl = type("subpsdata", (object,), {
                "ojip_light": ps_dal
            })

            ps = type("psdata", (object,), {
                'metadata': {
                    "ImageRows": 10,
                    "ImageCols": 10
                },
                "psd": sub_psd,
                "psl": sub_psl,
                "ojip_light": ps_dal,
                "ojip_dark": ps_dad,
                "pmt": None,
                "pml": None,
                "pmd": None
            })
            return ps

    @staticmethod
    def make_synthetic_pmt():
        """Build a 4x4 PMT cube laid out the way PMT._load fills it.

        t0 = dark-adapted baseline, t1 = light, t2 = recovery (also holds F0p).
        Every frame_label is zero outside the measurement it belongs to.
        """
        frame_labels = ["Fdark", "F0", "Fm", "Fdarksat",
                        "Flight", "Fp", "Fmp", "Flightsat",
                        "Fdarkpp", "F0pp", "Fmpp", "Fdarksatpp",
                        "F0p"]
        measurements = ["t0", "t1", "t2"]
        data = np.zeros((4, 4, len(frame_labels), len(measurements)))

        def put(label, meas, value):
            data[:, :, frame_labels.index(label), measurements.index(meas)] = value

        put("F0", "t0", 100)
        put("Fm", "t0", 500)
        put("Fp", "t1", 200)
        put("Fmp", "t1", 300)
        put("Fmpp", "t2", 400)
        put("F0p", "t2", 90)

        da = xr.DataArray(data=data,
                          dims=("x", "y", "frame_label", "measurement"),
                          coords={"frame_label": frame_labels,
                                  "frame_num": ("frame_label", list(range(len(frame_labels)))),
                                  "measurement": measurements},
                          name="pam_time")
        sub_ps = type("subpsdata", (object,), {"pam_time": da})
        return type("psdata", (object,), {"pmt": sub_ps})


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()


@pytest.fixture
def synthetic_mask():
    """Binary mask of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_mask()


@pytest.fixture
def synthetic_rgb():
    """BGR image of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_rgb()


@pytest.fixture
def synthetic_gray():
    """Grayscale image of the synthetic plant (see tests/synthetic.py)."""
    return synthetic.plant_gray()
