# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:53:34 2020

Functions used in time series linking after getting leaf instances segmented

@author: hudanyunsheng
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import random
import math
import skimage.io
import pickle as pkl
import re
from skimage.measure import find_contours
from matplotlib import patches, lines
from matplotlib.patches import Polygon
from plantcv import plantcv as pcv
import datetime
import copy
import colorsys
from plantcv.plantcv import fatal_error
from scipy.optimize import linear_sum_assignment
import csv
# from scipy.stats import wasserstein_distance
# sys.path.append('/shares/mgehan_share/hsheng/projects/test_plantcv/visualize_display_instances')
# import visualize_display_instances

def _compute_overlaps_masks(masks1, masks2):
    """Compute overlaps of two sets of binary masks.
     The overlaps are represented by IoU (intersection over union) and IoS (intersection over self-area).

    :param masks1: (numpy.ndarray of shape: [Height, Width, n1]) , where n1 is the number of instances
    :param masks2: (numpy.ndarray of shape: [Height, Width, n2]) , where n2 is the number of instances
    :return:
    n1: the number of instances in 1st set of binary masks
    n2: the number of instances in 2nd set of binary masks
    ious: (numpy.ndarray of shape: [n1, n2]) inversection over union between any pairs of instances in masks1 and masks2
    ioss: (numpy.ndarray of shape: [n1, n2]) inversection over self-area (areas of instances in 1st set of masks) between any pairs of instances in masks1 and masks2
    unions: (numpy.ndarray of shape: [n1, n2]) unions between any pairs of instances in masks1 and masks2
    """

    # If either set of masks is empty return empty result
    if masks1.shape[-1] == 0 or masks2.shape[-1] == 0:
        return np.zeros((masks1.shape[-1], masks2.shape[-1]))
    # If either set of masks contains only one mask, expand the 2nd dimension
    if len(masks1.shape) == 2:
        masks1 = np.expand_dims(masks1, 2)
    if len(masks2.shape) == 2:
        masks2 = np.expand_dims(masks2, 2)
    n1 = masks1.shape[2]
    n2 = masks2.shape[2]
    intersections = np.zeros((n1, n2))
    unions = np.zeros((n1, n2))
    ioss = np.zeros((n1, n2))
    for idx_m in range(0, n1):
        maski = np.expand_dims(masks1[:, :, idx_m], axis=2)
        masks_ = np.reshape(masks2 > .5, (-1, masks2.shape[-1])).astype(np.float32)
        maski_ = np.reshape(maski > .5, (-1, maski.shape[-1])).astype(np.float32)
        intersection = np.dot(masks_.T, maski_).squeeze()
        intersections[idx_m, :] = intersection
        union = np.sum(masks_, 0) + np.sum(maski_) - intersection
        unions[idx_m, :] = union
        ioss[idx_m, :] = intersection / maski_.sum()
    ious = np.divide(intersections, unions)
    return n1, n2, ious, ioss, unions


def _get_link(masks1, masks2, logic, thres):
    """
    Get link information between two sets of binary instance segmentation masks
    :param masks1: (numpy.ndarray of shape: [Height, Width, n1]), where n1 is the number of instances
    :param masks2: (numpy.ndarray of shape: [Height, Width, n1]), where n1 is the number of instances
    :param logic: linking logic to use. (currently) either "IOU" or "IOS"
    :param thres: threshold to link two masks (two binary segmentation masks can only be linked if the calculated overlap between is greater than the threshold)
    :return:
    weight (numpy.ndarray of shape: [n1,n2]): weight matrix (indicated by IoU or IoS) calculated based on two sets of masks
    link (numpy.1darray of length n1): link[i] = j means that the i-th mask in masks1 should be linked to j-th mask in masks2
    row_ind, col_ind: selected row indices and column indices based on the weight matrix to finalize the "link"
    """

    n1, n2, ious, ioss, _ = _compute_overlaps_masks(masks1, masks2)
    if logic.upper() == 'IOU':
        weight = ious
    elif logic.upper() == 'IOS':
        weight = ioss
    else:
        fatal_error("Currently only IOU and IOS as supported linking logic!")
    weight_ = copy.deepcopy(weight)
    link = -np.ones(n1, dtype=np.int64)

    idx_col = np.where(np.max(weight_, axis=0) < thres)[
        0]  # find those columns with maximum value < threshold (self.thres)
    avail_col = [x for x in range(0, n2) if x not in idx_col]

    weight_ = np.delete(weight_, idx_col, 1)

    row_ind, col_ind = linear_sum_assignment(weight_, maximize=True)
    for (r, c) in zip(row_ind, col_ind):
        if weight_[r, c] >= thres:
            link[r] = avail_col[c]
    return weight, link, row_ind, col_ind


def _get_emergence(uids):
    """
    get emergence as well as emerge times
    :param uids: unique ids at every time point
        (list of length T, where T is the total time)
        every sub-list uids[t] (for t in range of (0,T)) is also a list of length nt, where nt is the number of instances at t
    :return:
    emergence: new segments (leaves) compared to previous time-point
        (list of length T, where T is the total time)
        every sub-list emergence[t] if also a list. If there is no new segments at t compared to (t-1), the emergence[t] is empty; otherwise, emergence[t] is a list of unique ids appear at t but not at (t-1).
    emerge_times: (list) time points with emergence
    """

    emergence = [[] for i in uids]
    emergence[0] = list(uids[0])
    #     uid_lst      = []
    #     uid_lst += list(uids[0])
    for (t, temp) in enumerate(uids):
        if t >= 1:
            #             new = [x for x in temp if x not in uid_lst]
            new = [x for x in temp if x not in uids[t - 1]]
            emergence[t] = new
    #             uid_lst += new
    emerge_times = [i for i in range(len(emergence)) if len(emergence[i]) > 0]
    return emergence, emerge_times


def _get_ti(num_insts, uids, link_info):
    """
    getting ti (tracking information)
    :param num_insts: (list) number of instances at every time-point t
    :param uids: unique ids at every time point
    :param link_info:
    :return:
    ti: tracking information (np.ndarray of shape (T,max_uid))
        ti[t,k]=j represents for: at time t the k-th leaf has a local index of j
        if ti[t,k]=-1, the k-th leaf does not appear at time t
        number of non-negative elements every row: number of instances
    t_appear: (list, length: N) the appear time of every unique id
    t_disappear: (list, length: N) the disappear time of every unique id
    """

    emergence, emerge_times = _get_emergence(uids)
    T = len(num_insts)
    max_uid = max([max(temp) for temp in uids])
    N = max_uid + 1
    ti = -np.ones((T, N), dtype=np.int64)
    for t in range(T):
        if t == 0:
            ti[t, 0:num_insts[t]] = uids[0]
        else:
            link = link_info[t - 1]
            prev = ti[t - 1]
            cids = list(np.arange(0, num_insts[t]))

            for (uid, pid) in enumerate(prev):
                # pid: previous local id
                if pid >= 0:
                    cid = link[pid]
                    ti[t, uid] = cid
                    if cid >= 0:
                        cids.remove(cid)

            if t in emerge_times:
                new_ids = emergence[t]
                for (cid, new_id) in zip(cids, new_ids):
                    ti[t, new_id] = cid

    t_appear = np.zeros(N, dtype=np.int64)
    t_disappear = -np.ones(N, dtype=np.int64)
    for (t, uids_t) in enumerate(emergence):
        if uids_t:
            for uid in uids_t:
                t_appear[uid] = t
    for uid in range(0, N):
        t = 0
        while t < T:
            if (ti[t][uid] == -1) and (t > t_appear[uid]):
                t_disappear[uid] = t
                break
            else:
                t += 1
    return ti, t_appear, t_disappear


# def _visualize1(img, mask, savename=None):
#     """
#     Apply mask to original image
#     """
#     mask_1 = np.zeros(img.shape[0:2], dtype=np.uint8)
#     mask_1[np.where(mask)] = 255
#     masked_im = pcv.apply_mask(img, mask_1, mask_color='black')
#     if savename is not None:
#         pcv.print_image(masked_im, savename)
#     return masked_im

# def _visualize2(img, fig_title, mask=None, savename=None):
#     """
#     Apply mask with an alpha channel to the original image
#     Can be replaced with "overlay two images in the future"
#     img
#     mask
#     """
#     mask_2 = np.ones(img.shape[0:2]) * 0.5
#     if mask is not None:
#         mask_2[np.where(mask == True)] = 1
#     masked_im = np.concatenate((img.astype(float) / 255, np.expand_dims(mask_2, axis=2)), axis=2)
#
#     fig = plt.figure(figsize=(5, 5))
#     ax = fig.add_subplot(1, 1, 1)
#     ax.imshow(masked_im)
#     ax.axis('off')
#     ax.set_title(fig_title, fontsize=16)
#     if savename is not None:
#         plt.savefig(savename)
#     return masked_im

# def _visualize3(img, masks, colors, figsize=(16, 16), ax=None, captions=None, savename=None, title="", show_bbox=True):
#     visualize_display_instances.display_instances(img, masks.astype(np.uint8), figsize=figsize, title=title, ax=ax, colors=colors, captions=captions, show_bbox=True)
#     if savename is not None:
#         plt.savefig(savename)

class InstanceTimeSeriesLinking(object):
    """A class that links segmented instances throughout time
    Assumption: the timepoints are all sorted, the images and masks are also sorted by timepoints (chronologically)
    """

    def __init__(self):
        # a list of images which are ndarrays
        self.images = None
        # a list of masks which are ndarrays (of the same length of images)
        self.masks = None
        # a list of timepoints (of the same length of images)
        self.timepoints = None
        self.T = None
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = None

        # initialization for linking
        self.thres = None
        self.link_info = None
        self.uids = None
        self.max_uid = None
        self.emergence = None
        self.emerge_times = None
        self.ti = None
        self.t_appear = None
        self.t_disappear = None
        self.weights = None
        self.logic = None
        self.name_sub = None
        self.key_id = None

        # update releated
        self.updated = 0
        self.delta_t = None
        self.disp_uids = None
        self.ids_update = None

        self.ti_ = None
        self.t_appear_ = None
        self.t_disappear_ = None

    def save_linked_series(self, savedir, savename):
        """save linking information into a .pkl file with the same prefix of filename
        Inputs: savedir and savename
        """

        # pkl.dump(self, open(os.path.join(savedir, savename + '.pkl'), 'wb'))
        pkl.dump(vars(self), open(os.path.join(savedir, savename + ".pkl"), 'wb'))

    def import_linked_series(self, savedir, savename):
        """import a linked time-series from previously saved file

        :param savedir: saving directory
        :param savename: saving name
        :return:
        """
        linked = pkl.load(open(os.path.join(savedir, savename + '.pkl'), "rb"))
        for key, value in linked.items():
            setattr(self, key, value)

    # def save_to_csv(self, savedir, csvname1="link_series.csv", csvname2="link_series"):
    #     """ save linking information into 2 .csv files
    #     1. link_series.csv
    #     2. link_info.csv
    #     """
    #     # csvname1 = "link_series.csv"
    #     # csvname2 = "link_info.csv"
    #     l0 = ['', ''] + [x for (idx, x) in enumerate(self.timepoints)]
    #     l1 = ['unique_id', 'current_id'] + ['t{}'.format(idx) for (idx, x) in enumerate(self.timepoints)]
    #     csvfile1 = open(os.path.join(savedir, csvname1), 'w', newline='')
    #     writer1 = csv.writer(csvfile1, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #     writer1.writerow(l0)
    #     writer1.writerow(l1)
    #     csvfile2 = open(os.path.join(savedir, csvname2), 'w', newline='')
    #     writer_junk2 = csv.writer(csvfile2, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #     writer_junk2.writerow(['unique_id', 'emerging_time', 'file_name_emerge', 'current_time', 'file_name', 'current_id'])
    #     for (t0_, item) in self.link_series.items():
    #         t0 = int(t0_.replace('t', ''))
    #         for uid, cid in zip(item['uids'], item['ids']):
    #             link_t0_i  = item['inst{}'.format(cid)]
    #             new_line = ['{}'.format(uid), '{}'.format(cid)] + link_t0_i.tolist()
    #             writer1.writerow(new_line)
    #             for t in range(t0, self.T):
    #                 writer_junk2.writerow([uid, t0, self.timepoints[t0], t, self.timepoints[t], link_t0_i[t]])
    #     csvfile1.close()
    #     csvfile2.close()

    def linking(self, t0):
        """
        Link instance segments of t0 to those of t1 (t0+1) by calculating the overlaps of their masks
        :param t0: starting time point
        :return: None, but self.link_info would be updated
        """
        masks0, masks1 = copy.deepcopy(self.masks[t0]), copy.deepcopy(
            self.masks[t0 + 1])  # both masks0 and masks1 are ndarrays
        weight, self.link_info[t0], _, _ = _get_link(masks0, masks1, self.logic, self.thres)
        self.weights.append(weight)

    def get_uid(self):
        """
        get unique ids for every timepoint based on link_info
        uids: a list
            arrays inside the list
            every array has a length of num_insts for that corresponding time
        """
        self.uids = [-np.ones(n, dtype=np.int64) for n in self.n_insts]
        self.uids[0] = np.arange(len(self.link_info[0]), dtype=np.int64)
        self.max_uid = max(self.uids[0])
        for (t, link_t) in enumerate(self.link_info):
            for (cidt, cidt_) in enumerate(link_t):
                if cidt_ >= 0:
                    self.uids[t + 1][cidt_] = self.uids[t][cidt]
            if -1 in self.uids[t + 1]:  # -1 means there is not predecessor from a former timepoint -> assign new uids
                temp = np.where(self.uids[t + 1] == -1)[0]
                for tid in temp:
                    self.max_uid += 1
                    self.uids[t + 1][tid] = self.max_uid

    def update_ti(self, delta_t=2):
        self.delta_t = delta_t if delta_t else self.delta_t

        """ make copies for tc, t_appear, t_disappear """

        ti_ = copy.deepcopy(self.ti)
        t_appear_ = copy.deepcopy(self.t_appear)
        t_disappear_ = copy.deepcopy(self.t_disappear)

        # find disappeared uids
        disp_uids = np.where((t_disappear_ > -1) & (t_disappear_ < (self.T - 2)))[0]

        if len(disp_uids) == 0:
            print("\nno updates!")
        else:
            # use an array to record how to update tc
            ids_update = -np.ones(len(disp_uids), dtype=np.int64)
            for (uid_i, uid) in enumerate(disp_uids):
                if not (self.ti[:, uid] == -1).all():
                    disp_time = t_disappear_[uid]
                    t0 = disp_time - 1  # time last appear
                    t_ = t0 + 2  # start with t_ = t0+2

                    while (t_ <= t0 + self.delta_t) and (t_ <= self.T - 1):
                        uids_t = np.where(t_appear_ == t_)[0]  # find if there is new emergence at t_ (t0+delta)
                        if len(uids_t) > 0:
                            cidt0 = self.ti[t0, uid]
                            maskt0 = self.masks[t0][:, :, cidt0]  # there is only one mask
                            cidst_ = self.ti[t_, uids_t]  # there can be more than one potential indices at t_
                            maskst_ = self.masks[t_][:, :, cidst_]
                            weight, _, row_ind, col_ind = _get_link(maskt0, maskst_, self.logic, self.thres)
                            if len(row_ind) > 0:
                                for (r, c) in zip(row_ind, col_ind):
                                    if weight[r, c] >= self.thres:
                                        #                             cidt0 = cidt0
                                        #                             cidt_ = cidst_[c]
                                        """find corresponding uid """
                                        uidt_ = uids_t[c]
                                        """ recore how to update tc """
                                        ids_update[uid_i] = uidt_
                                    t_ += 1
                            else:
                                t_ += 1
                        else:
                            t_ += 1
            to_del = [idx for idx in ids_update if idx != -1]
            if len(to_del) == 0:
                print("\nno updates!")
            else:
                print("updates!!")
                # there will be updates, so save previous result in self.ti_, self.t_appear_, and self.t_disappear_, respectively
                self.ti_, self.t_appear_, self.t_disappear_ = ti_, t_appear_, t_disappear_
                for (idx, id_up) in enumerate(ids_update):
                    if id_up != -1:
                        id_old = disp_uids[idx]
                        t_ = t_appear_[id_up]
                        self.ti[t_:, id_old] = self.ti[t_:, id_up]
                self.ti = np.delete(self.ti, to_del, 1)
                self.t_appear = np.delete(self.t_appear, to_del)
                self.t_disappear = np.delete(self.t_disappear, to_del)

                self.ids_update = ids_update
                self.disp_uids = disp_uids
                self.updated = 1
                self.delta_t = delta_t
                self.max_uid = self.max_uid - len(np.where(ids_update > -1)[0])

    # def visualize(self, visualdir, colors=None, color_all=None):
    #     """
    #     Create 3 sets of visualization
    #     visualization set 1: one leaf per image (visualdir['1'])
    #     visualization set 2: show with an alpha channel (visualdir['2'])
    #     visualization method 3: show with bounding boxes (visualdir['3'])
    #     Also save a csv file called linking_info.csv (or other user defined name) that includes the linking information
    #     """
    #
    #     # create subfolders inside the provided directory of visualization
    #     visualdirs = dict()
    #     for i in range(1, 4):
    #         idx = str(i)
    #         visualdirs[idx] = os.path.join(visualdir, 'visualization{}'.format(idx))
    #         if not os.path.exists(visualdirs[idx]):
    #             os.makedirs(visualdirs[idx])
    #
    #     if colors is None:
    #         colors = visualize_display_instances._random_colors(self.max_uid) # worest case: all leaves are unique
    #     if color_all is None:
    #         color_all = [[tuple() for i in range(0, num)] for num in self.n_insts]
    #
    #     for (t,ti_t) in enumerate(self.ti):
    #         uids_t = [x for x in ti_t if x >= 0]
    #         for (idx,uid) in enumerate(uids_t):
    #             color_all[t][idx] = colors[uid]
    #
    #     for (img, masks, colors_t, t) in zip(self.images, self.masks, color_all, self.timepoints):
    #         savename3 = os.path.join(visualdirs['3'], '{}.jpg'.format(t))
    #         _visualize3(img, masks, colors_t, savename=savename3)
    #         plt.close("all")

    def __call__(self, images, masks, timepoints, savedir, savename, logic="IOS", thres=0.2, name_sub="instance",
                 colors=None, color_all=None, update=False, max_delta_t=2, savedir_=None, savename_=None):
        # a list of images which are ndarrays
        self.images = images
        # a list of masks which are ndarrays (of the same length of images)
        self.masks = masks
        # a list of timepoints (of the same length of images)
        self.timepoints = timepoints
        self.T = len(self.timepoints)
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = []
        for i in range(0, len(self.masks)):
            self.n_insts.append(self.masks[i].shape[2])

        # initialization for linking
        self.thres = thres
        self.link_info = [-np.ones((self.n_insts[i]), dtype=np.int64) for i in range(0, self.T - 1)]

        self.weights = []
        self.logic = logic.upper()
        self.name_sub = name_sub
        self.key_id = '{}_ids'.format(name_sub)

        for t0 in range(0, self.T - 1):
            self.linking(t0)
        self.get_uid()
        self.emergence, self.emerge_times = _get_emergence(self.uids)
        self.ti, self.t_appear, self.t_disappear = _get_ti(self.n_insts, self.uids, self.link_info)
        # visualdir = os.path.join(savedir, "visualization")
        # if not os.path.exists(visualdir):
        #     os.makedirs(visualdir)
        # self.visualize(visualdir)
        self.save_linked_series(savedir, savename)

        if update:
            self.update_ti(max_delta_t)
            if self.updated == 1:
                if savedir_ is not None and savedir_ != savedir:
                    visualdir_ = os.path.join(savedir, "visualization")
                else:
                    savedir_ = savedir
                    visualdir_ = os.path.join(savedir, "updated_visualization")
                if not os.path.exists(visualdir_):
                    os.makedirs(visualdir_)

                if savename_ is None:
                    savename_ = "{}_{}".format(savename, max_delta_t)

                # self.visualize(visualdir_)
                self.save_linked_series(savedir_, savename_)

        # self.save_to_csv(savedir, "link_series_old.csv", "link_info_old.csv")
