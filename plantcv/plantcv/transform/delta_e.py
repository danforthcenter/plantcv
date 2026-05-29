"""Calculate Delta E between color cards"""
import os
import cv2
import numpy as np
from skimage import color
from matplotlib import pyplot as plt
from plantcv.plantcv._globals import params, outputs
from plantcv.plantcv.transform.color_correction import std_color_matrix, astro_color_matrix


def _delta_e(obs_rgb, card_type=None, obs="uncalibrated", method="deltaE_ciede2000"):
    """Calculate summary of Delta E between two color cards

    Parameters
    ----------
    obs_rgb : numpy.ndarray
        Observed RGB color chip values as returned from plantcv.transform.detect_color_card
    card_type : str
        either "macbeth" or "astro" for color card type, defaults to None for compatibility with detection.
    obs : str
        string describing what the obs_rgb data is, typically "uncalibrated" for an image input into color correction
        or "calibrated" for an image that has been through color correction.
    method : str
        function name from skimage.color to calculate delta E. Currently deltaE_(cie76|ciede2000|ciede94|cmc) are
        supported

    Returns
    -------
    delta_e_mat
        numpy.ndarray, Delta E values between color chips.
    """
    if card_type is None or isinstance(card_type, tuple):
        card_type = "macbeth"
    if card_type.upper() == "ASTRO":
        std = astro_color_matrix()
        obs_mat = (255 * np.delete(obs_rgb, 0, axis=1).reshape(3, 5, 3)).astype("uint8")
        exp_mat = (255 * np.delete(std, 0, axis=1).reshape(3, 5, 3)).astype("uint8")
    else:
        std = std_color_matrix()
        # format both rgb colors into 6x4 uint8 image
        obs_mat = (255 * np.delete(obs_rgb, 0, axis=1).reshape(6, 4, 3)).astype("uint8")
        exp_mat = (255 * np.rot90(np.delete(std, 0, axis=1).reshape(4, 6, 3), 3)).astype("uint8")
    # convert to LAB for skimage color functions
    obs_lab = cv2.cvtColor(obs_mat, cv2.COLOR_RGB2LAB)
    exp_lab = cv2.cvtColor(exp_mat, cv2.COLOR_RGB2LAB)
    # get function from skimage color
    delta_e_fun = getattr(color, method)
    # there are other parameters we could allow changes to but I don't think we need to yet.
    delta_e_mat = delta_e_fun(obs_lab, exp_lab)
    # store metadata describing delta E
    outputs.add_metadata(term="mean_deltaE_" + obs, datatype=float, value=np.mean(delta_e_mat))
    outputs.add_metadata(term="std_deltaE_" + obs, datatype=float, value=np.std(delta_e_mat))
    outputs.add_metadata(term="max_deltaE_" + obs, datatype=float, value=np.max(delta_e_mat))
    outputs.add_metadata(term="min_deltaE_" + obs, datatype=float, value=np.min(delta_e_mat))
    # make a debug plot
    if params.debug:
        params.device += 1
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.imshow(obs_mat)
        ax1.set_title(obs.title() + ' Color Card')
        ax2.imshow(exp_mat)
        ax2.set_title('Reference Colors')
        if params.debug == "print":
            fig.savefig(fname=os.path.join(params.debug_outdir, f"{params.device}_{obs}_{method}.png"))
        if params.debug == "plot":
            plt.show()
        plt.close(fig)

    return delta_e_mat
