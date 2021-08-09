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


# def compute_dist_weights(pts1, pts2):
#     """ Compute weights between 2 sets of points based on their Euclidean distances
#     Inputs:
#     pts1: the list of point coordinates for set 1
#     pts2: the list of point coordinates for set 2
#     Outputs:
#     weight: weight matrix
#     n1: number of instances of set 1
#     n2: number of instances of set 2
#
#     :param pts1: list
#     :param pts2: list
#     :return weight: numpy.ndarray
#     :return n1: int
#     :return n2: int
#     """
#     n1, n2 = len(pts1), len(pts2)
#     weight = distance.cdist(pts1, pts2)
#     return weight, n1, n2

class InstanceTimeSeriesLinking(object):
    """A class that links segmented instances throughout time
    Assumption: the timepoints are all sorted, the images and masks are also sorted by timepoints (chronologically)
    """

    def __init__(self):
        # a list of masks which are ndarrays (of the same length of images)
        self.masks = None
        self.T = None
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = None

        # initialization for linking
        self.thres = None
        self.link_info = None
        self.uids = None
        # self.max_uid = None
        self.N = None
        self.emergence = None
        self.emerge_times = None
        self.ti = None
        self.t_appear = None
        self.t_disappear = None
        self.weights = None
        self.metric = None
        # self.name_sub = None
        # self.key_id = None
        self.leaf_status_report = None

        # update releated
        self.updated = 0
        self.delta_t = None
        self.disp_uids = None
        self.ids_update = None

        self.ti_ = None
        self.t_appear_ = None
        self.t_disappear_ = None

    @staticmethod
    def get_link(weight, thres):
        """Get the link (coordinates) between two sets of instances based on pre-calculated weight matrix
        Inputs:
        weight: weight matrix, the smaller the weight, the more possible two will be linked
        thres: maximum value to link two instances
        Outputs:
        link:
        row_ind:
        col_ind:

        :param weight: numpy.ndarray
        :param thres: float
        :return link: list
        :return row_ind: int
        :return col_ind: int
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
        return link, row_ind, col_ind


    @staticmethod
    def compute_overlaps_weights(masks1, masks2, metric):
        """Compute weights between 2 sets of binary masks based on their overlaps
        The overlaps are represented by IoU (intersection over union) and IoS (intersection over self-area of the 1st mask).
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
        if metric.upper() == "IOS":
            return ioss, n1, n2, unions

    def save_linked_series(self, savedir, savename):
        pkl.dump(vars(self), open(osp.join(savedir,  f"{savename}.pkl"), 'wb'))

    def import_linked_series(self, savedir, savename):
        linked = pkl.load(open(osp.join(savedir, savename + '.pkl'), "rb"))
        for key, value in linked.items():
            setattr(self, key, value)

    def linking(self,t0):
        """
        Time-series linking for a given timepoint to the next time point
        :param t0:
        :return:
        """
        masks0, masks1 = copy.deepcopy(self.masks[t0]), copy.deepcopy(self.masks[t0 + 1])  # both masks0 and masks1 are ndarrays
        self.weights[t0], _, _, _ = self.compute_overlaps_weights(masks0, masks1, self.metric)
        self.link_info[t0], _, _ = self.get_link(self.weights[t0], self.thres)

    @staticmethod
    def get_uid(link_info, n_insts):
        """
        Get unique ids for every timepoint
        Inputs:
        link_info = link information for every timepoint. If there are T timepoints in total, the length of link_info would be T-1
        n_insts   = number of instances for every timepiont
        Outputs:
        uids      = every array inside the list has a length of n_insts for that corresponding time
        N         = number of unique instances
        :param link_info: list
        :param n_insts: list
        :return uids: list
        :return N: int
        """

        uids = [-np.ones(n, dtype=np.int64) for n in n_insts]
        uids[0] = np.arange(len(link_info[0]), dtype=np.int64)
        max_uid = max(uids[0])
        N = len(uids[0]) # initial number of instances
        for (t, link_t) in enumerate(link_info):
            for (cidt, cidt_) in enumerate(link_t):
                if cidt_ >= 0:
                    uids[t + 1][cidt_] = uids[t][cidt]
            if -1 in uids[t + 1]:  # -1 means there is no predecessor from a former timepoint -> potential to assign new uids
                temp = np.where(uids[t + 1] == -1)[0]
                for tid in temp:
                    max_uid += 1
                    uids[t + 1][tid] = max_uid
                    N += 1
        return uids, N


    @staticmethod
    def get_emergence(uids):
        """
        Get emergence information of new unique instances, and their emerging times
        Inputs:
        uids         = every array inside the list has a length of n_insts for that corresponding time
        Outputs:
        emergence    =
        emerge_times =
        :param uids:
        :return emergence:
        :return emerge_times:
        """

        emergence = [[] for _ in uids]
        emergence[0] = list(uids[0])
        for (t, temp) in enumerate(uids):
            if t >= 1:
                new = [x for x in temp if x not in uids[t - 1]]
                emergence[t] = new
        emerge_times = [i for i in range(len(emergence)) if len(emergence[i]) > 0]
        return emergence, emerge_times


    @staticmethod
    def get_ti(T, N, n_insts, uids, link_info):
        emergence, emerge_times = InstanceTimeSeriesLinking.get_emergence(uids)
        ti = -np.ones((T, N), dtype=np.int64)
        ti[0,0:n_insts[0]] = uids[0] # initialize ti for 1st timepoint as unique ids of the 1st timepoint
        for t in range(1,T):
            link = link_info[t-1]                # link_info from t-1 to t
            prev = ti[t-1]                       # tracking info at previous timepoint (t-1)
            cids = list(np.arange(0,n_insts[t])) # possible values of current indices
            for (uid,pid) in enumerate(prev):
                if pid >= 0:
                    cid = link[pid]
                    ti[t,uid] = cid
                    if cid >= 0:
                        cids.remove(cid)
            # if t is a timepoint with new instances
            if t in emerge_times:
                new_ids = emergence[t]
                for (cid,new_id) in zip(cids,new_ids):
                    ti[t,new_id] = cid

        # get appear and disappear information
        t_appear    = np.zeros(N,dtype=np.int64)
        t_disappear = -np.ones(N, dtype=np.int64)

        for (t,uids_t) in enumerate(emergence):
            if uids_t:
                for uid in uids_t:
                    t_appear[uid] = t
        for uid in range(0,N):
            t = 0
            while t < T:
                if (ti[t][uid] == -1) and (t > t_appear[uid]):
                    t_disappear[uid] = t
                    break
                else:
                    t += 1
        return ti, t_appear, t_disappear


    @staticmethod
    def get_li_from_ti(ti):
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
    def status_report(ti, masks):
        leaf_status_report = np.zeros(ti.shape)
        for (t, masks_t) in enumerate(masks):
            ti_t = ti[t, :]
            for cid in range(masks_t.shape[2]):
                uid = np.where(ti_t == cid)[0][0]
                leaf_status_report[t, uid] = np.sum(masks_t[:, :, cid])
        return leaf_status_report

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
            if not ti:
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





    # def visualize(self, imgs, timepoints, visualdir, color_all=None):
    #     params.debug = "plot"
    #     if not osp.exists(visualdir):
    #         os.makedirs(visualdir)
    #     if color_all is None:
    #         colors_ = color_palette(self.N)
    #         colors = [tuple([ci / 255 for ci in c]) for c in colors_]
    #         color_all = [[tuple() for _ in range(0, num)] for num in self.n_insts]
    #         for (t,ti_t) in enumerate(self.ti):
    #             for (uid,cid) in enumerate(ti_t):
    #                 if cid > -1:
    #                     color_all[t][cid] = colors[uid]
    #     for img,masks,t,colors_t in zip(imgs, self.masks, timepoints, color_all):
    #         savename = osp.join(visualdir, '{}.jpg'.format(t))
    #         display_instances(img, masks, colors=colors_t)
    #         plt.savefig(savename, bbox_inches="tight", pad_inches=0)
    #         plt.close("all")

    def link(self, masks, metric="IOS", thres=0.2):

    # def __call__(self, masks, metric="IOS", thres=0.2):
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
            self.linking(t0)

        self.uids, self.N = self.get_uid(self.link_info, self.n_insts)
        self.emergence, self.emerge_times = self.get_emergence(self.uids)
        self.ti, self.t_appear, self.t_disappear = self.get_ti(self.T, self.N, self.n_insts, self.uids, self.link_info)

        self.leaf_status_report = InstanceTimeSeriesLinking.status_report(self.ti, self.masks)






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