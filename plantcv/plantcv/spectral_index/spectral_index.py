# Extract one of the predefined indices from a hyperspectral datacube

import os
import numpy as np
import cv2
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.transform import rescale
from plantcv.plantcv.hyperspectral import _find_closest


def ndvi(hsi, distance=20):
    """Normalized Difference Vegetation Index.

    NDVI = (R800 - R670) / (R800 + R670)

    The theoretical range for NDVI is [-1.0, 1.0]

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 670:
        # Obtain index that best represents NIR and red bands
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r800 = (hsi.array_data[:, :, r800_index])
        r670 = (hsi.array_data[:, :, r670_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r800 - r670) / (r800 + r670)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NDVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing distance.")


def gdvi(hsi, distance=20):
    """Green Difference Vegetation Index.

    GDVI = R800 - R550

    The theoretical range for GDVI is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 550:
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r800 = (hsi.array_data[:, :, r800_index])
        r550 = (hsi.array_data[:, :, r550_index])
        # Naturally ranges from -1 to 1
        index_array_raw = r800 - r550
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="GDVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing distance.")


def savi(hsi, distance=20):
    """Soil Adjusted Vegetation Index.

    SAVI = (1.5 * (R800 - R680)) / (R800 + R680 + 0.5)

    The theoretical range for SAVI is [-1.2, 1.2].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 680:
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r680_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 680)
        r800 = (hsi.array_data[:, :, r800_index])
        r680 = (hsi.array_data[:, :, r680_index])
        # Naturally ranges from -1.2 to 1.2
        index_array_raw = (1.5 * (r800 - r680)) / (r800 + r680 + 0.5)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SAVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing distance.")


def pri(hsi, distance=20):
    """Photochemical Reflectance Index.

    PRI = (R531 - R570) / (R531 + R570)

    The theoretical range for PRI is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 570 and (float(hsi.min_wavelength) - distance) <= 531:
        # Obtain index that best approximates 570 and 531 nm bands
        r570_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 570)
        r531_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 531)
        r570 = (hsi.array_data[:, :, r570_index])
        r531 = (hsi.array_data[:, :, r531_index])
        index_array_raw = (r531 - r570) / (r531 + r570)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PRI. Try increasing distance.")


def ari(hsi, distance=20):
    """Anthocyanin Reflectance Index.

    ARI = (1 / R550) - (1 / R700)

    The theoretical range for ARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        r550 = (hsi.array_data[:, :, r550_index])
        r700 = (hsi.array_data[:, :, r700_index])
        index_array_raw = (1 / r550) - (1 / r700)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="ARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating ARI. Try increasing distance.")


def ci_rededge(hsi, distance=20):
    """Chlorophyll Index Red Edge.

    CI_REDEDGE = (R800 / R700) - 1

    The theoretical range for CI_REDEDGE is [-1.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 700:
        r700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r700 = (hsi.array_data[:, :, r700_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -1 to inf
        index_array_raw = (r800 / r700) - 1
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CI_REDEDGE")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CI_REDEDGE. Try increasing distance.")


def cri550(hsi, distance=20):
    """Carotenoid Reflectance Index 550.

    CRI550 = (1 / R510) - (1 / R550)

    The theoretical range for CRI550 is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 550 and (float(hsi.min_wavelength) - distance) <= 510:
        r510_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 510)
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r510 = (hsi.array_data[:, :, r510_index])
        r550 = (hsi.array_data[:, :, r550_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (1 / r510) - (1 / r550)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI510")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CRI510. Try increasing distance.")


def cri700(hsi, distance=20):
    """Carotenoid Reflectance Index 700.

    CRI700 = (1 / R510) - (1 / R700)

    The theoretical range for CRI700 is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 510:
        r510_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 510)
        r700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        r510 = (hsi.array_data[:, :, r510_index])
        r700 = (hsi.array_data[:, :, r700_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (1 / r510) - (1 / r700)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI700")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CRI700. Try increasing distance.")


def egi(rgb_img):
    """Excess Green Index.

    r = R / (R + G + B)
    g = G / (R + G + B)
    b = B / (R + G + B)
    EGI = 2g - r - b

    The theoretical range for EGI is (-1, 2).

    Inputs:
    rgb_img      = Color image (np.array)

    Returns:
    index_array    = Index data as a Spectral_data instance

    :param rgb_img: np.array
    :return index_array: np.array
    """

    # Split the RGB image into component channels
    blue, green, red = cv2.split(rgb_img)
    # Calculate float32 sum of all channels
    total = red.astype(np.float32) + green.astype(np.float32) + blue.astype(np.float32)
    # Calculate normalized channels
    r = red.astype(np.float32) / total
    g = green.astype(np.float32) / total
    b = blue.astype(np.float32) / total
    index_array_raw = (2 * g) - r - b

    hsi = Spectral_data(array_data=None, max_wavelength=0, min_wavelength=0, max_value=255, min_value=0,
                        d_type=np.uint8, wavelength_dict={}, samples=None, lines=None, interleave=None,
                        wavelength_units=None, array_type=None, pseudo_rgb=None, filename=None, default_bands=None)

    return _package_index(hsi=hsi, raw_index=index_array_raw, method="EGI")


def evi(hsi, distance=20):
    """Enhanced Vegetation index.

    EVI = (2.5 * (R800 - R670)) / (1 + R800 + (6 * R670) - (7.5 * R480))

    The theoretical range for EVI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 480:
        r480_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 480)
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r480 = (hsi.array_data[:, :, r480_index])
        r670 = (hsi.array_data[:, :, r670_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (2.5 * (r800 - r670)) / (1 + r800 + (6 * r670) - (7.5 * r480))
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="EVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating EVI. Try increasing distance.")


def mari(hsi, distance=20):
    """Modified Anthocyanin Reflectance Index.

    MARI = ((1 / R550) - (1 / R700)) * R800

    The theoretical range for MARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r550 = (hsi.array_data[:, :, r550_index])
        r700 = (hsi.array_data[:, :, r700_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -inf to inf
        index_array_raw = ((1 / r550) - (1 / r700)) * r800
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MARI. Try increasing distance.")


def mcari(hsi, distance=20):
    """Modified Chlorophyll Absorption in Reflectance Index.

    MCARI = ((R700 - R670) - 0.2 * (R700 - R550)) * (R700 / R670)

    The theoretical range for MCARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        r550 = (hsi.array_data[:, :, r550_index])
        r670 = (hsi.array_data[:, :, r670_index])
        r700 = (hsi.array_data[:, :, r700_index])
        # Naturally ranges from -inf to inf
        index_array_raw = ((r700 - r670) - 0.2 * (r700 - r550)) * (r700 / r670)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MCARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MCARI. Try increasing distance.")


def mtci(hsi, distance=20):
    """MERIS Terrestrial Chlorophyll Index.

    MTCI = (R753.75 - R708.75) / (R708.75 - R681.25)

    The theoretical range for MTCI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 753.75 and (float(hsi.min_wavelength) - distance) <= 681.25:
        r681_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 681.25)
        r708_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 708.75)
        r753_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 753.75)
        r681 = (hsi.array_data[:, :, r681_index])
        r708 = (hsi.array_data[:, :, r708_index])
        r753 = (hsi.array_data[:, :, r753_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (r753 - r708) / (r708 - r681)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MTCI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MTCI. Try increasing distance.")


def ndre(hsi, distance=20):
    """Normalized Difference Red Edge.

    NDRE = (R790 - R720) / (R790 + R720)

    The theoretical range for NDRE is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 790 and (float(hsi.min_wavelength) - distance) <= 720:
        r720_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 720)
        r790_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 790)
        r790 = (hsi.array_data[:, :, r790_index])
        r720 = (hsi.array_data[:, :, r720_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r790 - r720) / (r790 + r720)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NDRE")
    else:
        fatal_error("Available wavelengths are not suitable for calculating NDRE. Try increasing distance.")


def psnd_chla(hsi, distance=20):
    """Pigment Specific Normalized Difference for Chlorophyll a.

    PSND_CHLA = (R800 - R680) / (R800 + R680)

    The theoretical range for PSND_CHLA is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 680:
        r680_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 680)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r680 = (hsi.array_data[:, :, r680_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r800 - r680) / (r800 + r680)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CHLA")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CHLA. Try increasing distance.")


def psnd_chlb(hsi, distance=20):
    """Pigment Specific Normalized Difference for Chlorophyll b.

    PSND_CHLB = (R800 - R635) / (R800 + R635)

    The theoretical range for PSND_CHLB is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 635:
        r635_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 635)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r635 = (hsi.array_data[:, :, r635_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r800 - r635) / (r800 + r635)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CHLB")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CHLB. Try increasing distance.")


def psnd_car(hsi, distance=20):
    """Pigment Specific Normalized Difference for Caroteniods.

    PSND_CAR = (R800 - R470) / (R800 + R470)

    The theoretical range for PSND_CAR is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 470:
        r470_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 470)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r470 = (hsi.array_data[:, :, r470_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r800 - r470) / (r800 + r470)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CAR")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CAR. Try increasing distance.")


def psri(hsi, distance=20):
    """Plant Senescence Reflectance Index.

    PSRI = (R678 - R500) / R750

    The theoretical range for PSRI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 750 and (float(hsi.min_wavelength) - distance) <= 500:
        r500_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 500)
        r678_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 678)
        r750_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 750)
        r500 = (hsi.array_data[:, :, r500_index])
        r678 = (hsi.array_data[:, :, r678_index])
        r750 = (hsi.array_data[:, :, r750_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (r678 - r500) / r750
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSRI. Try increasing distance.")


def pssr_chla(hsi, distance=20):
    """Pigment Specific Simple Ratio for Chlorophyll a.

    PSSR_CHLA = R800 / R680

    The theoretical range for PSSR_CHLA is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 680:
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r680_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 680)
        r800 = (hsi.array_data[:, :, r800_index])
        r680 = (hsi.array_data[:, :, r680_index])
        # Naturally ranges from 0 to inf
        index_array_raw = r800 / r680
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR_CHLA")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR_CHLA. Try increasing distance.")


def pssr_chlb(hsi, distance=20):
    """Pigment Specific Simple Ratio for Chlorophyll b.

    PSSR_CHLB = R800 / R635

    The theoretical range for PSSR_CHLB is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 635:
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r635_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 635)
        r800 = (hsi.array_data[:, :, r800_index])
        r635 = (hsi.array_data[:, :, r635_index])
        # Naturally ranges from 0 to inf
        index_array_raw = r800 / r635
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR_CHLB")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR_CHLB. Try increasing distance.")


def pssr_car(hsi, distance=20):
    """Pigment Specific Simple Ratio for Caroteniods.

    PSSR_CAR = R800 / R470

    The theoretical range for PSSR_CAR is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 470:
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r470_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 470)
        r800 = (hsi.array_data[:, :, r800_index])
        r470 = (hsi.array_data[:, :, r470_index])
        # Naturally ranges from 0 to inf
        index_array_raw = r800 / r470
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR_CAR")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR_CAR. Try increasing distance.")


def rgri(hsi, distance=20):
    """Red/green ratio index (Gamon and Surfus, 1999)
    The theoretical range for RGRI is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 560:
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r560_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        r670 = (hsi.array_data[:, :, r670_index])
        r560 = (hsi.array_data[:, :, r560_index])
        # Naturally ranges from 0 to inf
        index_array_raw = r670 / r560
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="RGRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating RGRI. Try increasing distance.")


def rvsi(hsi, distance=20):
    """Red-Edge Vegetation Stress Index.

    RVSI = ((R714 + R752) / 2) - R733

    The theoretical range for RVSI is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 752 and (float(hsi.min_wavelength) - distance) <= 714:
        r714_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 714)
        r733_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 733)
        r752_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 752)
        r714 = (hsi.array_data[:, :, r714_index])
        r733 = (hsi.array_data[:, :, r733_index])
        r752 = (hsi.array_data[:, :, r752_index])
        # Naturally ranges from -1 to 1
        index_array_raw = ((r714 + r752) / 2) - r733
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="RVSI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating RVSI. Try increasing distance.")


def sipi(hsi, distance=20):
    """Structure-Independent Pigment Index.

    SIPI = (R800 - R670) / (R800 - R480)

    The theoretical range for SIPI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 480:
        r480_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 480)
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r445 = (hsi.array_data[:, :, r480_index])
        r670 = (hsi.array_data[:, :, r670_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (r800 - r670) / (r800 - r445)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SIPI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SIPI. Try increasing distance.")


def sr(hsi, distance=20):
    """Simple Ratio.

    SR = R800 / R670

    The theoretical range for SR is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 670:
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        r670 = (hsi.array_data[:, :, r670_index])
        r800 = (hsi.array_data[:, :, r800_index])
        # Naturally ranges from 0 to inf
        index_array_raw = r800 / r670
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SR")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SR. Try increasing distance.")


def vari(hsi, distance=20):
    """Visible Atmospherically Resistant Index.

    VARI = (R550 - R670) / (R550 + R670 - R480)

    The theoretical range for VARI is (-Inf, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 480:
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r480_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 480)
        r670 = (hsi.array_data[:, :, r670_index])
        r550 = (hsi.array_data[:, :, r550_index])
        r480 = (hsi.array_data[:, :, r480_index])
        # Naturally ranges from -inf to inf
        index_array_raw = (r550 - r670) / (r550 + r670 - r480)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="VARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating VARI. Try increasing distance.")


def vi_green(hsi, distance=20):
    """Vegetation Index using green bands.

    VIgreen = (R550 - R670) / (R550 + R670)

    The theoretical range for VI_GREEN is [-1.0, 1.0].

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 550:
        r670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        r550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        r670 = (hsi.array_data[:, :, r670_index])
        r550 = (hsi.array_data[:, :, r550_index])
        # Naturally ranges from -1 to 1
        index_array_raw = (r550 - r670) / (r550 + r670)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="VI_GREEN")
    else:
        fatal_error("Available wavelengths are not suitable for calculating VI_GREEN. Try increasing distance.")


def wi(hsi, distance=20):
    """Water Index.

    WI = R900 / R970

    The theoretical range for WI is [0.0, Inf).

    Inputs:
    hsi         = hyperspectral image (PlantCV Spectral_data instance)
    distance    = how lenient to be if the required wavelengths are not available

    Returns:
    index_array = Index data as a Spectral_data instance

    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 970 and (float(hsi.min_wavelength) - distance) <= 900:
        r900_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 900)
        r970_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 970)
        r900 = (hsi.array_data[:, :, r900_index])
        r970 = (hsi.array_data[:, :, r970_index])
        # Naturally ranges from 0 to Inf
        index_array_raw = r900 / r970
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="WI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating WBI. Try increasing distance.")


def _package_index(hsi, raw_index, method):
    """Private function to package raw index array as a Spectral_data object.
    Inputs:
    hsi       = hyperspectral data (Spectral_data object)
    raw_index = raw index array
    method    = index method (e.g. NDVI)

    Returns:
    index        = index image as a Spectral_data object.

    :params hsi: __main__.Spectral_data
    :params raw_index: np.array
    :params method: str
    :params index: __main__.Spectral_data
    """
    params.device += 1

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Resulting array is float 32 from varying natural ranges, transform into uint8 for plotting
    all_positive = np.add(raw_index, 2 * np.ones(np.shape(raw_index)))
    scaled = rescale(all_positive)

    # Find array min and max values
    obs_max_pixel = float(np.nanmax(raw_index))
    obs_min_pixel = float(np.nanmin(raw_index))

    index = Spectral_data(array_data=raw_index, max_wavelength=0,
                          min_wavelength=0, max_value=obs_max_pixel,
                          min_value=obs_min_pixel, d_type=np.uint8,
                          wavelength_dict={}, samples=hsi.samples,
                          lines=hsi.lines, interleave=hsi.interleave,
                          wavelength_units=hsi.wavelength_units,
                          array_type="index_" + method.lower(),
                          pseudo_rgb=scaled, filename=hsi.filename, default_bands=None)

    # Restore debug mode
    params.debug = debug

    _debug(visual=index.pseudo_rgb,
           filename=os.path.join(params.debug_outdir, str(params.device) + method + "_index.png"))

    return index
