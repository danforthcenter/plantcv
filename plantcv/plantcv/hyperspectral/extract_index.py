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



def extract_index(array, index="NDVI", distance=20):
    """Pull out indices of interest from a hyperspectral datacube.

        Inputs:
        array = hyperspectral data instance
        index = index of interest, "ndvi", "gdvi", "savi", "pri", "aci", "ari", "cai", "cari", "ci_rededge", "cri1", "cri2", "evi",
        "mari", "mcari", "mtci", "ndre", "psnd_chla", "psnd_chlb", "psnd_car", "psri", "pssr1", "pssr2", "pssr3", "rgri", "rvsi", "sipi",
        "sr", "vari", "vi_green", "wbi".
        distance = how lenient to be if the required wavelengths are not available

        Returns:
        index_array    = Index data as a Spectral_data instance

        :param array: __main__.Spectral_data
        :param index: str
        :param distance: int
        :return index_array: __main__.Spectral_data
        """
    params.device += 1

    # Min and max available wavelength will be used to determine if an index can be extracted
    max_wavelength = float(array.max_wavelength)
    min_wavelength = float(array.min_wavelength)

    # Dictionary of wavelength and it's index in the list
    wavelength_dict = array.wavelength_dict.copy()
    array_data = array.array_data.copy()

    if index.upper() == "NDVI":
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 670:
            # Obtain index that best represents NIR and red bands
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            # Naturally ranges from -1 to 1
            index_array_raw = (nir - red) / (nir + red)
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDVI. Try increasing distance.")

    elif index.upper() == "GDVI":
        # Green Difference Vegetation Index [Sripada et al. (2006)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            # Naturally ranges from -2 to 2
            index_array_raw = nir - red
        else:
            fatal_error("Available wavelengths are not suitable for calculating GDVI. Try increasing distance.")

    elif index.upper() == "SAVI":
        # Soil Adjusted Vegetation Index [Huete et al. (1988)]
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 680:
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            nir = (array_data[:, :, [nir_index]])
            red = (array_data[:, :, [red_index]])
            # Naturally ranges from -1.2 to 1.2
            index_array_raw = (1.5 * (nir - red)) / (red + nir + 0.5)
        else:
            fatal_error("Available wavelengths are not suitable for calculating SAVI. Try increasing distance.")

    elif index.upper() == "PRI":
        #  Photochemical Reflectance Index (https://doi.org/10.1111/j.1469-8137.1995.tb03064.x)
        if (max_wavelength + distance) >= 570 and (min_wavelength - distance) <= 531:
            # Obtain index that best approximates 570 and 531 nm bands
            pri570_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 570)
            pri531_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 531)
            pri570 = (array_data[:, :, [pri570_index]])
            pri531 = (array_data[:, :, [pri531_index]])
            # PRI = (R531− R570)/(R531+ R570))
            denominator = pri531 + pri570
            # Avoid dividing by zero
            index_array_raw = np.where(denominator == 0, 0, ((pri531 - pri570) / denominator))
        else:
            fatal_error("Available wavelengths are not suitable for calculating PRI. Try increasing distance.")

    elif index.upper() == "ACI":
        #  Anthocyanim content index (Van den Berg et al. 2005)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 560:
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            nir_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            green = (array_data[:, :, [green_index]])
            nir   = (array_data[:, :, [nir_index]])
            # Naturally ranges from -1.0 to 1.0
            index_array_raw = green/nir
        else:
            fatal_error("Available wavelengths are not suitable for calculating ACI. Try increasing distance.")

    elif index.upper() == "ARI":
        # Anthocyanin reflectance index (Gitelson et al., 2001)
        if (max_wavelength + distance) >= 700 and (min_wavelength - distance) <= 550:
            ari550_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            ari700_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            ari550 = (array_data[:, :, [ari550_index]])
            ari700 = (array_data[:, :, [ari700_index]])
            index_array_raw = (1/ari550)-(1/ari700)
        else:
            fatal_error("Available wavelengths are not suitable for calculating ARI. Try increasing distance.")

    elif index.upper() == 'CAI':
        # Cellulose absorption index (Daughtry, 2001)
        if (max_wavelength + distance) >= 2206 and (min_wavelength - distance) <= 2019:
            cai2019_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 2019)
            cai2109_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 2109)
            cai2206_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 2206)
            cai2019 = (array_data[:, :, [cai2019_index]])
            cai2109 = (array_data[:, :, [cai2109_index]])
            cai2206 = (array_data[:, :, [cai2206_index]])
            index_array_raw = 0.5*(cai2019+cai2206)-cai2109
        else:
            fatal_error("Available wavelengths are not suitable for calculating CAI. Try increasing distance.")

    elif index.upper() == 'CARI':
        # Chlorophyll absorption in reflectance index (Giteson et al., 2003a)
        if (max_wavelength + distance) >= 700 and (min_wavelength - distance) <= 550:
            cari550_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            cari700_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            cari550 = (array_data[:, :, [cari550_index]])
            cari700 = (array_data[:, :, [cari700_index]])
            index_array_raw = (1/cari550)-(1/cari700)
        else:
            fatal_error("Available wavelengths are not suitable for calculating CARI. Try increasing distance.")

    elif index.upper() == 'CI_rededge':
        # Chlorophyll index red edge (Giteson et al., 2003a)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 750:
            rededge_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 750)
            nir_index     = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            rededge = (array_data[:, :, [rededge_index]])
            nir     = (array_data[:, :, [nir_index]])
            index_array_raw = nir/rededge - 1
        else:
            fatal_error("Available wavelengths are not suitable for calculating CI_rededge. Try increasing distance.")

    elif index.upper() == 'CRI1':
        # Carotenoid reflectance index (Gitelson et al., 2002b) (note: part 1 of 2)
        if (max_wavelength + distance) >= 550 and (min_wavelength - distance) <= 510:
            cri1510_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 510)
            cri1550_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            cri1510 = (array_data[:, :, [cri1510_index]])
            cri1550 = (array_data[:, :, [cri1550_index]])
            index_array_raw = 1/cri1510-1/cri1550
        else:
            fatal_error("Available wavelengths are not suitable for calculating CRI1. Try increasing distance.")

    elif index.upper() == 'CRI2':
        # Carotenoid reflectance index (Gitelson et al., 2002b) (note: part 1 of 2)
        if (max_wavelength + distance) >= 700 and (min_wavelength - distance) <= 510:
            cri1510_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 510)
            cri1700_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            cri1510 = (array_data[:, :, [cri1510_index]])
            cri1700 = (array_data[:, :, [cri1700_index]])
            index_array_raw = 1/cri1510-1/cri1700
        else:
            fatal_error("Available wavelengths are not suitable for calculating CRI2. Try increasing distance.")

    elif index.upper() == 'EVI':
        # Enhanced Vegetation index (Huete et al., 1997)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 470:
            blue_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 470)
            red_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            blue = (array_data[:, :, [blue_index]])
            red = (array_data[:, :, [red_index]])
            nir = (array_data[:, :, [nir_index]])
            index_array_raw = 2.5*(nir-red)/(nir+6*red-7.5*blue+1)
        else:
            fatal_error("Available wavelengths are not suitable for calculating EVI. Try increasing distance.")

    elif index.upper() == 'MARI':
        # Modified anthocyanin reflectance index (Gitelson et al., 2001)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 550:
            mari550_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            mari700_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            nir_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            mari550 = (array_data[:, :, [mari550_index]])
            mari700 = (array_data[:, :, [mari700_index]])
            nir = (array_data[:, :, [nir_index]])
            index_array_raw = ((1/mari550)-(1/mari700))*nir
        else:
            fatal_error("Available wavelengths are not suitable for calculating MARI. Try increasing distance.")

    elif index.upper() == 'MCARI':
        # Modified chlorophyll absorption in reflectance index (Daughtry et al., 2000)
        if (max_wavelength + distance) >= 700 and (min_wavelength - distance) <= 550:
            mcari550_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 550)
            mcari670_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            mcari700_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 700)
            mcari550 = (array_data[:, :, [mcari550_index]])
            mcari670 = (array_data[:, :, [mcari670_index]])
            mcari700 = (array_data[:, :, [mcari700_index]])
            index_array_raw = ((mcari700-mcari670)-0.2*(mcari700-mcari550))*(mcari700/mcari670)
        else:
            fatal_error("Available wavelengths are not suitable for calculating MCARI. Try increasing distance.")

    elif index.upper() == 'MTCI':
        # MERIS terrestrial chlorophyll index (Dash and Curran, 2004)
        if (max_wavelength + distance) >= 753.75 and (min_wavelength - distance) <= 681.25:
            mtci68125_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 681.25)
            mtci70875_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 708.75)
            mtci75375_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 753.75)
            mtci68125 = (array_data[:, :, [mtci68125_index]])
            mtci70875 = (array_data[:, :, [mtci70875_index]])
            mtci75375 = (array_data[:, :, [mtci75375_index]])
            index_array_raw = (mtci75375-mtci70875)/(mtci70875-mtci68125)
        else:
            fatal_error("Available wavelengths are not suitable for calculating MTCI. Try increasing distance.")

    elif index.upper() == 'NDRE':
        # Normalized difference red edge (Barnes et al., 2000)
        if (max_wavelength + distance) >= 790 and (min_wavelength - distance) <= 720:
            ndre720_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 720)
            ndre790_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 790)
            ndre790 = (array_data[:, :, [ndre790_index]])
            ndre720 = (array_data[:, :, [ndre720_index]])
            index_array_raw = (ndre790-ndre720)/(ndre790+ndre720)
        else:
            fatal_error("Available wavelengths are not suitable for calculating NDRE. Try increasing distance.")

    elif index.upper() == 'PSND_CHLA':
        # Pigment sensitive normalized difference (Blackburn, 1998) note: chl_a
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 675:
            psndchla675_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 675)
            psndchla800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            psndchla675 = (array_data[:, :, [psndchla675_index]])
            psndchla800 = (array_data[:, :, [psndchla800_index]])
            index_array_raw = (psndchla800-psndchla675)/(psndchla800+psndchla675)
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSND_CHLA. Try increasing distance.")

    elif index.upper() == 'PSND_CHLB':
        # Pigment sensitive normalized difference (Blackburn, 1998) note: chl_b (part 1 of 3)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 650:
            psndchlb650_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 650)
            psndchlb800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            psndchlb650 = (array_data[:, :, [psndchlb650_index]])
            psndchlb800 = (array_data[:, :, [psndchlb800_index]])
            index_array_raw = (psndchlb800-psndchlb650)/(psndchlb800+psndchlb650)
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSND_CHLB. Try increasing distance.")

    elif index.upper() == 'PSND_CAR':
        # Pigment sensitive normalized difference (Blackburn, 1998) note: chl_b (part 1 of 3)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 500:
            psndcar500_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 500)
            psndcar800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            psndcar500 = (array_data[:, :, [psndcar500_index]])
            psndcar800 = (array_data[:, :, [psndcar800_index]])
            index_array_raw = (psndcar800-psndcar500)/(psndcar800+psndcar500)
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSND_CAR. Try increasing distance.")

    elif index.upper() == 'PSRI':
        # Plant senescence reflectance index (Merzlyak et al., 1999) note: car (part 1 of 3)
        if (max_wavelength + distance) >= 750 and (min_wavelength - distance) <= 500:
            psri500_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 500)
            psri678_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 678)
            psri750_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 750)
            psri500 = (array_data[:, :, [psri500_index]])
            psri678 = (array_data[:, :, [psri678_index]])
            psri750 = (array_data[:, :, [psri750_index]])
            index_array_raw = (psri678-psri500)/psri750
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSRI. Try increasing distance.")

    elif index.upper() == 'PSSR1':
        # Pigment-specific spectral ration (Blackburn, 1998) note: part 1 of 3
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 675:
            pssr1_800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            pssr1_675_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 675)
            pssr1_800 = (array_data[:, :, [pssr1_800_index]])
            pssr1_675 = (array_data[:, :, [pssr1_675_index]])
            index_array_raw = pssr1_800/pssr1_675
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSSR1. Try increasing distance.")

    elif index.upper() == 'PSSR2':
        # Pigment-specific spectral ration (Blackburn, 1998) note: part 2 of 3
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 650:
            pssr2_800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            pssr2_650_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 650)
            pssr2_800 = (array_data[:, :, [pssr2_800_index]])
            pssr2_650 = (array_data[:, :, [pssr2_650_index]])
            index_array_raw = pssr2_800/pssr2_650
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSSR2. Try increasing distance.")

    elif index.upper() == 'PSSR3':
        # Pigment-specific spectral ration (Blackburn, 1998) note: part 3 of 3
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 500:
            pssr3_800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            pssr3_500_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 500)
            pssr3_800 = (array_data[:, :, [pssr3_800_index]])
            pssr3_500 = (array_data[:, :, [pssr3_500_index]])
            index_array_raw = pssr3_800/pssr3_500
        else:
            fatal_error("Available wavelengths are not suitable for calculating PSSR3. Try increasing distance.")

    elif index.upper() == 'RGRI':
        # Red/green ratio index (Gamon and Surfus, 1999)
        if (max_wavelength + distance) >= 670 and (min_wavelength - distance) <= 560:
            red_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            red   = (array_data[:, :, [red_index]])
            green = (array_data[:, :, [green_index]])
            index_array_raw = red / green
        else:
            fatal_error("Available wavelengths are not suitable for calculating RGRI. Try increasing distance.")

    elif index.upper() == 'RVSI':
        # Red-edge vegetation stress index (Metron and Huntington, 1999)
        if (max_wavelength + distance) >= 752 and (min_wavelength - distance) <= 714:
            rvsi714_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 714)
            rvsi733_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 733)
            rvsi752_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 752)
            rvsi714 = (array_data[:, :, [rvsi714_index]])
            rvsi733 = (array_data[:, :, [rvsi733_index]])
            rvsi752 = (array_data[:, :, [rvsi752_index]])
            index_array_raw = (rvsi714+rvsi752)/2 - rvsi733
        else:
            fatal_error("Available wavelengths are not suitable for calculating RVSI. Try increasing distance.")

    elif index.upper() == 'SIPI':
        # Structure-intensitive pigment index (Penuelas et al., 1995)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 445:
            sipi445_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 445)
            sipi680_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 680)
            sipi800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            sipi445 = (array_data[:, :, [sipi445_index]])
            sipi680 = (array_data[:, :, [sipi680_index]])
            sipi800 = (array_data[:, :, [sipi800_index]])
            index_array_raw = (sipi800-sipi445)/(sipi800-sipi680)
        else:
            fatal_error("Available wavelengths are not suitable for calculating SIPI. Try increasing distance.")

    elif index.upper() == 'SR':
        # Simple ratio (Jordan, 1969)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 675:
            sr675_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 675)
            sr800_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 800)
            sr675 = (array_data[:, :, [sr675_index]])
            sr800 = (array_data[:, :, [sr800_index]])
            index_array_raw = sr800/sr675
        else:
            fatal_error("Available wavelengths are not suitable for calculating SR. Try increasing distance.")

    elif index.upper() == 'VARI':
        # Visible atmospherically resistant index (Gitelson et al., 2002a)
        if (max_wavelength + distance) >= 670 and (min_wavelength - distance) <= 470:
            red_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            blue_index  = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 470)
            red    = (array_data[:, :, [red_index]])
            green  = (array_data[:, :, [green_index]])
            blue   = (array_data[:, :, [blue_index]])
            index_array_raw = (green-red)/(green+red-blue)
        else:
            fatal_error("Available wavelengths are not suitable for calculating VARI. Try increasing distance.")

    elif index.upper() == 'VI_green':
        # Vegetation index using green band (Gitelson et al., 2002a)
        if (max_wavelength + distance) >= 670 and (min_wavelength - distance) <= 560:
            red_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            red    = (array_data[:, :, [red_index]])
            green  = (array_data[:, :, [green_index]])
            index_array_raw = (green-red)/(green+red)
        else:
            fatal_error("Available wavelengths are not suitable for calculating VI_green. Try increasing distance.")

    elif index.upper() == 'WBI':
        # Water band index (Peñuelas et al., 1997)
        if (max_wavelength + distance) >= 800 and (min_wavelength - distance) <= 675:
            red_index   = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 670)
            green_index = _find_closest(np.array([float(i) for i in wavelength_dict.keys()]), 560)
            red    = (array_data[:, :, [red_index]])
            green  = (array_data[:, :, [green_index]])
            index_array_raw = (green-red)/(green+red)
        else:
            fatal_error("Available wavelengths are not suitable for calculating VI_green. Try increasing distance.")

    else:
        fatal_error(index + " is not one of the currently available indices for this function. Please open an issue " +
                    "on the PlantCV GitHub account so we can add more handy indicies!")

    # Reshape array into hyperspectral datacube shape
    index_array_raw = np.transpose(np.transpose(index_array_raw)[0])

    # Store debug mode
    debug = params.debug
    params.debug = None

    # Resulting array is float 32 from varying natural ranges, transform into uint8 for plotting
    all_positive = np.add(index_array_raw, 2 * np.ones(np.shape(index_array_raw)))
    scaled = rescale(all_positive)

    # Find array min and max values
    obs_max_pixel = float(np.nanmax(index_array_raw))
    obs_min_pixel = float(np.nanmin(index_array_raw))

    index_array = Spectral_data(array_data=index_array_raw, max_wavelength=0,
                                min_wavelength=0, max_value=obs_max_pixel, min_value=obs_min_pixel, d_type=np.uint8,
                                wavelength_dict={}, samples=array.samples,
                                lines=array.lines, interleave=array.interleave,
                                wavelength_units=array.wavelength_units, array_type="index_" + index.lower(),
                                pseudo_rgb=scaled, filename=array.filename, default_bands=None)

    # Restore debug mode
    params.debug = debug

    if params.debug == "plot":
        plot_image(index_array.pseudo_rgb)
    elif params.debug == "print":
        print_image(index_array.pseudo_rgb,
                    os.path.join(params.debug_outdir, str(params.device) + index + "_index.png"))

    return index_array
