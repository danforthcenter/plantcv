import os
import pickle as pkl
import glob
import numpy as np
import cv2
import re
import skimage
import datetime
from plantcv.plantcv.time_series import time_series_linking, evaluation
import matplotlib.pyplot as plt
import pandas as pd

plant = "Bean"
path_img_ = "/shares/bioinformatics/nfahlgren/projects/mrcnn/old/training_data_downloads/MSU/Dataset/Images"
path_gt_ = "/shares/mgehan_share/hsheng/projects/synthetic_data_MSU/label"
ext_img = "rgb.png"
ext_seg = "mask.pkl"
pattern_datetime = "day_.+_hour_.+_"

metric = "IOU"
thres = 0.05

path_save_ = path_gt_.replace("label", "time_series_linking")
junk = datetime.datetime.now()
subfolder = "{}-{}_{}-{}-{}-{}-{}".format(metric, thres, junk.year, str(junk.month).zfill(2), str(junk.day).zfill(2),
                                          str(junk.hour).zfill(2), str(junk.minute).zfill(2), str(junk.second).zfill(2))
path_save = os.path.join(path_save_, plant, subfolder)
if not os.path.exists(path_save):
    os.makedirs(path_save)

df_results = pd.DataFrame(
    columns=["Plant-ID", "num_leaves_gt", "num_leaves", "link_score", "track_score", "unmatched_rate", "fake_new_rate"])

for idx_p in range(1, 17):
    path_img = f"{path_img_}/{plant}/plant_{idx_p}"
    path_gt = path_img.replace(path_img_, path_gt_)
    path_seg = os.path.join(path_gt, "masks")

    # Get timepoints from available segmentation results
    list_seg = glob.glob(os.path.join(path_seg, "*{}".format(ext_seg)))

    # sort timepoints
    timepoints = []
    for f_seg in list_seg:
        tp_temp = re.search(pattern_datetime, f_seg).group()
        timepoints.append(tp_temp)
    timepoints.sort()

    # load images
    temp_imgs = []
    sz = []
    imgs = []
    for tp in timepoints:
        filename_ = "*{}{}".format(tp, ext_img)
        if "_09" in filename_:
            filename_ = filename_.replace("09", "9")
        filename = glob.glob(os.path.join(path_img, filename_))[0]
        junk = skimage.io.imread(os.path.join(path_img, filename))
        if len(junk.shape) == 2:
            junk = cv2.cvtColor(junk, cv2.COLOR_GRAY2BGR)
        temp_imgs.append(junk)
        sz.append(np.min(junk.shape[0:2]))
    min_dim = np.min(sz)
    for junk in temp_imgs:
        img = junk[0:min_dim, 0:min_dim, :]  # make all images the same size (if not the same size)
        imgs.append(img)

    # load instance segmentation results
    masks = []
    for tp in timepoints:
        filename_ = "*{}{}".format(tp, ext_seg)
        filename = glob.glob(os.path.join(path_seg, filename_))[0]
        r = pkl.load(open(filename, 'rb'))
        masks.append(r['masks'][0: min_dim, 0:min_dim, :])  # make all masks the same size (if not already)

    inst_ts_linking = time_series_linking.InstanceTimeSeriesLinking()

    inst_ts_linking.images = imgs
    inst_ts_linking.masks = masks
    inst_ts_linking.timepoints = timepoints
    inst_ts_linking.T = len(inst_ts_linking.timepoints)
    # inst_ts_linking.name_sub = name_sub
    # inst_ts_linking.key_id = '{}_ids'.format(name_sub)
    inst_ts_linking.link(masks, metric, thres)

    ## Leaf status report
    # extract timepoints
    tps_dd, tps_hh = [], []
    for tp in timepoints:
        temp = tp.split("_")
        idx_day = temp.index("day")
        idx_hour = temp.index("hour")
        dd = temp[idx_day + 1]
        hh = temp[idx_hour + 1]
        if hh.startswith("0"):
            hh = hh.replace("0", "")
        tps_dd.append(dd)
        tps_hh.append(hh)
    days = np.unique(tps_dd)
    locs = [tps_dd.index(d) for d in days]

    # plot leaf status report
    leaf_report = inst_ts_linking.leaf_status_report
    leaf_report[np.where(leaf_report == 0)] = np.nan
    fig, ax = plt.subplots(figsize=(10, 8))
    for uid in range(leaf_report.shape[1]):
        ax.plot(leaf_report[:, uid], ".-", label=f"leaf{uid}")
    ax.legend()
    ax.set_xlabel("Days", fontsize=15)
    ax.set_ylabel("Leaf Area", fontsize=15)
    ax.set_xticks(locs)
    ax.set_xticklabels(days, fontsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    plt.savefig(os.path.join(path_save, f"leaf_status_Plant{idx_p}.png"))
    plt.close("all")

    ## results evaluation
    # load ground truth
    loaded_gt = pkl.load(open(os.path.join(path_gt, "gt_link_info.pkl"), "rb"))
    li_gt = loaded_gt["link_info"]
    ti_gt = loaded_gt["ti"]
    score_link, num_insts, num_matched = evaluation.evaluate_link(inst_ts_linking.link_info, li_gt)
    r_unmatched, r_fake_new = evaluation.mismatch_rate(inst_ts_linking.ti, ti_gt)
    N, N_, confu, track_match, track_rate, score_track = evaluation.confusion(inst_ts_linking.ti, ti_gt)

    df_results = df_results.append({
        "Plant-ID": idx_p, "num_leaves_gt": N, "num_leaves": N_, "link_score": score_link, "track_score": score_track,
        "unmatched_rate": r_unmatched, "fake_new_rate": r_fake_new}, ignore_index=True)

df_results.to_csv(os.path.join(path_save, "summary.csv"), index=False)
