"""Rerun delta E calculation automatically if deltaE is in outputs and image is corrected"""
import re
from plantcv.plantcv._globals import outputs, params
from plantcv.plantcv.transform.delta_e import _delta_e
from plantcv.plantcv.transform.detect_color_card import detect_color_card


def _rerun_delta_e(corrected_img, fun="affine_color_correction"):
    """Rerun delta E calculation on a corrected image automatically if deltaE is already in outputs

    Parameters
    ----------

    Returns
    -------
    """
    delta_terms = [i for i in outputs.metadata.keys() if re.search("deltaE", i)]

    if delta_terms:
        color_chip_size = params.function_args["detect_color_card"]["color_chip_size"]
        roi = params.function_args["detect_color_card"]["roi"]
        kwargs_obj = params.function_args["detect_color_card"]["kwargs"]
        debug = params.debug
        params.debug = "None"
        obs_rgb = detect_color_card(corrected_img,
                                    color_chip_size=color_chip_size,
                                    roi=roi, deltaE=False, **kwargs_obj)
        params.debug = debug
        _ = _delta_e(obs_rgb, color_chip_size, obs=fun)
