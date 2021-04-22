import os
import sys
import re
import datetime
import pandas as pd
import itertools
import glob

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
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0)
    else:
        start_date = datetime.datetime.strptime(
            start_date, config.timestampformat)
    end_date = config.end_date
    if end_date is None:
        end_date = datetime.datetime.now()
        datestr = end_date.strftime(config.timestampformat)
        # if timestampformat does not include year then the strptime will use year 1900.
        # we need to make sure a timestamp without year still is filtered correctly by end_date and start_date
        if datetime.datetime.strptime(datestr, config.timestampformat).year == 1900:
            nextyear = (end_date+datetime.timedelta(days=366)).year
            end_date = datetime.datetime(nextyear, 12, 31, 23, 59, 59)
    else:
        end_date = datetime.datetime.strptime(end_date, config.timestampformat)

    # Metadata data structure
    meta = {}

    # Check whether there is a snapshot metadata file or not
    if os.path.exists(os.path.join(config.input_dir, "SnapshotInfo.csv")):

        # A dictionary of metadata terms and their index position in the filename metadata term list
        metadata_index = {}
        for i, term in enumerate(config.filename_metadata):
            metadata_index[term] = i

        # How many metadata terms are in the files we intend to process?
        meta_count = len(config.filename_metadata)

        # Compile regex (even if it's only a delimiter character)
        regex = re.compile(config.delimiter)

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
                    dirpath = os.path.join(
                        config.input_dir, 'snapshot' + data[colnames['id']])
                    filename = img + '.' + config.imgformat
                    if not os.path.exists(os.path.join(dirpath, filename)):
                        print(
                            f"Something is wrong, file {dirpath}/{filename} does not exist", file=sys.stderr)
                        continue
                        # raise IOError("Something is wrong, file {0}/{1} does not exist".format(dirpath, filename))
                    # Metadata from image file name
                    metadata = _parse_filename(
                        filename=img, delimiter=config.delimiter, regex=regex)
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
                                    if meta_value != config.metadata_filters[term]:
                                        img_pass = 0
                                img_meta[term] = meta_value
                            # If the same metadata is found in the CSV file, store the value
                            elif term in colnames:
                                meta_value = data[colnames[term]]
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
                            in_date_range = check_date_range(start_date, end_date,
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
                                                            img_meta['coimg'] = coimg + \
                                                                '.' + config.imgformat
                                                            coimg_pass = 1
                                                    else:
                                                        if cocamera == img_meta['camera']:
                                                            img_meta['coimg'] = coimg + \
                                                                '.' + config.imgformat
                                                            coimg_pass = 1
                                                else:
                                                    img_meta['coimg'] = coimg + \
                                                        '.' + config.imgformat
                                                    coimg_pass = 1
                                if coimg_pass == 0:
                                    print(
                                        f"Could not find an image to coprocess with {img_path}")
                            meta[filename] = img_meta
                        elif coimg_store == 1:
                            meta[filename] = img_meta

    else:
        # parse metadata from filenames
        image_filenames = _find_images(config)
        all_image_meta = _get_image_metadata(image_filenames, config)

        # if metadata filters are provided then filter dataframe
        if len(config.metadata_filters) == 0:
            filtered_image_meta = all_image_meta
        else:
            # convert metadata_filters to dataframe
            # for scalars (single filter values) the values must be a list otherwise you need to specify index for dataframe
            # to support multiple filter values per metadata term (hopefully one day!) all key values must be a list if key values are of different lengths.
            for key in config.metadata_filters.keys():
                if not isinstance(config.metadata_filters[key], list):
                    # make scalar values a list for dataframe conversion. hope no one is using a comma in their metadata!
                    config.metadata_filters[key] = config.metadata_filters[key].split(
                        ',')
            # we need all combinations
            metadata_filter = pd.DataFrame(list(itertools.product(
                *config.metadata_filters.values())), columns=config.metadata_filters.keys())
            # inner merge to filter for desired metadata terms
            filtered_image_meta = all_image_meta.merge(
                metadata_filter, how='inner')

        if 'timestamp' in config.filename_metadata:
            filtered_image_meta['timestamp'] = pd.to_datetime(
                filtered_image_meta.timestamp, format=config.timestampformat)
            filtered_image_meta = filtered_image_meta.query(
                'timestamp >= @start_date and timestamp <= @end_date')
            filtered_image_meta['timestamp'] = filtered_image_meta.timestamp.dt.strftime(
                config.timestampformat)

        if len(filtered_image_meta) > 0:
            # add missing metadata fields from default metadata dict
            default_meta = pd.DataFrame(
                config.metadata_terms).drop(['label', 'datatype'])
            # can't perform left join with datetime columns so if you need to keep timestamp as a datetime object then filter and drop default meta that is already in dataframe and then do a cross join:
            # missing_meta = default_meta.drop(default_meta.filter(filtered_image_meta,axis=1), axis=1)
            # image_meta_complete = filtered_image_meta.merge(missing_meta, how='cross')
            image_meta_complete = filtered_image_meta.merge(
                default_meta, how='left')
            # convert nan to 'none' for compatibility except timstamp
            image_meta_complete = image_meta_complete.where(
                pd.notna(image_meta_complete), 'none')
            # pandas uses nan for missing values. convert timestamp back to None if not specified
            if 'timestamp' not in config.filename_metadata:
                image_meta_complete['timestamp'] = None

            # add basename for compatibility
            image_meta_complete['filename'] = image_meta_complete.path.apply(
                os.path.basename)

            # meta dict
            meta = image_meta_complete.set_index('filename').to_dict('index')

    return meta
###########################################


def _find_images(config):
    """Find png images is specified directory

    Args:
        snapshotdir:    directory of image files
        ext:    extension of image files

    :param snapshotdir: str
    :param ext: str
    :return fns: list

    Raises:
        ValueError: if the given directory doesn't exist
        RuntimeError: if no files with extension png were found
    """

    if not os.path.exists(config.input_dir):
        raise ValueError('the path %s does not exist' % config.input_dir)

    if config.include_all_subdirs is False:
        fns = [fn for fn in glob.glob(pathname=os.path.join(
            config.input_dir, '*%s' % config.imgformat))]
    else:
        fns = []
        for root, dirs, files in os.walk(config.input_dir):
            for file in files:
                if file.endswith(config.imgformat):
                    fns.append(os.path.join(root, file))

    if len(fns) == 0:
        raise RuntimeError(
            'No files with extension %s were found in the directory specified.' % config.imgformat)

    return(fns)


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


def _get_image_metadata(fns, config):
    """Get image filenames and return dataframe of metadata from filenames

    Args:
        fns : filenames of image files
        config : PlantCV config 

    :param fns : list
    :param config : dict
    :return snapshotdf: pandas dataframe

    Raises:
        ValueError: if the filenames can't be parsed using the passed delimiter
    """

    # How many metadata terms are in the files we intend to process?
    meta_count = len(config.filename_metadata)

    # Compile regex (even if it's only a delimiter character)
    regex = re.compile(config.delimiter)

    flist = list()
    for fullfn in fns:
        fn = os.path.basename(fullfn)
        fn = os.path.splitext(fn)
        # if delimiter is a single character it will split filenam with delimiter otherwise uses regex
        f = _parse_filename(fn[0], config.delimiter, regex)
        # Not all images in a directory may have the same metadata structure only keep those that do
        if len(f) == meta_count:
            f.append(fullfn)
            flist.append(f)

    columnnames = config.filename_metadata.copy()
    columnnames.append('path')
    fdf = pd.DataFrame(flist,
                        columns=columnnames)

    return(fdf)

# Check to see if the image was taken between a specified date range
###########################################
def check_date_range(start_date, end_date, img_time, date_format):
    """Check image time versus included date range.

    Args:
        start_date: Start date as datetime object
        end_date:   End date as datetime object
        img_time:   Image datetime
        date_format: date format code for strptime

    :param start_date: datetime
    :param end_date: datetime
    :param img_time: str
    :param date_format: str
    :return: bool
    """

    # Convert image datetime string
    try:
        img_time = datetime.datetime.strptime(img_time, date_format)
    except ValueError as e:
        raise SystemExit(
            str(e) + '\n  --> Please specify the correct timestampformat argument <--\n')

    # Does the image date-time fall outside or inside the included range
    if img_time < start_date or img_time > end_date:
        return False
    else:
        return True
###########################################
