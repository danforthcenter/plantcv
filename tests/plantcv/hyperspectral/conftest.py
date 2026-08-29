import pytest
import os
import matplotlib
import numpy as np
import pickle as pkl

# Disable plotting
matplotlib.use("Template")


class HyperspectralTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "testdata")
        self.envi_bil_file = os.path.join(self.datadir, "darkReference")
        self.envi_no_default = os.path.join(self.datadir, "darkReference2")
        self.envi_appox_pseudo = os.path.join(self.datadir, "darkReference3")
        self.envi_bad_interleave = os.path.join(self.datadir, "darkReference4")
        self.arcgis = os.path.join(self.datadir, "darkReference_arcgis")
        self.arcgis_hdr = os.path.join(self.datadir, "darkReference_arcgis.hdr")
        self.bad_filename = os.path.join(self.datadir, "darkReference0")
        self.hsi_file = os.path.join(self.datadir, "hsi.pkl")
        self.hsi_mask_file = os.path.join(self.datadir, "hsi_mask.png")
        self.hsi_whiteref_file = os.path.join(self.datadir, "hsi_whiteref.pkl")
        self.hsi_darkref_file = os.path.join(self.datadir, "hsi_darkref.pkl")
        self.savi_file = os.path.join(self.datadir, "savi.pkl")

    @staticmethod
    def load_hsi(pkl_file):
        """Load PlantCV Spectral_data pickled object."""
        with open(pkl_file, "rb") as fp:
            return pkl.load(fp)

    @staticmethod
    def create_envi_data(outdir, filename, default_bands=None):
        """Create a small ENVI datacube and the matching header file.

        Inputs:
            outdir        = Directory to write the data and header files to
            filename      = Base name of the data and header files
            default_bands = Value of the default bands header field, or None to leave the field out

        Returns:
            datafile      = Path of the ENVI data file

        :param outdir: str
        :param filename: str
        :param default_bands: str
        :return datafile: str
        """
        lines, samples, bands = 2, 3, 5
        wavelengths = [500.0, 550.0, 600.0, 650.0, 700.0]
        default = "" if default_bands is None else "default bands = {" + default_bands + "}\n"
        header = ("ENVI\n"
                  f"samples = {samples}\n"
                  f"lines = {lines}\n"
                  f"bands = {bands}\n"
                  "header offset = 0\n"
                  "file type = ENVI Standard\n"
                  "data type = 12\n"
                  "interleave = bil\n"
                  "byte order = 0\n"
                  "wavelength units = nm\n"
                  f"{default}"
                  "wavelength = {" + ",".join(str(wl) for wl in wavelengths) + "}\n")
        datafile = os.path.join(str(outdir), filename)
        with open(datafile + ".hdr", "w") as fp:
            fp.write(header)
        # Band Interleaved by Line data stored as unsigned 16-bit integers (ENVI data type 12)
        np.arange(lines * bands * samples, dtype=np.uint16).reshape(lines, bands, samples).tofile(datafile)
        return datafile


@pytest.fixture(scope="session")
def hyperspectral_test_data():
    """Test data object for the PlantCV hyperspectral submodule."""
    return HyperspectralTestData()
