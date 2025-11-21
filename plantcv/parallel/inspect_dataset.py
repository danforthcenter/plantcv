import pandas as pd
import os
from plantcv.parallel.parsers import metadata_parser
from plantcv.parallel.workflowconfig import WorkflowConfig


def inspect_dataset(config):
    """Inspect a dataset before running plantcv in parallel over the directory
    Parameters
    ----------
    config   = plantcv.parallel.WorkflowConfig object or str, if str then very minimal processing is done

    Returns
    -------
    summary_df     = pandas.core.frame.DataFrame,
        dataframe of number of unique values of metadata filters and statuses.
    meta     = pandas.core.frame.DataFrame, dataframe of image metadata.
    """
    if isinstance(config, str):
        input_dir = config
        config = WorkflowConfig()
        if input_dir.endswith(".json"):
            config.import_config(config_file=input_dir)
        else:
            config.input_dir = input_dir
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
    if not removed.empty:
        meta = pd.concat(df.dropna(axis=1, how='all') for df in [meta, removed])
    # pull extensions
    meta['extension'] = meta['filepath'].apply(
        lambda x: os.path.splitext(os.path.basename(x))[1]
    )
    # count unique values by all filtered metadata and steps where images were dropped
    summary_df = meta.groupby(
        ['status', *config.metadata_filters],
        dropna=False
    ).agg(_agg_unique_values)
    return summary_df, meta


def _agg_unique_values(series):
    """Aggregate columns to a number of unique values and possibly their values
    Parameters
    ----------
    series     = pandas.core.series.Series, a metadata column of a pandas dataframe

    Return
    ------
    label      = str, a string describing the number of unique values and their
                 observed levels if there are <4.
    """
    n_unique = series.nunique()
    context = ""
    if n_unique:
        context = " (...)"
    series = series.astype("string")
    # if there are only a few options then print what they are
    if n_unique and n_unique < 4:
        uniques = series.dropna().unique()
        unique_vals = ", ".join(uniques)
        context = " (" + unique_vals + ")"
    label = str(n_unique) + context
    return label
