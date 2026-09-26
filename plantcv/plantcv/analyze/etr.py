"""Analyze electron transport rate"""

import re
from plantcv.plantcv._globals import outputs
from plantcv.plantcv.fatal_error import fatal_error


def etr(actinic_light, psi_psii_ratio=0.5):
    """Calculate electron transport rate from yii and alphaL outputs and add to outputs.

    Parameters
    ----------
    actinic_light = int or float,
        Light intensity in PAR
    psi_psii_ratio = float,
        PSI/PSII ratio. This should generally be left as 0.5

    Returns
    -------
    None, etr values are added to outputs
    """
    obs = outputs.observations
    for label, _ in obs.items():
        labs = [label2 for label2, _ in obs[label].items() if re.search("yii_mean.*[fqfm|t1]$", label2)]
        labs2 = [label2 for label2, _ in obs[label].items() if re.search("yii_median.*[fqfm|t1]$", label2)]
        aph_labs = [label3 for label3, _ in obs[label].items() if re.search("alphaL", label3)]
        if len(labs) < 1:
            fatal_error("YII mean data must be present in outputs," +
                        "run plantcv.plantcv.analyze.yii before plantcv.plantcv.analyze.etr.")
        yii_mean_val = obs[label][labs[0]]["value"]
        yii_median_val = obs[label][labs2[0]]["value"]
        if not bool(aph_labs):
            fatal_error("AlphaL mean data must be present in outputs," +
                        "run plantcv.plantcv.analyze.alphaL before plantcv.plantcv.analyze.etr.")
        alphaL_mean_val = obs[label]["alphaL_mean"]["value"]
        alphaL_median_val = obs[label]["alphaL_median"]["value"]
        # calculate ETR
        etr_mean_val = yii_mean_val * alphaL_mean_val * psi_psii_ratio * actinic_light
        etr_median_val = yii_median_val * alphaL_median_val * psi_psii_ratio * actinic_light
        # store outputs
        outputs.add_observation(sample=label,
                                variable='mean_etr', trait='mean electron transport rate',
                                method='plantcv.plantcv.analyze.etr',
                                scale='none', datatype=float,
                                value=etr_mean_val, label='none')
        outputs.add_observation(sample=label,
                                variable='median_etr', trait='median electron transport rate',
                                method='plantcv.plantcv.analyze.etr',
                                scale='none', datatype=float,
                                value=etr_median_val, label='none')
