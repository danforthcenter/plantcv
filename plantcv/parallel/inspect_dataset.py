import pandas as pd
from plantcv.parallel.parsers import metadata_parser


def inspect_dataset(config):
    """Inspect a dataset before running plantcv in parallel over the directory
    Parameters
    ----------
    config   = plantcv.parallel.WorkflowConfig object

    Returns = pandas.core.frame.DataFrame, dataframe of image metadata.
    -------
    """
    # run the metadata parser to find images and return dataframes
    meta, removed = metadata_parser(config)
    # make dataframe out of groupby object
    meta_filepaths = []
    for i, _ in meta["filepath"]:
        meta_filepaths.append(i[0])
    meta = meta.apply(lambda x: x, include_groups=False)
    meta["filepath"] = meta_filepaths
    # flag kept images
    meta["status"] = "Kept"
    # combine both dataframes
    df = pd.concat([meta, removed])
    return df


def _summarize_dataset(df):
    """
    """
    return(df)
