import pandas as pd
from plantcv.parallel.workflow_inputs import WorkflowConfig


def inspect_dataset(config):
    """Inspect a dataset before running plantcv in parallel over the directory
    Parameters
    ----------
    config   = plantcv.parallel.WorkflowConfig object or str, if string then this should be the input directory path.

    Returns = pandas.core.frame.DataFrame, dataframe of image metadata.
    -------
    """
    # if config is a path then make a config out of it
    if isinstance(config, str):
        input_dir = config
        config = WorkflowConfig()
        config.input_dir = input_dir
    # run the metadata parser to find images and return dataframes
    meta, removed = metadata_parser(config)
    # make dataframe out of groupby object
    meta = meta.apply(lambda x: x, include_groups=False)
    # flag kept images
    meta["status"] = "Kept"
    # combine both dataframes
    df = pd.concat([meta, removed])
    return df


def _summarize_dataset(df):
    """
    """
    return(df)
