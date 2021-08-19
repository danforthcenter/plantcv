# Link time-series

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import os.path as osp
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
from plantcv.plantcv import fatal_error, params, color_palette
from scipy.optimize import linear_sum_assignment
from scipy.spatial import distance
import csv
from plantcv.plantcv.visualize import display_instances
# import sys
# sys.path.append('/shares/mgehan_share/hsheng/projects/test_plantcv/visualize_display_instances')
# from visualize_display_instances import display_instances


class InstanceTimeSeriesLinking(object):
    """A class that links segmented instances throughout time
    Assumption: the timepoints are all sorted, the images and masks are also sorted by timepoints (chronologically)
    """

    def __init__(self):
        # a list of masks which are ndarrays (of the same length of images)
        self.masks, self.tips = None, None
        self.T, self.N, self.max_uid = None, None, None
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = None

        # initialization for linking
        self.thres, self.metric, self.uids, self.link_info, self.weights  = None, None, None, None, None
        self.ti, self.ti_old, self.tracking_report, self.tracking_report_old = None, None, None, None
        # self.name_sub = None
        # self.key_id = None

    def save_linked_series(self, savedir, savename):
        pkl.dump(vars(self), open(osp.join(savedir,  f"{savename}.pkl"), 'wb'))

    def import_linked_series(self, savedir, savename):
        linked = pkl.load(open(osp.join(savedir, savename + '.pkl'), "rb"))
        for key, value in linked.items():
            setattr(self, key, value)

    @staticmethod
    def get_link(weight, thres):
        """Get the link (coordinates) between two sets of instances based on pre-calculated weight matrix
        Inputs:
        weight = weight matrix, the smaller the weight, the more possible two will be linked
        thres = minimum weight value for two instances to be considered as the same one
        Outputs:
        link = a list containing link information: e.g. [0,2,3,1] -> item 0 link to item 0, item 1 link to item 2, item 2 link to item 3, item 3 link to item 1

        :param weight: numpy.ndarray
        :param thres: float
        :return link: list
        """
        n1, n2 = weight.shape
        link = -np.ones(n1, dtype=np.int64)
        idx_col = np.where(np.max(weight, axis=0) < thres)[0]  # find those columns with maximum value < threshold
        avail_col = [x for x in range(0, n2) if x not in idx_col]
        weight = np.delete(weight, idx_col, 1)
        row_ind, col_ind = linear_sum_assignment(weight, maximize=True)
        for (r, c) in zip(row_ind, col_ind):
            if weight[r, c] >= thres:
                link[r] = avail_col[c]
        return link#, row_ind, col_ind


    @staticmethod
    def compute_overlaps_weights(masks1, masks2, metric):
        """
        Compute weights between 2 sets of binary masks based on their overlaps
        The overlaps are represented by either IoU (intersection over union) and IoS (intersection over self-area of the 1st mask).
        Inputs:
        masks1 = Binary masks data correspond to the 1st image
        masks2 = Binary masks data correspond to the 2nd image
        metric = metric to evaluate the overlap between 2 sets of binary masks
        Outputs:
        n1     = the number of instances in 1st set of binary masks
        n2     = the number of instances in 2nd set of binary masks
        ious   = inversection over union between any pairs of instances in masks1 and masks2
        ioss   = inversection over self-area (areas of instances in 1st set of masks) between any pairs of instances in masks1 and masks2
        unions = unions between any pairs of instances in masks1 and masks2

        :param masks1: (numpy.ndarray of shape: [Height, Width, n1]) , where n1 is the number of instances
        :param masks2: (numpy.ndarray of shape: [Height, Width, n2]) , where n2 is the number of instances
        :param metric: str
        :return n1: int
        :return n2: int
        :return ious: numpy.ndarray of shape: [n1, n2]
        :return ioss: numpy.ndarray of shape: [n1, n2]
        :return unions: numpy.ndarray of shape: [n1, n2]
        """

        if not (metric.upper() == "IOU" or metric.upper() == "IOS"):
            fatal_error("Currently only calculating metrics 'IOU' and 'IOS' are available!")

        # If either set of masks is empty return an empty result
        # if masks1.shape[-1] == 0 or masks2.shape[-1] == 0:
        #     return np.zeros((masks1.shape[-1], masks2.shape[-1]))
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
        if metric.upper() == "IOU":
            return ious, n1, n2, unions
        else:
            return ioss, n1, n2, unions


    # @staticmethod
    # def compute_weights(measure1, measure2, metric):
    #     if metric.upper() == "IOU" or metric.upper() == "IOS":
    #         weights, n1, n2, _ = InstanceTimeSeriesLinking.compute_overlaps_weights(measure1, measure2, metric)
    #     elif metric.upper() == "DIST":
    #         weights, n1, n2, _ = InstanceTimeSeriesLinking.compute_dist_weights(measure1, measure2, metric)
    #     else:
    #         fatal_error("Currently only calculating metrics 'IOU', 'IOS', or 'DIST' are available!")
    #     return weights, n1, n2


    @staticmethod
    def get_sorted_uids(link_info, n_insts):
        """
        Get unique indices at every timestamp based on link information and number of instances at every timepoint
        Inputs:
        link_info = a list (length: T-1) of linking information, every sub-list contains the information of how every instance link to instances to the next timepoint
        n_insts   = a list (length: T) contains the information of number of instances at every timepoint.
        Outputs:
        uids_sort = a list of unique indices at every timepoint. Every element in the list is a numpy array. Every array contains the information of unique indices & location.
        e.g. [2,0,3,20] means that unique indices 0,2,3,20 are present in this timepoint, specifically, 2 is at location 0, 0 is at location 1, 3 is at location 2, and 20 is at location 3

        :param link_info: list
        :param n_insts: list
        :return uids_sort: list
        """
        uids_sort = [-1 * np.ones(num, dtype=np.int64) for num in n_insts]
        uids_sort[0] = np.arange(n_insts[0])
        max_uid = max(uids_sort[0])
        N = len(np.unique(uids_sort[0]))
        for t in range(1, len(link_info) + 1):

            li_t = link_info[t - 1]
            uids_sort_t = uids_sort[t]
            uids_sort_t_ = uids_sort[t - 1]
            for cidt_, cidt in enumerate(li_t):
                if cidt > -1:
                    uids_sort_t[cidt] = uids_sort_t_[cidt_]
            if -1 in uids_sort_t:
                ids = np.where(uids_sort_t == -1)[0]
                for i in ids:
                    max_uid += 1
                    N += 1
                    uids_sort_t[i] = max_uid
            uids_sort[t] = uids_sort_t
        return uids_sort, max_uid, N


    @staticmethod
    def get_uids_from_ti(ti):
        """
        Get unique indices at every timestamp based on tracking information
        :param ti: numpy.array
        :return uids_sort: list
        """
        # uids: a list of length T, where every sub-list has a length of n_t (# of instances at time t). Every sub-list is
        # contains the unique indices present at time t

        # uids_sort: basically the contains the same information as uids, however, in every sub-list of uids_sort, the
        # location of every unique-id represent the index of the leaf in the image (cid)
        T, N = ti.shape
        uids = [np.where(ti_t > -1)[0] for ti_t in ti]
        uids_sort = [[np.where(ti_t > -1)[0][i] for i in np.argsort(ti_t[np.where(ti_t > -1)])] for ti_t in ti]

        return uids_sort#, uids, T, N

    @staticmethod
    def get_emerg_disap_info(uids):
        """
        Get emergence and disappearence indices and corresponding timepoints based on uids
        Inputs:
        uids = unique indices present at evert timepoint
        Outputs:
        emergence     = new unique indices and their emerging times. e.g. emergence = {0: [0,1,2,3], 4, [4]} means that at t0, new uids 0,1,2,3 first appear, at t4, new uid 4 first appear
        disappearance = disappearence of unique indices and the last timepoint they exist
        :param uids: list
        :return emergence: dictionary
        :return disappearance: dictionary
        """
        emergence, disappearance = dict(), dict()
        emergence[0] = list(uids[0])
        for (t, temp) in enumerate(uids):
            if t >= 1:
                emerg = [x for x in temp if x not in uids[t - 1]]
                if len(emerg) > 0:
                    emergence[t] = emerg
            if t < len(uids) - 1:
                disap = [x for x in temp if x not in uids[t + 1]]
                if len(disap) > 0:
                    disappearance[t] = disap
        return emergence, disappearance


    @staticmethod
    def get_ti(uids, link_info, n_insts):
        """
        Get tracking information from linking information, number of instances, and unique indices at every timepoint
        :param uids: list
        :param link_info: list
        :param n_insts: list
        :return ti: numpy.array
        """
        emergence, _ = InstanceTimeSeriesLinking.get_emerg_disap_info(uids)
        N = max([max(uid) for uid in uids]) + 1
        T = len(uids)
        ti = -np.ones((T, N), dtype=np.int64)
        ti[0,0:n_insts[0]] = uids[0] # initialize ti for 1st timepoint as unique ids of the 1st timepoint
        for t in range(1,T):
            li_t = link_info[t-1]                # link_info from t-1 to t
            prev = ti[t-1]                       # tracking info at previous timepoint (t-1)
            cids = list(np.arange(0,n_insts[t])) # possible values of current indices
            for (uid,pid) in enumerate(prev):
                if pid >= 0:
                    cid = li_t[pid]
                    ti[t,uid] = cid
                    if cid >= 0:
                        cids.remove(cid)
            # if t is a timepoint with new instances
            if t in emergence.keys():
                new_ids = emergence[t]
                for (cid,new_id) in zip(cids,new_ids):
                    ti[t,new_id] = cid
        return ti


    @staticmethod
    def get_li_from_ti(ti):
        """
        Get linking information from tracking information
        :param ti: numpy.array
        :return link_info: list
        """
        T, N = ti.shape
        link_info = [np.empty(0) for _ in range(0, T - 1)]
        for t in range(T - 1):
            ti_0 = ti[t, :]
            ti_1 = ti[t + 1, :]
            l0 = [x for x in ti_0 if x >= 0]
            l1 = [x for (x, y) in zip(ti_1, ti_0) if y >= 0]
            link_t = -np.ones(len(l0), dtype=np.int64)
            for (idx, x) in enumerate(l0):
                link_t[x] = l1[idx]
            link_info[t] = link_t
        return link_info


    @staticmethod
    def area_tracking_report(ti, masks):
        tracking_report = np.zeros(ti.shape)
        for (t, masks_t) in enumerate(masks):
            ti_t = ti[t, :]
            for cid in range(masks_t.shape[2]):
                uid = np.where(ti_t == cid)[0][0]
                tracking_report[t, uid] = np.sum(masks_t[:, :, cid])
        return tracking_report


    # @staticmethod
    # def length_tracking_report(ti, masks):
    #     tracking_report = np.zeros(ti.shape)
    #     for (t, masks_t) in enumerate(masks):
    #         ti_t = ti[t, :]
    #         for cid in range(masks_t.shape[2]):
    #             uid = np.where(ti_t == cid)[0][0]
    #             tracking_report[t, uid] = np.sum(masks_t[:, :, cid])
    #     return tracking_report


    @staticmethod
    def visualize(imgs, masks, tps, savedir, ti = None, color_all = None):
        params.debug = "plot"
        if not osp.exists(savedir):
            os.makedirs(savedir)

        n_insts = [masks_t.shape[2] for masks_t in masks]
        if not color_all:
            if ti is None: # if no tracking information provided, the color assignment would base on local id (cid) solely
                N = max(n_insts)
                T = len(imgs)
            else:
                T, N = ti.shape
            colors_ = color_palette(N)
            colors = [tuple([ci / 255 for ci in c]) for c in colors_]
            if ti is None:
                color_all = [[colors[i] for i in range(0, num)] for num in n_insts]
            else:
                color_all = [[tuple() for _ in range(0, num)] for num in n_insts]
                for (t, ti_t) in enumerate(ti):
                    for (uid, cid) in enumerate(ti_t):
                        if cid > -1:
                            color_all[t][cid] = colors[uid]
        for img_t, masks_t, t, colors_t in zip(imgs, masks, tps, color_all):
            savename = osp.join(savedir, '{}.jpg'.format(t))
            display_instances(img_t, masks_t, colors=colors_t)
            plt.savefig(savename, bbox_inches="tight", pad_inches=0)
            plt.close("all")


    def link_t(self,t0):
        """
        Time-series linking for a given timepoint to the next time point
        :param t0:
        :return:
        """
        masks0, masks1 = copy.deepcopy(self.masks[t0]), copy.deepcopy(self.masks[t0 + 1])  # both masks0 and masks1 are ndarrays
        self.weights[t0], _, _, _ = self.compute_overlaps_weights(masks0, masks1, self.metric)
        # self.link_info[t0], _, _ = self.get_link(self.weights[t0], self.thres)
        self.link_info[t0] = self.get_link(self.weights[t0], self.thres)


    def link(self, masks, metric="IOS", thres=0.2):
        # a list of masks which are ndarrays (of the same length of images)
        self.masks = masks
        self.T = len(masks)
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = []
        for i in range(0, self.T):
            self.n_insts.append(self.masks[i].shape[2])

        # initialization for linking
        self.thres     = thres
        self.link_info = [-np.ones((self.n_insts[i]), dtype=np.int64) for i in range(0, self.T - 1)]

        self.weights  = [np.empty(0) for _ in range(self.T-1)]
        self.metric    = metric.upper()

        for t0 in range(0, self.T - 1):
            self.link_t(t0)

        # self.ti, self.t_appear, self.t_disappear = self.get_ti(self.T, self.N, self.n_insts, self.uids, self.link_info)
        # self.uids, uids_sort, _, self.N = self.get_uid(self.ti)
        # self.emergence, self.emerge_times = self.get_emerg_disap_info(uids_sort)

        self.uids, self.max_uid, self.N = InstanceTimeSeriesLinking.get_sorted_uids(self.link_info, self.n_insts)
        self.ti = self.get_ti(self.uids, self.link_info, self.n_insts)
        self.tracking_report = InstanceTimeSeriesLinking.area_tracking_report(self.ti, self.masks)


    @staticmethod
    def compute_dist_weights(pts1, pts2):
        n1, n2 = len(pts1), len(pts2)
        weight = distance.cdist(pts1, pts2)
        return weight, n1, n2


    def link_dist_t(self,t0):
        tips0, tips1 = copy.deepcopy(self.tips[t0]), copy.deepcopy(self.tips[t0 + 1])  # both masks0 and masks1 are ndarrays
        weights, _, _, _ = self.compute_dist_weights(tips0, tips1)
        self.weights[t0] = -weights
        self.link_info[t0] = self.get_link(self.weights[t0], self.thres)

    def link_dist(self, tips, thres=0.0):
        self.tips = tips
        self.T = len(tips)
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = []
        for i in range(0, self.T):
            self.n_insts.append(len(self.tips[i]))
        # initialization for linking
        self.thres     = thres
        self.link_info = [-np.ones((self.n_insts[i]), dtype=np.int64) for i in range(0, self.T - 1)]
        self.weights = [np.empty(0) for _ in range(self.T - 1)]

        for t0 in range(0, self.T - 1):
            self.link_dist_t(t0)

        self.uids, self.max_uid, self.N = InstanceTimeSeriesLinking.get_sorted_uids(self.link_info, self.n_insts)
        self.ti = self.get_ti(self.uids, self.link_info, self.n_insts)
        self.tracking_report = InstanceTimeSeriesLinking.area_tracking_report(self.ti, self.masks)


    @staticmethod
    def _update_ti(masks, metric, thres, ti, min_gap, max_gap):
        ti_ = copy.deepcopy(ti)
        T, N = ti.shape
        uids_sort = InstanceTimeSeriesLinking.get_uids_from_ti(ti)
        emergence, disappearance = InstanceTimeSeriesLinking.get_emerg_disap_info(uids_sort)
        t_emerg, t_disap = emergence.keys(), disappearance.keys()
        # loop over timepoints with disappearing leaves (in reversed order)
        for t in reversed(sorted(t_disap)):
            # unique indices(index) that last appear at t
            uids_disap = disappearance[t]
            # corresponding cid(s) (i.e. indices for masks)
            cids_disap = [uids_sort[t].index(i) for i in uids_disap]
            # pull out masks
            masks_t = np.take(masks[t], cids_disap, axis=2)

            # timepoints with potential link with t
            ts_pot = [te for te in t_emerg if t + min_gap < te < t + max_gap]
            # loop over timepoints for a potential link and get cids and masks for every timepoint
            for t_ in ts_pot:
                uids_emerg = emergence[t_]
                cids_emerg = [uids_sort[t_].index(i) for i in uids_emerg]
                masks_t_ = np.take(masks[t_], cids_emerg, axis=2)

                # calculate weight to calculate the link
                weights, n1, n2, _ = InstanceTimeSeriesLinking.compute_overlaps_weights(masks_t, masks_t_, metric)
                # li_ts, _, _ = InstanceTimeSeriesLinking.get_link(weights, self.thres)
                li_ts = InstanceTimeSeriesLinking.get_link(weights, thres)

                uids_undisap = []
                for (idx, uid_disap) in enumerate(uids_disap):  # loop over all disappeared indices
                    li_t = li_ts[idx]
                    if li_t > -1:
                        print(f"\n{t} -> {t_}: ")
                        print(f"{uid_disap} <- {uids_emerg[li_t]}")
                        # update ti
                        ti_[t_:, uid_disap] = ti_[t_:, uids_emerg[li_t]]
                        ti_[t_:, uids_emerg[li_t]] = -np.ones(T - t_, dtype=np.int64)
                        uids_undisap.append(uid_disap)
                    uids_disap = list(set(uids_disap).difference(set(uids_undisap)))

                    if len(uids_disap) == 0:
                        # remove key
                        disappearance.pop(t)
                        break
                    else:
                        # update
                        disappearance[t] = uids_disap
        remove_uids = []
        for uid in range(N):
            if (ti_[:, uid] == -1).all():
                remove_uids.append(uid)
        ti_ = np.delete(ti_, remove_uids, axis=1)
        return ti_


    # def update_ti(self, ti, max_gap=5):
    def update_ti(self, max_gap=5):
        # self.ti_old = ti
        self.ti_old = self.ti
        self.tracking_report_old = self.tracking_report
        min_gap = 1
        # ti_ = InstanceTimeSeriesLinking._update_ti(self.masks, self.metric, self.thres, ti, min_gap, max_gap)
        ti_ = InstanceTimeSeriesLinking._update_ti(self.masks, self.metric, self.thres, self.ti_old, min_gap, max_gap)
        while True:
            min_gap += 1
            ti = ti_
            ti_ = InstanceTimeSeriesLinking._update_ti(self.masks, self.metric, self.thres, ti, min_gap, max_gap)
            if np.array_equal(ti_, ti) or min_gap == max_gap - 2:
                # return ti_
                self.ti = ti_
                # update tracking_report
                self.tracking_report = InstanceTimeSeriesLinking.area_tracking_report(self.ti, self.masks)
                break


    # def __call__(self, images, masks, timepoints, metric="IOS", thres=0.2, name_sub="instance", update=False, max_delta_t=2):
    #     # a list of images which are ndarrays
    #     self.images = images
    #     # a list of masks which are ndarrays (of the same length of images)
    #     self.masks = masks
    #     # a list of timepoints (of the same length of images)
    #     self.timepoints = timepoints
    #     self.T = len(self.timepoints)
    #     self.name_sub = name_sub
    #     self.key_id = '{}_ids'.format(name_sub)
    #     # number of instances: a list in which every element represent for number of instances in corresponding image
    #     self.n_insts = []
    #     for i in range(0, len(self.masks)):
    #         self.n_insts.append(self.masks[i].shape[2])
    #     if update:
    #         self.update_ti(max_delta_t)
