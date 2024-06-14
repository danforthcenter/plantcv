import os
import re
import json
import glob
import pandas as pd
import itertools


# Parse dataset metadata
###########################################
def metadata_parser(config):
    """Image metadata parser.

    Keyword arguments:
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    meta   = image metadata dataframe

    :param config: plantcv.parallel.WorkflowConfig
    :return meta: pandas.core.frame.DataFrame
    """
    # Read the input dataset
    dataset = _read_dataset(config=config)

    # Convert the dataset metadata to a dataframe
    meta = _dataset2dataframe(dataset=dataset, config=config)

    # Apply user-supplied metadata filters
    meta = _apply_metadata_filters(df=meta, config=config)

    # Apply user-supplied date range filters
    meta = _apply_date_range_filter(df=meta, config=config)

    # Apply metadata grouping
    meta = _group_metadata(df=meta, config=config)

    return meta
###########################################


# Parse dataset metadata
###########################################
def _read_dataset(config):
    """Read image datasets.

    Keyword arguments:
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    dataset = dataset metadata

    :param config: plantcv.parallel.WorkflowConfig
    :return dataset: dict
    """
    # Each dataset reader function outputs the dataset metadata in the same format
    # This makes the dataset compatible with the downstream steps
    # If you want to add a new dataset type, just add the logic here and create a new reader function

    # If the directory contains a metadata.json file it is a "phenodata" dataset
    if os.path.exists(os.path.join(config.input_dir, "metadata.json")):
        dataset = _read_phenodata(metadata_file=os.path.join(config.input_dir, "metadata.json"))
    # If the directory contains a SnapshotInfo.csv file it is a legacy "phenofront" dataset
    elif os.path.exists(os.path.join(config.input_dir, "SnapshotInfo.csv")):
        dataset = _read_phenofront(config=config, metadata_file=os.path.join(config.input_dir, "SnapshotInfo.csv"))
    # Otherwise we will extract metadata from filenames
    else:
        dataset = _read_filenames(config=config)
    return dataset
###########################################


# Convert a dataset dictionary to a DataFrame
###########################################
def _dataset2dataframe(dataset, config):
    """Convert a dataset to a dataframe.

    Keyword arguments:
    dataset = dataset metadata dictionary
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    df = dataset metadata dataframe

    :param dataset: dict
    :param config: plantcv.parallel.WorkflowConfig
    :return df: pandas.core.frame.DataFrame
    """
    # Build a metadata dictionary of lists of metadata values
    metadata = {
        "filepath": []
    }
    # Populate metadata terms from the standard metadata vocabulary
    for term in config.metadata_terms:
        metadata[term] = []
    # Iterate over all image metadata and append metadata values to the dictionary
    for image in dataset["images"]:
        metadata["filepath"].append(os.path.join(config.input_dir, image))
        for term in config.metadata_terms:
            metadata[term].append(dataset["images"][image].get(term))
    df = pd.DataFrame(data=metadata)
    utc = bool("Z" in config.timestampformat)
    df["timestamp"] = pd.to_datetime(df.timestamp, format=config.timestampformat, utc=utc)
    return df
###########################################


# Filter a metadata dataframe with user-supplied filters
###########################################
def _apply_metadata_filters(df, config):
    """Apply filters to metadata.

    Keyword arguments:
    df = metadata dataframe
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    filtered_df = filtered metadata dataframe

    :param df: pandas.core.frame.DataFrame
    :param config: plantcv.parallel.WorkflowConfig
    :return filtered_df: pandas.core.frame.DataFrame
    """
    # Convert all metadata filter values to a list type
    for term in config.metadata_filters:
        if not isinstance(config.metadata_filters[term], list):
            # Store term value as a list
            config.metadata_filters[term] = [config.metadata_filters[term]]
        # Convert filter values to strings
        config.metadata_filters[term] = list(map(str, config.metadata_filters[term]))
    # Create a metadata filter dataframe as the product of all combinations of values
    metadata_filter = pd.DataFrame(list(itertools.product(*config.metadata_filters.values())),
                                   columns=config.metadata_filters.keys(), dtype="object")
    # If there are no filters provide the metadata_filter dataframe will be empty and we can return the input dataframe
    if not metadata_filter.empty:
        filtered_df = df.merge(metadata_filter, how="inner")
        return filtered_df
    return df
###########################################


# Filter a metadata dataframe within a date range
###########################################
def _apply_date_range_filter(df, config):
    """Filter metadata based on a date range.

    Keyword arguments:
    df = metadata dataframe
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    filtered_df = filtered metadata dataframe

    :param df: pandas.core.frame.DataFrame
    :param config: plantcv.parallel.WorkflowConfig
    :return filtered_df: pandas.core.frame.DataFrame
    """
    # If either the start or end date is None then do not filter
    if None in [config.start_date, config.end_date]:
        return df
    # Set whether the datetime code is in UTC or not
    utc = bool("Z" in config.timestampformat)
    # Convert start and end dates to datetimes
    start_date = pd.to_datetime(config.start_date, format=config.timestampformat, utc=utc)
    end_date = pd.to_datetime(config.end_date, format=config.timestampformat, utc=utc)
    # Keep rows with dates between start and end date
    filtered_df = df.loc[df["timestamp"].between(start_date, end_date, inclusive="both")]
    return filtered_df
###########################################


# Group metadata dataframe into sets
###########################################
def _group_metadata(df, config):
    """Group metadata.

    Keyword arguments:
    df = metadata dataframe
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    groups = grouped metadata

    :param df: pandas.core.frame.DataFrame
    :param config: plantcv.parallel.WorkflowConfig
    :return groups: pandas.core.groupby.generic.DataFrameGroupBy
    """
    groups = df.groupby(by=config.groupby)
    return groups
###########################################


# Initialize a dataset dictionary
###########################################
def _init_dataset():
    """Initialize a dataset."""
    dataset = {
        "dataset": {
            "experiment": ""
        },
        "environment": {},
        "images": {}
    }
    return dataset
###########################################


# Index positional filename metadata
###########################################
def _filename_metadata_index(config):
    """Index positional filename metadata.

    Keyword arguments:
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    metadata_index = dictionary of metadata terms and positions

    :param config: plantcv.parallel.WorkflowConfig
    :return metadata_index: dict
    """
    # A dictionary of metadata terms and their index position in the filename metadata term list
    metadata_index = {}
    # Enumerate the terms listed in the user configuration
    for i, term in enumerate(config.filename_metadata):
        # Store the term and the listed order
        metadata_index[term] = i
    return metadata_index
###########################################


# Filename metadata parser
###########################################
def _parse_filename(filename, config, metadata_index):
    """Parse metadata from a filename.

    Keyword arguments:
    filename = Filename to parse metadata from
    config = plantcv.parallel.WorkflowConfig object
    metadata_index = dictionary of metadata terms and positions

    Outputs:
    img_meta = dictionary of image metadata keys and valaues

    :param filename: str
    :param config: plantcv.parallel.WorkflowConfig
    :return metadata_index: dict
    :return img_meta: dict
    """
    # Image metadata
    img_meta = {}
    meta_list = []
    # Split the filename on delimiter if it is a single character
    if len(config.delimiter) == 1:
        meta_list = filename.split(config.delimiter)
    # Otherwise use a regular expression to parse metadata terms
    else:
        # Search using the supplied regular expression
        meta_list = re.search(config.delimiter, filename)
        # If there is a match convert the collected matches to a list
        if meta_list is not None:
            meta_list = list(meta_list.groups())
        # If thre is no match meta_list will be None, make an empty list
        else:
            meta_list = []
    if len(meta_list) == len(config.filename_metadata):
        # For each of the type of metadata PlantCV keeps track of
        for term in config.metadata_terms:
            # First store the default value for each term
            img_meta[term] = config.metadata_terms[term]["value"]
            # If the same metadata is found in the image filename, store the value
            if term in metadata_index:
                img_meta[term] = meta_list[metadata_index[term]]
    return img_meta
###########################################


# Reads "phenodata" datasets
###########################################
def _read_phenodata(metadata_file):
    """Read a phenodata metadata file.

    Keyword arguments:
    metadata_file = phenodata metadata.json file

    Outputs:
    dataset = dataset metadata

    :param metadata_file: str
    :return dataset: dict
    """
    # Reads metadata.json file from our LemnaTec database export tool
    # For phenodata datasets, all metadata is already parsed and stored in a JSON file
    with open(metadata_file, "r") as fp:
        dataset = json.load(fp)
        return dataset
###########################################


# Reads "phenofront" datasets
###########################################
def _read_phenofront(config, metadata_file):
    """Read phenofront metadata.

    Keyword arguments:
    config = plantcv.parallel.WorkflowConfig object
    metadata_file = phenofront SnapshotInfo.csv file

    Outputs:
    dataset = dataset metadata

    :param config: plantcv.parallel.WorkflowConfig
    :param metadata_file: str
    :return dataset: dict
    """
    # Create a dataset
    dataset = _init_dataset()
    # Index filename metadata based on user-supplied parsing parameters
    metadata_index = _filename_metadata_index(config=config)
    # Open the SnapshotInfo.csv file
    with open(metadata_file, 'r') as fp:
        # Read the first header line
        header = fp.readline()
        header = header.rstrip('\n')

        # Remove whitespace from the field names
        header = header.replace(" ", "")

        # Table column order
        cols = header.split(',')
        colnames = {}
        for i, col in enumerate(cols):
            colnames[col] = i

        # Read through the CSV file, each row is a snapshot
        for snapshot in fp:
            # Remove the line return
            snapshot = snapshot.rstrip('\n')
            # Split the snapshot metadata on commas
            snapshot_meta = snapshot.split(',')
            # Create the snapshot ID
            snapshot_id = f"snapshot{snapshot_meta[colnames['id']]}"
            # Store the snapshot metadata in the dataset dictionary
            dataset["environment"][snapshot_id] = {
                "barcode": snapshot_meta[colnames["plantbarcode"]],
                "cartag": snapshot_meta[colnames["cartag"]],
                "timestamp": snapshot_meta[colnames["timestamp"]],
                "weight_before": snapshot_meta[colnames["weightbefore"]],
                "weight_after": snapshot_meta[colnames["weightafter"]],
                "water_amount": snapshot_meta[colnames["wateramount"]],
                "completed": snapshot_meta[colnames["completed"]]
            }
            # Store the experiment name
            dataset["dataset"]["experiment"] = snapshot_meta[colnames["experiment"]]
            # Image names are stored in the tiles column
            img_list_str = snapshot_meta[colnames["tiles"]]
            # The tiles column can have a trailing semicolon
            img_list_str = img_list_str[:-1] if len(img_list_str) > 0 and img_list_str[-1] == ";" else img_list_str
            # Create a list of files by splitting on semicolon
            img_list = img_list_str.split(';')
            # Iterate over each image and store the metadata
            for img in img_list:
                # Parse camera label metaata
                img_meta = _parse_filename(filename=img, config=config, metadata_index=metadata_index)
                # Construct the filename
                filename = f"{img}.{config.imgformat}"
                # The dataset key is the dataset relative path to the image
                rel_path = os.path.join(snapshot_id, filename)
                # Store the parsed image metadata
                dataset["images"][rel_path] = img_meta
                # Update the metadata with metaata from SnapshotInfo.csv
                dataset["images"][rel_path].update({
                    "snapshot": snapshot_id,
                    "barcode": snapshot_meta[colnames["plantbarcode"]],
                    "cartag": snapshot_meta[colnames["cartag"]],
                    "timestamp": snapshot_meta[colnames["timestamp"]],
                    "camera_label": img
                })
    return dataset
###########################################


# Reads filename-based datasets
###########################################
def _read_filenames(config):
    """Read metadata from filenames.

    Keyword arguments:
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    dataset = dataset metadata

    :param config: plantcv.parallel.WorkflowConfig
    :return dataset: dict
    """
    # Get a list of all files
    if config.include_all_subdirs is False:
        # If subdirectories are excluded, use glob to get a list of all image files
        fns = list(glob.glob(pathname=os.path.join(config.input_dir, f'*{config.imgformat}')))
    else:
        # If subdirectories are included, recursively walk through the path
        fns = []
        for root, _, files in os.walk(config.input_dir):
            for file in files:
                if file.endswith(config.imgformat):
                    # Keep the files that end with the image extension
                    fns.append(os.path.join(root, file))
    # Create a dataset
    dataset = _init_dataset()
    # Name the experiment with the input directory
    dataset["dataset"]["experiment"] = config.input_dir
    # Index filename metadata based on user-supplied parsing parameters
    metadata_index = _filename_metadata_index(config=config)
    for filepath in fns:
        # Get the image dataset-relative path to use as the dataset key
        rel_path = os.path.relpath(filepath, start=config.input_dir)
        # Pull off the filename
        filename = os.path.basename(filepath)
        # Remove the extension
        metadata, _ = os.path.splitext(filename)
        # Store the image filename metadata
        dataset["images"][rel_path] = _parse_filename(filename=metadata, config=config, metadata_index=metadata_index)
    return dataset
###########################################
