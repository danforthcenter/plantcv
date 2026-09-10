import sys


def parallel_print(message, file=sys.stdout, verbose=True):
    """Print messages for parallel plantcv

    Parameters
    ----------
    message   = str, message to be printed
    file      = where to print, defaults to sys.stdout but sys.stderr is common throughout
    verbose   = bool, whether or not to print (depends on configuration.verbose)

    Returns
    -------
    None
    """
    if verbose:
        print(message, file=file)
