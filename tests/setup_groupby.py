import os
import plantcv.parallel
import re
import pandas as pd

PARALLEL_TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parallel_data")
TEST_TMPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".cache")
TEST_IMG_DIR = "images"
TEST_IMG_DIR2 = "images_w_date"
TEST_SNAPSHOT_DIR = "snapshots"
TEST_PIPELINE = os.path.join(PARALLEL_TEST_DATA, "plantcv-script.py")

# Create config instance
config = plantcv.parallel.WorkflowConfig()
config.input_dir = os.path.join(PARALLEL_TEST_DATA, TEST_SNAPSHOT_DIR)
config.json = os.path.join(TEST_TMPDIR, "test_plantcv_parallel_metadata_parser_fail_images", "output.json")
config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
config.workflow = TEST_PIPELINE
config.metadata_filters = {"imgtype": ["VIS","NIR"],"camera":"SV"}#{"cartag":"A1",
config.imgformat = "jpg"
config.coprocess = "NIR"
# config.start_date = "1970-01-01 00:00:00.0"
# config.end_date = "1970-01-01 00:00:00.0"
# config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'


def find_images(config):
    """Find png images is specified directory

    Parameters
    ----------
    snapshotdir : str
        directory of image files
    ext : str
        extension of image files

    Returns
    -------
    filenames of image files : list

    Raises
    ------
    ValueError
        if the given directory doesn't exist
    RuntimeError
        if no files with extension png were found

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


def get_image_metadata(fns, config):
    """Get image filenames and metadata from filenames
    Parameters
    ----------
        fns : list
            filenames of image files
        config : dict
            PlantCV config 


    Returns
    -------
        snapshotdf : pandas dataframe
            dataframe of snapshot metadata

    Raises
    ------
    ValueError
        if the filenames do not have 6 pieces delimited by a `-`

    """
    # How many metadata terms are in the files we intend to process?
    meta_count = len(config.filename_metadata)
    
    # Compile regex (even if it's only a delimiter character)
    regex = re.compile(config.delimiter)

    flist = list()
    for fullfn in fns:
        fn = os.path.basename(fullfn)
        fn = os.path.splitext(fn)
        f = parse_filename(fn[0], config.delimiter, regex) #if delimiter is a single character it will split filenam with delimiter otherwise uses regex
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

# Filename metadata parser, from plantcv 3.10
###########################################
def parse_filename(filename, delimiter, regex):
    """Parse the input filename and return a list of metadata.

    Parameters
    ----------
        filename : str
            Filename to parse metadata from
        delimiter :  str
            Delimiter character to split the filename on
        regex : re.Pattern
            Compiled regular expression pattern to process file with

    Returns
    -------
        metadata : list
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