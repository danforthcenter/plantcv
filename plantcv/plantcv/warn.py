# Warnings handling

import sys
from plantcv.plantcv import params


def warn(warning):
    """Print a warning message to stderr.

    Parameters
    ----------
    warning : str
        Warning message to print.

    Returns
    -------
    None
        Function does not return anything.
    """
    if params.verbose:
        print(f"Warning: {warning}", file=sys.stderr)
