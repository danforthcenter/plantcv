# Functions used to evaulate time-series linking result
"""
Notations and Definitions:
T: total time
N: total number of (unique) leaves in ground truth
N_: total number of (unique) leaves in tracking result
li (link info): a list of length (T-1)
    every element of li, i.e. li[t] represents how n_t link to n_{t+1}
    length of li[t]: n_t
    li[t][i]=j: the i-th segment at time t is the j-th segment at time t+1
li_gt (link info in ground truth): same definition as li, represents the same information in ground truth
ti (tracking info): a matrix (2d-array) of size (T,N)
    tk-th element of ti: ti[t,k]: local index of leaf k at time t if k leaf k appears at time t, -1 others.
    Total number of non-negative elements in a row t: # of leaves at time t
    Every column k: local indices for leaf k at different timepoints(ts).
ti_gt (tracking info in ground truth): same definition as ti, represents the same information in ground truth
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
import copy
from plantcv.plantcv import fatal_error


def evaluate_link(li, li_gt):
    """
    Evaluate the link_info by comparing the result to the ground truth
    :param li: link info
    :param li_gt: link info in ground truth
    :return:
    score: final score for linking, defined as total # of correct matches / total # of matches
    num_insts: number of instances at every time point except the last one
    num_matched: number of matched instances at every time point except the last one
    """
    if not len(li) == len(li_gt):
        fatal_error('Linking information not same length!!')
    else:
        max_t = len(li_gt)
        if not sum([len(x)==len(y) for (x,y) in zip(li_gt, li)]) == max_t:
            fatal_error('Different number of instances!!')
    num_insts   = [len(x) for x in li_gt]
    # num_matched = [(sum(x == y)) for (x,y) in zip(li_gt, li)]
    num_matched = [(sum(x == y)) for (x, y) in zip(li_gt, li)]
    score = sum(num_matched)/sum(num_insts)
    return score, num_insts, num_matched


def mismatch_rate(ti, ti_gt):
    """
    Calculate rates related to two types of mis-match: unmatched and fake-new
    :param ti: tracking info
    :param ti_gt: tracking info in ground truth
    :return:
    r_unmatched: 0 if N_ >= N
    r_fake_new: 0 if N_ <= N
    """
    r_unmatched, r_fake_new = 0, 0
    N, N_ = ti_gt.shape[1], ti.shape[1]
    if N_ < N:
        r_unmatched = (N-N_)/N
    elif N_ > N:
        r_fake_new = (N_-N)/N
    return r_unmatched, r_fake_new


def confusion(ti, ti_gt):
    """
    Generate a confusion matrix based on tracking info and ground truth of tracking info
    :param ti: tracking info
    :param ti_gt: tracking info in ground truth
    :return:
    confu: confusion matrix of size (N,N_)
    match: (list of length N) "diagonal" elements of confu. (If N_<N, there will be N-N_ 0s in match; if N_>N, there will still be N elements in "match")
    rate: (list of length N) match/existence_times
    score: averate rate of all leaves
    """
    N, N_ = ti_gt.shape[1], ti.shape[1]
    # existance times for every leaf (unique id in ground truth)
    life_gt = [len(np.where(ti_gt[:, i] > -1)[0]) for i in range(N)]
    life = [len(np.where(ti[:, i] > -1)[0]) for i in range(N_)]
    confu = np.zeros((N, N_), dtype=np.int64)
    for t, (ti_t, ti_gt_t) in enumerate(zip(ti, ti_gt)):
        temp = np.zeros((N, N_), dtype=np.int64)
        for (uid_gt, cid_gt) in enumerate(ti_gt_t):
            if cid_gt > -1:
                uid_t = np.where(ti_t == cid_gt)[0][0]
                temp[uid_gt, uid_t] = 1
        confu = confu + temp

    # if N_<N, append (N-N_) columns with all zeros
    confu_ = copy.deepcopy(confu)
    if N_ < N:
        delta_N = N - N_
        new_col = np.zeros((N, delta_N), dtype=int)
        confu_ = np.append(confu_, new_col, 1)
        life = life + [0 for n in range(delta_N)]

    # delta matrix of lift and life_gt
    # delta_life = -np.ones((N,max(N_,N)),dtype=int)
    # for i in range(0,N):
    #     delta_life[i,:] = abs(np.int64(life_gt[i])-life)

    # linear assignment based on delta_life: find most probable corresponding based on life
    # row_i, col_i = linear_sum_assignment(delta_life)

    # linear assignment based on confusion matrix: find those with largest values in confusion matrix
    row_i, col_i = linear_sum_assignment(confu_, maximize=True)

    match = [confu_[i, j] for (i, j) in zip(row_i, col_i)]  # "diagonal"
    rate = [match_t / time_i for (match_t, time_i) in zip(match, life_gt)]

    # # always make the same length of num_gt
    # if N_ < N:
    #     for i in range(N_-N):
    #         match.append(0)
    #         rate.append(0)
    score = sum(rate) / N

    return N, N_, confu, match, rate, score


def get_scores(li, ti, li_gt, ti_gt):
    """
    get scores from different evaluation methods given li, ti, li_gt, ti_gt
    :param li:
    :param ti:
    :param li_gt:
    :param ti_gt:
    :return:
    scores: a dictionary with keys: num_insts, link_score, link_matched, unmatched, fake_new, N, N_, track, track_match, track_rate, track_score
    """
    score_link, num_insts, num_matched = evaluate_link(li, li_gt)
    r_unmatched, r_fake_new = mismatch_rate(ti, ti_gt)
    N, N_, confu, track_match, track_rate, track_score = confusion(ti, ti_gt)

    scores = dict()
    scores["num_insts"] = num_insts
    scores["link_score"] = score_link
    scores["link_matched"] = num_matched
    scores["unmatched"] = r_unmatched
    scores["fake_new"] = r_fake_new
    scores['N'] = N
    scores['N_'] = N_
    scores["track"] = confu
    scores["track_match"] = track_match
    scores["track_rate"] = track_rate
    scores["track_score"] = track_score
    return scores
