import os
import re
import json
import glob
import pandas as pd
import itertools


# Parse dataset metadata
###########################################
def metadata_parser(config):
    """Parse image metadata from a dataset.

    Parameters
    ----------
    config : plantcv.parallel.WorkflowConfig
        Workflow configuration object.

    Returns
    -------
    pandas.core.groupby.generic.DataFrameGroupBy
        Grouped dataframe of image metadata.
    """
    # Read the input dataset to a dictionary
    dataset = _read_dataset(config=config)

    # Convert the dataset metadata to a dataframe
    meta = _dataset2dataframe(dataset=dataset, config=config)

    # Split file paths into metadata terms 0:N-1
    meta = _parse_filepath(df=meta, config=config)

    # Apply user-supplied metadata filters
    meta, removed_df = _apply_metadata_filters(df=meta, config=config)

    # Apply user-supplied date range filters
    meta, removed_df = _apply_date_range_filter(df=meta, config=config, removed_df=removed_df)

    # Apply metadata grouping
    meta = _group_metadata(df=meta, config=config)

    return meta, removed_df
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
        "filepath": [],
        "n_metadata_terms": []
    }
    # Populate metadata terms from the standard metadata vocabulary
    for term in config.metadata_terms:
        metadata[term] = []
    # Iterate over all image metadata and append metadata values to the dictionary
    for image in dataset["images"]:
        metadata["filepath"].append(os.path.join(config.input_dir, image))
        metadata["n_metadata_terms"].append(dataset["images"][image].get("n_metadata_terms"))
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
    Parameters
    ----------
    df = pandas.core.frame.Dataframe, metadata dataframe
    config = plantcv.parallel.WorkflowConfig object

    Returns:
    --------
    filtered_df = pandas.core.frame.Dataframe, filtered metadata dataframe
    removed_df  = pandas.core.frame.Dataframe, metadata dataframe of what was removed
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
    # If there are no filters provide the metadata_filter dataframe will be empty and we can return the input datafram
    removed_df = pd.DataFrame()
    filtered_df = df
    if not metadata_filter.empty:
        filtered_df = df.merge(metadata_filter, how="inner")
        removed_df = _anti_join(df, filtered_df)
        removed_df["status"] = "Removed by config.metadata_filters"
        # if a row has None for all metadata then it was not able to be parsed due to variable length
        removed_df.loc[removed_df[list(config.metadata_filters.keys())].isnull().apply(all, axis=1),
                       'status'] = "Incorrect metadata length"
    if bool(config.metadata_regex):
        prev_df = filtered_df
        for key, value in config.metadata_regex.items():
            filtered_df = filtered_df[filtered_df[key].astype(str).str.contains(value, regex=True, na=False)]
        removed_df_2 = _anti_join(prev_df, filtered_df)
        removed_df_2["status"] = "Removed by config.metadata_regex"
        removed_df = pd.concat([removed_df, removed_df_2])
    return filtered_df, removed_df
###########################################


# Filter a metadata dataframe within a date range
###########################################
def _apply_date_range_filter(df, config, removed_df):
    """Filter metadata based on a date range.
    Parameters
    ----------
    df = pandas.core.frame.DataFrame, metadata dataframe
    config = plantcv.parallel.WorkflowConfig object
    removed_df = pandas.core.frame.DataFrame, dataframe of images removed up to this point

    Returns
    -------
    filtered_df = pandas.core.frame.DataFrame, filtered metadata dataframe
    removed_df = pandas.core.frame.DataFrame, dataframe of removed metadata
    """
    # Set whether the datetime code is in UTC or not
    utc = bool("Z" in config.timestampformat)

    # Include all by default
    after_start_date = pd.Series([True] * df.shape[0])
    before_end_date = pd.Series([True] * df.shape[0])

    # Make boolean vector for start and end date filtering if dates are not None
    if config.start_date is not None:
        after_start_date = df["timestamp"] >= pd.to_datetime(config.start_date, format=config.timestampformat, utc=utc)
    if config.end_date is not None:
        before_end_date = df["timestamp"] <= pd.to_datetime(config.end_date, format=config.timestampformat, utc=utc)

    # And of boolean vectors
    keep_dates = after_start_date & before_end_date
    # Keep rows with dates between start and end date
    filtered_df = df.loc[keep_dates]
    not_between_df = _anti_join(df, filtered_df)
    not_between_df["status"] = "Removed by config.start_date and config.end_date"
    removed_df = pd.concat([removed_df, not_between_df])

    return filtered_df, removed_df
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

    Parameters
    ----------
    config = plantcv.parallel.WorkflowConfig object

    Return
    ------
    metadata_index = dict, metadata terms and positions
    config = plantcv.parallel.WorkflowConfig object
    """
    # if filename_metadata is not specified then estimate it
    if not bool(config.filename_metadata):
        print("Warning: Creating config.filename_metadata based on file names.")
        config = _estimate_filename_metadata(config)

    # A dictionary of metadata terms and their index position in the filename metadata term list
    metadata_index = {}
    # Enumerate the terms listed in the user configuration
    for i, term in enumerate(config.filename_metadata):
        # Store the term and the listed order
        metadata_index[term] = i

    return metadata_index, config
###########################################


# Filename metadata parser
###########################################
def _parse_filename(filename, config, metadata_index):
    """Parse metadata from a filename.

    Parameters
    ----------
    filename = str, Filename to parse metadata from
    config = plantcv.parallel.WorkflowConfig object
    metadata_index = dict, dictionary of metadata terms and positions

    Returns
    -------
    img_meta = dict, dictionary of image metadata keys and valaues
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
    # if all metadata terms start with "metadata_" then they are blank defaults and
    # we will include all pieces of the filepath.
    dummy_metadata = all(term.startswith("metadata_") for term in config.filename_metadata)
    if len(meta_list) == len(config.filename_metadata) or dummy_metadata:
        # For each of the type of metadata PlantCV keeps track of
        for i, term in enumerate(config.metadata_terms):
            # First store the default value for each term
            img_meta[term] = config.metadata_terms[term]["value"]
            # If the same metadata is found in the image filename, store the value
            if term in metadata_index:
                mi_term = metadata_index[term]
                img_meta[term] = None
                if i <= len(meta_list) - 1:
                    img_meta[term] = meta_list[mi_term]
    img_meta["n_metadata_terms"] = len(meta_list)
    return img_meta
###########################################


# Parses file paths into metadata columns
###########################################
def _parse_filepath(df, config):
    """Parse metadata from a filename.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe of image metadata.
    config : plantcv.parallel.WorkflowConfig
        PlantCV parallel configureation object.

    Returns
    -------
    pandas.DataFrame
        Dataframe with added filepath metadata columns.
    """
    # remove extraneous config.input_dir from file path
    paths_after_input = df["filepath"].map(lambda st: os.path.relpath(st, config.input_dir))
    path_metadata = []
    for i, fp in enumerate(paths_after_input):
        # for every file path, split it and add the elements to a list
        splits = fp.split(os.sep)
        path_metadata.append(splits[1:])
    # bind list into a dataframe
    path_metadata_df = pd.DataFrame(path_metadata)
    # rename columns to filepath1:N, basename
    path_metadata_df.columns = ["filepath"+str(i + 1) for i in range(len(path_metadata_df.columns))]
    if not path_metadata_df.empty:
        path_metadata_df.rename(columns={path_metadata_df.columns[-1]: "basename"}, inplace=True)
    # bind new columns onto existing metadata
    meta2 = df.reset_index(drop=True).join(path_metadata_df)
    return meta2
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
    metadata_index, config = _filename_metadata_index(config=config)
    # if imgformat is all then set to png for legacy
    extension = config.imgformat
    if config.imgformat == "all":
        extension = "png"
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
                filename = f"{img}.{extension}"
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
    # make imgformat a list if multiple
    extensions = config.imgformat
    if isinstance(config.imgformat, str):
        extensions = _replace_string_extension(config.imgformat)
    # Get a list of all files
    if config.include_all_subdirs is False:
        # If subdirectories are excluded, use glob to get a list of all image files
        fns = [f for ext in extensions for f in glob.glob(os.path.join(config.input_dir, "*[.]" + ext))]
    else:
        # If subdirectories are included, recursively walk through the path
        fns = []
        for root, _, files in os.walk(config.input_dir):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    # Keep the files that end with the image extension
                    fns.append(os.path.join(root, file))
    # Create a dataset
    dataset = _init_dataset()
    # Name the experiment with the input directory
    dataset["dataset"]["experiment"] = config.input_dir
    # Index filename metadata based on user-supplied parsing parameters
    metadata_index, config = _filename_metadata_index(config=config)
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


def _anti_join(df1, df2=None):
    """Anti join function for pandas dataframes
    Parameters
    ----------
    df1      = pandas.core.frame.Dataframe, dataframe of metadata
    df2      = pandas.core.frame.Dataframe, dataframe of filtered metadata

    Returns
    -------
    anti_joined = pandas.core.frame.Dataframe, metadata dataframe of what was removed
    """
    outer = df1.merge(df2, how='outer', indicator=True)
    anti_joined = outer[(outer['_merge'] == 'left_only')].drop('_merge', axis=1)
    return anti_joined
###########################################


# Reads filename-based datasets
###########################################

def _estimate_filename_metadata(config):
    """Estimate filename_metadata if it is missing
    Parameters
    ----------
    config = plantcv.parallel.WorkflowConfig object

    Returns
    -------
    config = plantcv.parallel.WorkflowConfig object with filename_metadata added
    """
    metadata_lengths = [1]
    imgformats = tuple(_replace_string_extension(config.imgformat))
    fns = []
    if config.include_all_subdirs is False:
        # If subdirectories are excluded, use glob to get a list of all image files
        for ext in imgformats:
            extfns = list(glob.glob(pathname=os.path.join(config.input_dir, f'*{ext}')))
            extfns = [os.path.basename(f) for f in extfns]
            fns.extend(extfns)
    else:
        fns = []
        for _, _, files in os.walk(config.input_dir):
            for file in files:
                if file.endswith(imgformats):
                    fns.append(file)
    # check length of metadata from all files, take the max, use those default terms.
    for file in fns:
        # get length of split filename
        metadata_lengths.append(len(file.split(config.delimiter)))
    config.filename_metadata = ["metadata_" + str(i) for i in range(max(metadata_lengths))]
    # if we had to make default metadata terms then add them to config.metadata_terms
    for term in config.filename_metadata:
        config.metadata_terms[term] = {
                "label": f"{term}",
                "datatype": "<class 'str'>",
                "value": "none"
            }

    return config
###########################################


def _replace_string_extension(imgformat):
    """Replace "all" with a list of file extensions.

    Parameters
    ----------
    imgformat : str
        The image format string, typically from a plantcv.parallel.WorkflowConfig object.

    Returns
    -------
    extensions : list of str
        A list of file extensions. If `imgformat` is "all", returns a list of common image file extensions;
        otherwise, returns a list containing only `imgformat`.
    """
    extensions = [imgformat]
    if imgformat == "all":
        extensions = ['bmp', 'dib', 'jpeg', 'jpg', 'jpe', 'jp2', 'png', 'ppm', 'pgm', 'ppm', 'sr', 'ras', 'tiff', 'tif']
    return extensions
###########################################
