import os
import re
import datetime
from dateutil.parser import parse as dt_parser


# Parse metadata from filenames in a directory
###########################################
def metadata_parser(data_dir, meta_fields, valid_meta, meta_filters, start_date, end_date, error_log, delimiter="_",
                    file_type="png", coprocess=None):
    """Reads metadata the input data directory.

    Args:
        data_dir:     Input data directory.
        meta_fields:  Dictionary of image filename metadata fields and index positions.
        valid_meta:   Dictionary of valid metadata keys.
        meta_filters: Dictionary of metadata filters (key-value pairs).
        start_date:   Analysis start date in Unix time.
        end_date:     Analysis end date in Unix time.
        error_log:    Error log filehandle object.
        delimiter:    Filename metadata delimiter string.
        file_type:    Image filetype extension (e.g. png).
        coprocess:    Coprocess the specified imgtype with the imgtype specified in meta_filters.

    Returns:
        jobcount:     The number of processing jobs.
        meta:         Dictionary of image metadata (one entry per image to be processed).

    :param data_dir: str
    :param meta_fields: dict
    :param valid_meta: dict
    :param meta_filters: dict
    :param start_date: int
    :param end_date: int
    :param error_log: obj
    :param delimiter: str
    :param file_type: str
    :param coprocess: str
    :return jobcount: int
    :return meta: dict
    """

    # Metadata data structure
    meta = {}
    jobcount = 0

    # How many metadata fields are in the files we intend to process?
    meta_count = len(meta_fields.keys())

    # Check whether there is a snapshot metadata file or not
    if os.path.exists(os.path.join(data_dir, "SnapshotInfo.csv")):
        # Open the SnapshotInfo.csv file
        csvfile = open(os.path.join(data_dir, 'SnapshotInfo.csv'), 'r')

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
            img_list = data[colnames['tiles']]
            if img_list[:-1] == ';':
                img_list = img_list[:-1]
            imgs = img_list.split(';')
            for img in imgs:
                if len(img) != 0:
                    dirpath = os.path.join(data_dir, 'snapshot' + data[colnames['id']])
                    filename = img + '.' + file_type
                    if not os.path.exists(os.path.join(dirpath, filename)):
                        error_log.write("Something is wrong, file {0}/{1} does not exist".format(dirpath, filename))
                        continue
                        # raise IOError("Something is wrong, file {0}/{1} does not exist".format(dirpath, filename))
                    # Metadata from image file name
                    metadata = img.split(delimiter)
                    # Not all images in a directory may have the same metadata structure only keep those that do
                    if len(metadata) == meta_count:
                        # Image metadata
                        img_meta = {'path': dirpath}
                        img_pass = 1
                        coimg_store = 0
                        # For each of the type of metadata PlantCV keeps track of
                        for field in valid_meta:
                            # If the same metadata is found in the image filename, store the value
                            if field in meta_fields:
                                meta_value = metadata[meta_fields[field]]
                                # If the metadata type has a user-provided restriction
                                if field in meta_filters:
                                    # If the input value does not match the image value, fail the image
                                    if meta_value != meta_filters[field]:
                                        img_pass = 0
                                img_meta[field] = meta_value
                            # If the same metadata is found in the CSV file, store the value
                            elif field in colnames:
                                meta_value = data[colnames[field]]
                                # If the metadata type has a user-provided restriction
                                if field in meta_filters:
                                    # If the input value does not match the image value, fail the image
                                    if meta_value != meta_filters[field]:
                                        img_pass = 0
                                img_meta[field] = meta_value
                            # Or use the default value
                            else:
                                img_meta[field] = valid_meta[field]["value"]

                        if start_date and end_date and img_meta['timestamp'] is not None:
                            in_date_range = _check_date_range(start_date, end_date, img_meta['timestamp'])
                            if in_date_range is False:
                                img_pass = 0

                        if img_pass:
                            jobcount += 1

                        if coprocess is not None:
                            if img_meta['imgtype'] == coprocess:
                                coimg_store = 1

                        # If the image meets the user's criteria, store the metadata
                        if img_pass == 1:
                            # Link image to coprocessed image
                            coimg_pass = 0
                            if coprocess is not None:
                                for coimg in imgs:
                                    if len(coimg) != 0:
                                        meta_parts = coimg.split(delimiter)
                                        coimgtype = meta_parts[meta_fields['imgtype']]
                                        if coimgtype == coprocess:
                                            if 'camera' in meta_fields:
                                                cocamera = meta_parts[meta_fields['camera']]
                                                if 'frame' in meta_fields:
                                                    coframe = meta_parts[meta_fields['frame']]
                                                    if cocamera == img_meta['camera'] and coframe == img_meta['frame']:
                                                        img_meta['coimg'] = coimg + '.' + file_type
                                                        coimg_pass = 1
                                                else:
                                                    if cocamera == img_meta['camera']:
                                                        img_meta['coimg'] = coimg + '.' + file_type
                                                        coimg_pass = 1
                                            else:
                                                img_meta['coimg'] = coimg + '.' + file_type
                                                coimg_pass = 1
                                if coimg_pass == 0:
                                    error_log.write(
                                        "Could not find an image to coprocess with " + os.path.join(dirpath,
                                                                                                    filename) + '\n')
                            meta[filename] = img_meta
                        elif coimg_store == 1:
                            meta[filename] = img_meta
    else:
        # Compile regular expression to remove image file extensions
        pattern = re.escape('.') + file_type + '$'
        ext = re.compile(pattern, re.IGNORECASE)

        # Walk through the input directory and find images that match input criteria
        for (dirpath, dirnames, filenames) in os.walk(data_dir):
            for filename in filenames:
                # Is filename and image?
                is_img = ext.search(filename)
                # If filename is an image, parse the metadata
                if is_img is not None:
                    # Remove the file extension
                    prefix = ext.sub('', filename)
                    metadata = prefix.split(delimiter)

                    # Image metadata
                    img_meta = {'path': dirpath}
                    img_pass = 1
                    # For each of the type of metadata PlantCV keeps track of
                    for field in valid_meta:
                        # If the same metadata is found in the image filename, store the value
                        if field in meta_fields:
                            meta_value = metadata[meta_fields[field]]
                            # If the metadata type has a user-provided restriction
                            if field in meta_filters:
                                # If the input value does not match the image value, fail the image
                                if meta_value != meta_filters[field]:
                                    img_pass = 0
                            img_meta[field] = meta_value
                        # Or use the default value
                        else:
                            img_meta[field] = valid_meta[field]["value"]

                    if start_date and end_date and img_meta['timestamp'] is not None:
                        in_date_range = _check_date_range(start_date, end_date, img_meta['timestamp'])
                        if in_date_range is False:
                            img_pass = 0

                    # If the image meets the user's criteria, store the metadata
                    if img_pass == 1:
                        meta[filename] = img_meta
                        jobcount += 1

    return jobcount, meta
###########################################


# Check to see if the image was taken between a specified date range
###########################################
def _check_date_range(start_date, end_date, img_time):
    """Check image time versus included date range.

    Args:
        start_date: Start date in Unix time
        end_date:   End date in Unix time
        img_time:   Image datetime

    :param start_date: int
    :param end_date: int
    :param img_time: str
    :return: bool
    """

    # Convert image datetime to unix time
    timestamp = dt_parser(img_time)
    time_delta = timestamp - datetime.datetime(1970, 1, 1)
    unix_time = (time_delta.days * 24 * 3600) + time_delta.seconds
    # Does the image date-time fall outside or inside the included range
    if unix_time < start_date or unix_time > end_date:
        return False
    else:
        return True
###########################################
