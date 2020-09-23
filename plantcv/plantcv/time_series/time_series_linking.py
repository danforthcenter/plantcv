#### link utilities
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

def _random_colors(num, bright=True):
    """
    Generate desired number of random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    Inputs:
    num: number of colors to be generated
    bright: True or False, if true, the brightness would be 1.0; if False, the brightness would be 0.7. By default it would be True (brightness 0.7)
    Output: generated colors (a tuple)
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / num, 1, brightness) for i in range(num)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


def _apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image with a color and alpha channel assigned.
    Inputs:
    image: original RGB image
    mask: a binary mask of same size to the image
    color: a list of 3 values
    alpha: alpha value indicating transparency, by default 0.5
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image


def _get_ax(rows=1, cols=1, size=16):  # ???
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.

    Adjust the size attribute to control how big to render images
    """
    fig, ax = plt.subplots(rows, cols, figsize=(size * cols, size * rows))
    fig.tight_layout()
    return ax


def _display_instances(image, masks, figsize=(16, 16), title="", ax=None, colors=None):
    """
    This function is inspired by the function in mrcnn
    masks: [height, width, num_instances]
    inst_ids: [num_instances]
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # If no axis is passed, create one and automatically call show()
    # auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        # auto_show = True

    num_insts = masks.shape[2]
    # Generate random colors
    colors = colors or _random_colors(num_insts)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(num_insts):
        color = colors[i]

        # Mask
        mask = masks[:, :, i]
        masked_image = _apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))
    # if auto_show:
    #     plt.show()


def _compute_overlaps_masks(masks1, masks2):
    """Computes IoU and IoS overlaps between two sets of masks.
    The masks should be of the same size
    masks1, masks2: [Height, Width, instances]
    """
    # If either set of masks is empty return empty result
    if masks1.shape[-1] == 0 or masks2.shape[-1] == 0:
        return np.zeros((masks1.shape[-1], masks2.shape[-1]))
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
    return ious, ioss


class InstanceTimeSeriesLinking(object):
    """A class that links segmented instances throughout time
    Assumption: the timepoints are all sorted, the images and masks are also sorted by timepoints (chronologically)
    """

    def __init__(self, images, masks, timepoints, logic='IOS', thres=0.2, name_sub='instance'):
        # a list of images which are ndarrays
        self.images = images
        # a list of masks which are ndarrays (of the same length of images)
        self.masks = masks
        # a list of timepoints (of the same length of images)
        self.timepoints = timepoints
        self.total_time = len(self.timepoints)
        # number of instances: a list in which every element represent for number of instances in corresponding image
        self.n_insts = []
        for i in range(0, len(self.masks)):
            self.n_insts.append(self.masks[i].shape[2])

        # initialization for linking
        self.thres = thres
        self.link_info = [-np.ones((self.n_insts[i]), dtype=int) for i in range(0, self.total_time - 1)]
        self.unlinked_insts = [np.array(range(0, self.n_insts[i])) for i in range(0, self.total_time)]
        self.link_series = dict()  # only for those newly emerging leaves
        self.weights = []
        self.logic = logic.upper()
        self.name_sub = name_sub
        self.key_id = '{}_ids'.format(name_sub)

    def save_linked_series(self, savedir, savename):
        """save lining information into a .csv file and a .pkl file with the same prefix of filename
        Inputs: savedir and savename
        """
        l0 = ['', ''] + [x for (idx, x) in enumerate(self.timepoints)]
        l1 = ['unique_id', 'current_id'] + ['t{}'.format(idx) for (idx, x) in enumerate(self.timepoints)]
        csvfile = open(os.path.join(savedir, savename + '.csv'), 'w', newline='')
        writer_junk = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer_junk.writerow(l0)
        writer_junk.writerow(l1)
        for (t0, item) in self.link_series.items():
            for uid, cid in zip(item['unique_id'], item[self.key_id]):
                new_line = ['{}'.format(uid), '{}'.format(cid)] + item['{}{}'.format(self.name_sub, cid)].tolist()
                writer_junk.writerow(new_line)
        csvfile.close()
        pkl.dump(self, open(os.path.join(savedir, savename + '.pkl'), 'wb'))

    def linking(self, t0):
        """
        Link instance segments of t0 to those of t1 (t0+1) by calculating the overlaps of their masks
        :param t0: starting time point
        :return: None, but self.link_info would be updated
        """
        masks0, masks1 = copy.deepcopy(self.masks[t0]), copy.deepcopy(
            self.masks[t0 + 1])  # both masks0 and masks1 are ndarrays
        n0, n1 = masks0.shape[2], masks1.shape[2]
        weight = -np.inf * np.ones((n0, n1))
        link = -np.ones(n0)
        ious, ioss = _compute_overlaps_masks(masks0, masks1)
        if self.logic == 'IOU':
            weight = ious
        elif self.logic == 'IOS':
            weight = ioss
        self.weights.append(weight)
        idx_col = np.where(np.max(weight, axis=0) < self.thres)[
            0]  # find those columns with maximum value < threshold (self.thres)
        avail_col = [x for x in range(0, n1) if x not in idx_col]
        weight_ = copy.deepcopy(weight)
        weight_ = np.delete(weight_, idx_col, 1)

        row_ind, col_ind = linear_sum_assignment(weight_, maximize=True)
        for (r, c) in zip(row_ind, col_ind):
            if weight_[r, c] >= self.thres:
                link[r] = avail_col[c]
        self.link_info[t0] = link

    def get_series(self):
        """
        Using the self.link_info to create a dictionary save in self.link_series
        which is a dictionary contains information for every timepoint with new instances not seen before,
        and the linking information for every instance
        :return:
        """
        # define new leaves and their unique identifiers at time points with new leaves emerging
        t = 0
        key_t = 't{}'.format(t)
        self.link_series[key_t] = dict()
        self.link_series[key_t][self.key_id] = self.unlinked_insts[0]
        #
        self.link_series[key_t]['unique_id'] = self.link_series[key_t][self.key_id]
        unique_id = len(self.link_series[key_t][self.key_id])

        for t in range(1, self.total_time):
            new_insts = [i for i in self.unlinked_insts[t] if i not in self.link_info[t - 1]]
            if new_insts:
                key_t = 't{}'.format(t)
                self.link_series[key_t] = dict()
                self.link_series[key_t][self.key_id] = np.array(new_insts)

                id_temp = []
                for new_inst in new_insts:
                    id_temp.append(unique_id)
                    unique_id = unique_id + 1
                self.link_series[key_t]['unique_id'] = np.array(id_temp)
        ## for time points with new leaves emerging, get the linking information for every new instance
        for key_t in self.link_series:
            t0 = int(key_t.replace('t', ''))
            for (leaf_unique, inst) in zip(self.link_series[key_t]['unique_id'], self.link_series[key_t][self.key_id]):
                key_inst = '{}{}'.format(self.name_sub, inst)
                self.link_series[key_t][key_inst] = -np.ones(self.total_time, dtype=int)
                self.link_series[key_t][key_inst][t0] = inst
                if t0 < self.total_time - 1:
                    self.link_series[key_t][key_inst][t0 + 1] = self.link_info[t0][inst]
                    for t_ in range(t0 + 2, self.total_time):
                        idx = self.link_series[key_t][key_inst][t_ - 1]
                        if idx < 0:
                            break
                        else:
                            self.link_series[key_t][key_inst][t_] = self.link_info[t_ - 1][idx]

    def update_series(self):
        """
        Update the linking by comparing pairs of timepoint which are t and t+2
        :return:
        """
        link_series = copy.deepcopy(self.link_series)
        for t_, content in link_series.items():
            t = int(t_.replace('t', ''))
            for inst_id in content[self.key_id]:
                temp = np.where(content['{}{}'.format(self.name_sub, inst_id)] < 0)[0]
                if len(temp) > 0:
                    t0 = temp[0] - 1
                    t2 = t0 + 2
                    if t2 <= self.total_time - 1:
                        t2_ = 't{}'.format(t2)
                        if t2_ in self.link_series:
                            t0_ = 't{}'.format(t0)
                            # print('\nt0: {}, t2: {}'.format(t0_, t2_))
                            idx0 = content['{}{}'.format(self.name_sub, inst_id)][t0]
                            mask0 = np.expand_dims(self.masks[t0][:, :, idx0], axis=2)
                            idxs2 = self.link_series[t2_][self.key_id]
                            masks2 = self.masks[t2][:, :, idxs2]
                            n2 = masks2.shape[2]
                            ious, ioss = _compute_overlaps_masks(mask0, masks2)
                            if self.logic == 'IOU':
                                weight = ious
                            elif self.logic == 'IOS':
                                weight = ioss
                            idx_col = np.where(np.max(weight, axis=0) < self.thres)[
                                0]  # find those columns with maximum value < thres
                            # avail_col = [x for x in range(0, n2) if x not in idx_col]
                            weight_ = copy.deepcopy(weight)
                            weight_ = np.delete(weight_, idx_col, 1)
                            row_ind, col_ind = linear_sum_assignment(weight_, maximize=True)
                            for (r, c) in zip(row_ind, col_ind):
                                if weight_[r, c] >= self.thres:
                                    inst0 = idx0
                                    inst2 = idxs2[c]

                                    # find the time point
                                    idx_l2 = np.where(self.link_series[t2_][self.key_id] == inst2)[0][0]
                                    # add information to t_
                                    self.link_series[t_]['{}{}'.format(self.name_sub, leaf_id)][t0 + 1:] = \
                                    self.link_series[t2_]['{}{}'.format(self.name_sub, inst2)][t0 + 1:]
                                    # delete from t2_
                                    self.link_series[t2_][self.key_id] = np.delete(self.link_series[t2_][self.key_id],
                                                                                   idx_l2)
                                    self.link_series[t2_]['unique_id'] = np.delete(self.link_series[t2_]['unique_id'],
                                                                                   idx_l2)
                                    del self.link_series[t2_]['{}{}'.format(self.name_sub, inst2)]
                                    # if nothing left for t2_, delete it entirely
                                    if len(self.link_series[t2_]['unique_id']) == 0:
                                        del self.link_series[t2_]
        # update unique ids
        uid = 0
        for t in self.link_series:
            num = len(self.link_series[t][self.key_id])
            self.link_series[t]['unique_id'] = np.arange(uid, uid + num)
            uid = uid + num

    def visualize(self, visualdir, csvdir, csvname='linking_info', colors=None, color_all=None):
        """
        Create 3 sets of visualization
        visualization set 1: one leaf per image (visualdir['1'])
        visualization set 2: show with an alpha channel (visualdir['2'])
        visualization method 3: show with bounding boxes (visualdir['3'])
        Also save a csv file called linking_info.csv (or other user defined name) that includes the linking information
        """

        # create subfolders inside the provided directory of visualization
        visualdirs = dict()
        for i in range(1, 4):
            idx = str(i)
            visualdirs[idx] = os.path.join(visualdir, 'visualization{}'.format(idx))
            if not os.path.exists(visualdirs[idx]):
                os.makedirs(visualdirs[idx])

        if colors is None:
            colors = _random_colors(40)
        if color_all is None:
            color_all = [[tuple() for i in range(0, num)] for num in self.n_insts]

        count = 0
        csvfile = open(os.path.join(csvdir, csvname + '.csv'), 'w', newline='')
        writer_junk = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer_junk.writerow(
            ['unique_id', 'emerging_time', 'file_name_emerge', 'current_time', 'file_name', 'current_id'])
        for key_t in self.link_series:
            ids = self.link_series[key_t]['unique_id']
            start_time = int(key_t.replace('t', ''))
            insts_t = self.link_series[key_t][self.key_id]
            for (unique_id, inst) in zip(ids, insts_t):
                key_inst = '{}{}'.format(self.name_sub, inst)
                link_inst = self.link_series[key_t][key_inst]
                start_idx = link_inst[start_time]
                for t in range(0, self.total_time):
                    img_t = self.images[t]
                    # initialize mask used in 1st visualization
                    mask_1 = np.zeros(img_t.shape[0:2], dtype=np.uint8)
                    # initialize mask used in 2nd visualization (with an alpha channel, ahpha=0.5)
                    mask_2 = np.ones(img_t.shape[0:2]) * 0.5
                    title_vis2 = '{} (t{})'.format(self.timepoints[t], t)
                    if link_inst[t] >= 0:
                        title_vis2 = title_vis2 + ' leaf {}'.format(link_inst[t])
                        mask_t = self.masks[t][:, :, link_inst[t]]
                        color_all[t][link_inst[t]] = colors[count]

                        ## 1. save the masked image, i.e. single leaves
                        mask_1[np.where(mask_t)] = 255
                        leaf_t = pcv.apply_mask(img_t, mask_1, mask_color='black')
                        writer_junk.writerow(
                            [unique_id, start_time, self.timepoints[start_time], t, self.timepoints[t], link_inst[t]])

                        pcv.print_image(leaf_t, os.path.join(visualdirs['1'],
                                                             '{}_{}-{}-{}-{}_{}.png'.format(unique_id, start_time,
                                                                                            start_idx, t, link_inst[t],
                                                                                            self.timepoints[t])))
                        mask_2[np.where(mask_t == True)] = 1
                    masked_im = np.concatenate((img_t.astype(float) / 255, np.expand_dims(mask_2, axis=2)), axis=2)
                    # for 2nd set of visualization, a folder for one unique instance
                    save_dir_ = os.path.join(visualdirs['2'], '{}_{}-{}'.format(unique_id, start_time, start_idx))
                    if not os.path.exists(save_dir_):
                        os.makedirs(save_dir_)
                    fig2 = plt.figure(figsize=(5, 5))
                    ax2 = fig2.add_subplot(1, 1, 1)
                    ax2.imshow(masked_im)
                    ax2.axis('off')
                    ax2.set_title(title_vis2, fontsize=16)
                    plt.savefig(os.path.join(save_dir_, str(self.timepoints[t]) + '.png'))
                    plt.close(fig2)

                count += 1
        csvfile.close()
        ## 3. visualize with bounding boxes
        for (img, masks, color, t) in zip(self.images, self.masks, color_all, self.timepoints):
            _display_instances(img, masks, figsize=(16, 16), title="", ax=_get_ax(rows=1, cols=1, size=16),
                               colors=color)
            plt.savefig(os.path.join(visualdirs['3'], '{}.png'.format(t)))
            plt.close('all')

    def __call__(self, savedir, visualdir_, visualdir, savename_, savename, colors=None, color_all=None):
        for t0 in range(0, self.total_time - 1):
            self.linking(t0)
        self.get_series()
        self.visualize(visualdir_, savedir, 'link_info_old', colors, color_all)
        self.save_linked_series(savedir, savename_)

        self.update_series()
        self.visualize(visualdir, savedir, 'link_info', colors, color_all)
        self.save_linked_series(savedir, savename)

class InstanceTSLinkingWrapper(object):
    """A class that is a wrapper for InstanceTimeSeriesLinking
    Assumptions:
    1) The segmentation are saved in a different folder from original images
    2) The segmentation result and the original images have corresponding image names, which include "date-time" part with a specific pattern
    the date-time pattern for names of original images and names of segmentation results are the same
    3) For every image, there is a corresponding segmentation result
    Otherwise, please get your data prepared and use the "InstanceTimeSeriesLinking" class directly
    """
    def __init__(self, dir_save, savename):
        self.dir_save = dir_save
        self.savename = savename
        self.savename_ = '{}_old'.format(savename)
        self.dir_img = None
        self.dir_seg = None
        self.time_cond = None
        self.suffix    = None
        self.ext       = None
        self.suffix_seg = None
        self.timepoints = []
        self.imgfiles = []
        self.segfiles = []
        self.dir_visual = None
        self.dir_visual_ = None

    def set_save_dirs(self):
        junk = datetime.datetime.now()
        subfolder = '{}-{}-{}-{}-{}'.format(junk.year, str(junk.month).zfill(2), str(junk.day).zfill(2),
                                            str(junk.hour).zfill(2), str(junk.minute).zfill(2), str(junk.second).zfill(2))
        self.dir_save = os.path.join(self.dir_save, subfolder)
        if not os.path.exists(self.dir_save):
            os.makedirs(self.dir_save)
        self.dir_visual = os.path.join(self.dir_save, 'visualization')
        if not os.path.exists(self.dir_visual):
            os.makedirs(self.dir_visual)
        self.dir_visual_ = os.path.join(self.dir_save, 'visualization_old')
        if not os.path.exists(self.dir_visual_):
            os.makedirs(self.dir_visual_)

    def sort_time(self, dir_img, dir_seg, pattern_dt, time_cond, suffix='.jpg', suffix_seg='.pkl'):
        """
        This function is designed for files with file names which contain a "date-time" part, with an user-defined pattern
        sort time based on names of original images
        :param dir_img: directory of original images
        :param dir_seg: directory of segmentation results
        :param pattern_dt: the common pattern of date-time part in file names, e.g. YYYY-MM-DD-hh-mm
        :param time_cond: the date time of data intended to be included in the analysis
        :param suffix: the common suffix of all original image files
        :param suffix_seg: the common suffix of all segmentation result files
        :return: sorted and trimed list of images as well as segmentation files
        """
        self.dir_img = dir_img
        self.dir_seg = dir_seg
        self.time_cond  = time_cond
        self.suffix     = suffix
        self.suffix_seg = suffix_seg

        # file name extension of original images
        ext1, ext2 = os.path.splitext(self.suffix)
        if ext1.startswith('.'):
            self.ext = ext1
        elif ext2.startswith('.'):
            self.ext = ext2

        imgfs_all = [f for f in os.listdir(self.dir_img) if f.endswith(self.suffix)]
        segfs_all = [f for f in os.listdir(self.dir_seg) if f.endswith(self.suffix_seg)]
        imgfs_all.sort()
        segfs_all.sort()
        for (fi, fs) in zip(imgfs_all, segfs_all):
            tempi = re.search(pattern_dt, fi)
            temps = re.search(pattern_dt, fs)
            if tempi and temps:
                timepart = tempi.group()  #timeparts = temps.group() the assumption is that original image and the results have the same dt_pattern
                for cond in self.time_cond:
                    if timepart.endswith(cond):
                        self.timepoints.append(timepart)
                        continue
        index_temp = np.argsort(self.timepoints)
        self.timepoints   = [self.timepoints[i] for i in index_temp]
        self.imgfiles = [imgfs_all[i] for i in index_temp]
        self.segfiles = [segfs_all[i] for i in index_temp]

    def load_images(self):
        """
        Get the list of images (nd-arrays) ready
        :return:
        """
        temp_imgs = []
        sz = []
        imgs = []
        for f in self.imgfiles:
            junk = skimage.io.imread(os.path.join(self.dir_img, f))
            temp_imgs.append(junk)
            sz.append(np.min(junk.shape[0:2]))
        min_dim = np.min(sz)
        for junk in temp_imgs:
            img = junk[0: min_dim, 0: min_dim, :]  # make all images the same size
            imgs.append(img)
        return imgs, min_dim

    def load_segs(self, min_dim):
        """
        Get the list of segmentation masks (nd-arrays) ready
        :param min_dim: minimum dimension of images (get from original images) (Assumption: square images)
        :return:
        """
        segs = []
        for f in self.segfiles:
            r = pkl.load(open(os.path.join(self.dir_seg, f), 'rb'))
            segs.append(r["masks"][0:min_dim, 0:min_dim, :])  # make all masks the same size
        return segs

    def __call__(self, dir_img, dir_seg, pattern_dt, time_cond, logic, thres, name_sub, suffix, suffix_seg,colors=None,color_all=None):
        self.set_save_dirs()
        self.sort_time(dir_img, dir_seg, pattern_dt, time_cond, suffix, suffix_seg)
        imgs,min_dim = self.load_images()
        segs = self.load_segs(min_dim)
        # create an instance of InstanceTimeSeriesLinkingClass
        inst_ts_linking = InstanceTimeSeriesLinking(imgs, segs, self.timepoints, logic, thres, name_sub)
        inst_ts_linking(self.dir_save, self.dir_visual_, self.dir_visual, self.savename_, self.savename, colors, color_all)
        return inst_ts_linking
