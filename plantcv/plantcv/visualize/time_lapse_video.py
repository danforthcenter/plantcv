# Color mask(s) in any color

import os
import cv2
import numpy as np
import copy
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
import warnings


def _resize_img(img, size):
    """Resize the image to the given new size
    If the given size is larger than the original image size, zero-pad the image.
    If the given size is smaller than the origina image size, crop the image (right & bottom).
    """

    # original image size
    r_ori, c_ori = np.shape(img)[0], np.shape(img)[1]
    r, c = size[0], size[1]

    if len(img.shape) > 2:
        b_ori = np.shape(img)[2]
        junk = copy.deepcopy(img)
    else:
        b_ori = 1
        junk = np.expand_dims(img, axis=2)

    # deal with rows
    img1 = copy.deepcopy(junk)
    if r < r_ori:
        img1 = junk[0:r, :, :]
    elif r > r_ori:
        img1 = np.zeros_like(junk, shape=[r, c_ori, b_ori])
        img1[0:r_ori, :, :] = junk

    # update
    r_ori, c_ori = np.shape(img1)[0], np.shape(img1)[1]
    img2 = copy.deepcopy(img1)

    # deal with columns
    if c < c_ori:
        img2 = img1[:, 0:c, :]
    elif c > c_ori:
        img2 = np.zeros_like(img1, shape=[r_ori, c, b_ori])
        img2[:, 0:c_ori, :] = img1

    if len(img.shape) == 2:
        output_img = np.squeeze(img2, axis=2)
    else:
        output_img = img2
    return output_img


def time_lapse_video(img_directory, list_img=None, suffix_img=None, size_frame=None, fps=29.97,
                     name_video='time_lapse_video', path_video=None, display='on'):
    """Generate time-lapse video given a folder of images
    Inputs:
        img_directory: the directory of folder of images to make the time-lapse video
        list_img: desired list of images in img_directory to create the video. If None is passed, all images would be included by default.
        suffix_img: the suffix of input images. e.g. suffix='.jpg' or suffix='.png' or suffix='img10.jpg'. Make sure all images have the same suffix
            note: If neigher list_img nor suffix_img is provided, all images in the directory will be included
        name_video: the prefix of output video name
        size_frame: the desired size of every frame.
            In a video, every frame should have the same size.
            The assumption is that all images given should have same size. However, in some cases, the sizes of images are slightly differ from each other.
            If the frame size is given, if an images is larger than the given size, the image would be cropped automatically; if an image is smaller than the given size, the image would be zero-padded automatically
            If the frame size is not given, the largest size of all images would be used as the frame size.
            The assumption is that If some videos are smaller,
        fps: (frames per second) frame rate
            Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60
        path_video: the desired saving path of output video. If not given, the video would be saved the the same directory of the images.
        display: indicator of whether to display current status (by displaying saving directory and saving name) while running this function
    No return value
        """
    ## Get the list of image files and sort them alphabetically by their names
    # make sure there is images inside the provided directory
    list_img_1 = [img for img in os.listdir(img_directory) if img.endswith('.jpg')]
    list_img_2 = [img for img in os.listdir(img_directory) if img.endswith('.png')]
    if len(list_img_1) == 0 and len(list_img_2) == 0:
        fatal_error("There is no file in the provided folder that is an image, please check the provided directory!")
    elif len(list_img_1) > 0:
        temp_list = list_img_1
    else:
        temp_list = list_img_2

    # if the list of images is provided, stick to it
    if list_img is not None:
        if not set(list_img) <= set(temp_list):
            # print(
            #     "Warning: Some files in the provided list not found, the video will be created based on available files in the provided directory!")
            warnings.warn("Warning: Some files in the provided list not found, the video will be created based on available files in the provided directory!")
            remove_list = [f for f in list_img if f not in (temp_list)]
            for f in remove_list:
                list_img.remove(f)
                # if a wrong list is proveded
                if len(list_img) == 0:
                    fatal_error("The provided list of files is not contained in the given directory")

    # if the list of images is not provided, check if suffix information is available
    elif suffix_img is not None:
        list_img = [f for f in temp_list if f.endswith(suffix_img)]
        if len(list_img) == 0:
            fatal_error("There is no file that matches the provided suffix, please check again!")
            # both are not provided
    else:
        list_img = temp_list
    list_img.sort()

    imgs = []
    max_r = 0
    max_c = 0
    for file in list_img:
        img = cv2.imread(os.path.join(img_directory, file))
        max_r = max(max_r, img.shape[0])
        max_c = max(max_c, img.shape[1])
        imgs.append(img)

    # If the frame size is not provided, use the largest size of the images as the frame size
    if size_frame is None:
        size_frame = (max_r, max_c)

    # If the video saving directory is not provided, save it in the same directory of the images
    if path_video is None:
        path_video = img_directory

    # Full video save name
    save_name = os.path.join(path_video, name_video + '.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(save_name, fourcc, fps, size_frame)
    for img in imgs:
        out.write(_resize_img(img, size_frame))

    out.release()
    cv2.destroyAllWindows()
    if display is 'on':
        print('The generated video: \n{},\nAnd is saved here:\n{}.'.format(save_name, path_video))
