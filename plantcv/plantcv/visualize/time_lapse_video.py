# Create time-lapse videos with input directory of images

import os
import cv2
import numpy as np
import mimetypes
from plantcv.plantcv import params
from plantcv.plantcv import fatal_error
from plantcv.plantcv.transform import resize
# import warnings
from plantcv.plantcv import warn


def time_lapse_video(img_directory, list_img=None, auto_sort=True, suffix_img=None, size_frame=None, fps=29.97,
                     name_video='time_lapse_video', path_video=None, display='on'):
    """ Generate time-lapse video given a folder of images
    Inputs:
    img_directory  = the directory of folder of images to make the time-lapse video.
    list_img       = the desired list of images in img_directory to create the video.
            If None is passed, all images would be included by default.
    auto_sort      = whether to automatically sort the list of images.
                    Sometimes if the user provided the list of images, they don't want it to be alphabetically sorted
    suffix_img     = common suffix of all image files, can be more than extension
    size_frame     = the desired size of every frame.
            In a video, every frame should have the same size.
            The assumption is that all images given should have same size. However, in some cases, the sizes of images are
            slightly differ from each other.
            If the frame size is given, if an image is larger than the given size, the image would be cropped automatically;
            if an image is smaller than the given size, the image would be zero-padded automatically
            If the frame size is not given, the largest size of all images would be used as the frame size.
    fps            = (frames per second) frame rate.
            Commonly used values: 23.98, 24, 25, 29.97, 30, 50, 59.94, 60
    name_video     = desired saving name for the generated video
    path_video     = the desired saving path of output video. If not given, the video would be saved
            in the same directory of the images.
    display        = indicator of whether to display current status (by displaying saving directory and saving name)
            while running this function
    Outputs:
    list_img       = the list of images used to generate the video
    size_frame     = the frame size of the generated video

    :param img_directory: string
    :param list_img: list
    :param auto_sort: boolean
    :param suffix_img: string
    :param size_frame: tuple
    :param fps: float
    :param name_video: string
    :param path_video: string
    :param display: boolean
    :return list_img: list
    :return size_frame: tuple
    """

    ## Get the list of image files in the given directory and sort them alphabetically by their names
    temp_list = []
    for f in os.listdir(img_directory):
        type_f = mimetypes.guess_type(f)[0]
        if type_f:
            if type_f.startswith('image'):
                temp_list.append(f)
    if len(temp_list) <= 0:
        fatal_error("There is no file in the provided folder that is an image, please check the provided directory!")

    # get an "extension free" list of images
    temp_list_no_ext = [os.path.splitext(f)[0] if os.path.splitext(f)[1] else f for f in temp_list]

    ## if the list of images is provided, stick to it, but automatically handle the extension issue
    if list_img is not None:
        #  make the list of images extension free
        list_img_no_ext = [os.path.splitext(f)[0] if os.path.splitext(f)[1] else f for f in list_img]
        temp_set        = set(temp_list_no_ext)
        list_img_ = []
        # check if the images in the given list exist in the directory by comparing both lists
        # only include the images in the provided list who is also availabe in the given directory
        for (f,f_) in zip(list_img_no_ext,list_img):
            if f in temp_set:
                list_img_.append(f_)

        list_img = list_img_
        if len(list_img) == 0:
            fatal_error("The provided list of files is not contained in the given directory")
        elif len(list_img) < len(list_img_no_ext):
            # warnings.warn("Warning: Some files in the provided list not found, the video will be created based on "
            #               "available files in the provided directory!")
            warn("Some files in the provided list not found, the video will be created based on "
                          "available files in the provided directory!")

    # if the list of images is not provided, check if suffix information is available
    elif suffix_img is not None:
        list_img = [f for f in temp_list if f.endswith(suffix_img)]
        if len(list_img) == 0:
            fatal_error("There is no file that matches the provided suffix in the provided directory, please check again!")

    # neither the list of image nor the suffix is provided
    else:
        list_img = temp_list
    if auto_sort:
        list_img.sort()

    imgs   = []
    list_r = []
    list_c = []
    for file in list_img:
        img = cv2.imread(os.path.join(img_directory, file))
        list_r.append(img.shape[0])
        list_c.append(img.shape[1])
        imgs.append(img)
    max_c, max_r = np.max(list_c), np.max(list_r)

    # If the frame size is not provided, use the largest size of the images as the frame size
    size_frame = size_frame or (max_c, max_r)

    if not (len(np.unique(list_r)) == 1 and len(np.unique(list_c)) == 1):
        warn(f"The sizes of images are not the same, an image resizing (cropping or zero-padding) will be done "
                      "to make all images the same size ({size_frame[0]}x{size_frame[1])}) before creating the video! "
                      "If you assume the images should have the same size, please check the images used to generate this video!")

    # If the video saving directory is not provided, save it in the same directory of the images
    if path_video is None:
        path_video = img_directory

    # Full video save name
    save_name = os.path.join(path_video, name_video + '.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use lower case
    out = cv2.VideoWriter(save_name, fourcc, fps, size_frame)

    for img in imgs:
        out.write(resize(img, size_frame, interpolation=None))
    out.release()
    cv2.destroyAllWindows()
    if display == 'on':
        print(f'The generated video: \n{save_name},\nAnd is saved here:\n{path_video}.')

    return list_img, size_frame
