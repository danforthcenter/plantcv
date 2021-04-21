import os
import re
import datetime
import pandas as pd
from itertools import product


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
        start_date = datetime.datetime(1970, 1, 1, 0, 0, 1)
    end_date = config.end_date
    if end_date is None:
        end_date = datetime.datetime.now()


    # Metadata data structure
    image_filenames = _find_images(config)
    all_image_meta = _get_image_metadata(image_filenames, config)

    if config.metadata_filters is None:
        filtered_image_meta = all_image_meta
    else:
        # convert metadata_filters to dataframe
        # for scalars (single filter values) the values must be a list otherwise you need to specify index for dataframe
        # to support multiple filter values per metadata term (hopefully one day!) all key values must be a list if key values are of different lengths. 
        for key in config.metadata_filters.keys():
            if not isinstance(config.metadata_filters[key], list):
                config.metadata_filters[key] = config.metadata_filters[key].split(',') #make scalar values a list for dataframe conversion. hope no one is using a comma in their metadata!
        # we need all combinations
        metadata_filter = pd.DataFrame(list(itertools.product(*config.metadata_filters.values())), columns=config.metadata_filters.keys())
        # inner merge to filter for desired metadata terms
        filtered_image_meta = all_image_meta.merge(metadata_filter, how='inner')
        # merge error if metadata_filters contains ONLY keys not pressent in columns of all_image_meta
        # merge succeeds but results in extra column if metadata_filters contains keys present and not present in columns of all_image_meta
        # we could further filter for filename_metadata but would give unexpected results: filtered_image_meta.filter(all_image_meta.columns)
        # do we check that timestamp is not in config.metadata_filters
        
    if 'timestamp' in config.filename_metadata:
        filtered_image_meta = filtered_image_meta.query('"timestamp" >= start_date and "timestamp" <= end_date')

    # add missing metadata fields from default metadata dict
    default_meta = pd.DataFrame(config.metadata_terms).drop(['label'])
    image_meta_complete = filtered_image_meta.merge(default_meta, how='left')

    # meta dict
    meta = image_meta_complete.set_index('path').to_dict('index')

    return meta
###########################################



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
        fns = [fn for fn in glob.glob(pathname=os.path.join(config.input_dir, '*%s' % ext))]
    else:
        fns = []
        for root, dirs, files in os.walk(config.input_dir):
            for file in files:
                if file.endswith(config.imgformat):
                    fns.append(os.path.join(root, file))
        
    if len(fns) == 0:
        raise RuntimeError('No files with extension %s were found in the directory specified.' % ext)

    return(fns)


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
        f = _parse_filename(fn[0], config.delimiter, regex) #if delimiter is a single character it will split filenam with delimiter otherwise uses regex
        # Not all images in a directory may have the same metadata structure only keep those that do
        if len(f) == meta_count:
            f.append(fullfn)
            flist.append(f)

    columnnames = config.filename_metadata
    columnnames.append('path')
    try:
        fdf = pd.DataFrame(flist,
                        columns=columnnames)
    except ValueError as e:
        raise ValueError('The filenames did have correctly formated metadata as specified by delimiter argument.') from e

    return(fdf)

