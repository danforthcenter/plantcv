# Deprecation handling

import sys
from importlib.metadata import version
from plantcv.plantcv._globals import params


def deprecation_warning(warning):
    """Print out deprecation warning

    Inputs:
    warning = warning message text

    :param warning: str
    """
    v = version("plantcv")
    warning_msg = f"DeprecationWarning: {warning} Current PlantCV version: {v}"
    if params.verbose is True:
        print(warning_msg, file=sys.stderr)
