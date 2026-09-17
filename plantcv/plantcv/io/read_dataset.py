# Read dataset of images

import os
import re


def read_dataset(img_dir, pattern='', sort=True):
    """Read a dataset of images as a list of paths.

    Parameters:
    -----------
    img_dir  = str,
        Path to the directory containing the images
    pattern      = str,
        Optional, return only filenames containing the pattern
    sort         = boolean,
        True by default, sorts the paths alphabetically

    Returns:
    --------
    dataset = list,
        List of paths to the images in the source path
    """
    if not os.path.exists(img_dir):
        raise IOError(f"Directory does not exist: {img_dir}")

    img_path_list = []
    img_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif']

    for root, _, files in os.walk(img_dir):
        for file in files:
            # Look for images that contain [pattern] in the name
            if re.search(pattern, file):
                # Check file type so that only images get selected
                _, ext = os.path.splitext(file)
                if ext.lower() in img_extensions:
                    img_path_list.append(os.path.join(root, file))

    if sort is True:
        img_path_list = sorted(img_path_list)

    return img_path_list
