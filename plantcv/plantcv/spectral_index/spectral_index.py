# Extract one of the predefined indices from a hyperspectral datacube

import os
import numpy as np
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import Spectral_data
from plantcv.plantcv.transform import rescale
from plantcv.plantcv.hyperspectral import _find_closest

def ndvi(hsi, distance=20):
    """Normalized Difference Vegetation Index.
    The theoretical range for NDVI is [-1.0, 1.0]

    inputs:
    hsi           = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    params.device += 1

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 670:
        # Obtain index that best represents NIR and red bands
        nir_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        red_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        nir = (hsi.array_data[:, :, [nir_index]])
        red = (hsi.array_data[:, :, [red_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (nir - red) / (nir + red)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NDVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing distance.")

def gdvi(hsi, distance=20):
    """Green Difference Vegetation Index [Sripada et al. (2006)]
    The theoretical range for GDVI is [-1.0, 1.0].

    inputs:
    hsi           = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 580:
        nir_index   = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 580)
        nir   = (hsi.array_data[:, :, [nir_index]])
        green = (hsi.array_data[:, :, [green_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = nir - green
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="GDVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing distance.")

def savi(hsi, distance=20):
    """Soil Adjusted Vegetation Index [Huete et al. (1988)]
    The theoretical range for SAVI is [-1.2, 1.2].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 680:
        nir_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        red_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 680)
        nir = (hsi.array_data[:, :, [nir_index]])
        red = (hsi.array_data[:, :, [red_index]])
        # Naturally ranges from -1.2 to 1.2
        index_array_raw = (1.5 * (nir - red)) / (red + nir + 0.5)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SAVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing distance.")

def pri(hsi, distance=20):
    """Photochemical Reflectance Index (https://doi.org/10.1111/j.1469-8137.1995.tb03064.x)
    The theoretical range for PRI is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 570 and (float(hsi.min_wavelength) - distance) <= 531:
        # Obtain index that best approximates 570 and 531 nm bands
        pri570_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 570)
        pri531_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 531)
        pri570 = (hsi.array_data[:, :, [pri570_index]])
        pri531 = (hsi.array_data[:, :, [pri531_index]])
        index_array_raw = (R531- R570)/(R531+ R570)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PRI. Try increasing distance.")

def aci(hsi, distance=20):
    """Anthocyanin content index (Van den Berg et al., 2005)
    The theoretical range for ACI is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 560:
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        nir_index   = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        green = (hsi.array_data[:, :, [green_index]])
        nir   = (hsi.array_data[:, :, [nir_index]])
        index_array_raw = green / nir
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="ACI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating ACI. Try increasing distance.")

def ari(hsi, distance=20):
    """Anthocyanin reflectance index (Gitelson et al., 2001)
    The theoretical range for ARI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        ari550_indes = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        ari700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        ari550 = (hsi.array_data[:, :, [ari550_indes]])
        ari700 = (hsi.array_data[:, :, [ari700_index]])
        index_array_raw = (1 / ari550) - (1 / ari700)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="ARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating ARI. Try increasing distance.")

def cari(hsi, distance=20):
    """Chlorophyll absorption in reflectance index (Daughtry et al., 2000)
    The theoretical range for CARI is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """
    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        cari550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        cari670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        cari700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        cari550 = (hsi.array_data[:, :, [cari550_index]])
        cari670 = (hsi.array_data[:, :, [cari670_index]])
        cari700 = (hsi.array_data[:, :, [cari700_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (cari700 - cari670) - 0.2 * (cari700 - cari550)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CARI. Try increasing distance.")

def ci_rededge(hsi, distance=20):
    """Chlorophyll index red edge (Giteson et al., 2003a)
    The theoretical range for CI_REDEDGE is [-1.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 750:
        rededge_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 750)
        nir_index     = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        rededge = (hsi.array_data[:, :, [rededge_index]])
        nir     = (hsi.array_data[:, :, [nir_index]])
        # Naturally ranges from -1 to inf
        index_array_raw = nir / rededge - 1
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CI_REDEDGE")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CI_REDEDGE. Try increasing distance.")

def cri1(hsi, distance=20):
    """Carotenoid reflectance index (Gitelson et al., 2002b) (note: part 1 of 2)
    The theoretical range for CRI1 is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 550 and (float(hsi.min_wavelength) - distance) <= 510:
        cri1510_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 510)
        cri1550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        cri1510 = (hsi.array_data[:, :, [cri1510_index]])
        cri1550 = (hsi.array_data[:, :, [cri1550_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = 1 / cri1510 - 1 / cri1550
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI1")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CRI1. Try increasing distance.")

def cri2(hsi, distance=20):
    """Carotenoid reflectance index (Gitelson et al., 2002b) (note: part 2 of 2)
    The theoretical range for CRI2 is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 510:
        cri1510_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 510)
        cri1700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        cri1510 = (hsi.array_data[:, :, [cri1510_index]])
        cri1700 = (hsi.array_data[:, :, [cri1700_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = 1 / cri1510 - 1 / cri1700
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="CRI2")
    else:
        fatal_error("Available wavelengths are not suitable for calculating CRI2. Try increasing distance.")

def egi(hsi, distance=20):
    """Excess Green Index (Wobbecke et al., 1995)
    The theoretical range for EGI is (-2/3, 2/3).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 470:
        red_index  = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        blue_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 470)
        red  = (hsi.array_data[:, :, [red_index]])
        green  = (hsi.array_data[:, :, [green_index]])
        blue = (hsi.array_data[:, :, [blue_index]])
        summation = red+green+blue
        r = red/summation
        g = green/summation
        b = blue/summation
        index_array_raw = 2*g - r - b
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="EGI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating EGI. Try increasing distance.")

def evi(hsi, distance=20):
    """Enhanced Vegetation index (Huete et al., 1997)
    The theoretical range for EVI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 470:
        blue_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 470)
        red_index  = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        nir_index  = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        blue = (hsi.array_data[:, :, [blue_index]])
        red  = (hsi.array_data[:, :, [red_index]])
        nir  = (hsi.array_data[:, :, [nir_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="EVI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating EVI. Try increasing distance.")

def mari(hsi, distance=20):
    """Modified anthocyanin reflectance index (Gitelson et al., 2001)
    The theoretical range for MARI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 550:
        mari550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        mari700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        nir_index     = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        mari550 = (hsi.array_data[:, :, [mari550_index]])
        mari700 = (hsi.array_data[:, :, [mari700_index]])
        nir     = (hsi.array_data[:, :, [nir_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = ((1 / mari550) - (1 / mari700)) * nir
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MARI. Try increasing distance.")

def mcari(hsi, distance=20):
    """Modified chlorophyll absorption in reflectance index (Daughtry et al., 2000)
    The theoretical range for MCARI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 700 and (float(hsi.min_wavelength) - distance) <= 550:
        mcari550_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 550)
        mcari670_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        mcari700_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 700)
        mcari550 = (hsi.array_data[:, :, [mcari550_index]])
        mcari670 = (hsi.array_data[:, :, [mcari670_index]])
        mcari700 = (hsi.array_data[:, :, [mcari700_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = ((mcari700 - mcari670) - 0.2 * (mcari700 - mcari550)) * (mcari700 / mcari670)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MCARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MCARI. Try increasing distance.")

def mtci(hsi, distance=20):
    """MERIS terrestrial chlorophyll index (Dash and Curran, 2004)
    The theoretical range for MTCI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 753.75 and (float(hsi.min_wavelength) - distance) <= 681.25:
        mtci68125_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 681.25)
        mtci70875_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 708.75)
        mtci75375_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 753.75)
        mtci68125 = (hsi.array_data[:, :, [mtci68125_index]])
        mtci70875 = (hsi.array_data[:, :, [mtci70875_index]])
        mtci75375 = (hsi.array_data[:, :, [mtci75375_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = (mtci75375 - mtci70875) / (mtci70875 - mtci68125)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="MTCI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating MTCI. Try increasing distance.")

def ndre(hsi, distance=20):
    """Normalized difference red edge (Barnes et al., 2000)
    The theoretical range for NDRE is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 790 and (float(hsi.min_wavelength) - distance) <= 720:
        ndre720_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 720)
        ndre790_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 790)
        ndre790 = (hsi.array_data[:, :, [ndre790_index]])
        ndre720 = (hsi.array_data[:, :, [ndre720_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (ndre790 - ndre720) / (ndre790 + ndre720)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="NDRE")
    else:
        fatal_error("Available wavelengths are not suitable for calculating NDRE. Try increasing distance.")

def psnd_chla(hsi, distance=20):
    """Pigment sensitive normalized difference (Blackburn, 1998) note: chl_a (part 1 of 3)
    The theoretical range for PSND_CHLA is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 675:
        psndchla675_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 675)
        psndchla800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        psndchla675 = (hsi.array_data[:, :, [psndchla675_index]])
        psndchla800 = (hsi.array_data[:, :, [psndchla800_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (psndchla800 - psndchla675) / (psndchla800 + psndchla675)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CHLA")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CHLA. Try increasing distance.")

def psnd_chlb(hsi, distance=20):
    """Pigment sensitive normalized difference (Blackburn, 1998) note: chl_b (part 2 of 3)
    The theoretical range for PSND_CHLB is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 650:
        psndchlb650_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 650)
        psndchlb800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        psndchlb650 = (hsi.array_data[:, :, [psndchlb650_index]])
        psndchlb800 = (hsi.array_data[:, :, [psndchlb800_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (psndchlb800 - psndchlb650) / (psndchlb800 + psndchlb650)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CHLB")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CHLB. Try increasing distance.")

def psnd_car(hsi, distance=20):
    """Pigment sensitive normalized difference (Blackburn, 1998) note: car (part 3 of 3)
    The theoretical range for PSND_CAR is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 500:
        psndcar500_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 500)
        psndcar800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        psndcar500 = (hsi.array_data[:, :, [psndcar500_index]])
        psndcar800 = (hsi.array_data[:, :, [psndcar800_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (psndcar800 - psndcar500) / (psndcar800 + psndcar500)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSND_CAR")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSND_CAR. Try increasing distance.")

def psri(hsi, distance=20):
    """Plant senescence reflectance index (Merzlyak et al., 1999)
    The theoretical range for PSRI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance)>= 750 and (float(hsi.min_wavelength) - distance) <= 500:
        psri500_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 500)
        psri678_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 678)
        psri750_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 750)
        psri500 = (hsi.array_data[:, :, [psri500_index]])
        psri678 = (hsi.array_data[:, :, [psri678_index]])
        psri750 = (hsi.array_data[:, :, [psri750_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = (psri678 - psri500) / psri750
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSRI. Try increasing distance.")

def pssr1(hsi, distance=20):
    """Pigment-specific spectral ration (Blackburn, 1998) note: part 1 of 3
    The theoretical range for PSSR1 is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 675:
        pssr1_800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        pssr1_675_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 675)
        pssr1_800 = (hsi.array_data[:, :, [pssr1_800_index]])
        pssr1_675 = (hsi.array_data[:, :, [pssr1_675_index]])
        # Naturally ranges from 0 to inf
        index_array_raw = pssr1_800 / pssr1_675
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR1")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR1. Try increasing distance.")

def pssr2(hsi, distance=20):
    """Pigment-specific spectral ration (Blackburn, 1998) note: part 2 of 3
    The theoretical range for PSSR2 is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 650:
        pssr2_800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        pssr2_650_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 650)
        pssr2_800 = (hsi.array_data[:, :, [pssr2_800_index]])
        pssr2_650 = (hsi.array_data[:, :, [pssr2_650_index]])
        # Naturally ranges from 0 to inf
        index_array_raw = pssr2_800 / pssr2_650
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR2")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR2. Try increasing distance.")

def pssr3(hsi, distance=20):
    """Pigment-specific spectral ration (Blackburn, 1998) note: part 3 of 3
    The theoretical range for PSSR3 is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 500:
        pssr3_800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        pssr3_500_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 500)
        pssr3_800 = (hsi.array_data[:, :, [pssr3_800_index]])
        pssr3_500 = (hsi.array_data[:, :, [pssr3_500_index]])
        # Naturally ranges from 0 to inf
        index_array_raw = pssr3_800 / pssr3_500
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="PSSR3")
    else:
        fatal_error("Available wavelengths are not suitable for calculating PSSR3. Try increasing distance.")

def rgri(hsi, distance=20):
    """Red/green ratio index (Gamon and Surfus, 1999)
    The theoretical range for RGRI is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 560:
        red_index   = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        red   = (hsi.array_data[:, :, [red_index]])
        green = (hsi.array_data[:, :, [green_index]])
        # Naturally ranges from 0 to inf
        index_array_raw = red / green
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="RGRI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating RGRI. Try increasing distance.")

def rvsi(hsi, distance=20):
    """Red-edge vegetation stress index (Metron and Huntington, 1999)
    The theoretical range for RVSI is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 752 and (float(hsi.min_wavelength) - distance) <= 714:
        rvsi714_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 714)
        rvsi733_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 733)
        rvsi752_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 752)
        rvsi714 = (hsi.array_data[:, :, [rvsi714_index]])
        rvsi733 = (hsi.array_data[:, :, [rvsi733_index]])
        rvsi752 = (hsi.array_data[:, :, [rvsi752_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (rvsi714 + rvsi752) / 2 - rvsi733
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="RVSI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating RVSI. Try increasing distance.")

def sipi(hsi, distance=20):
    """Structure-intensitive pigment index (Penuelas et al., 1995)
    The theoretical range for SIPI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 445:
        sipi445_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 445)
        sipi680_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 680)
        sipi800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        sipi445 = (hsi.array_data[:, :, [sipi445_index]])
        sipi680 = (hsi.array_data[:, :, [sipi680_index]])
        sipi800 = (hsi.array_data[:, :, [sipi800_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = (sipi800 - sipi445) / (sipi800 - sipi680)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SIPI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SIPI. Try increasing distance.")

def sr(hsi, distance=20):
    """Simple ratio (Jordan, 1969)
    The theoretical range for SR is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 800 and (float(hsi.min_wavelength) - distance) <= 675:
        sr675_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 675)
        sr800_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 800)
        sr675 = (hsi.array_data[:, :, [sr675_index]])
        sr800 = (hsi.array_data[:, :, [sr800_index]])
        # Naturally ranges from 0 to inf
        index_array_raw = sr800 / sr675
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="SR")
    else:
        fatal_error("Available wavelengths are not suitable for calculating SR. Try increasing distance.")

def vari(hsi, distance=20):
    """Visible atmospherically resistant index (Gitelson et al., 2002a)
    The theoretical range for VARI is (-Inf, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 670 and (float(hsi.min_wavelength) - distance) <= 470:
        red_index   = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        blue_index  = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 470)
        red   = (hsi.array_data[:, :, [red_index]])
        green = (hsi.array_data[:, :, [green_index]])
        blue  = (hsi.array_data[:, :, [blue_index]])
        # Naturally ranges from -inf to inf
        index_array_raw = (green - red) / (green + red - blue)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="VARI")
    else:
        fatal_error("Available wavelengths are not suitable for calculating VARI. Try increasing distance.")

def vi_green(hsi, distance=20):
    """Vegetation index using green band (Gitelson et al., 2002a)
    The theoretical range for VI_GREEN is [-1.0, 1.0].

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >=  670 and (float(hsi.min_wavelength) - distance) <= 560:
        red_index   = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 670)
        green_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 560)
        red   = (hsi.array_data[:, :, [red_index]])
        green = (hsi.array_data[:, :, [green_index]])
        # Naturally ranges from -1 to 1
        index_array_raw = (green - red) / (green + red)
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="VI_GREEN")
    else:
        fatal_error("Available wavelengths are not suitable for calculating VI_GREEN. Try increasing distance.")

def wbi(hsi, distance=20):
    """Water band index (Peñuelas et al., 1997)
    The theoretical range for WBI is [0.0, Inf).

    inputs:
    hsi      = hyperspectral image (PlantCV Spectral_data instance)
    distance = how lenient to be if the required wavelengths are not available

    Returns:
    index_array    = Index data as a Spectral_data instance
    :param hsi: __main__.Spectral_data
    :param distance: int
    :return index_array: __main__.Spectral_data
    """

    if (float(hsi.max_wavelength) + distance) >= 970 and (float(hsi.min_wavelength) - distance) <= 900:
        wbi900_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 900)
        wbi970_index = _find_closest(np.array([float(i) for i in hsi.wavelength_dict.keys()]), 970)
        wbi900 = (hsi.array_data[:, :, [wbi900_index]])
        wbi970 = (hsi.array_data[:, :, [wbi970_index]])
        # Naturally ranges from 0 to Inf
        index_array_raw = wbi900 / wbi970
        return _package_index(hsi=hsi, raw_index=index_array_raw, method="WBI")
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
    # Reshape array into hyperspectral datacube shape
    raw_index = np.transpose(np.transpose(raw_index)[0])

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

    if params.debug == "plot":
        plot_image(index.pseudo_rgb)
    elif params.debug == "print":
        print_image(index.pseudo_rgb,
                    os.path.join(params.debug_outdir, str(params.device) + method + "_index.png"))

    return index

