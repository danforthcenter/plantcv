#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 09:53:34 2020

Functions used in time series linking after getting leaf instance segmentation result (from maskRCNN)

@author: hudanyunsheng
"""

import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import pickle as pkl
import re
from plantcv import plantcv as pcv
import copy
from plantcv.plantcv.time_series import link_utilities as funcs
# import link_utilities as funcs

def time_series_linking(imagedir, segmentationdir, savedir, pattern_datetime, time_cond, link_logic=1,
                        class_names=['BG', 'Leaf'], mode='link', suffix='.jpg'):
    """
    Function used to get leaf instance growth information after segment leaf instances (using maskrcnn or other methods)
    Input:
        imagedir: directory of original image used
        segmentationdir: directory of leaf instance segmentation result
        savedir: desired saving directory of linking result
        time_cond: condition of data used, indicated by list of times, e.g. time_cond = ["08-05", "15-05"] represents for including data collected at 8:05am and 3:05pm everyday in this experiment
        link_logic: 1: IoU (intersection over union), 2: Io1A (intersection over 1st area), default value: 1
        class_names: used in bounding box visualization. By default there are background and leaf
        mode: either 'link' or 'load'. When creating a new linking, use in mode 'link', when trying to load from saved file, use in mode 'load'. By default the mode is 'link'.
    Output:
        An instance from "Plant" class would be returned, all the results will be saved in a folder with name of date and time when the function runs inside the user defined "savedir". Sample folder name: 2020-06-23-15-42 (a format of YYYY-MM-DD-HH-mm).
        1. colors.pkl: the colors (indicated by arrays) used in bounding box visualization. Without this predefined list of color, the assignment of color will be random. With this predefined color set, same color will represent for the same leaf all the time
        2. details.txt: the logic of linking as well as time condition will be shown, so that would be easier for users to check these parameters for the specific expreiment
        3. saved_plant.pkl: a "Plant" instance will be saved, with all the information included: time points, original images, instance segmentation masks, etc.
        4. a folder called "visualization", which contains 3 subfolders:
            1) a folder call "visualization 1", which contains 1st set of visualization
                In this set of visualization, the instance segmentation masks are applied to original images, so that there is only 1 leaf in every image.
                result name: {}_{}-{}-{}-{}_{}.png
                Naming convention for file names:
                    1st digit: unique identifier of the leaf
                    2nd digit: time of first emergence of the leaf
                    3rd digut: leaf index when it first emerges
                    4rd digit: current time point
                    5th digit: current leaf index
                    6th digit: original image name

            2) a folder called "visualization 2", which contains 2nd set of visualization
                This set of visualization show results with an alpha channel, such that we can see the main leaf in the original image, with other parts being half transparent
                There are several subfolders, the number of subfolders depends on the number of "new leaves" in total
                Every subfolder is a "new leaf", whose name is {}_{}-{}
                Naming convention for folder names:
                    1st digit: unique identifier of the leaf
                    2nd digit: time of first emergence of the leaf
                    3rd digut: leaf index when it first emerges
                Inside every folder, images of leaves with names same as original image names are contained.

            3) a folder called "visualization 3", which containes 3rd set of visualization
                This set of visualization show results with bounding boxes. In every image, different leaves are show in bounding boxes with different colors.
                Naming format: {}-visual.png
                The original image name is inside the {}.
    """
    if mode == 'link':
        # initialize Plant class
        Plant = funcs.PlantData(imagedir, segmentationdir, savedir, pattern_datetime, mode, suffix)

        Plant.getpath(Plant.imagedir)
        Plant.Sorttime(time_cond)
        Plant.load_images()

        # load mrcnn inferencing results
        Plant.load_results()

        Plant.getinitleaf()
        Plant.getmaxleaf()

        Plant.gettotaltime()
        Plant.getnumemergence()

        # plot the #leaves vs. time relationship
        plt.plot(np.array(range(0, len(Plant.num_leaves))), Plant.num_leaves)

        if not os.path.exists(os.path.join(Plant.savedir, 'details.txt')):
            file = open(os.path.join(Plant.savedir, 'details.txt'), 'w')
            if link_logic == 1:
                file.write('mode: IOU\n')
            else:
                file.write('mode: IOP\n')
            file.write('Directory of original images: {}\n'.format(Plant.imagedir))
            file.write('Directory of instance segmentation: {}\n'.format(Plant.segmentationdir))
            file.write('Image conditions: {}'.format(time_cond))
            file.close()

        print('start\n')
        print('...')

        # linking initialization
        Plant.initialize_linking()

        # link
        for t in range(0, Plant.total_time - 1):
            Plant.linking(t, mode=link_logic)
        Plant.get_series()

        ####### visualization #######
        # load original images
        if len(Plant.images) == 0:
            Plant.load_images()  # Plant.images

        # visualization method 1: show only one leaf per image
        path_visual1 = os.path.join(Plant.visualdir, 'visualization1')
        if not os.path.exists(path_visual1):
            os.makedirs(path_visual1)

        # visualization method 2: show with an alpha channel
        path_visual2 = os.path.join(Plant.visualdir, 'visualization2')
        if not os.path.exists(path_visual2):
            os.makedirs(path_visual2)

        # visualization method 3: show with bounding boxes
        path_visual3 = os.path.join(Plant.visualdir, 'visualization3')
        if not os.path.exists(path_visual3):
            os.makedirs(path_visual3)

        count = 0
        if not os.path.exists('{}/colors.pkl'.format(Plant.savedir)):
            colors = funcs._random_colors(40)
            pkl.dump(colors, open('{}/colors.pkl'.format(Plant.savedir), 'wb'))
        else:
            colors = pkl.load(open('{}/colors.pkl'.format(Plant.savedir), 'rb'))

        color_all = [[tuple() for i in range(0, num)] for num in Plant.num_leaves]
        for key_t in Plant.link_series:
            #
            ids = Plant.link_series[key_t]['unique_id']

            start_time = int(key_t.replace('t', ''))
            leaves_t = Plant.link_series[key_t]['new_leaf']
            for (unique_id, leaf) in zip(ids, leaves_t):
                key_leaf = 'leaf{}'.format(leaf)
                link_leaf = Plant.link_series[key_t][key_leaf]
                start_idx = link_leaf[start_time]
                for t in range(start_time, Plant.total_time):
                    img = Plant.images[t]
                    if link_leaf[t] >= 0:
                        color_all[t][link_leaf[t]] = colors[count]
                        mask_t = Plant.masks[t][:, :, link_leaf[t]]

                        ## 1. save the masked image, i.e. single leaves
                        mask = np.zeros(mask_t.shape, dtype=np.uint8)
                        mask[np.where(mask_t)] = 255
                        leaf_t = pcv.apply_mask(img, mask, mask_color='black')
                        pcv.print_image(leaf_t, os.path.join(path_visual1,
                                                             '{}_{}-{}-{}-{}_{}.png'.format(unique_id, start_time,
                                                                                            start_idx, t, link_leaf[t],
                                                                                            Plant.filename_pre[t],
                                                                                            Plant.ext)))
                        pcv.print_image(leaf_t, os.path.join(path_visual1,
                                                             '{}_{}-{}-{}-{}_{}{}'.format(unique_id, start_time,
                                                                                          start_idx, t, link_leaf[t],
                                                                                          Plant.filename_pre[t],
                                                                                          Plant.ext)))
                        # pkl.dump(leaf_t, open(os.path.join(path_visual1, '{}_{}_{}_{}_{}_{}.pkl'.format(unique_id, start_time, start_idx, t, link_leaf[t], Plant.filename_pre[t])), 'wb'))

                        ## 2. show result with an alpha channel
                        # update the mask where there is an alpha channel (alpha=0.5)
                        mask_ = np.ones(mask_t.shape) * 0.5
                        mask_[np.where(mask_t == True)] = 1
                        masked_im = np.concatenate((img.astype(float) / 255, np.expand_dims(mask_, axis=2)), axis=2)
                        save_dir_ = os.path.join(path_visual2, '{}_{}-{}'.format(unique_id, start_time, start_idx))
                        if not os.path.exists(save_dir_):
                            os.makedirs(save_dir_)
                        fig2 = plt.figure(figsize=(5, 5))
                        ax2 = fig2.add_subplot(1, 1, 1)
                        ax2.imshow(masked_im)
                        ax2.axis('off')
                        plt.savefig(os.path.join(save_dir_, str(Plant.filename_pre[t]) + Plant.ext))
                        plt.close(fig2)

                count += 1
        ## 3. visualize with bounding boxes
        for (img, mask, roi, class_id, score, color, t) in zip(Plant.images, Plant.masks, Plant.rois, Plant.class_ids,
                                                               Plant.scores, color_all, Plant.filename_pre):
            funcs.display_instances(img, roi, mask, class_id,
                                    class_names, score, ax=funcs.get_ax(rows=1, cols=1, size=16), show_bbox=True,
                                    show_mask=True,
                                    colors=color)
            plt.savefig(os.path.join(path_visual3, '{}-visual{}'.format(t, Plant.ext)))
            plt.close('all')

        # save all information
        pkl.dump(Plant, open(os.path.join(Plant.savedir, 'saved_plant.pkl'), 'wb'))

    else:
        # initialize Plant class
        Plant = funcs.PlantData(imagedir, segmentationdir, savedir, mode='load')
        # Load from existed PlantData instance
        Plant = pkl.load(open(os.path.join(Plant.savedir, 'saved_plant.pkl'), 'rb'))

    print('\nFinished!\nThe results are saved here:\n{}'.format(Plant.savedir))

    return Plant
