import pandas as pd
from plantcv.parallel.parsers import metadata_parser


def inspect_dataset(config):
    """Inspect a dataset before running plantcv in parallel over the directory
    Parameters
    ----------
    config   = plantcv.parallel.WorkflowConfig object or str, if string then this should be the input directory path.

    Returns = pandas.core.frame.DataFrame, dataframe of image metadata.
    -------
    """
    # if config is a path then make a config out of it
    # NOTE i can't just grab WorkflowConfig from parallel because I can't
    # export this while with parallel while that workflowconfig class is defined
    # in that __init__.py file.
    if isinstance(config, str):
        input_dir = config
        # if there is no config file then make a cheap copy
        config = type('dummyconfig', (), {'input_dir': input_dir,
                                          'filename_metadata': ["filepath"],
                                          'include_all_subdirs':True,
                                          'metadata_terms': {'timestamp'},
                                          'metadata_filters':{},
                                          'timestampformat':"%Y-%m-%dT%H:%M:%S.%fZ",
                                          'start_date': None,
                                          'end_date': None,
                                          'imgformat':"png",
                                          'delimiter':'&&&',
                                          'groupby':'filepath'
                                          })
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
