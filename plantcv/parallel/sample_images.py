import os
import random
import shutil
import json
from plantcv.plantcv import fatal_error
from plantcv.parallel.workflowconfig import WorkflowConfig
from plantcv.parallel.parsers import metadata_parser


def sample_images(source, dest_path="./sampled_images", num=100):
    """Gets a sample of images from the source directory and copies them to the destination directory.

    Parameters
    ----------
    source : str or WorkflowConfig object
        The directory containing the images to be sampled or a configuration file
    dest_path : str
        The directory where the sampled images will be copied
    num : int, optional
        The number of images to sample, by default 100

    Return
    ------
    None
    """
    if not os.path.exists(source):
        raise IOError(f"Directory does not exist: {source}")

    os.makedirs(dest_path, exist_ok=True)  # exist_ok argument does not exist in python 2

    # if source is a directory then read from it
    if os.path.isdir(source):
        _sample_from_directory(source, dest_path, num)
        return None
    # if source is a file, read that as a WorkflowConfig
    elif os.path.isfile(source):
        config = WorkflowConfig()
        config.import_config(source)
        source = config
    # `source` at this point should be a WorkflowConfig
    _sample_from_config(source, dest_path, num)


def _sample_from_config(config, dest_path, num):
    """Sample from images that a parallel configuration will use

    Parameters
    ----------
    source      = plantcv.parallel.WorkflowConfig, configuration file for parallel workflow
    dest_path   = str, Path to save sampled images.
    num         = int, Number of images to sample.

    Returns
    -------
    None
    """
    meta, _ = metadata_parser(config)
    # need a helper to read meta and copy `num` of those files
    # will run metadata_parser on a config and prototype an image copying function, probably basically the same as filename option below?
    sampled = meta.sample(n=num, axis=0)
    # I think this has filenames in it, need to make sure I know how to get those. I think image?
    for filepath in sampled["filepath"]:
        # recreate destination path so you can do filepath filtering
        dst = os.path.join(dest_path, os.path.relpath(filepath, start=config.input_dir))
        # make directories to mirror structure
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        # copy file to new outpath
        shutil.copy(filepath, dst)


def _sample_from_directory(source_path, dest_path, num):
    """Sample from various directory formats

    Parameters
    ----------
    source_path = str, Path to phenodata images.
    dest_path   = str, Path to save sampled images.
    num         = int, Number of images to sample.

    Returns
    -------
    None
    """
    if os.path.exists(os.path.join(source_path, 'SnapshotInfo.csv')):
        _sample_phenofront(source_path, dest_path, num)
    elif os.path.exists(os.path.join(source_path, 'metadata.json')):
        _sample_phenodata(source_path, dest_path, num)
    else:
        _sample_filenames(source_path, dest_path, num)


def _sample_phenofront(source_path, dest_path, num=100):
    """Sample images from a phenofront dataset.

    Parameters
    ----------
    source_path = str, Path to phenodata images.
    dest_path   = str, Path to save sampled images.
    num         = int, Number of images to sample.

    Returns
    -------
    None
    """
    line_array = []
    with open(os.path.join(source_path, 'SnapshotInfo.csv')) as fp:
        header = fp.readline()
        for line in fp:
            line = line.rstrip("\n")
            element_arr = line.split(',')
            if element_arr[-1]:
                line_array.append(element_arr)

    # Check to make sure number of imgs to select is less than number of images found
    if num > len(line_array):
        fatal_error(f"Number of snapshots found ({len(line_array)}) less than 'num'.")

    # Create SnapshotInfo file
    with open(os.path.join(dest_path, 'SnapshotInfo.csv'), 'w') as out_file:
        out_file.write(header)

        # Get random snapshots
        random_index = random.sample(range(0, len(line_array) - 1), num)
        for i in random_index:
            row = line_array[int(i)]
            out_file.write(','.join(row) + "\n")
            snap_path = os.path.join(source_path, "snapshot" + row[1])
            folder_path = os.path.join(dest_path, "snapshot" + row[1])
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)  # the beginning of folder_path (dest_path) already exists from above
            for root, _, files in os.walk(snap_path):
                for file in files:
                    shutil.copy(os.path.join(root, file), folder_path)


def _sample_filenames(source_path, dest_path, num=100):
    """Sample images from a generic dataset.

    Parameters
    ----------
    source_path = str, Path to phenodata images.
    dest_path   = str, Path to save sampled images.
    num         = int, Number of images to sample.

    Returns
    -------
    None
    """
    img_element_array = []
    img_extensions = ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'ppm',
                      'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']
    for root, _, files in os.walk(source_path):
        for file in files:
            # Check file type so that only images get copied over
            if file.lower().endswith(tuple(img_extensions)):
                img_element_array.append(os.path.join(root, file))

    # Check to make sure number of imgs to select is less than number of images found
    if num > len(img_element_array):
        print(f"Only {len(img_element_array)} images found, lowering 'num' to match.")
        num = len(img_element_array)

    # Get random images
    random_index = random.sample(range(0, len(img_element_array) - 1), num)
    # Copy images over to destination
    for i in random_index:
        shutil.copy(img_element_array[int(i)], dest_path)


def _sample_phenodata(source_path, dest_path, num=100):
    """Sample images from a phenodata dataset.

    Parameters
    ----------
    source_path = str, Path to phenodata images.
    dest_path   = str, Path to save sampled images.
    num         = int, Number of images to sample.

    Returns
    -------
    None
    """
    # Initialize an empty dataset
    sampled_dataset = {}
    # Read in the metadata
    with open(os.path.join(source_path, "metadata.json"), "r") as fp:
        dataset = json.load(fp)
    # Set the dataset to the sampled dataset
    sampled_dataset["dataset"] = dataset["dataset"]
    # Leave the environment secton empty
    sampled_dataset["environment"] = {}
    # Initialize the images section
    sampled_dataset["images"] = {}
    # Create a unique dictionary of snapshot IDs
    snapshots = {}
    # Store the snapshot IDs in the snapshots dictionary
    for value in dataset["images"].values():
        snapshots[value["snapshot"]] = True
    # Check to make sure number of imgs to select is less than number of images found
    if len(snapshots) < num:
        fatal_error(f"Number of snapshots found ({len(snapshots)}) less than 'num'.")
    # Randomly select the snapshots
    random_snapshots = random.sample(list(snapshots.keys()), num)
    # Iterate over all images in the dataset
    for fpath, meta in dataset["images"].items():
        # If the snapshot ID is in the random snapshots
        if meta["snapshot"] in random_snapshots:
            # Store the image in the sampled dataset
            sampled_dataset["images"][fpath] = meta
            # Copy the image to the destination directory
            parent_path = os.path.split(fpath)[0]
            os.makedirs(os.path.join(dest_path, parent_path), exist_ok=True)
            shutil.copy(os.path.join(source_path, fpath), os.path.join(dest_path, fpath))
    # Write the sampled dataset to a JSON file
    with open(os.path.join(dest_path, "metadata.json"), "w") as fp:
        json.dump(sampled_dataset, fp, indent=4)

