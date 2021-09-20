# Generate a plm multivariate space for downstream use in homology group assignments

import numpy as np
from plantcv.plantcv import params


def space(cur_plms, include_bound_dist=False, include_centroid_dist=False, include_orient_angles=False):
    """
    Generate a plm multivariate space for downstream use in homology group assignments

    Inputs:
    cur_plms    = A pandas array of acute plms representing capturing two adjacent frames in a time series
                  or otherwise analogous dataset in order to enable homology assignments
    include_bound_dist = Add bounding box distances to space for Starscape clustering
    include_centroid_dist = Add centroid distances to space for Starscape clustering
    include_orient_angles = Add plm and centroid orientation angles to space for Starscape clustering

    :param cur_plms: pandas.core.frame.DataFrame
    :param include_bound_dist: bool
    :param include_centroid_dist: bool
    :param include_orient_angles: bool
    :return new_plms: pandas.core.frame.DataFrame
    """
    new_plms = cur_plms.copy(deep=True)
    bot_left = [int(min(new_plms.loc[:, ['plm_x']].values)), int(max(new_plms.loc[:, ['plm_y']].values))]
    bot_right = [int(max(new_plms.loc[:, ['plm_x']].values)), int(max(new_plms.loc[:, ['plm_y']].values))]
    top_left = [int(min(new_plms.loc[:, ['plm_x']].values)), int(min(new_plms.loc[:, ['plm_y']].values))]
    top_right = [int(max(new_plms.loc[:, ['plm_x']].values)), int(min(new_plms.loc[:, ['plm_y']].values))]
    centroid = [int(np.mean(new_plms.loc[:, ['plm_x']].values)), int(np.mean(new_plms.loc[:, ['plm_y']].values))]

    bot_left_dist = np.sqrt(np.square(new_plms.loc[:, ['plm_x']].values - bot_left[0]) + np.square(
        new_plms.loc[:, ['plm_y']].values - bot_left[1]))
    bot_right_dist = np.sqrt(np.square(new_plms.loc[:, ['plm_x']].values - bot_right[0]) + np.square(
        new_plms.loc[:, ['plm_y']].values - bot_right[1]))
    top_left_dist = np.sqrt(np.square(new_plms.loc[:, ['plm_x']].values - top_left[0]) + np.square(
        new_plms.loc[:, ['plm_y']].values - top_left[1]))
    top_right_dist = np.sqrt(np.square(new_plms.loc[:, ['plm_x']].values - top_right[0]) + np.square(
        new_plms.loc[:, ['plm_y']].values - top_right[1]))

    if include_bound_dist is True:
        new_plms.insert(len(new_plms.columns), 'bot_left_dist', bot_left_dist, True)
        new_plms.insert(len(new_plms.columns), 'bot_right_dist', bot_right_dist, True)
        new_plms.insert(len(new_plms.columns), 'top_left_dist', top_left_dist, True)
        new_plms.insert(len(new_plms.columns), 'top_right_dist', top_right_dist, True)

    centroid_dist = np.sqrt(np.square(new_plms.loc[:, ['plm_x']].values - centroid[0]) + np.square(
        new_plms.loc[:, ['plm_y']].values - centroid[1]))

    if include_centroid_dist is True:
        new_plms.insert(len(new_plms.columns), 'centroid_dist', centroid_dist, True)

    run = (
                  (new_plms.loc[:, ['SS_x']].values + new_plms.loc[:, ['TS_x']].values) / 2
          ) - new_plms.loc[:, ['plm_x']].values
    rise = (
                   (new_plms.loc[:, ['SS_y']].values + new_plms.loc[:, ['TS_y']].values) / 2
           ) - new_plms.loc[:, ['plm_y']].values
    # print('delta_y=',rise,'   delta_x=',run)
    # slope=rise/run

    centroid_run = (new_plms.loc[:, ['plm_x']].values - centroid[0])
    centroid_rise = (new_plms.loc[:, ['plm_y']].values - centroid[1])
    # print('cent_delta_y=',centroid_rise,'   cent_delta_x=',centroid_run)
    # centroid_slope=centroid_rise/centroid_run

    orientation = []
    centroid_orientation = []

    for m in range(0, len(run)):
        # Use the sign of the run to determine if the weight should shift
        # in the 0-180 or 180-360 range for 360 arc conversion
        a = 0
        if run[m] > 0:
            a = 90 - (np.arctan(rise[m] / run[m]) * (180 / np.pi))
        elif run[m] < 0:
            a = -(90 - (np.arctan(rise[m] / run[m]) * (180 / np.pi)))
        orientation.append(float(a))

        # Use the sign of the run to determine if the weight should
        # shift in the 0-180 or 180-360 range for 360 arc conversion
        centroid_a = 0
        if centroid_run[m] > 0:
            centroid_a = 90 - (np.arctan(centroid_rise[m] / centroid_run[m]) * (180 / np.pi))
        elif centroid_run[m] < 0:
            centroid_a = -(90 - (np.arctan(centroid_rise[m] / centroid_run[m]) * (180 / np.pi)))
        centroid_orientation.append(float(centroid_a))

    if include_orient_angles is True:
        new_plms.insert(len(new_plms.columns), 'orientation', orientation, True)
        new_plms.insert(len(new_plms.columns), 'centroid_orientation', centroid_orientation, True)

    if params.debug is not None:
        print(new_plms.head())

    return new_plms
