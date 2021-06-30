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
        now = datetime.datetime.now()
        # now() maybe be before time of images if timestampformat is subdaily 
        # if timestampformat is only hours,min,sec then the strptime will use year 1900
        if now > datetime.datetime.strptime(end_date, config.timestampformat):
            nextyear = (now+datetime.timedelta(days=366)).year
            end_date = datetime.datetime(nextyear,12,31,23,59,59).strftime(config.timestampformat)

    start_date_unixtime = convert_datetime_to_unixtime(timestamp_str=start_date, date_format=config.timestampformat)
    end_date_unixtime = convert_datetime_to_unixtime(timestamp_str=end_date, date_format=config.timestampformat)

    # Metadata data structure
    meta = {}

    # A dictionary of metadata terms and their index position in the filename metadata term list
    metadata_index = {}
    for i, term in enumerate(config.filename_metadata):
        metadata_index[term] = i

    # How many metadata terms are in the files we intend to process?
    meta_count = len(config.filename_metadata)

    # Compile regex (even if it's only a delimiter character)
    regex = re.compile(config.delimiter)

    # Check whether there is a snapshot metadata file or not
    if os.path.exists(os.path.join(config.input_dir, "SnapshotInfo.csv")):
        # Open the SnapshotInfo.csv file
        csvfile = open(os.path.join(config.input_dir, 'SnapshotInfo.csv'), 'r')

        # Read the first header line
        header = csvfile.readline()
        header = header.rstrip('\n')

        # Remove whitespace from the field names
        header = header.replace(" ", "")

        # Table column order
        cols = header.split(',')
        colnames = {}
        for i, col in enumerate(cols):
            colnames[col] = i

        # Read through the CSV file
        for row in csvfile:
            row = row.rstrip('\n')
            data = row.split(',')
            img_list_str = data[colnames['tiles']]
            if img_list_str[:-1] == ';':
                img_list_str = img_list_str[:-1]
            img_list = img_list_str.split(';')
            for img in img_list:
                if len(img) != 0:
                    dirpath = os.path.join(config.input_dir, 'snapshot' + data[colnames['id']])
                    filename = img + '.' + config.imgformat
                    if not os.path.exists(os.path.join(dirpath, filename)):
                        print(f"Something is wrong, file {dirpath}/{filename} does not exist", file=sys.stderr)
                        continue
                        # raise IOError("Something is wrong, file {0}/{1} does not exist".format(dirpath, filename))
                    # Metadata from image file name
                    metadata = _parse_filename(filename=img, delimiter=config.delimiter, regex=regex)
                    # Not all images in a directory may have the same metadata structure only keep those that do
                    if len(metadata) == meta_count:
                        # Image metadata
                        img_path = os.path.join(dirpath, filename)
                        img_meta = {'path': img_path}
                        img_pass = 1
                        coimg_store = 0
                        # For each of the type of metadata PlantCV keeps track of
                        for term in config.metadata_terms:
                            # If the same metadata is found in the image filename, store the value
                            if term in metadata_index:
                                meta_value = metadata[metadata_index[term]]
                                # If the metadata type has a user-provided restriction
                                if term in config.metadata_filters:
                                    # If the input value does not match the image value, fail the image
                                    img_pass = _metdata_filter(img_metadata=meta_value,
                                                               filters=config.metadata_filters[term],
                                                               img_pass=img_pass)
                                img_meta[term] = meta_value
                            # If the same metadata is found in the CSV file, store the value
                            elif term in colnames:
                                meta_value = data[colnames[term]]
                                # If the metadata type has a user-provided restriction
                                if term in config.metadata_filters:
                                    # If the input value does not match the image value, fail the image
                                    img_pass = _metdata_filter(img_metadata=meta_value,
                                                               filters=config.metadata_filters[term],
                                                               img_pass=img_pass)
                                img_meta[term] = meta_value
                            # Or use the default value
                            else:
                                img_meta[term] = config.metadata_terms[term]["value"]

                        if img_meta['timestamp'] is not None:
                            in_date_range = check_date_range(start_date_unixtime, end_date_unixtime,
                                                             img_meta['timestamp'], config.timestampformat)
                            if in_date_range is False:
                                img_pass = 0

                        if config.coprocess is not None:
                            if img_meta['imgtype'] == config.coprocess:
                                coimg_store = 1

                        # If the image meets the user's criteria, store the metadata
                        if img_pass == 1:
                            # Link image to coprocessed image
                            coimg_pass = 0
                            if config.coprocess is not None:
                                for coimg in img_list:
                                    if len(coimg) != 0:
                                        meta_parts = _parse_filename(filename=coimg, delimiter=config.delimiter,
                                                                     regex=regex)
                                        if len(meta_parts) > 0:
                                            coimgtype = meta_parts[metadata_index['imgtype']]
                                            if coimgtype == config.coprocess:
                                                if 'camera' in config.filename_metadata:
                                                    cocamera = meta_parts[metadata_index['camera']]
                                                    if 'frame' in config.filename_metadata:
                                                        coframe = meta_parts[metadata_index['frame']]
                                                        if cocamera == img_meta['camera'] and coframe == img_meta['frame']:
                                                            img_meta['coimg'] = coimg + '.' + config.imgformat
                                                            coimg_pass = 1
                                                    else:
                                                        if cocamera == img_meta['camera']:
                                                            img_meta['coimg'] = coimg + '.' + config.imgformat
                                                            coimg_pass = 1
                                                else:
                                                    img_meta['coimg'] = coimg + '.' + config.imgformat
                                                    coimg_pass = 1
                                if coimg_pass == 0:
                                    print(f"Could not find an image to coprocess with {img_path}")
                            meta[filename] = img_meta
                        elif coimg_store == 1:
                            meta[filename] = img_meta
    else:
        # Compile regular expression to remove image file extensions
        pattern = re.escape('.') + config.imgformat + '$'
        ext = re.compile(pattern, re.IGNORECASE)

        # Prepare lists of paths and filenames of images by walking through the input directory and get only files
        # Initialize the dictionary with two keys: "dirpath" and "filename"
        paths_files = dict({'dirpath':[],'filename':[]})
        if config.include_all_subdirs is True:
            for (dirpath, dirnames, filenames) in os.walk(config.input_dir):
                for filename in filenames:
                    # Is it a file?
                    if os.path.isfile(os.path.join(dirpath, filename)):
                        paths_files['dirpath'].append(dirpath)
                        paths_files['filename'].append(filename)
        else:
            paths_files['filename'] = [f for f in os.listdir(config.input_dir) if os.path.isfile(os.path.join(config.input_dir,f))]
            paths_files['dirpath']  = [config.input_dir for i in paths_files['filename']]

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
                                img_pass = _metdata_filter(img_metadata=meta_value,
                                                           filters=config.metadata_filters[term],
                                                           img_pass=img_pass)
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


# Metadata filter
###########################################
def _metdata_filter(img_metadata, filters, img_pass):
    """Check if an image metadata value matches a filter value.

    Args:
        img_metadata: The metadata value for the given image
        filters:      The metadata filter values
        img_pass:     The current pass/fail state

    :param img_metadata: str
    :param filters: str or list
    :param img_pass: int
    :return img_pass: int
    """
    if isinstance(filters, list):
        # list of multiple filters
        if img_metadata not in filters:
            img_pass = 0
    else:
        # single filter as string
        if img_metadata != filters:
            img_pass = 0

    return img_pass
###########################################
