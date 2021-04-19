import os
import re
import sys
import datetime


# Parse metadata from filenames in a directory
###########################################
def metadata_parser(config):
    """Image metadata parser.

    Inputs:
    config = plantcv.parallel.WorkflowConfig object

    Outputs:
    meta   = image metadata dictionary

    :param config: plantcv.parallel.WorkflowConfig
    :return meta: dict
    """
    # Configured start and end datetime in Unix time
    start_date = config.start_date
    if start_date is None:
        start_date = datetime.datetime(1970, 1, 1, 0, 0, 1).strftime(config.timestampformat)
    end_date = config.end_date
    if end_date is None:
        end_date = datetime.datetime.now().strftime(config.timestampformat)

    start_date_unixtime = convert_datetime_to_unixtime(timestamp_str=start_date, date_format=config.timestampformat)
    end_date_unixtime = convert_datetime_to_unixtime(timestamp_str=end_date, date_format=config.timestampformat)

    # Metadata data structure
    image_filenames = find_images(config)
    all_image_meta = get_image_metadata(image_filenames, config)
    metadata_filter = pd.DataFrame(config.metadata_filters)
    # for single filter values for each key, one of the values must be a list length 1 otherwise you need to specify index for dataframe
    # to support multiple filter values per metadata term keys must be a list. repeated keys will lose the first identical key 
    # config.metadata_filters.values()
    
    
    # this should work ???!!
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html?highlight=isin#pandas.DataFrame.isin
    all_image_meta.isin(config.metadata_filters)

    # https://towardsdatascience.com/masteriadsf-246b4c16daaf#9c1c
    semi_table = all_image_meta.merge(metadata_filter, how='inner')
    in_both = all_image_meta.isin(semi_table[metadata_filter.columns])
    users_in_both = all_image_meta[in_both]
    # i don't think this works with multiple columns (or tables with different # rows?) because index AND columns must match for isin()


    if config.metadata_filters is None:
        filtered_image_meta = all_image_meta
    else:
        filtered_image_meta = all_image_meta.merge(metadata_filter, how='inner')
        # merge error if metadata_filters contains ONLY keys not pressent in columns of all_image_meta
        # merge succeeds but results in extra column if metadata_filters contains keys present and not present in columns of all_image_meta
        # we could further filter for filename_metadata but would give unexpected results: filtered_image_meta.filter(all_image_meta.columns)
        # do we check that config.filename_metadata contains config.metadata_filters?
        # do we check that timestamp is not in config.metadata_filters
        
    if 'timestamp' in config.filename_metadata:
        filtered_image_meta = filtered_image_meta.query('"timestamp" >= start_date and "timestamp" <= end_date')

    # add missing metadata fields from default metadata dict
    config2 = plantcv.parallel.WorkflowConfig()
    default_meta = pd.DataFrame(config2.metadata_terms).drop(['datatype','label'])
    image_meta_complete = filtered_image_meta.merge(default_meta, how='left')

    # meta dict
    meta = image_meta_complete.set_index('path').to_dict('index')

    
    # Walk through all files and find images that match input criteria
    for (dirpath, filename) in zip(paths_files['dirpath'], paths_files['filename']):
        # Is filename and image?
        is_img = ext.search(filename)
        # If filename is an image, parse the metadata
        if is_img is not None:
            # Remove the file extension
            prefix = ext.sub('', filename)
            metadata = _parse_filename(filename=prefix, delimiter=config.delimiter, regex=regex)

            # Not all images in a directory may have the same metadata structure only keep those that do
            if len(metadata) == meta_count:
                # Image metadata
                img_path = os.path.join(dirpath, filename)
                img_meta = {'path': img_path}
                img_pass = 1
                # For each of the type of metadata PlantCV keeps track of
                for term in config.metadata_terms:
                    # If the same metadata is found in the image filename, store the value
                    if term in metadata_index:
                        meta_value = metadata[metadata_index[term]]
                        # If the metadata type has a user-provided restriction
                        if term in config.metadata_filters:
                            # If the input value does not match the image value, fail the image
                            if meta_value != config.metadata_filters[term]:
                                img_pass = 0
                        img_meta[term] = meta_value
                    # Or use the default value
                    else:
                        img_meta[term] = config.metadata_terms[term]["value"]

                if img_meta['timestamp'] is not None:
                    in_date_range = check_date_range(start_date_unixtime, end_date_unixtime,
                                                        img_meta['timestamp'], config.timestampformat)
                    if in_date_range is False:
                        img_pass = 0

                # If the image meets the user's criteria, store the metadata
                if img_pass == 1:
                    meta[filename] = img_meta

    return meta
###########################################


# Check to see if the image was taken between a specified date range
###########################################
def check_date_range(start_date, end_date, img_time, date_format):
    """Check image time versus included date range.

    Args:
        start_date: Start date in Unix time
        end_date:   End date in Unix time
        img_time:   Image datetime
        date_format: date format code for strptime

    :param start_date: int
    :param end_date: int
    :param img_time: str
    :param date_format: str
    :return: bool
    """

    # Convert image datetime to unix time
    unix_time = convert_datetime_to_unixtime(timestamp_str=img_time, date_format=date_format)
    # Does the image date-time fall outside or inside the included range
    if unix_time < start_date or unix_time > end_date:
        return False
    else:
        return True
###########################################


# Convert datetime string to Unix time
###########################################
def convert_datetime_to_unixtime(timestamp_str, date_format):
    """Converts a timestamp string to a Unix time integer.

    Inputs:
    timestamp_str = a datetime string.
    date_format   = date format code for strptime

    Returns:
        unix_time = an integar value of seconds elapsed since epoch (1970-01-01 00:00:00)

    :param timestamp_str: str
    :param date_format: str
    :return unix_time: int
    """
    # Convert image datetime to unix time
    try:
        timestamp = datetime.datetime.strptime(timestamp_str, date_format)
    except ValueError as e:
        raise SystemExit(str(e) + '\n  --> Please specify the correct timestampformat parameter <--\n')

    time_delta = timestamp - datetime.datetime(1970, 1, 1)
    unix_time = (time_delta.days * 24 * 3600) + time_delta.seconds
    return unix_time


# Filename metadata parser
###########################################
def _parse_filename(filename, delimiter, regex):
    """Parse the input filename and return a list of metadata.

    Args:
        filename:   Filename to parse metadata from
        delimiter:  Delimiter character to split the filename on
        regex:      Compiled regular expression pattern to process file with

    :param filename: str
    :param delimiter: str
    :param regex: re.Pattern
    :return metadata: list
    """

    # Split the filename on delimiter if it is a single character
    if len(delimiter) == 1:
        metadata = filename.split(delimiter)
    else:
        metadata = re.search(regex, filename)
        if metadata is not None:
            metadata = list(metadata.groups())
        else:
            metadata = []
    return metadata
###########################################
